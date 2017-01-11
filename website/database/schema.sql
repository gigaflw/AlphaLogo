DROP TABLE IF EXISTS LOGOS;
CREATE TABLE LOGOS
(   
    IND           INTEGER         PRIMARY KEY,
    FILENAME      VARCHAR(16)     NOT NULL,
    ENT_NAME      VARCHAR(32)     NOT NULL,
    INFO          VARCHAR(1024)   NOT NULL,
    THEME_COLORS  VARCHAR(128),
    THEME_WEIGHTS VARCHAR(32),
    S             REAL,
    V             REAL,
    -- TODO: not thrifty to store s,v deliberately
    INDUSTRY      INTEGER       
);