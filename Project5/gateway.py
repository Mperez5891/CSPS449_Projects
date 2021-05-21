#
# Simple API gateway in Python
#
# Inspired by <https://github.com/vishnuvardhan-kumar/loadbalancer.py>
#

import sys
import json
import http.client
import logging.config

import bottle
from bottle import route, request, response, auth_basic
import requests


# Allow JSON values to be loaded from app.config[key]
#
def json_config(key):
    value = app.config[key]
    return json.loads(value)


# Set up app and logging
#
app = bottle.default_app()
app.config.load_config('./etc/gateway.ini')

logging.config.fileConfig(app.config['logging.config'])

# If you want to see traffic being sent from and received by calls to
# the Requests library, add the following to etc/gateway.ini:
#
#   [logging]
#   requests = true
#
if json_config('logging.requests'):
    http.client.HTTPConnection.debuglevel = 1

    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    logging.debug('Requests logging enabled')




# Return errors in JSON
#
# Adapted from <https://stackoverflow.com/a/39818780>
#
def json_error_handler(res):
    if res.content_type == 'application/json':
        return res.body
    res.content_type = 'application/json'
    if res.body == 'Unknown Error.':
        res.body = bottle.HTTP_CODES[res.status_code]
    return bottle.json_dumps({'error': res.body})


app.default_error_handler = json_error_handler


# Disable warnings produced by Bottle 0.12.19 when reloader=True
#
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
#
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore', ResourceWarning)

timelineIndex = 0
upstream_servers = json_config('proxy.upstreams')



def check(user,password):
    upstream_response = requests.post(upstream_servers["users"][0]+"/users/login",json = {'username':user, 'password': password})
    message=json.loads(upstream_response.content.decode("ascii"))
    return message['success']

@route('<url:re:.*>', method='ANY')
# @auth_basic(check,realm="private", text="Username or Password are wrong")
def gateway(url):

    logging.info(request.auth)
    global timelineIndex, upstream_servers
    path = request.urlparts._replace(scheme='', netloc='').geturl()
    if path.split("/")[1]=="users":
        if path.split("/")[2]=="login":
            return json.dumps({"success": True})

    collection=path.split("/")[1]
    if collection!="timelines":
        upstream_server = upstream_servers[collection][0]
    else:
        upstream_server = upstream_servers[collection][timelineIndex]
        lenS=len(upstream_servers[collection])
        timelineIndex = 0 if timelineIndex==lenS-1 else timelineIndex+1

    upstream_url = upstream_server + path
    logging.debug('Upstream URL: %s', upstream_url)

    headers = {}
    for name, value in request.headers.items():
        if name.casefold() == 'content-length' and not value:
            headers['Content-Length'] = '0'
        else:
            headers[name] = value

    try:
        upstream_response = requests.request(
            request.method,
            upstream_url,
            data=request.body,
            headers=headers,
            cookies=request.cookies,
            stream=True,
        )
    except requests.exceptions.RequestException as e:
        logging.exception(e)
        response.status = 503
        return {
            'method': e.request.method,
            'url': e.request.url,
            'exception': type(e).__name__,
        }

    if upstream_response.status_code>=500 and collection == "timeline":
        upstream_servers["timeline"].remove(upstream_server)
        timelineIndex = 0



    response.status = upstream_response.status_code
    for name, value in upstream_response.headers.items():
        if name.casefold() == 'transfer-encoding':
            continue
        response.set_header(name, value)
    return upstream_response.content
