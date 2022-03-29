DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS hotel;
DROP TABLE IF EXISTS hotel_image;
DROP TABLE IF EXISTS hotel_service;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS review;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(50),
    password TEXT NOT NULL,
    isAdmin boolean NOT NULL DEFAULT false
);

CREATE TABLE hotel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(250) NOT NULL UNIQUE,
    description TEXT,
    location TEXT
);

CREATE TABLE hotel_image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hotel_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (hotel_id) REFERENCES hotel (id) ON DELETE CASCADE
);

CREATE TABLE hotel_service (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hotel_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(50),
    -- price should be the lowest money unit (cents for example)
    price INTEGER NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel (id) ON DELETE CASCADE
);

CREATE TABLE booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hotel_service_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    starting_date DATE NOT NULL,
    ending_date DATE NOT NULL,
    FOREIGN KEY (hotel_service_id) REFERENCES hotel_service (id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE SET NULL
);

CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    hotel_id INTEGER NOT NULL,
    score INTEGER NOT NULL CHECK(score between 1 and 5),
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE SET NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel (id) ON DELETE CASCADE
)