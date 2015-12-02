CREATE EXTENSION postgis;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    firstname TEXT,
    surname TEXT,
    url TEXT,
    ispublic BOOLEAN DEFAULT FALSE,
    metric TEXT DEFAULT 'KM'::TEXT,
    fb_token TEXT,
    email TEXT,
    password TEXT
);
