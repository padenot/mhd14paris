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

CREATE UNIQUE INDEX mbid_undx ON release (mbid);
CREATE INDEX deezer_undx ON release (deezer_id);

COMMIT;
