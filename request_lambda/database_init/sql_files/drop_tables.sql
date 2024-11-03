# SQL To Drop App Tables From the Database

-- Drop Core Tables in Order of Dependencies
DROP TABLE IF EXISTS sentiments;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS requests;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS schools;