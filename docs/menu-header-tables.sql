-- ============================================================
-- Menu Header tables
-- Run in order — each table depends on the one above it.
-- ============================================================

-- 1. Top-level navigation titles
CREATE TABLE menu_headers (
    id            SERIAL          PRIMARY KEY,
    image_url     TEXT,
    direct_url    VARCHAR(500),
    display_order INTEGER         NOT NULL,
    is_active     BOOLEAN         NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_menu_headers_display_order ON menu_headers (display_order);
CREATE INDEX idx_menu_headers_is_active     ON menu_headers (is_active);


-- 2. Per-language title + auto-generated slug for each header
CREATE TABLE menu_header_translations (
    id        SERIAL       PRIMARY KEY,
    header_id INTEGER      NOT NULL
                           REFERENCES menu_headers (id) ON DELETE CASCADE,
    lang_code VARCHAR(5)   NOT NULL,          -- 'az' | 'en'
    title     VARCHAR(200) NOT NULL,
    slug      VARCHAR(200) NOT NULL,

    CONSTRAINT uq_menu_header_translations_header_lang
        UNIQUE (header_id, lang_code)
);

CREATE INDEX idx_menu_header_translations_header_id ON menu_header_translations (header_id);


-- 3. First-level dropdown items under a header
CREATE TABLE menu_header_items (
    id            SERIAL       PRIMARY KEY,
    header_id     INTEGER      NOT NULL
                               REFERENCES menu_headers (id) ON DELETE CASCADE,
    direct_url    VARCHAR(500),
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_menu_header_items_header_id     ON menu_header_items (header_id);
CREATE INDEX idx_menu_header_items_display_order ON menu_header_items (display_order);
CREATE INDEX idx_menu_header_items_is_active     ON menu_header_items (is_active);


-- 4. Per-language title + slug for each item
CREATE TABLE menu_header_item_translations (
    id        SERIAL       PRIMARY KEY,
    item_id   INTEGER      NOT NULL
                           REFERENCES menu_header_items (id) ON DELETE CASCADE,
    lang_code VARCHAR(5)   NOT NULL,
    title     VARCHAR(200) NOT NULL,
    slug      VARCHAR(200) NOT NULL,

    CONSTRAINT uq_menu_header_item_translations_item_lang
        UNIQUE (item_id, lang_code)
);

CREATE INDEX idx_menu_header_item_translations_item_id ON menu_header_item_translations (item_id);


-- 5. Second-level leaf items (always have a direct_url)
CREATE TABLE menu_header_sub_items (
    id            SERIAL       PRIMARY KEY,
    item_id       INTEGER      NOT NULL
                               REFERENCES menu_header_items (id) ON DELETE CASCADE,
    direct_url    VARCHAR(500) NOT NULL,
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_menu_header_sub_items_item_id       ON menu_header_sub_items (item_id);
CREATE INDEX idx_menu_header_sub_items_display_order ON menu_header_sub_items (display_order);
CREATE INDEX idx_menu_header_sub_items_is_active     ON menu_header_sub_items (is_active);


-- 6. Per-language title + slug for each sub-item
CREATE TABLE menu_header_sub_item_translations (
    id          SERIAL       PRIMARY KEY,
    sub_item_id INTEGER      NOT NULL
                             REFERENCES menu_header_sub_items (id) ON DELETE CASCADE,
    lang_code   VARCHAR(5)   NOT NULL,
    title       VARCHAR(200) NOT NULL,
    slug        VARCHAR(200) NOT NULL,

    CONSTRAINT uq_menu_header_sub_item_translations_sub_item_lang
        UNIQUE (sub_item_id, lang_code)
);

CREATE INDEX idx_menu_header_sub_item_translations_sub_item_id
    ON menu_header_sub_item_translations (sub_item_id);
