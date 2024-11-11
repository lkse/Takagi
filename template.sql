CREATE DATABASE IF NOT EXISTS Takagi;

USE Takagi;

CREATE TABLE guilds (
    GID INT PRIMARY KEY,
    LogChannel INT,
    Blacklisted BOOLEAN,
);

CREATE TABLE users (
    UID INT PRIMARY KEY,
    Blacklisted BOOLEAN
);

