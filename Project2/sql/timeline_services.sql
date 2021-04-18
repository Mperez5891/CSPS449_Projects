PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- drop tables ------------------------------------------------
DROP TABLE IF EXISTS user_posts;

-- create tables ----------------------------------------------
CREATE TABLE IF NOT EXISTS user_posts(
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        post TEXT,
        timestamp DATETIME2
);

-- enter elements --------------------------------------------
INSERT INTO user_posts(username, post, timestamp)
VALUES
('bubbly_snowflake', 'Hello. This is my test post.', '2021-1-3 09:10:00'),
('chuntttttt', 'Awh yea baby!', '2021-1-3 09:10:23'),
('usidor_the_blue', 'WIZARD OF THE 12TH REALM OF EPHYSIYIES 
MASTER OF LIGHT AND SHADOW MANIPULATOR OF MAGICAL DELIGHTS 
DEVOURER OF CHAOS CHAMPION OF THE GREAT HALLS OF TERRAKKAS
THE ELVES KNOW ME AS FIANG YALOK THE DWARES KNOW ME AS
ZOENEN HOOGSTANDJES I AM KNOWN IN THE NORTHEAST AS GAISMUENAS MEISTAR
AND THERE MAY BE OTHER SECRET NAMES YOU DO NOT KNOW YET', '2021-1-3 09:11:50'),
('arny', 'Hello from the magic tavern!', '2021-1-3 09:12:54'),
('b.with.photos', 'Look at this sweet picture', '2021-1-3 15:10:23'),
('b.with.photos', 'Did you look at my sweet picture', '2021-1-3 17:37:00'),
('need_more_coffee', 'I love coffee', '2021-3-3 09:10:00'),
('need_more_coffee', 'Do you have coffee', '2021-4-3 09:10:00'),
('need_more_coffee', 'Bring me coffee...', '2021-5-3 09:10:00'),
('need_more_coffee', '...pls', '2021-6-3 09:10:00');

COMMIT;

