CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin'))
);


CREATE TABLE user_cars (
    id SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    carname TEXT NOT NULL
);


CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    addressname TEXT NOT NULL,
    channels_per_station INTEGER DEFAULT 0
);


CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    id_station INTEGER NOT NULL REFERENCES stations(id) ON DELETE CASCADE,
    title TEXT,
    price NUMERIC(10, 2),
    occupancy BOOLEAN DEFAULT FALSE,
    occupiedby TEXT
);


CREATE TABLE channel_usercars (
    id SERIAL PRIMARY KEY,
    id_channel INTEGER REFERENCES channels(id) ON DELETE SET NULL,
    id_user INTEGER REFERENCES users(id) ON DELETE CASCADE,
    id_user_car INTEGER REFERENCES user_cars(id) ON DELETE SET NULL,
    startcharge TIMESTAMP WITH TIME ZONE,
    endcharge TIMESTAMP WITH TIME ZONE
);


CREATE TABLE reported_users_list (
    id SERIAL PRIMARY KEY,
    id_station INTEGER REFERENCES stations(id) ON DELETE SET NULL,
    station_address TEXT,
    id_channel INTEGER REFERENCES channels(id) ON DELETE SET NULL,
    id_user INTEGER REFERENCES users(id) ON DELETE CASCADE,
    additional_tip TEXT
);