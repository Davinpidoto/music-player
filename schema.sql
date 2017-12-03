CREATE TABLE artists(
  id INT UNSIGNED NOT NULL  AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE albums(
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  artist_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  KEY artist_index (artist_id),
  FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE songs(
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  file VARCHAR(255) NOT NULL,
  album_id INT UNSIGNED,
  PRIMARY KEY(id),
  KEY album_index (album_id),
  FOREIGN KEY (album_id) REFERENCES albums(id)
);