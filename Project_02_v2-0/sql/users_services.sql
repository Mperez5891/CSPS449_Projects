PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- drop tables ------------------------------------------------
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS following;

-- create tables ----------------------------------------------
CREATE TABLE IF NOT EXISTS users(
   	username TEXT PRIMARY KEY,
	email TEXT NOT NULL UNIQUE,
	password NOT NULL
);

CREATE TABLE IF NOT EXISTS following(
	username TEXT,
         user_followed TEXT,
         FOREIGN KEY(user_followed)
             REFERENCES users(username)
             ON DELETE CASCADE,
         FOREIGN KEY(username)
             REFERENCES users(username)
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
('blaze_assault', 'blsault@csu.fullerton.edu', 'Password105'),
('darkcarnage', 'darnage@csu.fullerton.edu', 'Password106'),
('frozen_gunner', 'frunner@csu.fullerton.edu', 'Password107'),
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

INSERT INTO following(username, user_followed)
VALUES
('bubbly_snowflake', 'dmvphobia'),
('bubbly_snowflake', 'blaze_assault'),
('bubbly_snowflake', 'frozen_gunner'),
('bubbly_snowflake', 'need_more_coffee'),
('dmvphobia', 'rage_quitter1'),
('dmvphobia', 'usidor_the_blue'),
('dmvphobia', 'arny'),
('dmvphobia', 'darkcarnage'),
('dmvphobia', 'bubbly_snowflake'),
('turboslayer', 'b.with.photos'),
('turboslayer', 'fbi_surveillance_team'),
('turboslayer', 'dravenfact'),
('cryptichatter', 'stealtheddefender'),
('cryptichatter', 'bubbly_snowflake'),
('cryptichatter', 'chuntttttt'),
('cryptichatter', 'turboslayer'),
('cryptichatter', 'dmvphobia'),
('stealtheddefender', 'fbi_surveillance_team');

SELECT * FROM users;
COMMIT;
