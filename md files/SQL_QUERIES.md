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
    description  TEXT       NOT NULL,
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

CREATE TABLE admin_users (
    id                  SERIAL PRIMARY KEY,
    username            VARCHAR(50)  NOT NULL UNIQUE,
    hashed_password     VARCHAR(255) NOT NULL,
    is_active           BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE,
    last_login_at       TIMESTAMP WITH TIME ZONE,
    refresh_token_hash  VARCHAR(255)
);

CREATE TYPE degree_level_enum AS ENUM ('Bachelor', 'Master', 'PhD');
CREATE TYPE day_of_week_enum AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
CREATE TYPE education_level_enum AS ENUM ('bachelor', 'master');

CREATE TABLE employees (
    id             SERIAL PRIMARY KEY,
    employee_code  VARCHAR(50)  NOT NULL UNIQUE,
    profile_image  VARCHAR(255),
    faculty_code   VARCHAR(50)  REFERENCES faculties(faculty_code) ON DELETE SET NULL,
    cafedra_code   VARCHAR(50)  REFERENCES cafedras(cafedra_code)  ON DELETE SET NULL,
    created_at     TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at     TIMESTAMP WITH TIME ZONE
);

CREATE TABLE employee_tr (
    id                   SERIAL PRIMARY KEY,
    employee_code        VARCHAR(50)  NOT NULL REFERENCES employees(employee_code) ON DELETE CASCADE,
    lang_code            VARCHAR(10)  NOT NULL,
    first_name           VARCHAR(100),
    last_name            VARCHAR(100),
    full_name            VARCHAR(255),
    academic_degree      VARCHAR(100),
    academic_title       VARCHAR(100),
    position             VARCHAR(255),
    scientific_interests TEXT,
    biography            TEXT,
    created_at           TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at           TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_employee_tr_code_lang UNIQUE (employee_code, lang_code)
);

CREATE TABLE employee_contacts (
    id            SERIAL PRIMARY KEY,
    employee_code VARCHAR(50)  NOT NULL UNIQUE REFERENCES employees(employee_code) ON DELETE CASCADE,
    email         VARCHAR(255) NOT NULL,
    phone         VARCHAR(50)  NOT NULL,
    building      VARCHAR(100) NOT NULL,
    floor         VARCHAR(20)  NOT NULL,
    room          VARCHAR(50)  NOT NULL,
    CONSTRAINT uq_employee_contacts_code UNIQUE (employee_code)
);

CREATE TABLE education (
    id              SERIAL PRIMARY KEY,
    employee_code   VARCHAR(50)        NOT NULL REFERENCES employees(employee_code) ON DELETE CASCADE,
    degree_level    degree_level_enum  NOT NULL,
    graduation_year INTEGER
);

CREATE TABLE education_tr (
    id              SERIAL PRIMARY KEY,
    education_id    INTEGER      NOT NULL REFERENCES education(id) ON DELETE CASCADE,
    lang_code       VARCHAR(10)  NOT NULL,
    institution     VARCHAR(255),
    specialization  VARCHAR(255),
    CONSTRAINT uq_education_tr_id_lang UNIQUE (education_id, lang_code)
);

CREATE TABLE office_hours (
    id            SERIAL PRIMARY KEY,
    employee_code VARCHAR(50)       NOT NULL REFERENCES employees(employee_code) ON DELETE CASCADE,
    day_of_week   day_of_week_enum  NOT NULL,
    start_time    TIME              NOT NULL,
    end_time      TIME              NOT NULL
);

CREATE TABLE employee_research (
    id                   SERIAL PRIMARY KEY,
    employee_code        VARCHAR(50) NOT NULL UNIQUE REFERENCES employees(employee_code) ON DELETE CASCADE,
    scopus_url           TEXT,
    google_scholar_url   TEXT,
    orcid_url            TEXT,
    researchgate_url     TEXT,
    academia_url         TEXT,
    publications         TEXT,
    CONSTRAINT uq_employee_research_code UNIQUE (employee_code)
);

CREATE TABLE teaching_courses (
    id              SERIAL PRIMARY KEY,
    employee_code   VARCHAR(50)           NOT NULL REFERENCES employees(employee_code) ON DELETE CASCADE,
    education_level education_level_enum  NOT NULL
);

CREATE TABLE teaching_course_tr (
    id          SERIAL PRIMARY KEY,
    course_id   INTEGER      NOT NULL REFERENCES teaching_courses(id) ON DELETE CASCADE,
    lang_code   VARCHAR(10)  NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    CONSTRAINT uq_teaching_course_tr_id_lang UNIQUE (course_id, lang_code)
);