DROP TABLE IF EXISTS wishes;

CREATE TABLE wishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator  TEXT,
    title TEXT NOT NULL,
    isFulfilled BOOLEAN NOT NULL
);
