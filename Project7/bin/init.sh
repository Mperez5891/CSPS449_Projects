#!/bin/sh

sqlite3 ./Project2-users.db < ./sql/users_services.sql
sqlite3 ./Project2-timeline.db < ./sql/timeline_services.sql