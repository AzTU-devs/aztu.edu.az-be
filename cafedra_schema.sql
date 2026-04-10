CREATE TABLE cafedras (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    cafedra_code VARCHAR(50) UNIQUE NOT NULL,

    -- Statistics
    bachelor_programs_count INT DEFAULT 0,
    master_programs_count INT DEFAULT 0,
    phd_programs_count INT DEFAULT 0,
    international_collaborations_count INT DEFAULT 0,
    laboratories_count INT DEFAULT 0,
    projects_patents_count INT DEFAULT 0,
    industrial_collaborations_count INT DEFAULT 0,
    sdgs JSONB DEFAULT '[]',

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedras_tr (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    cafedra_name VARCHAR(255) NOT NULL,
    about_text TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (cafedra_code, lang_code)
);

CREATE TABLE cafedra_directors (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) UNIQUE NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    room_number VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_director_tr (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES cafedra_directors(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    scientific_degree VARCHAR(255),
    scientific_title VARCHAR(255),
    bio TEXT,
    scientific_research_fields JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (director_id, lang_code)
);

CREATE TABLE cafedra_director_working_hours (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES cafedra_directors(id) ON DELETE CASCADE,
    time_range VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_director_working_hour_tr (
    id SERIAL PRIMARY KEY,
    working_hour_id INT NOT NULL REFERENCES cafedra_director_working_hours(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    day VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (working_hour_id, lang_code)
);

CREATE TABLE cafedra_director_scientific_events (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES cafedra_directors(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_director_scientific_event_tr (
    id SERIAL PRIMARY KEY,
    scientific_event_id INT NOT NULL REFERENCES cafedra_director_scientific_events(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    event_title VARCHAR(255) NOT NULL,
    event_description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (scientific_event_id, lang_code)
);

CREATE TABLE cafedra_director_educations (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES cafedra_directors(id) ON DELETE CASCADE,
    start_year VARCHAR(20),
    end_year VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_director_education_tr (
    id SERIAL PRIMARY KEY,
    education_id INT NOT NULL REFERENCES cafedra_director_educations(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    degree VARCHAR(255) NOT NULL,
    university VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (education_id, lang_code)
);

CREATE TABLE cafedra_deputy_directors (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_deputy_director_tr (
    id SERIAL PRIMARY KEY,
    deputy_director_id INT NOT NULL REFERENCES cafedra_deputy_directors(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    duty VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (deputy_director_id, lang_code)
);

CREATE TABLE cafedra_scientific_council (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_council_member_tr (
    id SERIAL PRIMARY KEY,
    council_member_id INT NOT NULL REFERENCES cafedra_scientific_council(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    duty VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (council_member_id, lang_code)
);

CREATE TABLE cafedra_workers (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_worker_tr (
    id SERIAL PRIMARY KEY,
    worker_id INT NOT NULL REFERENCES cafedra_workers(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    duty VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (worker_id, lang_code)
);

-- ============================================================
-- SECTION TABLES
-- ============================================================

CREATE TABLE cafedra_laboratories (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_laboratory_tr (
    id SERIAL PRIMARY KEY,
    laboratory_id INT NOT NULL REFERENCES cafedra_laboratories(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (laboratory_id, lang_code)
);

CREATE TABLE cafedra_research_works (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_research_work_tr (
    id SERIAL PRIMARY KEY,
    research_work_id INT NOT NULL REFERENCES cafedra_research_works(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (research_work_id, lang_code)
);

CREATE TABLE cafedra_partner_companies (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_partner_company_tr (
    id SERIAL PRIMARY KEY,
    partner_company_id INT NOT NULL REFERENCES cafedra_partner_companies(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (partner_company_id, lang_code)
);

CREATE TABLE cafedra_objectives (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_objective_tr (
    id SERIAL PRIMARY KEY,
    objective_id INT NOT NULL REFERENCES cafedra_objectives(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (objective_id, lang_code)
);

CREATE TABLE cafedra_duties (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_duty_tr (
    id SERIAL PRIMARY KEY,
    duty_id INT NOT NULL REFERENCES cafedra_duties(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (duty_id, lang_code)
);

CREATE TABLE cafedra_projects (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_project_tr (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES cafedra_projects(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (project_id, lang_code)
);

CREATE TABLE cafedra_directions_of_action (
    id SERIAL PRIMARY KEY,
    cafedra_code VARCHAR(50) NOT NULL REFERENCES cafedras(cafedra_code) ON DELETE CASCADE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cafedra_direction_of_action_tr (
    id SERIAL PRIMARY KEY,
    direction_of_action_id INT NOT NULL REFERENCES cafedra_directions_of_action(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (direction_of_action_id, lang_code)
);