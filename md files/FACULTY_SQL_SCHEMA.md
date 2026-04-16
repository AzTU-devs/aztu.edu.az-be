
CREATE TABLE faculties (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) UNIQUE NOT NULL,
    
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

CREATE TABLE faculties_tr (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    faculty_name VARCHAR(255) NOT NULL,
    about_text TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (faculty_code, lang_code)
);





CREATE TABLE faculty_directors (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) UNIQUE NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
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

CREATE TABLE faculty_director_tr (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES faculty_directors(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    scientific_degree VARCHAR(255),
    scientific_title VARCHAR(255),
    bio TEXT,
    scientific_research_fields JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (director_id, lang_code)
);

CREATE TABLE faculty_director_working_hours (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES faculty_directors(id) ON DELETE CASCADE,
    time_range VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE faculty_director_working_hour_tr (
    id SERIAL PRIMARY KEY,
    working_hour_id INT NOT NULL REFERENCES faculty_director_working_hours(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    day VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (working_hour_id, lang_code)
);

CREATE TABLE faculty_director_educations (
    id SERIAL PRIMARY KEY,
    director_id INT NOT NULL REFERENCES faculty_directors(id) ON DELETE CASCADE,
    start_year VARCHAR(20),
    end_year VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE faculty_director_education_tr (
    id SERIAL PRIMARY KEY,
    education_id INT NOT NULL REFERENCES faculty_director_educations(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    degree VARCHAR(255) NOT NULL,
    university VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (education_id, lang_code)
);





CREATE TABLE faculty_deputy_deans (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE faculty_deputy_dean_tr (
    id SERIAL PRIMARY KEY,
    deputy_dean_id INT NOT NULL REFERENCES faculty_deputy_deans(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    duty VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (deputy_dean_id, lang_code)
);

CREATE TABLE faculty_scientific_council (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE faculty_council_member_tr (
    id SERIAL PRIMARY KEY,
    council_member_id INT NOT NULL REFERENCES faculty_scientific_council(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    duty VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (council_member_id, lang_code)
);

CREATE TABLE faculty_workers (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE faculty_worker_tr (
    id SERIAL PRIMARY KEY,
    worker_id INT NOT NULL REFERENCES faculty_workers(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    duty VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (worker_id, lang_code)
);





CREATE TABLE faculty_directions_of_action (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE faculty_direction_of_action_tr (
    id SERIAL PRIMARY KEY,
    direction_of_action_id INT NOT NULL REFERENCES faculty_directions_of_action(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    UNIQUE (direction_of_action_id, lang_code)
);