-- Create tables for depression crawler
-- Groups table
CREATE TABLE IF NOT EXISTS groups (
    id BIGINT PRIMARY KEY,  -- VK group id
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crawler runs table
CREATE TABLE IF NOT EXISTS crawler_runs (
    id SERIAL PRIMARY KEY,
    target_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Run groups mapping table
CREATE TABLE IF NOT EXISTS run_groups (
    run_id INTEGER REFERENCES crawler_runs(id),
    group_id BIGINT REFERENCES groups(id),
    PRIMARY KEY (run_id, group_id)
);

-- Depression predictions table
CREATE TABLE IF NOT EXISTS depression_predictions (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES crawler_runs(id),
    owner_id BIGINT REFERENCES groups(id),  -- wall owner_id where the post is published
    post_id BIGINT NOT NULL,  -- 0 for posts, actual post_id for comments
    vk_id BIGINT NOT NULL,    -- post_id for posts, comment_id for comments
    depression_prediction BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_post UNIQUE (owner_id, post_id, vk_id)
);