-- migrate:up


CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    en BOOLEAN DEFAULT TRUE,
    name VARCHAR(50) NOT NULL,
    pass_hash VARCHAR(255) NOT NULL,
    join_date timestamp WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() at time zone 'utc')
);


CREATE UNIQUE INDEX unique_user_index on users(en, name);



-- migrate:down

