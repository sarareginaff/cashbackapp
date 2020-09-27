DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS purchase_status;
DROP TABLE IF EXISTS purchases;

CREATE TABLE users (
  id        INTEGER   PRIMARY KEY AUTOINCREMENT,
  full_name TEXT      NOT NULL,
  cpf       TEXT      UNIQUE NOT NULL,
  email     TEXT      NOT NULL,
  password  TEXT      NOT NULL
);

CREATE TABLE purchase_status (
  id            INTEGER PRIMARY KEY,
  status_desc   TEXT    NOT NULL
);

INSERT INTO purchase_status VALUES (1, "Approved");
INSERT INTO purchase_status VALUES (2, "Validation");

CREATE TABLE purchases (
  id            INTEGER         PRIMARY KEY AUTOINCREMENT,
  code          TEXT            NOT NULL,
  value         INTEGER         NOT NULL,
  dth_purchase  TEXT            NOT NULL,
  id_user       INTEGER         NOT NULL,
  id_status     INTEGER         NOT NULL,

  FOREIGN KEY (id_user) REFERENCES user (id),
  FOREIGN KEY (id_status) REFERENCES purchase_status (id)
);

