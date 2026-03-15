CREATE TABLE faculties (
    id           SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50)  NOT NULL UNIQUE,
    created_at   TIMESTAMP    NOT NULL,
    updated_at   TIMESTAMP
);

CREATE TABLE faculties_tr (
    id           SERIAL PRIMARY KEY,
    faculty_name VARCHAR(255) NOT NULL,
    faculty_code VARCHAR(50)  NOT NULL,
    lang_code    VARCHAR(10)  NOT NULL,
    created_at   TIMESTAMP    NOT NULL,
    updated_at   TIMESTAMP,
    CONSTRAINT uq_faculties_tr_code_lang UNIQUE (faculty_code, lang_code)
);

CREATE TABLE cafedras (
    id           SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    cafedra_code VARCHAR(50) NOT NULL,
    created_at   TIMESTAMP   NOT NULL,
    updated_at   TIMESTAMP,
    CONSTRAINT uq_cafedras_code UNIQUE (cafedra_code)
);

CREATE TABLE cafedras_tr (
    id           SERIAL PRIMARY KEY,
    cafedra_name VARCHAR(255) NOT NULL,
    cafedra_code VARCHAR(50)  NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    lang_code    VARCHAR(10)  NOT NULL,
    created_at   TIMESTAMP    NOT NULL,
    updated_at   TIMESTAMP,
    CONSTRAINT uq_cafedras_tr_code_lang UNIQUE (cafedra_code, lang_code)
);

CREATE TABLE news_category (
    id          SERIAL PRIMARY KEY,
    category_id INTEGER   NOT NULL UNIQUE,
    created_at  TIMESTAMP NOT NULL,
    updated_at  TIMESTAMP
);

CREATE TABLE news_category_translation (
    id          SERIAL PRIMARY KEY,
    category_id INTEGER     NOT NULL,
    lang_code   VARCHAR(2)  NOT NULL,
    title       TEXT        NOT NULL
);

CREATE TABLE news (
    id            SERIAL PRIMARY KEY,
    news_id       INTEGER   NOT NULL UNIQUE,
    category_id   INTEGER   NOT NULL,
    display_order INTEGER   NOT NULL,
    is_active     BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP NOT NULL,
    updated_at    TIMESTAMP
);

CREATE TABLE news_translation (
    id           SERIAL PRIMARY KEY,
    news_id      INTEGER    NOT NULL,
    lang_code    VARCHAR(2) NOT NULL,
    title        TEXT       NOT NULL,
    html_content TEXT       NOT NULL
);

CREATE TABLE news_gallery (
    id       SERIAL PRIMARY KEY,
    news_id  INTEGER NOT NULL,
    image    TEXT    NOT NULL,
    is_cover BOOLEAN NOT NULL
);

