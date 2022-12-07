
CREATE TABLE IF NOT EXISTS team(
	team_id int NOT NULL,
	team_info VARCHAR(255),
	rank int,
	PRIMARY KEY(team_id)
);

CREATE TABLE IF NOT EXISTS users(
	user_id SERIAL,
	username VARCHAR(255),
	name VARCHAR(255),
	email VARCHAR(255),
	pinned_team int,
	password VARCHAR(255),
	PRIMARY KEY (user_id),
	FOREIGN KEY (pinned_team) REFERENCES team(team_id)
);

CREATE TABLE IF NOT EXISTS posts(
	post_id SERIAL,
	likes int,
	dislikes int,
	post_title VARCHAR(255),
	post_body VARCHAR(255),
	poster_id int,
	PRIMARY KEY(post_id),
	FOREIGN KEY(poster_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS comments(
	comment_id SERIAL,
	likes int, 
	dislikes int,
	content VARCHAR(255),
	post_id int,
	commentor_id int,
	PRIMARY KEY(comment_id),
	FOREIGN KEY(post_id) REFERENCES posts(post_id),
	FOREIGN KEY(commentor_id) REFERENCES users(user_id)
);