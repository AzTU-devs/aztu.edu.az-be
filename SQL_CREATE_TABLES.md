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






CREATE TABLE faculties (
    id           SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50)  NOT NULL UNIQUE,
    created_at   TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at   TIMESTAMP WITH TIME ZONE
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






CREATE TABLE faculty_directors (
    id            SERIAL PRIMARY KEY,
    faculty_code  VARCHAR(50)  NOT NULL UNIQUE REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    father_name   VARCHAR(100),
    email         VARCHAR(255),
    phone         VARCHAR(50),
    room_number   VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at    TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at    TIMESTAMP WITH TIME ZONE
);




CREATE TABLE faculty_director_tr (
    id                SERIAL PRIMARY KEY,
    director_id       INTEGER NOT NULL REFERENCES faculty_directors(id) ON DELETE CASCADE,
    lang_code         VARCHAR(10) NOT NULL,
    scientific_degree VARCHAR(255),
    scientific_title  VARCHAR(255),
    bio               TEXT,
    created_at        TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at        TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_director_tr_id_lang UNIQUE (director_id, lang_code)
);



These sections follow a similar pattern:

CREATE TABLE faculty_laboratories (
    id            SERIAL PRIMARY KEY,
    faculty_code  VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at    TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at    TIMESTAMP WITH TIME ZONE
);

CREATE TABLE faculty_laboratory_tr (
    id            SERIAL PRIMARY KEY,
    laboratory_id INTEGER NOT NULL REFERENCES faculty_laboratories(id) ON DELETE CASCADE,
    lang_code     VARCHAR(10) NOT NULL,
    title         VARCHAR(255) NOT NULL,
    description   TEXT,
    created_at    TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at    TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_laboratory_tr_id_lang UNIQUE (laboratory_id, lang_code)
);

*(Similar tables exist for `faculty_research_works`, `faculty_partner_companies`, `faculty_objectives`, `faculty_duties`, `faculty_projects`, and `faculty_directions_of_action`)*





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
    room          VARCHAR(50)  NOT NULL
);




CREATE TYPE day_of_week_enum AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

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
    publications         TEXT
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






CREATE TABLE menu_headers (
    id            SERIAL PRIMARY KEY,
    image_url     TEXT,
    direct_url    VARCHAR(500),
    display_order INTEGER NOT NULL,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);




CREATE TABLE menu_header_translations (
    id        SERIAL PRIMARY KEY,
    header_id INTEGER NOT NULL REFERENCES menu_headers(id) ON DELETE CASCADE,
    lang_code VARCHAR(5) NOT NULL,
    title     VARCHAR(200) NOT NULL,
    slug      VARCHAR(200) NOT NULL
);




CREATE TABLE menu_header_items (
    id            SERIAL PRIMARY KEY,
    header_id     INTEGER NOT NULL REFERENCES menu_headers(id) ON DELETE CASCADE,
    direct_url    VARCHAR(500),
    display_order INTEGER NOT NULL,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);




CREATE TABLE menu_header_item_translations (
    id        SERIAL PRIMARY KEY,
    item_id   INTEGER NOT NULL REFERENCES menu_header_items(id) ON DELETE CASCADE,
    lang_code VARCHAR(5) NOT NULL,
    title     VARCHAR(200) NOT NULL,
    slug      VARCHAR(200) NOT NULL
);




CREATE TABLE menu_header_sub_items (
    id            SERIAL PRIMARY KEY,
    item_id       INTEGER NOT NULL REFERENCES menu_header_items(id) ON DELETE CASCADE,
    direct_url    VARCHAR(500) NOT NULL,
    display_order INTEGER NOT NULL,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);




CREATE TABLE menu_header_sub_item_translations (
    id          SERIAL PRIMARY KEY,
    sub_item_id INTEGER NOT NULL REFERENCES menu_header_sub_items(id) ON DELETE CASCADE,
    lang_code   VARCHAR(5) NOT NULL,
    title       VARCHAR(200) NOT NULL,
    slug        VARCHAR(200) NOT NULL
);






CREATE TABLE hero (
    id         SERIAL PRIMARY KEY,
    hero_id    INTEGER   NOT NULL UNIQUE,
    video      TEXT      NOT NULL,
    is_active  BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
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

