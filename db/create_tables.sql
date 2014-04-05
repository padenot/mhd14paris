BEGIN;

CREATE TABLE release (
    id         SERIAL,
    mbid       TEXT,
    red        INTEGER,
    green      INTEGER,
    blue       INTEGER,
    color      CUBE
);

CREATE TABLE color_index (
    red        INTEGER,
    green      INTEGER,
    blue       INTEGER,
    deezer_id  TEXT,
    mbid       TEXT
);

CREATE UNIQUE INDEX rgb_index ON color_index (red, green, blue);
CREATE UNIQUE INDEX mbid_undx ON release (mbid);
CREATE INDEX deezer_undx ON release (deezer_id);
CREATE INDEX release_cube_idx ON release USING gist (color);

COMMIT;
