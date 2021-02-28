PRAGMA foreign_keys = ON;

-- drop tables ------------------------------------------------
--DROP TABLE users;
--DROP TABLE following;
--DROP TABLE user_posts;

-- create tables ----------------------------------------------
CREATE TABLE IF NOT EXISTS users(
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
   	username TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE,
	password NOT NULL
);

CREATE TABLE IF NOT EXISTS following(
	user_id INTEGER,
         user_followed TEXT,
         FOREIGN KEY(user_followed)
             REFERENCES users(username)
             ON DELETE CASCADE,
         FOREIGN KEY(user_id)
             REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS user_posts(
	user_id INTEGER,
         post TEXT,
         timestamp TIME,
         FOREIGN KEY(user_id)
             REFERENCES users(user_id)
             ON DELETE CASCADE
);

-- enter elements --------------------------------------------
INSERT INTO users(username, email, password)
VALUES
('bubbly_snowflake', 'buflake@csu.fullerton.edu', 'Password100'),
('dmvphobia', 'dmhobia@csu.fullerton.edu', 'Password101'),
('turboslayer', 'tulayer@csu.fullerton.edu', 'Password102'),
('cryptichatter', 'cratter@csu.fullerton.edu', 'Password103'),
('stealtheddefender', 'stender@csu.fullerton.edu', 'Password104'),
('blaze assault', 'blsault@csu.fullerton.edu', 'Password105'),
('darkcarnage', 'darnage@csu.fullerton.edu', 'Password106'),
('frozen gunner', 'frunner@csu.fullerton.edu', 'Password107'),
('b.with.photos', 'b.hotos@csu.fullerton.edu', 'Password108'),
('music_viking', 'muiking@csu.fullerton.edu', 'Password109'),
('readingpro', 'rengpro@csu.fullerton.edu', 'Password110'),
('dravenfact', 'drnfact@csu.fullerton.edu', 'Password111'),
('rage_quitter1', 'ratter1@csu.fullerton.edu', 'Password112'),
('need_more_coffee', 'neoffee@csu.fullerton.edu', 'Password113'),
('fbi_surveillance_team', 'fb_team@csu.fullerton.edu', 'Password114'),
('chuntttttt', 'chttttt@csu.fullerton.edu', 'Password115'),
('usidor_the_blue', 'us_blue@csu.fullerton.edu', 'Password116'),
('arny', 'ar@csu.fullerton.edu', 'Password117');

INSERT INTO following(user_id, user_followed)
VALUES
(1, 'dmvphobia'),
(1, 'blaze assault'),
(1, 'frozen gunner'),
(1, 'need_more_coffee'),
(2, 'rage_quitter1'),
(2, 'usidor_the_blue'),
(2, 'arny'),
(2, 'darkcarnage'),
(2, 'bubbly_snowflake'),
(3, 'b.with.photos'),
(3, 'fbi_surveillance_team'),
(3, 'dravenfact'),
(4, 'stealtheddefender'),
(4, 'bubbly_snowflake'),
(4, 'chuntttttt'),
(4, 'turboslayer'),
(4, 'dmvphobia'),
(5, 'fbi_surveillance_team');

INSERT INTO user_posts(user_id, post, timestamp)
VALUES
(1, 'Hello. This is my test post.', '09:10:00');

-- test code -------------------------------------------------
-- SELECT * FROM following;
-- SELECT * FROM users;
-- SELECT * FROM user_posts;

-- SELECT username, user_followed 
-- FROM users 
-- INNER JOIN following 
-- ON following.user_id = users.user_id;