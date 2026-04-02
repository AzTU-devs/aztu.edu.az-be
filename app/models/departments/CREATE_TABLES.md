CREATE TABLE departments (
    id          SERIAL PRIMARY KEY,
    department_code VARCHAR(50) NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ
);

CREATE TABLE departments_tr (
    id              SERIAL PRIMARY KEY,
    department_code VARCHAR(50) NOT NULL
        REFERENCES departments(department_code) ON DELETE CASCADE,
    lang_code       VARCHAR(10) NOT NULL,
    department_name VARCHAR(255) NOT NULL,
    about_html      TEXT,
    created_at      TIMESTAMPTZ NOT NULL,
    updated_at      TIMESTAMPTZ,
    CONSTRAINT uq_departments_tr_code_lang UNIQUE (department_code, lang_code)
);


CREATE TABLE department_objectives (
    id              SERIAL PRIMARY KEY,
    department_code VARCHAR(50) NOT NULL
        REFERENCES departments(department_code) ON DELETE CASCADE,
    display_order   INTEGER NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL,
    updated_at      TIMESTAMPTZ
);

CREATE TABLE department_objective_tr (
    id           SERIAL PRIMARY KEY,
    objective_id INTEGER NOT NULL
        REFERENCES department_objectives(id) ON DELETE CASCADE,
    lang_code    VARCHAR(10) NOT NULL,
    html_content TEXT NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL,
    updated_at   TIMESTAMPTZ,
    CONSTRAINT uq_department_objective_tr_id_lang UNIQUE (objective_id, lang_code)
);


CREATE TABLE department_core_functions (
    id              SERIAL PRIMARY KEY,
    department_code VARCHAR(50) NOT NULL
        REFERENCES departments(department_code) ON DELETE CASCADE,
    display_order   INTEGER NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL,
    updated_at      TIMESTAMPTZ
);

CREATE TABLE department_core_function_tr (
    id               SERIAL PRIMARY KEY,
    core_function_id INTEGER NOT NULL
        REFERENCES department_core_functions(id) ON DELETE CASCADE,
    lang_code        VARCHAR(10) NOT NULL,
    html_content     TEXT NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL,
    updated_at       TIMESTAMPTZ,
    CONSTRAINT uq_department_core_function_tr_id_lang UNIQUE (core_function_id, lang_code)
);

CREATE TABLE department_directors (
    id              SERIAL PRIMARY KEY,
    department_code VARCHAR(50) NOT NULL
        REFERENCES departments(department_code) ON DELETE CASCADE,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    father_name     VARCHAR(100),
    room_number     VARCHAR(50),
    profile_image   VARCHAR(1024),
    created_at      TIMESTAMPTZ NOT NULL,
    updated_at      TIMESTAMPTZ,
    CONSTRAINT uq_department_directors_code UNIQUE (department_code)
);
CREATE TABLE department_director_tr (
    id               SERIAL PRIMARY KEY,
    director_id      INTEGER NOT NULL
        REFERENCES department_directors(id) ON DELETE CASCADE,
    lang_code        VARCHAR(10) NOT NULL,
    scientific_degree VARCHAR(255),
    scientific_title  VARCHAR(255),
    bio              TEXT,
    created_at       TIMESTAMPTZ NOT NULL,
    updated_at       TIMESTAMPTZ,
    CONSTRAINT uq_department_director_tr_id_lang UNIQUE (director_id, lang_code)
);


CREATE TABLE department_director_working_hours (
    id          SERIAL PRIMARY KEY,
    director_id INTEGER NOT NULL
        REFERENCES department_directors(id) ON DELETE CASCADE,
    time_range  VARCHAR(50) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ
);

CREATE TABLE department_director_working_hour_tr (
    id              SERIAL PRIMARY KEY,
    working_hour_id INTEGER NOT NULL
        REFERENCES department_director_working_hours(id) ON DELETE CASCADE,
    lang_code       VARCHAR(10) NOT NULL,
    day             VARCHAR(50) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL,
    updated_at      TIMESTAMPTZ,
    CONSTRAINT uq_department_director_working_hour_tr_id_lang UNIQUE (working_hour_id, lang_code)
);

CREATE TABLE department_director_educations (
    id          SERIAL PRIMARY KEY,
    director_id INTEGER NOT NULL
        REFERENCES department_directors(id) ON DELETE CASCADE,
    start_year  VARCHAR(20),
    end_year    VARCHAR(20),
    created_at  TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ
);

CREATE TABLE department_director_education_tr (
    id           SERIAL PRIMARY KEY,
    education_id INTEGER NOT NULL
        REFERENCES department_director_educations(id) ON DELETE CASCADE,
    lang_code    VARCHAR(10) NOT NULL,
    degree       VARCHAR(255) NOT NULL,
    university   VARCHAR(255) NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL,
    updated_at   TIMESTAMPTZ,
    CONSTRAINT uq_department_director_education_tr_id_lang UNIQUE (education_id, lang_code)
);

CREATE TABLE department_workers (
    id              SERIAL PRIMARY KEY,
    department_code VARCHAR(50) NOT NULL
        REFERENCES departments(department_code) ON DELETE CASCADE,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    father_name     VARCHAR(100),
    email           VARCHAR(255),
    phone           VARCHAR(50),
    profile_image   VARCHAR(1024),
    created_at      TIMESTAMPTZ NOT NULL,
    updated_at      TIMESTAMPTZ
);


CREATE TABLE department_worker_tr (
    id               SERIAL PRIMARY KEY,
    worker_id        INTEGER NOT NULL
        REFERENCES department_workers(id) ON DELETE CASCADE,
    lang_code        VARCHAR(10) NOT NULL,
    duty             VARCHAR(255) NOT NULL,
    scientific_degree VARCHAR(255),
    scientific_name   VARCHAR(255),
    created_at       TIMESTAMPTZ NOT NULL,
    updated_at       TIMESTAMPTZ,
    CONSTRAINT uq_department_worker_tr_id_lang UNIQUE (worker_id, lang_code)
);

