BEGIN;

CREATE TABLE release (
    id         SERIAL,
    mbid       TEXT,
    deezer_id  TEXT,
    red        INTEGER,
    green      INTEGER,
    blue       INTEGER,
    color      CUBE
);

COMMIT;
