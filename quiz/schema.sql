DROP TABLE IF EXISTS chapter;
DROP TABLE IF EXISTS learning_goal;
DROP TABLE IF EXISTS quiz_item;


CREATE TABLE chapter (
  no INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE learning_goal (
  id INTEGER PRIMARY KEY,
  chapter_no INTEGER NOT NULL,
  no INTEGER NOT NULL,
  description TEXT NOT NULL,
  FOREIGN KEY (chapter_no) REFERENCES chapter (no),
  CONSTRAINT combination UNIQUE (chapter_no, no)
);

CREATE TABLE quiz_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chapter_no INTEGER NOT NULL,
  lg_no INTEGER NOT NULL,
  no INTEGER NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  explanation TEXT NOT NULL,
  FOREIGN KEY (chapter_no) REFERENCES chapter (no)
  FOREIGN KEY (lg_no) REFERENCES learning_goal (no)
);

