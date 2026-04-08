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

