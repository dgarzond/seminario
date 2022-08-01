CREATE SCHEMA workshop;
DROP TABLE IF EXISTS workshop.crypto;
CREATE TABLE workshop.crypto (
  date timestamptz NOT NULL,
  price double precision	NOT NULL,
  currency varchar(10) NOT NULL,
   PRIMARY KEY(date)
);
