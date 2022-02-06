create table book
(
  id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  title VARCHAR(100),
  insert_timestamp DATETIME DEFAULT NULL
);

create table notes
(
  id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  title VARCHAR(100),
  body VARCHAR(300),
  date DATETIME DEFAULT NULL
);
