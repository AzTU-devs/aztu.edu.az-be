-- Information Technology Department (İnformasiya Texnologiyaları departamenti) Seed Data
DO $$
DECLARE
    dept_code VARCHAR(50) := 'it_department';
    obj_id INT;
    func_id INT;
    dir_id INT;
    wh_id INT;
    edu_id INT;
    w_id INT;
BEGIN
    -- 1. Departament
    INSERT INTO departments (department_code, created_at)
    VALUES (dept_code, NOW())
    ON CONFLICT (department_code) DO NOTHING;

    -- 2. Departament Tərcümələri (Haqqında)
    INSERT INTO departments_tr (department_code, lang_code, department_name, about_html, created_at)
    VALUES 
    (dept_code, 'az', 'İnformasiya Texnologiyaları departamenti', 
    '<p>İnformasiya Texnologiyaları departamenti Universitetin texnoloji sistemlərini idarə edən və eyni zamanda həm akademik, həm də inzibati heyətə texniki xidmət göstərən şöbədir. Departament öz fəaliyyətində əsasnamə, fəaliyyət planı və hesabatlılıq prinsiplərini rəhbər tutur.</p>', NOW()),
    (dept_code, 'en', 'Information Technology Department', 
    '<p>The Information Technology Department is responsible for managing the university’s technological systems and providing technical services to both academic and administrative staff. The department is guided by its regulations, action plans, and reporting principles in its activities.</p>', NOW())
    ON CONFLICT (department_code, lang_code) DO NOTHING;

    -- 3. Məqsəd (Objectives)
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Departamentin əsas məqsədi texnoloji resurslardan istifadə edərək Universitetin daxili proseslərini sürətləndirməkdir.', NOW()),
    (obj_id, 'en', 'The main goal of the department is to accelerate the University’s internal processes by utilizing technological resources.', NOW());

    -- 4. Fəaliyyət istiqamətləri (Core Functions)
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Universitetin vahid kompüter şəbəkəsinin yaradılmasını və bu şəbəkənin fasiləsiz fəaliyyətini təmin edir.', NOW()),
    (func_id, 'en', 'Ensures the creation and continuous operation of the university’s unified computer network.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Elektron poçtun, internet səhifəsinin, mövcud sistemlərin və proqram təminatlarının fəaliyyətini tənzimləyir.', NOW()),
    (func_id, 'en', 'Regulates the operation of email services, the website, existing systems, and software.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Elektron informasiya ehtiyatlarının nüsxələrini arxivləşdirir.', NOW()),
    (func_id, 'en', 'Archives copies of electronic information resources.', NOW());

    -- 5. Departament Müdiri (Director)
    INSERT INTO department_directors (department_code, first_name, last_name, father_name, room_number, created_at)
    VALUES (dept_code, 'İnam', 'Həsənov', 'Mədət oğlu', 'II korpus, 303-cü otaq', NOW())
    RETURNING id INTO dir_id;

    INSERT INTO department_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, created_at)
    VALUES 
    (dir_id, 'az', 'Bakalavr', NULL, 
    'İnam Mədət oğlu Həsənov 16 mart 1984-cü ildə Bakı şəhərində anadan olmuşdur. 2012-ci ildə Azərbaycan Texniki Universitetinin İnformatika və Kompüter Texnologiyaları fakültəsini bitirmişdir. 2006-cı ildə "Unitech Co, LTD" şirkətində servis meneceri, 2012-ci ildə Dövlət Torpaq və Xəritəçəkmə Komitəsində İT şöbəsinin müdiri, 2015-ci ildə "Təmiz Şəhər" ASC-də Elektron idarəetmə şöbəsinin müdiri, 2022-ci ildə "Daşkəsən Dəmir Filiz" MMC-də İKT şöbəsinin müdiri vəzifələrində çalışmışdır. 2024-cü ildən etibarən Azərbaycan Texniki Universitetində İT departamentinin müdiri vəzifəsində çalışır.', NOW()),
    (dir_id, 'en', 'Bachelor', NULL, 
    'Inam Madat oglu Hasanov was born on March 16, 1984, in Baku. In 2012, he graduated from the Faculty of Informatics and Computer Technology of Azerbaijan Technical University. He previously served as a Service Manager at Unitech Co, LTD (2006), Head of the IT Department at the State Committee for Land and Cartography (2012), Head of the Electronic Management Department at Tamiz Shahar JSC (2015), and Head of the ICT Department at Dashkasan Iron Ore LLC (2022). Since 2024, he has been the Head of the IT Department at Azerbaijan Technical University.', NOW());

    -- Təhsil
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '2008', '2012', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES 
    (edu_id, 'az', 'Bakalavr, İnformatika və Kompüter Texnologiyaları', 'Azərbaycan Texniki Universiteti', NOW()),
    (edu_id, 'en', 'Bachelor, Informatics and Computer Technology', 'Azerbaijan Technical University', NOW());

    -- 6. Əlaqə məlumatları (Working Hours / Contact)
    INSERT INTO department_director_working_hours (director_id, time_range, created_at)
    VALUES (dir_id, '09:00 – 17:30', NOW()) RETURNING id INTO wh_id;
    INSERT INTO department_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
    VALUES 
    (wh_id, 'az', 'Bazar ertəsi – Cuma', NOW()),
    (wh_id, 'en', 'Monday – Friday', NOW());

    -- 7. Əməkdaşlar (Personnel)
    -- 1. Lalə Rüstəmova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Lalə', 'Rüstəmova', 'Məzahir qızı', 'lala.rustamova@aztu.edu.az', '(+994) 50 376 42 20', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Bakalavr', NOW()), (w_id, 'en', 'Specialist', 'Bachelor', NOW());

    -- 2. Həsənov Kənan
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Kənan', 'Həsənov', 'Sahib oğlu', 'kenan.hesenov@aztu.edu.az', '+994 55 943 13 74', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Magistr', NOW()), (w_id, 'en', 'Specialist', 'Master', NOW());

    -- 3. Ruhid Novruzov
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Ruhid', 'Novruzov', 'Seymur oğlu', 'ruhid.novruzov@aztu.edu.az', '(+994) 050 779 60 99', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Bakalavr', NOW()), (w_id, 'en', 'Specialist', 'Bachelor', NOW());

    -- 4. Ceyhun Qasımov
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Ceyhun', 'Qasımov', 'Müqabil oğlu', 'jeyhun.gasimov@aztu.edu.az', '+994 70 825 00 19', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Bakalavr', NOW()), (w_id, 'en', 'Specialist', 'Bachelor', NOW());

    -- 5. Sərxan Mövsümov
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Sərxan', 'Mövsümov', 'Orxan oğlu', 'sarkhan.movsumov@aztu.edu.az', '+994 50 604 77 67', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Magistr', NOW()), (w_id, 'en', 'Specialist', 'Master', NOW());

    -- 6. Leyla Əhmədova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Leyla', 'Əhmədova', 'Məhəmməd qızı', 'leyla.akhmadova@aztu.edu.az', '+994 77 825 47 19', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Magistr', NOW()), (w_id, 'en', 'Specialist', 'Master', NOW());

    -- 7. Mikayıl İbrahim
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Mikayıl', 'İbrahim', 'Asif oğlu', 'mikayil.ibrahim@aztu.edu.az', '+994 50 834 60 16', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Bakalavr', NOW()), (w_id, 'en', 'Specialist', 'Bachelor', NOW());

    -- 8. Məhəmməd Bağırov
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Məhəmməd', 'Bağırov', 'Tair oğlu', 'mahammad.bagirov@aztu.edu.az', '+994 70 433 73 38', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Magistr', NOW()), (w_id, 'en', 'Specialist', 'Master', NOW());

    -- 9. Soltan Məlikov
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Soltan', 'Məlikov', 'Müşfiq oğlu', 'soltan.malikov@aztu.edu.az', '055 847 44 03', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Bakalavr', NOW()), (w_id, 'en', 'Specialist', 'Bachelor', NOW());

    -- 10. Günel Məmmədli
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Günel', 'Məmmədli', 'Mirzə qızı', 'gunel.memmedli@aztu.edu.az', '(+994) 51 543 96 10', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Magistr', NOW()), (w_id, 'en', 'Specialist', 'Master', NOW());

    -- 11. Elçin Əliyev
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Elçin', 'Əliyev', 'Rəşid oğlu', 'elchinaliyev@aztu.edu.az', '(+994) 55 572 03 64', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', 'Magistr', NOW()), (w_id, 'en', 'Specialist', 'Master', NOW());

END $$;
