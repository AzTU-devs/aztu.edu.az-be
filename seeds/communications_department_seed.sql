-- Communications Department (Kommunikasiya şöbəsi) Seed Data
DO $$
DECLARE
    dept_code VARCHAR(50) := 'communications_department';
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
    (dept_code, 'az', 'Kommunikasiya şöbəsi',
    '<p>Azərbaycan Texniki Universitetinin Kommunikasiya şöbəsi universitet daxilində effektiv əlaqələndirməni təmin edən və tələbə yönümlü fəaliyyətləri dəstəkləyən əsas struktur bölmələrdən biridir.</p><p>Şöbə fakültələr, tələbə təşkilatları və digər struktur bölmələr arasında koordinasiyanı təşkil edir, universitet mühitində aktiv ictimai və sosial həyatın formalaşmasına töhfə verir.</p><p>Kommunikasiya şöbəsi eyni zamanda tələbə təşəbbüslərinin inkişafını təşviq edir, yeni ideyaların reallaşdırılmasına dəstək olur və universitet daxilində sağlam kommunikasiya mühitinin qurulmasına xidmət edir.</p>', NOW()),
    (dept_code, 'en', 'Communications Department',
    '<p>The Communications Department of Azerbaijan Technical University is one of the key structural units that ensures effective coordination within the university and supports student-centered initiatives.</p><p>The department facilitates coordination among faculties, student organizations, and other structural units, contributing to the development of an active social and public environment within the university.</p><p>It also promotes the development of student initiatives, supports the implementation of new ideas, and plays an important role in fostering a healthy and effective communication environment across the university.</p>', NOW())
    ON CONFLICT (department_code, lang_code) DO NOTHING;

    -- 3. Məqsədlər (Objectives)
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Universitet daxilində effektiv kommunikasiya və koordinasiyanı təmin etmək.', NOW()),
    (obj_id, 'en', 'To ensure effective communication and coordination within the university.', NOW());

    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Tələbə təşkilatlarının fəaliyyətini sistemli şəkildə inkişaf etdirmək.', NOW()),
    (obj_id, 'en', 'To systematically develop and strengthen the activities of student organizations.', NOW());

    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Tələbə klublarının yaradılması və inkişafını dəstəkləmək.', NOW()),
    (obj_id, 'en', 'To support the establishment and development of student clubs.', NOW());

    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Sosial, mədəni və ictimai fəaliyyətlərin genişlənməsinə töhfə vermək.', NOW()),
    (obj_id, 'en', 'To contribute to the expansion of social, cultural, and public activities.', NOW());

    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Universitet mühitində aktiv və iştirakçı tələbə icması formalaşdırmaq.', NOW()),
    (obj_id, 'en', 'To foster an active and engaged student community within the university.', NOW());

    -- 4. Əsas fəaliyyət istiqamətləri (Core Functions)
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Fakültələr arasında koordinasiyanın təşkili.', NOW()),
    (func_id, 'en', 'Organizing coordination among faculties.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Tələbə təşkilatlarının fəaliyyətinin əlaqələndirilməsi.', NOW()),
    (func_id, 'en', 'Coordinating the activities of student organizations.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Tələbə klublarının inkişafının dəstəklənməsi və yeni klubların yaradılması.', NOW()),
    (func_id, 'en', 'Supporting the development of student clubs and facilitating the creation of new ones.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Universitet daxilində keçirilən tədbirlərin təşkilində iştirak.', NOW()),
    (func_id, 'en', 'Participating in the organization of events held within the university.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Sosial və ictimai fəaliyyətlərin təşkili və dəstəklənməsi.', NOW()),
    (func_id, 'en', 'Organizing and supporting social and public engagement activities.', NOW());

    -- 5. Şöbə Müdiri (Director)
    INSERT INTO department_directors (department_code, first_name, last_name, father_name, room_number, profile_image, created_at)
    VALUES (dept_code, 'Səfa', 'Bağırov', 'Teyyub oğlu', 'I korpus, 318-ci otaq', '/media/prod/departments/communication/sefa_baghirov.JPG', NOW())
    RETURNING id INTO dir_id;

    INSERT INTO department_director_tr (director_id, lang_code, bio, created_at)
    VALUES
    (dir_id, 'az',
    'Səfa Bağırov kommunikasiya və media sahəsində 20 ildən artıq təcrübəyə malik mütəxəssisdir. Hazırda Azərbaycan Texniki Universitetində Kommunikasiya şöbəsinin müdiri vəzifəsində çalışır. O, fəaliyyətini rəqəmsal kommunikasiya, media istehsalı və institusional brendin inkişafı istiqamətlərində qurmuş, universitet daxilində kommunikasiya strategiyasının formalaşdırılması və tətbiqində mühüm rol oynamışdır. Karyerası ərzində dövlət və özəl sektorda müxtəlif rəhbər vəzifələrdə çalışaraq kommunikasiya sistemlərinin qurulması, media layihələrinin idarə olunması və genişmiqyaslı tədbirlərin təşkili sahəsində təcrübə qazanmışdır.', NOW()),
    (dir_id, 'en',
    'Safa Baghirov is a specialist with over 20 years of experience in the field of communications and media. Currently, he serves as the Head of the Communications Department at Azerbaijan Technical University. His work focuses on digital communication, media production, and institutional brand development, and he has played an important role in shaping and implementing the communication strategy within the university. Throughout his career, he has held various leadership positions in both the public and private sectors, gaining extensive experience in building communication systems, managing media projects, and organizing large-scale events.', NOW());

    -- Təhsil
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '1997', '2001', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES
    (edu_id, 'az', 'Bakalavr, Kommunikasiya fakültəsi', 'Qazi Universiteti', NOW()),
    (edu_id, 'en', 'Bachelor''s Degree, Faculty of Communication', 'Gazi University', NOW());

    -- Əlaqə (director also as worker contact)
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, profile_image, created_at)
    VALUES (dept_code, 'Səfa', 'Bağırov', 'Teyyub oğlu', 'safa.baghirov@aztu.edu.az', '1160 (I korpus, 318-ci otaq)', '/media/prod/departments/communication/sefa_baghirov.JPG', NOW())
    ON CONFLICT DO NOTHING;

    -- 6. Əməkdaşlar (Personnel)
    -- 1. Mehti Namazov
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, profile_image, created_at)
    VALUES (dept_code, 'Mehti', 'Namazov', 'Kamil oğlu', 'mehti.namazov@aztu.edu.az', '/media/prod/departments/communication/mehti_namazov.JPG', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Daxili koordinasiya qrupunun meneceri', NOW()),
    (w_id, 'en', 'Internal Coordination Group Manager', NOW());

    -- 2. Sona Hüseynli
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, profile_image, created_at)
    VALUES (dept_code, 'Sona', 'Hüseynli', 'Etibar qızı', 'sona.huseynli@aztu.edu.az', '/media/prod/departments/communication/sona_huseynli.JPG', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Tədbirlərin idarə edilməsi qrupunun tədbir təşkili mütəxəssisi', NOW()),
    (w_id, 'en', 'Event Organizing Specialist, Event Management Group', NOW());

    -- 3. Nazan Babayeva (no image provided)
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, created_at)
    VALUES (dept_code, 'Nazan', 'Babayeva', 'Pavel qızı', 'nazan.babayeva@aztu.edu.az', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Tədbirlərin idarə edilməsi qrupunun tədbir təşkili mütəxəssisi', NOW()),
    (w_id, 'en', 'Event Organizing Specialist, Event Management Group', NOW());

    -- 4. Teymur Mehtiyev
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, profile_image, created_at)
    VALUES (dept_code, 'Teymur', 'Mehtiyev', 'Mehtiquli oğlu', 'teymur.mehtiyev@aztu.edu.az', '/media/prod/departments/communication/teymur_mehtiyev.JPG', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Tədbirlərin idarə edilməsi qrupunun tədbir təşkili mütəxəssisi', NOW()),
    (w_id, 'en', 'Event Organizing Specialist, Event Management Group', NOW());

    -- 5. Mahmudov İbrahimxəlil
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, profile_image, created_at)
    VALUES (dept_code, 'İbrahimxəlil', 'Mahmudov', 'İrşad oğlu', 'ibrahim.mahmudov@aztu.edu.az', '/media/prod/departments/communication/ibrahimxalil_mahmudov.JPG', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Videoqraf', NOW()),
    (w_id, 'en', 'Videographer', NOW());

    -- 6. Nəbiyeva Əsmər
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, profile_image, created_at)
    VALUES (dept_code, 'Əsmər', 'Nəbiyeva', 'Namiq qızı', 'esmer.nebiyeva@aztu.edu.az', '/media/prod/departments/communication/esmer_nabiyeva.JPG', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Tədbirlərin idarə edilməsi qrupunun tədbirlərin təşkili və idarəedilməsi meneceri', NOW()),
    (w_id, 'en', 'Event Planning and Management Manager, Event Management Group', NOW());

END $$;
