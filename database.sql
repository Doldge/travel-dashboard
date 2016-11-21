CREATE EXTENSION postgis;
CREATE TABLE member (
    id SERIAL PRIMARY KEY,
    firstname TEXT,
    surname TEXT,
    url TEXT UNIQUE,
    ispublic BOOLEAN DEFAULT FALSE,
    metric TEXT DEFAULT 'KM'::TEXT,
    fb_id BIGINT,
    email TEXT UNIQUE,
    password TEXT,
    departure TIMESTAMPTZ,
    current_tz TEXT 
);

CREATE TABLE friends (
    fb_id BIGINT PRIMARY KEY,
    start_value INT,
    current_value INT,
    created TIMESTAMPTZ default now(),
    lastupdate TIMESTAMPTZ default now(),
);

CREATE FUNCTION update_friends() RETURNS trigger as $$
BEGIN
    IF NEW.lastupdate IS NULL THEN
        NEW.lastupdate = now();
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_friends BEFORE UPDATE ON friends EXECUTE PROCEDURE update_friends();

CREATE TABLE facebook (
    id BIGINT PRIMARY KEY,
    access_token TEXT,
    expires_in INT,
    created TIMESTAMPTZ DEFAULT now(),
    signed_request TEXT
);


CREATE TABLE locations (
    fb_id BIGINT,
    name TEXT,
    city TEXT,
    country TEXT,
    position POINT,
    PRIMARY KEY ( fb_id )
);

CREATE TABLE member_locations (
    member_id INT REFERENCES member (id),
    location_id BIGINT REFERENCES locations(fb_id),
    visit_date TIMESTAMPTZ,
    PRIMARY KEY ( member_id, visit_date )
);

