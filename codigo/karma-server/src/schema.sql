BEGIN TRANSACTION;
CREATE TABLE votes (
	observation_id VARCHAR(64) NOT NULL, 
	upvotes INTEGER, 
	downvotes INTEGER, 
	PRIMARY KEY (observation_id), 
	FOREIGN KEY(observation_id) REFERENCES observation (_id)
);
CREATE TABLE user_observations (
	observation_id VARCHAR(64), 
	user_id VARCHAR(64), 
	FOREIGN KEY(observation_id) REFERENCES observation (_id), 
	FOREIGN KEY(user_id) REFERENCES user (_id)
);
CREATE TABLE user (
	_id VARCHAR(64) NOT NULL, 
	PRIMARY KEY (_id)
);
CREATE TABLE puntuation (
	observation_id VARCHAR(64) NOT NULL, 
	positive INTEGER, 
	negative INTEGER, 
	PRIMARY KEY (observation_id), 
	FOREIGN KEY(observation_id) REFERENCES observation (_id)
);
CREATE TABLE position (
	observation_id VARCHAR(64) NOT NULL, 
	x_position INTEGER, 
	y_position INTEGER, 
	PRIMARY KEY (observation_id), 
	FOREIGN KEY(observation_id) REFERENCES observation (_id)
);
CREATE TABLE policy (
	_id VARCHAR(64) NOT NULL, 
	"_Policy__formula" VARCHAR(128), 
	max_level INTEGER, 
	PRIMARY KEY (_id)
);
INSERT INTO `policy` VALUES ('default','math.log ( ( level / 3 ) + 1 ) * 350',10);
CREATE TABLE observation (
	_id VARCHAR(64) NOT NULL, 
	state VARCHAR(8), 
	image_id VARCHAR(64), 
	brightness INTEGER, 
	PRIMARY KEY (_id), 
	FOREIGN KEY(image_id) REFERENCES image (_id), 
	CONSTRAINT state CHECK (state IN ('DENYED', 'APPROVED', 'PENDING', 'DISPUTED'))
);
CREATE TABLE image (
	_id VARCHAR(64) NOT NULL, 
	x_size INTEGER, 
	y_size INTEGER, 
	probability INTEGER, 
	fwhm INTEGER, 
	PRIMARY KEY (_id)
);
COMMIT;
