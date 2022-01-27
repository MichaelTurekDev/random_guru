DROP TABLE IF EXISTS History;

CREATE TABLE History (
    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    patternName     TEXT        NOT NULL,
    visitCount      INTEGER     NOT NULL
);
