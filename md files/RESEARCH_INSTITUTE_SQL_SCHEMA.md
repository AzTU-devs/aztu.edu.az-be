CREATE TABLE research_institutes (
    id SERIAL PRIMARY KEY,
    institute_code VARCHAR(50) NOT NULL,
    image_url VARCHAR(1024),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_research_institutes_code UNIQUE (institute_code)
);


CREATE TABLE research_institutes_tr (
    id SERIAL PRIMARY KEY,
    institute_code VARCHAR(50) NOT NULL REFERENCES research_institutes(institute_code) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    name VARCHAR(255) NOT NULL,
    about TEXT,
    vision TEXT,
    mission TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_research_institutes_tr_code_lang UNIQUE (institute_code, lang_code)
);


CREATE TABLE institute_objectives (
    id SERIAL PRIMARY KEY,
    institute_code VARCHAR(50) NOT NULL REFERENCES research_institutes(institute_code) ON DELETE CASCADE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);


CREATE TABLE institute_objective_tr (
    id SERIAL PRIMARY KEY,
    objective_id INTEGER NOT NULL REFERENCES institute_objectives(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_institute_objective_tr_id_lang UNIQUE (objective_id, lang_code)
);


CREATE TABLE institute_research_directions (
    id SERIAL PRIMARY KEY,
    institute_code VARCHAR(50) NOT NULL REFERENCES research_institutes(institute_code) ON DELETE CASCADE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);


CREATE TABLE institute_research_direction_tr (
    id SERIAL PRIMARY KEY,
    research_direction_id INTEGER NOT NULL REFERENCES institute_research_directions(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_institute_rd_tr_id_lang UNIQUE (research_direction_id, lang_code)
);


CREATE TABLE institute_directors (
    id SERIAL PRIMARY KEY,
    institute_code VARCHAR(50) NOT NULL REFERENCES research_institutes(institute_code) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    office VARCHAR(100),
    image_url VARCHAR(1024),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_institute_directors_code UNIQUE (institute_code)
);


CREATE TABLE institute_director_tr (
    id SERIAL PRIMARY KEY,
    director_id INTEGER NOT NULL REFERENCES institute_directors(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255),
    biography TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_institute_director_tr_id_lang UNIQUE (director_id, lang_code)
);


CREATE TABLE institute_director_educations (
    id SERIAL PRIMARY KEY,
    director_id INTEGER NOT NULL REFERENCES institute_directors(id) ON DELETE CASCADE,
    start_year VARCHAR(50),
    end_year VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);


CREATE TABLE institute_director_education_tr (
    id SERIAL PRIMARY KEY,
    education_id INTEGER NOT NULL REFERENCES institute_director_educations(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    university VARCHAR(255) NOT NULL,
    degree VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_director_edu_tr_id_lang UNIQUE (education_id, lang_code)
);


CREATE TABLE director_research_areas (
    id SERIAL PRIMARY KEY,
    director_id INTEGER NOT NULL REFERENCES institute_directors(id) ON DELETE CASCADE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);


CREATE TABLE director_research_area_tr (
    id SERIAL PRIMARY KEY,
    research_area_id INTEGER NOT NULL REFERENCES director_research_areas(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_director_ra_tr_id_lang UNIQUE (research_area_id, lang_code)
);


CREATE TABLE institute_staff (
    id SERIAL PRIMARY KEY,
    institute_code VARCHAR(50) NOT NULL REFERENCES research_institutes(institute_code) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    image_url VARCHAR(1024),
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);


CREATE TABLE institute_staff_tr (
    id SERIAL PRIMARY KEY,
    staff_id INTEGER NOT NULL REFERENCES institute_staff(id) ON DELETE CASCADE,
    lang_code VARCHAR(10) NOT NULL,
    title VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_institute_staff_tr_id_lang UNIQUE (staff_id, lang_code)
);
```
