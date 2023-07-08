-- migrate:up


CREATE TABLE posts(
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    created_at timestamp WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() at time zone 'utc'),
    author_id BIGINT NOT NULL REFERENCES users(id)
);


-- migrate:down