CREATE TABLE hero (
    id         SERIAL PRIMARY KEY,
    hero_id    INTEGER   NOT NULL UNIQUE,
    video      TEXT      NOT NULL,
    is_active  BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE announcement (
    id              SERIAL PRIMARY KEY,
    announcement_id INTEGER   NOT NULL UNIQUE,
    image           TEXT      NOT NULL,
    display_order   INTEGER   NOT NULL,
    is_active       BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE
);

CREATE TABLE announcement_translation (
    id              SERIAL PRIMARY KEY,
    announcement_id INTEGER    NOT NULL,
    lang_code       VARCHAR(2) NOT NULL,
    title           TEXT       NOT NULL,
    html_content    TEXT       NOT NULL
);

CREATE TABLE project (
    id            SERIAL PRIMARY KEY,
    project_id    INTEGER   NOT NULL UNIQUE,
    bg_image      TEXT      NOT NULL,
    display_order INTEGER   NOT NULL,
    is_active     BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP WITH TIME ZONE
);

CREATE TABLE project_translation (
    id           SERIAL PRIMARY KEY,
    project_id   INTEGER NOT NULL REFERENCES project(project_id) ON DELETE CASCADE,
    lang_code    VARCHAR(2) NOT NULL,
    title        TEXT       NOT NULL,
    desc         TEXT       NOT NULL,
    html_content TEXT       NOT NULL
);

CREATE TABLE menu_header_sections (
    id            SERIAL PRIMARY KEY,
    section_key   VARCHAR(50)  NOT NULL UNIQUE,
    image_url     TEXT         NOT NULL,
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_header_section_translations (
    id         SERIAL PRIMARY KEY,
    section_id INTEGER      NOT NULL REFERENCES menu_header_sections(id) ON DELETE CASCADE,
    lang_code  VARCHAR(5)   NOT NULL,
    label      VARCHAR(100) NOT NULL,
    base_path  VARCHAR(200) NOT NULL
);

CREATE TABLE menu_header_items (
    id            SERIAL PRIMARY KEY,
    section_id    INTEGER      NOT NULL REFERENCES menu_header_sections(id) ON DELETE CASCADE,
    slug          VARCHAR(200),
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_header_item_translations (
    id        SERIAL PRIMARY KEY,
    item_id   INTEGER      NOT NULL REFERENCES menu_header_items(id) ON DELETE CASCADE,
    lang_code VARCHAR(5)   NOT NULL,
    title     VARCHAR(200) NOT NULL
);

CREATE TABLE menu_header_sub_items (
    id            SERIAL PRIMARY KEY,
    item_id       INTEGER      NOT NULL REFERENCES menu_header_items(id) ON DELETE CASCADE,
    slug          VARCHAR(200) NOT NULL,
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_header_sub_item_translations (
    id          SERIAL PRIMARY KEY,
    sub_item_id INTEGER      NOT NULL REFERENCES menu_header_sub_items(id) ON DELETE CASCADE,
    lang_code   VARCHAR(5)   NOT NULL,
    title       VARCHAR(200) NOT NULL
);

CREATE TABLE menu_footer_columns (
    id            SERIAL PRIMARY KEY,
    display_order INTEGER NOT NULL,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_footer_column_translations (
    id        SERIAL PRIMARY KEY,
    column_id INTEGER      NOT NULL REFERENCES menu_footer_columns(id) ON DELETE CASCADE,
    lang_code VARCHAR(5)   NOT NULL,
    title     VARCHAR(200) NOT NULL
);

CREATE TABLE menu_footer_links (
    id            SERIAL PRIMARY KEY,
    column_id     INTEGER      NOT NULL REFERENCES menu_footer_columns(id) ON DELETE CASCADE,
    url           VARCHAR(500) NOT NULL,
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_footer_link_translations (
    id        SERIAL PRIMARY KEY,
    link_id   INTEGER      NOT NULL REFERENCES menu_footer_links(id) ON DELETE CASCADE,
    lang_code VARCHAR(5)   NOT NULL,
    label     VARCHAR(200) NOT NULL
);

CREATE TABLE menu_footer_partner_logos (
    id            SERIAL PRIMARY KEY,
    label         VARCHAR(200) NOT NULL,
    image_url     TEXT         NOT NULL,
    url           TEXT         NOT NULL,
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_footer_quick_icons (
    id            SERIAL PRIMARY KEY,
    icon          VARCHAR(100) NOT NULL,
    url           TEXT         NOT NULL,
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_footer_quick_icon_translations (
    id        SERIAL PRIMARY KEY,
    icon_id   INTEGER      NOT NULL REFERENCES menu_footer_quick_icons(id) ON DELETE CASCADE,
    lang_code VARCHAR(5)   NOT NULL,
    label     VARCHAR(200) NOT NULL
);

CREATE TABLE menu_social_links (
    id            SERIAL PRIMARY KEY,
    platform      VARCHAR(50) NOT NULL,
    url           TEXT        NOT NULL,
    context       VARCHAR(20) NOT NULL,   -- 'footer' | 'quick' | 'both'
    display_order INTEGER     NOT NULL,
    is_active     BOOLEAN     NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_contacts (
    id        SERIAL PRIMARY KEY,
    context   VARCHAR(20)  NOT NULL,      -- 'footer' | 'quick'
    email     VARCHAR(200) NOT NULL,
    is_active BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_contact_phones (
    id            SERIAL PRIMARY KEY,
    contact_id    INTEGER     NOT NULL REFERENCES menu_contacts(id) ON DELETE CASCADE,
    phone         VARCHAR(50) NOT NULL,
    display_order INTEGER     NOT NULL
);

CREATE TABLE menu_contact_addresses (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER    NOT NULL REFERENCES menu_contacts(id) ON DELETE CASCADE,
    lang_code  VARCHAR(5) NOT NULL,
    address    TEXT       NOT NULL
);

CREATE TABLE menu_quick_left_items (
    id            SERIAL PRIMARY KEY,
    url           TEXT    NOT NULL,
    display_order INTEGER NOT NULL,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_quick_left_item_translations (
    id        SERIAL PRIMARY KEY,
    item_id   INTEGER      NOT NULL REFERENCES menu_quick_left_items(id) ON DELETE CASCADE,
    lang_code VARCHAR(5)   NOT NULL,
    label     VARCHAR(200) NOT NULL
);

CREATE TABLE menu_quick_sections (
    id            SERIAL PRIMARY KEY,
    section_key   VARCHAR(50) NOT NULL UNIQUE,
    display_order INTEGER     NOT NULL,
    is_active     BOOLEAN     NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_quick_section_translations (
    id         SERIAL PRIMARY KEY,
    section_id INTEGER      NOT NULL REFERENCES menu_quick_sections(id) ON DELETE CASCADE,
    lang_code  VARCHAR(5)   NOT NULL,
    title      VARCHAR(200) NOT NULL
);

CREATE TABLE menu_quick_section_items (
    id            SERIAL PRIMARY KEY,
    section_id    INTEGER NOT NULL REFERENCES menu_quick_sections(id) ON DELETE CASCADE,
    url           TEXT    NOT NULL,
    display_order INTEGER NOT NULL,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE menu_quick_section_item_translations (
    id        SERIAL PRIMARY KEY,
    item_id   INTEGER      NOT NULL REFERENCES menu_quick_section_items(id) ON DELETE CASCADE,
    lang_code VARCHAR(5)   NOT NULL,
    label     VARCHAR(200) NOT NULL
);

CREATE TABLE collaboration (
    id               SERIAL PRIMARY KEY,
    collaboration_id INTEGER   NOT NULL,
    logo             TEXT      NOT NULL,
    website_url      TEXT,
    display_order    INTEGER   NOT NULL,
    is_active        BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_collaboration_collaboration_id UNIQUE (collaboration_id)
);

CREATE TABLE collaboration_translation (
    id               SERIAL PRIMARY KEY,
    collaboration_id INTEGER      NOT NULL REFERENCES collaboration(collaboration_id) ON DELETE CASCADE,
    lang_code        VARCHAR(2)   NOT NULL,
    name             VARCHAR(255) NOT NULL,
    CONSTRAINT uq_collaboration_translation_id_lang UNIQUE (collaboration_id, lang_code)
);