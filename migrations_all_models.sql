-- =====================================================================
-- PostgreSQL schema generated from SQLAlchemy models in app/models/
-- =====================================================================

-- ---------------------------------------------------------------------
-- ENUM TYPES
-- ---------------------------------------------------------------------
do $$ begin
    create type education_level_enum as enum ('bachelor', 'master');
exception when duplicate_object then null; end $$;

do $$ begin
    create type degree_level_enum as enum ('Bachelor', 'Master', 'PhD');
exception when duplicate_object then null; end $$;

do $$ begin
    create type day_of_week_enum as enum ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
exception when duplicate_object then null; end $$;


-- ---------------------------------------------------------------------
-- ADMIN
-- ---------------------------------------------------------------------
create table if not exists admin_users (
    id integer primary key,
    username varchar(50) not null unique,
    hashed_password varchar(255) not null,
    is_active boolean not null default true,
    created_at timestamptz not null default current_timestamp,
    updated_at timestamptz,
    last_login_at timestamptz,
    refresh_token_hash varchar(255)
);
create index if not exists ix_admin_users_username on admin_users (username);


-- ---------------------------------------------------------------------
-- FACULTIES (parent of cafedras / employees etc.)
-- ---------------------------------------------------------------------
create table if not exists faculties (
    id integer primary key,
    faculty_code varchar(50) not null unique,
    bachelor_programs_count integer default 0,
    master_programs_count integer default 0,
    phd_programs_count integer default 0,
    international_collaborations_count integer default 0,
    laboratories_count integer default 0,
    projects_patents_count integer default 0,
    industrial_collaborations_count integer default 0,
    sdgs jsonb default '[]'::jsonb,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculties_tr (
    id integer primary key,
    faculty_name varchar(255) not null,
    about_text text,
    faculty_code varchar(50) not null,
    lang_code varchar(10) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculties_tr_code_lang unique (faculty_code, lang_code)
);

create table if not exists faculty_directors (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    room_number varchar(50),
    profile_image varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_directors_code unique (faculty_code)
);

create table if not exists faculty_director_tr (
    id integer primary key,
    director_id integer not null references faculty_directors(id) on delete cascade,
    lang_code varchar(10) not null,
    scientific_degree varchar(255),
    scientific_title varchar(255),
    bio text,
    scientific_research_fields jsonb default '[]'::jsonb,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_director_tr_id_lang unique (director_id, lang_code)
);

create table if not exists faculty_director_working_hours (
    id integer primary key,
    director_id integer not null references faculty_directors(id) on delete cascade,
    time_range varchar(50) not null,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_director_working_hour_tr (
    id integer primary key,
    working_hour_id integer not null references faculty_director_working_hours(id) on delete cascade,
    lang_code varchar(10) not null,
    day varchar(50) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_director_working_hour_tr_id_lang unique (working_hour_id, lang_code)
);

create table if not exists faculty_director_scientific_events (
    id integer primary key,
    director_id integer not null references faculty_directors(id) on delete cascade,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_director_scientific_event_tr (
    id integer primary key,
    scientific_event_id integer not null references faculty_director_scientific_events(id) on delete cascade,
    lang_code varchar(10) not null,
    event_title varchar(255) not null,
    event_description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_director_scientific_event_tr_id_lang unique (scientific_event_id, lang_code)
);

create table if not exists faculty_director_educations (
    id integer primary key,
    director_id integer not null references faculty_directors(id) on delete cascade,
    start_year varchar(20),
    end_year varchar(20),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_director_education_tr (
    id integer primary key,
    education_id integer not null references faculty_director_educations(id) on delete cascade,
    lang_code varchar(10) not null,
    degree varchar(255) not null,
    university varchar(255) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_director_education_tr_id_lang unique (education_id, lang_code)
);

create table if not exists faculty_laboratories (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_laboratory_tr (
    id integer primary key,
    laboratory_id integer not null references faculty_laboratories(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_laboratory_tr_id_lang unique (laboratory_id, lang_code)
);

create table if not exists faculty_research_works (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_research_work_tr (
    id integer primary key,
    research_work_id integer not null references faculty_research_works(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_research_work_tr_id_lang unique (research_work_id, lang_code)
);

create table if not exists faculty_partner_companies (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_partner_company_tr (
    id integer primary key,
    partner_company_id integer not null references faculty_partner_companies(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_partner_company_tr_id_lang unique (partner_company_id, lang_code)
);

create table if not exists faculty_objectives (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_objective_tr (
    id integer primary key,
    objective_id integer not null references faculty_objectives(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_objective_tr_id_lang unique (objective_id, lang_code)
);

create table if not exists faculty_duties (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_duty_tr (
    id integer primary key,
    duty_id integer not null references faculty_duties(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_duty_tr_id_lang unique (duty_id, lang_code)
);

create table if not exists faculty_projects (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_project_tr (
    id integer primary key,
    project_id integer not null references faculty_projects(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_project_tr_id_lang unique (project_id, lang_code)
);

create table if not exists faculty_directions_of_action (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_direction_of_action_tr (
    id integer primary key,
    direction_of_action_id integer not null references faculty_directions_of_action(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_direction_of_action_tr_id_lang unique (direction_of_action_id, lang_code)
);

create table if not exists faculty_deputy_deans (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    profile_image varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_deputy_dean_tr (
    id integer primary key,
    deputy_dean_id integer not null references faculty_deputy_deans(id) on delete cascade,
    lang_code varchar(10) not null,
    scientific_name varchar(255),
    scientific_degree varchar(255),
    duty varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_deputy_dean_tr_id_lang unique (deputy_dean_id, lang_code)
);

create table if not exists faculty_scientific_council (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_council_member_tr (
    id integer primary key,
    council_member_id integer not null references faculty_scientific_council(id) on delete cascade,
    lang_code varchar(10) not null,
    duty varchar(255) not null,
    scientific_name varchar(255),
    scientific_degree varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_council_member_tr_id_lang unique (council_member_id, lang_code)
);

create table if not exists faculty_workers (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    profile_image varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists faculty_worker_tr (
    id integer primary key,
    worker_id integer not null references faculty_workers(id) on delete cascade,
    lang_code varchar(10) not null,
    duty varchar(255) not null,
    scientific_name varchar(255),
    scientific_degree varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_faculty_worker_tr_id_lang unique (worker_id, lang_code)
);


-- ---------------------------------------------------------------------
-- CAFEDRAS
-- ---------------------------------------------------------------------
create table if not exists cafedras (
    id integer primary key,
    faculty_code varchar(50) not null references faculties(faculty_code) on delete cascade,
    cafedra_code varchar(50) not null,
    bachelor_programs_count integer default 0,
    master_programs_count integer default 0,
    phd_programs_count integer default 0,
    international_collaborations_count integer default 0,
    laboratories_count integer default 0,
    projects_patents_count integer default 0,
    industrial_collaborations_count integer default 0,
    sdgs jsonb default '[]'::jsonb,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedras_code unique (cafedra_code)
);

create table if not exists cafedras_tr (
    id integer primary key,
    cafedra_name varchar(255) not null,
    about_text text,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    lang_code varchar(10) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedras_tr_code_lang unique (cafedra_code, lang_code)
);

create table if not exists cafedra_directors (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    room_number varchar(50),
    profile_image varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_directors_code unique (cafedra_code)
);

create table if not exists cafedra_director_tr (
    id integer primary key,
    director_id integer not null references cafedra_directors(id) on delete cascade,
    lang_code varchar(10) not null,
    scientific_degree varchar(255),
    scientific_title varchar(255),
    bio text,
    scientific_research_fields jsonb default '[]'::jsonb,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_director_tr_id_lang unique (director_id, lang_code)
);

create table if not exists cafedra_director_working_hours (
    id integer primary key,
    director_id integer not null references cafedra_directors(id) on delete cascade,
    time_range varchar(50) not null,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_director_working_hour_tr (
    id integer primary key,
    working_hour_id integer not null references cafedra_director_working_hours(id) on delete cascade,
    lang_code varchar(10) not null,
    day varchar(50) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_director_working_hour_tr_id_lang unique (working_hour_id, lang_code)
);

create table if not exists cafedra_director_educations (
    id integer primary key,
    director_id integer not null references cafedra_directors(id) on delete cascade,
    start_year varchar(20),
    end_year varchar(20),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_director_education_tr (
    id integer primary key,
    education_id integer not null references cafedra_director_educations(id) on delete cascade,
    lang_code varchar(10) not null,
    degree varchar(255) not null,
    university varchar(255) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_director_education_tr_id_lang unique (education_id, lang_code)
);

create table if not exists cafedra_director_scientific_events (
    id integer primary key,
    director_id integer not null references cafedra_directors(id) on delete cascade,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_director_scientific_event_tr (
    id integer primary key,
    scientific_event_id integer not null references cafedra_director_scientific_events(id) on delete cascade,
    lang_code varchar(10) not null,
    event_title varchar(255) not null,
    event_description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_director_scientific_event_tr_id_lang unique (scientific_event_id, lang_code)
);

create table if not exists cafedra_laboratories (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    image_url varchar(1024),
    room_number varchar(50),
    authorized_person varchar(255),
    email varchar(255),
    phone_number varchar(50),
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_laboratory_tr (
    id integer primary key,
    laboratory_id integer not null references cafedra_laboratories(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_laboratory_tr_id_lang unique (laboratory_id, lang_code)
);

create table if not exists cafedra_laboratory_objectives (
    id integer primary key,
    laboratory_id integer not null references cafedra_laboratories(id) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_laboratory_objective_tr (
    id integer primary key,
    objective_id integer not null references cafedra_laboratory_objectives(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(500) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_lab_objective_tr_id_lang unique (objective_id, lang_code)
);

create table if not exists cafedra_laboratory_equipments (
    id integer primary key,
    laboratory_id integer not null references cafedra_laboratories(id) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_laboratory_equipment_tr (
    id integer primary key,
    equipment_id integer not null references cafedra_laboratory_equipments(id) on delete cascade,
    lang_code varchar(10) not null,
    name varchar(500) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_lab_equipment_tr_id_lang unique (equipment_id, lang_code)
);

create table if not exists cafedra_laboratory_gallery_images (
    id integer primary key,
    laboratory_id integer not null references cafedra_laboratories(id) on delete cascade,
    image_url varchar(1024) not null,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_research_works (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_research_work_tr (
    id integer primary key,
    research_work_id integer not null references cafedra_research_works(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_research_work_tr_id_lang unique (research_work_id, lang_code)
);

create table if not exists cafedra_partner_companies (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_partner_company_tr (
    id integer primary key,
    partner_company_id integer not null references cafedra_partner_companies(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_partner_company_tr_id_lang unique (partner_company_id, lang_code)
);

create table if not exists cafedra_objectives (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_objective_tr (
    id integer primary key,
    objective_id integer not null references cafedra_objectives(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_objective_tr_id_lang unique (objective_id, lang_code)
);

create table if not exists cafedra_duties (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_duty_tr (
    id integer primary key,
    duty_id integer not null references cafedra_duties(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_duty_tr_id_lang unique (duty_id, lang_code)
);

create table if not exists cafedra_projects (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_project_tr (
    id integer primary key,
    project_id integer not null references cafedra_projects(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_project_tr_id_lang unique (project_id, lang_code)
);

create table if not exists cafedra_directions_of_action (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    display_order integer default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_direction_of_action_tr (
    id integer primary key,
    direction_of_action_id integer not null references cafedra_directions_of_action(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255) not null,
    description text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_doa_tr_id_lang unique (direction_of_action_id, lang_code)
);

create table if not exists cafedra_workers (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    profile_image varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_worker_tr (
    id integer primary key,
    worker_id integer not null references cafedra_workers(id) on delete cascade,
    lang_code varchar(10) not null,
    duty varchar(255) not null,
    scientific_name varchar(255),
    scientific_degree varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_worker_tr_id_lang unique (worker_id, lang_code)
);

create table if not exists cafedra_deputy_directors (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    profile_image varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_deputy_director_tr (
    id integer primary key,
    deputy_director_id integer not null references cafedra_deputy_directors(id) on delete cascade,
    lang_code varchar(10) not null,
    scientific_name varchar(255),
    scientific_degree varchar(255),
    duty varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_deputy_director_tr_id_lang unique (deputy_director_id, lang_code)
);

create table if not exists cafedra_scientific_council (
    id integer primary key,
    cafedra_code varchar(50) not null references cafedras(cafedra_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists cafedra_council_member_tr (
    id integer primary key,
    council_member_id integer not null references cafedra_scientific_council(id) on delete cascade,
    lang_code varchar(10) not null,
    duty varchar(255) not null,
    scientific_name varchar(255),
    scientific_degree varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_cafedra_council_member_tr_id_lang unique (council_member_id, lang_code)
);


-- ---------------------------------------------------------------------
-- DEPARTMENTS
-- ---------------------------------------------------------------------
create table if not exists departments (
    id integer primary key,
    department_code varchar(50) not null unique,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists departments_tr (
    id integer primary key,
    department_code varchar(50) not null references departments(department_code) on delete cascade,
    lang_code varchar(10) not null,
    department_name varchar(255) not null,
    about_html text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_departments_tr_code_lang unique (department_code, lang_code)
);

create table if not exists department_directors (
    id integer primary key,
    department_code varchar(50) not null references departments(department_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    room_number varchar(50),
    profile_image varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_department_directors_code unique (department_code)
);

create table if not exists department_director_tr (
    id integer primary key,
    director_id integer not null references department_directors(id) on delete cascade,
    lang_code varchar(10) not null,
    scientific_degree varchar(255),
    scientific_title varchar(255),
    bio text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_department_director_tr_id_lang unique (director_id, lang_code)
);

create table if not exists department_director_working_hours (
    id integer primary key,
    director_id integer not null references department_directors(id) on delete cascade,
    time_range varchar(50) not null,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists department_director_working_hour_tr (
    id integer primary key,
    working_hour_id integer not null references department_director_working_hours(id) on delete cascade,
    lang_code varchar(10) not null,
    day varchar(50) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_department_director_working_hour_tr_id_lang unique (working_hour_id, lang_code)
);

create table if not exists department_director_educations (
    id integer primary key,
    director_id integer not null references department_directors(id) on delete cascade,
    start_year varchar(20),
    end_year varchar(20),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists department_director_education_tr (
    id integer primary key,
    education_id integer not null references department_director_educations(id) on delete cascade,
    lang_code varchar(10) not null,
    degree varchar(255) not null,
    university varchar(255) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_department_director_education_tr_id_lang unique (education_id, lang_code)
);

create table if not exists department_objectives (
    id integer primary key,
    department_code varchar(50) not null references departments(department_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists department_objective_tr (
    id integer primary key,
    objective_id integer not null references department_objectives(id) on delete cascade,
    lang_code varchar(10) not null,
    html_content text not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_department_objective_tr_id_lang unique (objective_id, lang_code)
);

create table if not exists department_core_functions (
    id integer primary key,
    department_code varchar(50) not null references departments(department_code) on delete cascade,
    display_order integer not null default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists department_core_function_tr (
    id integer primary key,
    core_function_id integer not null references department_core_functions(id) on delete cascade,
    lang_code varchar(10) not null,
    html_content text not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_department_core_function_tr_id_lang unique (core_function_id, lang_code)
);

create table if not exists department_workers (
    id integer primary key,
    department_code varchar(50) not null references departments(department_code) on delete cascade,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    father_name varchar(100),
    email varchar(255),
    phone varchar(50),
    profile_image varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists department_worker_tr (
    id integer primary key,
    worker_id integer not null references department_workers(id) on delete cascade,
    lang_code varchar(10) not null,
    duty varchar(255) not null,
    scientific_degree varchar(255),
    scientific_name varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_department_worker_tr_id_lang unique (worker_id, lang_code)
);


-- ---------------------------------------------------------------------
-- RESEARCH INSTITUTES
-- ---------------------------------------------------------------------
create table if not exists research_institutes (
    id integer primary key,
    institute_code varchar(50) not null,
    image_url varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_research_institutes_code unique (institute_code)
);

create table if not exists research_institutes_tr (
    id integer primary key,
    institute_code varchar(50) not null references research_institutes(institute_code) on delete cascade,
    lang_code varchar(10) not null,
    name varchar(255) not null,
    about text,
    vision text,
    mission text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_research_institutes_tr_code_lang unique (institute_code, lang_code)
);

create table if not exists institute_objectives (
    id integer primary key,
    institute_code varchar(50) not null references research_institutes(institute_code) on delete cascade,
    display_order integer default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists institute_objective_tr (
    id integer primary key,
    objective_id integer not null references institute_objectives(id) on delete cascade,
    lang_code varchar(10) not null,
    content text not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_institute_objective_tr_id_lang unique (objective_id, lang_code)
);

create table if not exists institute_research_directions (
    id integer primary key,
    institute_code varchar(50) not null references research_institutes(institute_code) on delete cascade,
    display_order integer default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists institute_research_direction_tr (
    id integer primary key,
    research_direction_id integer not null references institute_research_directions(id) on delete cascade,
    lang_code varchar(10) not null,
    content text not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_institute_rd_tr_id_lang unique (research_direction_id, lang_code)
);

create table if not exists institute_directors (
    id integer primary key,
    institute_code varchar(50) not null references research_institutes(institute_code) on delete cascade,
    full_name varchar(255) not null,
    email varchar(255),
    office varchar(100),
    image_url varchar(1024),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_institute_directors_code unique (institute_code)
);

create table if not exists institute_director_tr (
    id integer primary key,
    director_id integer not null references institute_directors(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255),
    biography text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_institute_director_tr_id_lang unique (director_id, lang_code)
);

create table if not exists institute_director_educations (
    id integer primary key,
    director_id integer not null references institute_directors(id) on delete cascade,
    start_year varchar(50),
    end_year varchar(50),
    display_order integer default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists institute_director_education_tr (
    id integer primary key,
    education_id integer not null references institute_director_educations(id) on delete cascade,
    lang_code varchar(10) not null,
    university varchar(255) not null,
    degree varchar(255) not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_director_edu_tr_id_lang unique (education_id, lang_code)
);

create table if not exists director_research_areas (
    id integer primary key,
    director_id integer not null references institute_directors(id) on delete cascade,
    display_order integer default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists director_research_area_tr (
    id integer primary key,
    research_area_id integer not null references director_research_areas(id) on delete cascade,
    lang_code varchar(10) not null,
    content text not null,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_director_ra_tr_id_lang unique (research_area_id, lang_code)
);

create table if not exists institute_staff (
    id integer primary key,
    institute_code varchar(50) not null references research_institutes(institute_code) on delete cascade,
    full_name varchar(255) not null,
    email varchar(255),
    phone varchar(50),
    image_url varchar(1024),
    display_order integer default 0,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists institute_staff_tr (
    id integer primary key,
    staff_id integer not null references institute_staff(id) on delete cascade,
    lang_code varchar(10) not null,
    title varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_institute_staff_tr_id_lang unique (staff_id, lang_code)
);


-- ---------------------------------------------------------------------
-- EMPLOYEES
-- ---------------------------------------------------------------------
create table if not exists employees (
    id integer primary key,
    employee_code varchar(50) not null unique,
    profile_image varchar(255),
    faculty_code varchar(50) references faculties(faculty_code) on delete set null,
    cafedra_code varchar(50) references cafedras(cafedra_code) on delete set null,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists employee_tr (
    id integer primary key,
    employee_code varchar(50) not null references employees(employee_code) on delete cascade,
    lang_code varchar(10) not null,
    first_name varchar(100),
    last_name varchar(100),
    full_name varchar(255),
    academic_degree varchar(100),
    academic_title varchar(100),
    position varchar(255),
    scientific_interests text,
    biography text,
    created_at timestamptz not null,
    updated_at timestamptz,
    constraint uq_employee_tr_code_lang unique (employee_code, lang_code)
);

create table if not exists employee_contacts (
    id integer primary key,
    employee_code varchar(50) not null unique references employees(employee_code) on delete cascade,
    email varchar(255) not null,
    phone varchar(50) not null,
    building varchar(100) not null,
    floor varchar(20) not null,
    room varchar(50) not null,
    constraint uq_employee_contacts_code unique (employee_code)
);

create table if not exists employee_research (
    id integer primary key,
    employee_code varchar(50) not null unique references employees(employee_code) on delete cascade,
    scopus_url text,
    google_scholar_url text,
    orcid_url text,
    researchgate_url text,
    academia_url text,
    publications text,
    constraint uq_employee_research_code unique (employee_code)
);

create table if not exists office_hours (
    id integer primary key,
    employee_code varchar(50) not null references employees(employee_code) on delete cascade,
    day_of_week day_of_week_enum not null,
    start_time time not null,
    end_time time not null
);

create table if not exists education (
    id integer primary key,
    employee_code varchar(50) not null references employees(employee_code) on delete cascade,
    degree_level degree_level_enum not null,
    graduation_year integer
);

create table if not exists education_tr (
    id integer primary key,
    education_id integer not null references education(id) on delete cascade,
    lang_code varchar(10) not null,
    institution varchar(255),
    specialization varchar(255),
    constraint uq_education_tr_id_lang unique (education_id, lang_code)
);

create table if not exists teaching_courses (
    id integer primary key,
    employee_code varchar(50) not null references employees(employee_code) on delete cascade,
    education_level education_level_enum not null
);

create table if not exists teaching_course_tr (
    id integer primary key,
    course_id integer not null references teaching_courses(id) on delete cascade,
    lang_code varchar(10) not null,
    course_name varchar(255) not null,
    constraint uq_teaching_course_tr_id_lang unique (course_id, lang_code)
);


-- ---------------------------------------------------------------------
-- CHAT
-- ---------------------------------------------------------------------
create table if not exists chat_sessions (
    id integer primary key,
    session_id varchar(36) not null unique,
    ip_address varchar(45) not null,
    started_at timestamptz not null default current_timestamp,
    last_active_at timestamptz not null default current_timestamp
);
create index if not exists ix_chat_sessions_session_id on chat_sessions (session_id);

create table if not exists chat_messages (
    id integer primary key,
    session_id varchar(36) not null references chat_sessions(session_id) on delete cascade,
    role varchar(10) not null,
    content text not null,
    created_at timestamptz not null default current_timestamp
);
create index if not exists ix_chat_messages_session_id on chat_messages (session_id);

create table if not exists chatbot_knowledge_sources (
    id integer primary key,
    url text not null unique,
    label varchar(255),
    is_active boolean not null default true,
    last_scraped_at timestamptz,
    created_at timestamptz not null default current_timestamp
);

create table if not exists chatbot_knowledge (
    id integer primary key,
    source_id integer not null references chatbot_knowledge_sources(id) on delete cascade,
    content text not null,
    scraped_at timestamptz not null default current_timestamp,
    is_active boolean not null default true
);
create index if not exists ix_chatbot_knowledge_source_id on chatbot_knowledge (source_id);


-- ---------------------------------------------------------------------
-- COLLABORATION
-- ---------------------------------------------------------------------
create table if not exists collaboration (
    id integer primary key,
    collaboration_id integer not null unique,
    logo text not null,
    website_url text,
    display_order integer not null,
    is_active boolean not null default true,
    created_at timestamptz not null default current_timestamp,
    updated_at timestamptz
);

create table if not exists collaboration_translation (
    id integer primary key,
    collaboration_id integer not null references collaboration(collaboration_id),
    lang_code varchar(2) not null,
    name varchar(255) not null
);


-- ---------------------------------------------------------------------
-- PROJECT
-- ---------------------------------------------------------------------
create table if not exists project (
    id integer primary key,
    project_id integer not null unique,
    bg_image text not null,
    display_order integer not null,
    is_active boolean not null default true,
    created_at timestamptz not null default current_timestamp,
    updated_at timestamptz
);

create table if not exists project_translation (
    id integer primary key,
    project_id integer not null references project(project_id),
    lang_code varchar(2) not null,
    title text not null,
    description text not null,
    html_content text not null
);


-- ---------------------------------------------------------------------
-- NEWS / NEWS CATEGORY / GALLERY
-- ---------------------------------------------------------------------
create table if not exists news_category (
    id integer primary key,
    category_id integer not null unique,
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists news_category_translation (
    id integer primary key,
    category_id integer not null,
    lang_code varchar(2) not null,
    title text not null
);

create table if not exists news (
    id integer primary key,
    news_id integer not null unique,
    category_id integer not null,
    display_order integer not null,
    is_active boolean not null default true,
    sdg_numbers jsonb,
    faculty_code varchar(50),
    cafedra_code varchar(50),
    created_at timestamptz not null,
    updated_at timestamptz
);

create table if not exists news_translation (
    id integer primary key,
    news_id integer not null,
    lang_code varchar(2) not null,
    title text not null,
    html_content text not null
);

create table if not exists news_gallery (
    id integer primary key,
    news_id integer not null,
    image text not null,
    is_cover boolean not null,
    display_order integer not null default 0
);


-- ---------------------------------------------------------------------
-- ANNOUNCEMENT
-- ---------------------------------------------------------------------
create table if not exists announcement (
    id integer primary key,
    announcement_id integer not null unique,
    image text,
    display_order integer not null,
    is_active boolean not null default false,
    created_at timestamptz not null default current_timestamp,
    updated_at timestamptz,
    published_date date
);

create table if not exists announcement_translation (
    id integer primary key,
    announcement_id integer not null,
    lang_code varchar(2) not null,
    title text not null,
    html_content text not null
);


-- ---------------------------------------------------------------------
-- HERO
-- ---------------------------------------------------------------------
create table if not exists hero (
    id integer primary key,
    hero_id integer not null unique,
    video text not null,
    is_active boolean not null default true,
    created_at timestamptz not null,
    updated_at timestamptz
);


-- ---------------------------------------------------------------------
-- MENU - HEADER
-- ---------------------------------------------------------------------
create table if not exists menu_headers (
    id integer primary key,
    image_url text,
    direct_url varchar(500),
    has_subitems boolean not null default true,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_header_translations (
    id integer primary key,
    header_id integer not null references menu_headers(id) on delete cascade,
    lang_code varchar(5) not null,
    title varchar(200) not null,
    slug varchar(200) not null
);

create table if not exists menu_header_items (
    id integer primary key,
    header_id integer not null references menu_headers(id) on delete cascade,
    direct_url varchar(500),
    has_subitems boolean not null default true,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_header_item_translations (
    id integer primary key,
    item_id integer not null references menu_header_items(id) on delete cascade,
    lang_code varchar(5) not null,
    title varchar(200) not null,
    slug varchar(200) not null
);

create table if not exists menu_header_sub_items (
    id integer primary key,
    item_id integer not null references menu_header_items(id) on delete cascade,
    direct_url varchar(500),
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_header_sub_item_translations (
    id integer primary key,
    sub_item_id integer not null references menu_header_sub_items(id) on delete cascade,
    lang_code varchar(5) not null,
    title varchar(200) not null,
    slug varchar(200) not null
);


-- ---------------------------------------------------------------------
-- MENU - QUICK
-- ---------------------------------------------------------------------
create table if not exists menu_quick_left_items (
    id integer primary key,
    url text not null,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_quick_left_item_translations (
    id integer primary key,
    item_id integer not null references menu_quick_left_items(id) on delete cascade,
    lang_code varchar(5) not null,
    label varchar(200) not null
);

create table if not exists menu_quick_sections (
    id integer primary key,
    section_key varchar(50) not null unique,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_quick_section_translations (
    id integer primary key,
    section_id integer not null references menu_quick_sections(id) on delete cascade,
    lang_code varchar(5) not null,
    title varchar(200) not null
);

create table if not exists menu_quick_section_items (
    id integer primary key,
    section_id integer not null references menu_quick_sections(id) on delete cascade,
    url text not null,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_quick_section_item_translations (
    id integer primary key,
    item_id integer not null references menu_quick_section_items(id) on delete cascade,
    lang_code varchar(5) not null,
    label varchar(200) not null
);


-- ---------------------------------------------------------------------
-- MENU - SHARED
-- ---------------------------------------------------------------------
create table if not exists menu_social_links (
    id integer primary key,
    platform varchar(50) not null,
    url text not null,
    context varchar(20) not null,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_contacts (
    id integer primary key,
    context varchar(20) not null,
    email varchar(200) not null,
    is_active boolean not null default true
);

create table if not exists menu_contact_phones (
    id integer primary key,
    contact_id integer not null references menu_contacts(id) on delete cascade,
    phone varchar(50) not null,
    display_order integer not null
);

create table if not exists menu_contact_addresses (
    id integer primary key,
    contact_id integer not null references menu_contacts(id) on delete cascade,
    lang_code varchar(5) not null,
    address text not null
);


-- ---------------------------------------------------------------------
-- MENU - FOOTER
-- ---------------------------------------------------------------------
create table if not exists menu_footer_columns (
    id integer primary key,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_footer_column_translations (
    id integer primary key,
    column_id integer not null references menu_footer_columns(id) on delete cascade,
    lang_code varchar(5) not null,
    title varchar(200) not null
);

create table if not exists menu_footer_links (
    id integer primary key,
    column_id integer not null references menu_footer_columns(id) on delete cascade,
    url varchar(500) not null,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_footer_link_translations (
    id integer primary key,
    link_id integer not null references menu_footer_links(id) on delete cascade,
    lang_code varchar(5) not null,
    label varchar(200) not null
);

create table if not exists menu_footer_partner_logos (
    id integer primary key,
    label varchar(200) not null,
    image_url text not null,
    url text not null,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_footer_quick_icons (
    id integer primary key,
    icon varchar(100) not null,
    url text not null,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists menu_footer_quick_icon_translations (
    id integer primary key,
    icon_id integer not null references menu_footer_quick_icons(id) on delete cascade,
    lang_code varchar(5) not null,
    label varchar(200) not null
);
