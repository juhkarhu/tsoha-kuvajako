CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT,
    visible INTEGER DEFAULT 1,
    admin INTEGER DEFAULT 0,
    banned INTEGER DEFAULT 0
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    visible INTEGER DEFAULT 1
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY, 
    content TEXT, 
    post_id INTEGER REFERENCES posts, 
    user_id INTEGER REFERENCES users,  
    sent_at TIMESTAMP,
    visible INTEGER DEFAULT 1
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    message_id INTEGER REFERENCES posts,
    data BYTEA,
    visible INTEGER DEFAULT 1
);

