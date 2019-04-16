PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  vk_id INTEGER UNIQUE NOT NULL,
  photo TEXT(256),
  first_name TEXT(256) NOT NULL,
  last_name TEXT(256),
  sex INTEGER,
  bdate TEXT(256),
  country TEXT(256),
  city TEXT(256),
  about TEXT(256),
  activities TEXT(256),
  books TEXT(256),
  games TEXT(256),
  movies TEXT(256),
  music TEXT(256),
  quotes TEXT(256),
  tv TEXT(256),
  interests TEXT(256),
  company_name TEXT(256),
  position TEXT(256),
  company_country TEXT(256),
  company_city TEXT(256),
  company_from INTEGER,
  company_until INTEGER,
  university_name TEXT(256),
  university_country TEXT(256),
  university_city TEXT(256),
  university_faculty TEXT(256),
  university_graduation INTEGER,
  school_name TEXT(256),
  school_country TEXT(256),
  school_city TEXT(256),
  school_year_from INTEGER,
  school_year_until INTEGER,
  school_graduation INTEGER,
  school_type TEXT(256),
  school_class TEXT(256),
  school_speciality TEXT(256),
  military_unit TEXT(256),
  military_country TEXT(256),
  military_from INTEGER,
  military_until INTEGER,
  political TEXT(256),
  langs TEXT(256),
  religion TEXT(256),
  inspired_by TEXT(256),
  people_main TEXT(256),
  life_main TEXT(256),
  smoking TEXT(256),
  alcohol TEXT(256),
  occupation TEXT(256),
  relation TEXT(256),
  connections TEXT(256),
  deactivated TEXT(256),
  is_closed TEXT(256),
  FOREIGN KEY (sex) REFERENCES sex(sex_id)
);

DROP TABLE IF EXISTS sex;

CREATE TABLE sex (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sex_id INTEGER UNIQUE,
  value TEXT(256)
);

INSERT INTO sex (sex_id, value)
VALUES (0, 'Не указан');
INSERT INTO sex (sex_id, value)
VALUES (1, 'Женский');
INSERT INTO sex (sex_id, value)
VALUES (2, 'Мужской');

DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  country_id INTEGER UNIQUE,
  value TEXT(256) UNIQUE
);

DROP TABLE IF EXISTS cities;

CREATE TABLE cities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  city_id INTEGER UNIQUE,
  value TEXT(256) UNIQUE,
  country_id INTEGER,
  FOREIGN KEY (country_id) REFERENCES countries(country_id)
);
