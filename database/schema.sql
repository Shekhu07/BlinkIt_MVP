CREATE TABLE IF NOT EXISTS raw_reviews (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50), -- 'play_store', 'app_store', 'reddit'
    source_id VARCHAR(255) UNIQUE,
    content TEXT,
    rating INTEGER,
    created_at TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS filtered_reviews (
    id SERIAL PRIMARY KEY,
    raw_review_id INTEGER REFERENCES raw_reviews(id),
    filtered_content TEXT,
    tf_idf_score FLOAT,
    is_relevant BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Column order below deliberately matches the live database (pg_attribute.attnum order), so a
-- rebuilt DB stays COPY-compatible with pg_dump output taken from the live one.
CREATE TABLE IF NOT EXISTS extractions (
    id SERIAL PRIMARY KEY,
    filtered_review_id INTEGER REFERENCES filtered_reviews(id),
    behavior_type VARCHAR(100),
    category VARCHAR(100),
    reason TEXT,
    confidence FLOAT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- REQUIRED by the Two-Step Gated Schema (analysis/extract_themes.py). These were missing from
    -- this file while present in the live DB, so a fresh `docker-compose up` built a table the
    -- pipeline could not write to. mentions_category_behavior is the gate itself — the field every
    -- headline number is filtered on (1,094 of 4,740 rows true).
    mentions_category_behavior BOOLEAN,
    sentiment VARCHAR(100),

    -- Added to the live DB on 2026-07-24 for the extraction-prompt v2 experiment
    -- (docs/extraction_prompt_v2_proposal.md). The committed v1 pipeline never writes these, so
    -- they are NULL for all 4,740 rows; declared here only so this file matches the real schema.
    habit_signal VARCHAR(100),
    discovery_channel VARCHAR(100),
    info_needed VARCHAR(100),
    explorer_signal VARCHAR(100),
    unmet_need TEXT
);

CREATE TABLE IF NOT EXISTS themes (
    id SERIAL PRIMARY KEY,
    theme_name VARCHAR(255),
    description TEXT,
    user_segment VARCHAR(255),
    evidence_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS theme_evidence (
    id SERIAL PRIMARY KEY,
    theme_id INTEGER REFERENCES themes(id),
    extraction_id INTEGER REFERENCES extractions(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS validation_samples (
    id SERIAL PRIMARY KEY,
    theme_id INTEGER REFERENCES themes(id),
    sample_review_id INTEGER REFERENCES raw_reviews(id),
    human_validation_status VARCHAR(50), -- 'confirmed', 'contradicted', 'unclear'
    llm_validation_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS company_disclosures (
    id SERIAL PRIMARY KEY,
    source_document VARCHAR(255), -- 'Q3_2025_Earnings_Call'
    content_snippet TEXT,
    theme_id INTEGER REFERENCES themes(id),
    signal_type VARCHAR(50), -- 'corroborates', 'contradicts', 'unrelated'
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
