
CREATE TABLE faculties (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);




CREATE TABLE faculties_tr (
    id SERIAL PRIMARY KEY,
    faculty_name VARCHAR(255) NOT NULL,
    about_text TEXT,
    faculty_code VARCHAR(50) NOT NULL,
    lang_code VARCHAR(10) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculties_tr_code_lang UNIQUE (faculty_code, lang_code)
);





CREATE TABLE faculty_directors (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    scientific_degree VARCHAR(255),
    scientific_title VARCHAR(255),
    bio TEXT,
    email VARCHAR(255),
    phone VARCHAR(50),
    room_number VARCHAR(50),
    profile_image VARCHAR(1024),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_director_working_hours (
    id SERIAL PRIMARY KEY,
    director_id INTEGER NOT NULL REFERENCES faculty_directors(id) ON DELETE CASCADE,
    day VARCHAR(50) NOT NULL,
    time_range VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_director_scientific_events (
    id SERIAL PRIMARY KEY,
    director_id INTEGER NOT NULL REFERENCES faculty_directors(id) ON DELETE CASCADE,
    event_title VARCHAR(255) NOT NULL,
    event_description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_director_educations (
    id SERIAL PRIMARY KEY,
    director_id INTEGER NOT NULL REFERENCES faculty_directors(id) ON DELETE CASCADE,
    degree VARCHAR(255) NOT NULL,
    university VARCHAR(255) NOT NULL,
    start_year VARCHAR(20),
    end_year VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_laboratories (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_laboratory_tr (
    id SERIAL PRIMARY KEY,
    laboratory_id INTEGER NOT NULL REFERENCES faculty_laboratories(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_laboratory_tr_id_lang UNIQUE (laboratory_id, lang_code)
);





CREATE TABLE faculty_research_works (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_research_work_tr (
    id SERIAL PRIMARY KEY,
    research_work_id INTEGER NOT NULL REFERENCES faculty_research_works(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_research_work_tr_id_lang UNIQUE (research_work_id, lang_code)
);





CREATE TABLE faculty_partner_companies (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_partner_company_tr (
    id SERIAL PRIMARY KEY,
    partner_company_id INTEGER NOT NULL REFERENCES faculty_partner_companies(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_partner_company_tr_id_lang UNIQUE (partner_company_id, lang_code)
);





CREATE TABLE faculty_objectives (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_objective_tr (
    id SERIAL PRIMARY KEY,
    objective_id INTEGER NOT NULL REFERENCES faculty_objectives(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_objective_tr_id_lang UNIQUE (objective_id, lang_code)
);





CREATE TABLE faculty_duties (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_duty_tr (
    id SERIAL PRIMARY KEY,
    duty_id INTEGER NOT NULL REFERENCES faculty_duties(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_duty_tr_id_lang UNIQUE (duty_id, lang_code)
);


CREATE TABLE faculty_projects (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);


CREATE TABLE faculty_project_tr (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES faculty_projects(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_project_tr_id_lang UNIQUE (project_id, lang_code)
);


CREATE TABLE faculty_directions_of_action (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);


CREATE TABLE faculty_direction_of_action_tr (
    id SERIAL PRIMARY KEY,
    direction_of_action_id INTEGER NOT NULL REFERENCES faculty_directions_of_action(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_direction_of_action_tr_id_lang UNIQUE (direction_of_action_id, lang_code)
);





CREATE TABLE faculty_projects (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_project_tr (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES faculty_projects(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_faculty_project_tr_id_lang UNIQUE (project_id, lang_code)
);





CREATE TABLE faculty_deputy_deans (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    duty VARCHAR(255),
    profile_image VARCHAR(1024),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_scientific_council (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    duty VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);





CREATE TABLE faculty_workers (
    id SERIAL PRIMARY KEY,
    faculty_code VARCHAR(50) NOT NULL REFERENCES faculties(faculty_code) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    duty VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    scientific_degree VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);