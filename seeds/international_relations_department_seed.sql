-- International Relations Department (Beynəlxalq Əlaqələr Şöbəsi) Seed Data
-- Image base path: /media/prod/departments/bex/
DO $$
DECLARE
    dept_code VARCHAR(50) := 'international_relations_department';
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
    (dept_code, 'az', 'Beynəlxalq Əlaqələr Şöbəsi',
    '<p>Beynəlxalq Əlaqələr Şöbəsi universitetin xarici ölkələrin ali təhsil müəssisələri, elmi təşkilatları və beynəlxalq qurumları ilə əməkdaşlıq əlaqələrinin qurulmasını və inkişaf etdirilməsini təmin edən struktur bölməsidir. Şöbə universitetin beynəlmiləlləşmə siyasətinin həyata keçirilməsində mühüm rol oynayır və beynəlxalq səviyyədə tərəfdaşlıq əlaqələrinin genişləndirilməsi, birgə layihələrin təşkili və akademik mübadilə proqramlarının koordinasiyası ilə məşğul olur.</p><p>Eyni zamanda xarici tələbələrin universitetə cəlb olunması və onların təhsil prosesinə inteqrasiyası istiqamətində də fəaliyyət göstərir. AzTU-nun Beynəlmiləlləşmə Siyasətinə uyğun olaraq Şöbə 23-dən çox ölkənin 140-dan çox universiteti və beynəlxalq qurumu ilə əməkdaşlıq edir, tələbə və müəllim mübadiləsini, birgə tədqiqatları və qlobal akademik şəbəkələrə intiqrasiyanı əsas prioritet istiqamətlər olaraq həyata keçirir.</p><p>Şöbə öz fəaliyyəti ilə AzTU-nun beynəlxalq təhsil və elmi məkanda mövqeyini gücləndirməsinə dəstək verir, Azərbaycanın ali təhsil sisteminin inkişafına və ölkənin elmi-sosial-iqtisadi tərəqqisinə töhfə verir.</p>', NOW()),
    (dept_code, 'en', 'International Relations Department',
    '<p>The International Relations Department of Azerbaijan Technical University (AzTU) is the structural unit responsible for establishing and developing cooperation with foreign higher education institutions, scientific organizations, and international bodies. The department plays a vital role in implementing the university''s internationalization policy and is engaged in expanding partnership relations at the international level, organizing joint projects, and coordinating academic exchange programs.</p><p>The department actively works to attract foreign students to the university and supports their integration into the educational process. In line with AzTU''s Internationalization Policy, the department coordinates cooperation with over 117 universities and organizations from more than 23 countries, promoting student and faculty mobility, joint research, international accreditation, and integration into the global academic network.</p><p>Through its activities, the International Relations Department supports AzTU''s mission to strengthen its presence in the global education and science arena, while contributing to the development of Azerbaijan''s higher education system and the country''s broader scientific and socio-economic progress.</p>', NOW())
    ON CONFLICT (department_code, lang_code) DO NOTHING;

    -- 3. Məqsədlər (Objectives)
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Beynəlxalq əlaqələrin genişləndirilməsi: Xarici universitetlər, tədqiqat mərkəzləri və beynəlxalq qurumlarla əməkdaşlıq imkanlarını artırmaq.', NOW()),
    (obj_id, 'en', 'Expand International Relations: Strengthen cooperation with foreign universities, research centers, and international organizations to broaden partnership opportunities.', NOW());

    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Beynəlxalq proqramlarda iştirak: Universitetin beynəlxalq proqram və layihələrə daha fəal cəlb olunmasını təmin etmək.', NOW()),
    (obj_id, 'en', 'Enhance International Participation: Ensure the university''s active involvement in international programs, projects, and initiatives aligned with global academic standards.', NOW());

    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Akademik mobilliyin inkişafı: Tələbə və müəllimlərin beynəlxalq akademik mübadilə, təcrübə və treninq proqramlarında iştirak imkanlarını genişləndirmək.', NOW()),
    (obj_id, 'en', 'Develop Academic Mobility: Facilitate student and faculty participation in international academic exchange programs, internships, and training opportunities.', NOW());

    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Qlobal inteqrasiyanın gücləndirilməsi: AzTU-nun beynəlxalq təhsil və elmi məkanına inteqrasiyasını təmin etmək, universitetin qlobal tanınmasına töhfə vermək.', NOW()),
    (obj_id, 'en', 'Strengthen Global Integration: Reinforce AzTU''s integration into the international education and science arena, contributing to the university''s global standing and recognition.', NOW());

    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Xarici tələbələrin cəlb olunması: Əcnəbi tələbələrin universitetə qəbulunu dəstəkləmək və onların təhsil mühitinə uğurlu inteqrasiyasını təmin etmək.', NOW()),
    (obj_id, 'en', 'Attract International Students: Support the recruitment of foreign students and ensure their successful adaptation and integration into the university''s educational environment.', NOW());

    -- 4. Əsas Funksiyalar (Core Functions)
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Tərəfdaşlıqların inkişafı: Xarici universitetlər və beynəlxalq təşkilatlarla əməkdaşlıq əlaqələrinin qurulması və inkişaf etdirilməsi.', NOW()),
    (func_id, 'en', 'Partnership Development: Establishing and advancing cooperation with foreign universities and international organizations.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Müqavilə koordinasiyası: Beynəlxalq müqavilə və memorandumların hazırlanması və icrasının koordinasiyası.', NOW()),
    (func_id, 'en', 'Agreement Coordination: Preparing and coordinating the implementation of international agreements and memoranda of understanding.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Akademik mobillik: Tələbə və müəllimlərin mübadilə proqramları və təcrübə proqramları daxil olmaqla akademik mobilliyinin təşkili.', NOW()),
    (func_id, 'en', 'Academic Mobility: Organizing student and faculty academic mobility, including exchange programs and internship opportunities.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Qrant və layihə idarəetməsi: Beynəlxalq qrant və layihələrin hazırlanması və həyata keçirilməsinin koordinasiyası.', NOW()),
    (func_id, 'en', 'Grant and Project Management: Coordinating the preparation and implementation of international grants and joint research projects.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Xarici tələbələrə dəstək: Xarici tələbələrin universitetə cəlb olunması və onların təhsil prosesinə uyğunlaşmasına dəstək göstərilməsi.', NOW()),
    (func_id, 'en', 'International Student Support: Attracting foreign students to the university and providing support for their academic adaptation and integration.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 6, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Tədbirlərin təşkili: Beynəlxalq konfranslar, seminarlar və digər akademik tədbirlərin təşkili və koordinasiyası.', NOW()),
    (func_id, 'en', 'Event Organization: Organizing and coordinating international meetings, seminars, and other academic events.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 7, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Protokol idarəetməsi: Universitet rəhbərliyinin beynəlxalq səfərlərinin və xarici nümayəndə heyətlərinin qəbulunun təşkil edilməsi.', NOW()),
    (func_id, 'en', 'Protocol and Delegation Management: Arranging university leadership''s international visits and organizing the reception of foreign delegations.', NOW());

    -- 5. Şöbə Müdiri (Director) - Orxan Vətənxah
    INSERT INTO department_directors (department_code, first_name, last_name, father_name, room_number, profile_image, created_at)
    VALUES (dept_code, 'Orxan', 'Vətənxah', 'Mirzağa oğlu', 'I korpus, 325', '/media/prod/departments/bex/orxan_vatankhah.jpg', NOW())
    RETURNING id INTO dir_id;

    INSERT INTO department_director_tr (director_id, lang_code, scientific_degree, bio, created_at)
    VALUES
    (dir_id, 'az', 'PhD namizədi',
    'Orxan Vətənxah Azərbaycan Texniki Universitetinin Beynəlxalq Əlaqələr Şöbəsinin müdiri və Sənaye mühəndisliyi və Davamlı iqtisadiyyat kafedrasında müəllimdir. O, 2015-ci ildə Xəzər Universitetində Biznesin idarə edilməsi üzrə magistr dərəcəsi almış və Ghent University-də (Belçika) Erasmus mübadilə proqramında iştirak etmişdir. Avropa və Asiya üzrə akademik mobillik, peşəkar təlim proqramları və qlobal təşəbbüslərdə iştirakı vasitəsilə geniş beynəlxalq təcrübə qazanmış, ali təhsildə beynəlmiləlləşmə və sərhədlərarası əməkdaşlıq sahəsində ixtisaslaşmasını gücləndirib. Hazırda o, Azərbaycan Texniki Universitetində İnnovasiya iqtisadiyyatı ixtisası üzrə fəlsəfə doktoru (PhD) namizədidir. Tədqiqatı ali təhsil müəssisələrində tədqiqat, innovasiya və sahibkarlıq ekosistemlərinin roluna yönəlmişdir. Doktorantura tədqiqatı çərçivəsində 2024–2025-ci illərdə City University of New York (CUNY)-də Fulbright proqramı üzrə dəvətli tədqiqatçı kimi fəaliyyət göstərmişdir.', NOW()),
    (dir_id, 'en', 'PhD Candidate',
    'Orkhan Vatankhah is the Head of the International Relations Office and a Lecturer in the Department of Industrial Engineering and Sustainable Economy at Azerbaijan Technical University. He holds a Master''s degree in Business Administration from Khazar University (2015) and participated in the Erasmus mobility program at Ghent University in Belgium. He has developed extensive international experience through academic mobility, professional training programs, and engagement in global initiatives across Europe and Asia, strengthening his expertise in internationalization and cross-border collaboration in higher education. He is currently a PhD candidate in the field of Economics of Innovation at Azerbaijan Technical University, where his research focuses on the role of research, innovation, and entrepreneurial ecosystems in higher education institutions. As part of his doctoral research, he served as a Fulbright Visiting Researcher at the City University of New York (CUNY) during 2024–2025, examining the economic impact of university-driven research and innovation.', NOW());

    -- Director Working Hours
    INSERT INTO department_director_working_hours (director_id, time_range, created_at) VALUES (dir_id, '09:00–17:30', NOW()) RETURNING id INTO wh_id;
    INSERT INTO department_director_working_hour_tr (working_hour_id, lang_code, day, created_at) VALUES
    (wh_id, 'az', 'Bazar ertəsi–Cümə', NOW()),
    (wh_id, 'en', 'Monday–Friday', NOW());

    -- Director Education
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '2007', '2012', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES
    (edu_id, 'az', 'Bakalavr', 'Azərbaycan Texniki Universiteti', NOW()),
    (edu_id, 'en', 'Bachelor''s degree', 'Azerbaijan Technical University', NOW());

    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '2012', '2015', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES
    (edu_id, 'az', 'Magistratura, Biznesin idarə edilməsi', 'Xəzər Universiteti', NOW()),
    (edu_id, 'en', 'Master''s degree, Business Administration', 'Khazar University', NOW());

    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '2021', '2025', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES
    (edu_id, 'az', 'İqtisadiyyat üzrə fəlsəfə doktoru (PhD)', 'Azərbaycan Texniki Universiteti', NOW()),
    (edu_id, 'en', 'Doctor of Philosophy (PhD) in Economics', 'Azerbaijan Technical University', NOW());

    -- Director also as worker contact
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, profile_image, created_at)
    VALUES (dept_code, 'Orxan', 'Vətənxah', 'Mirzağa oğlu', 'orxan.vatan@aztu.edu.az', '(012) 539 13 28 / 1240 (I korpus, 325)', '/media/prod/departments/bex/orxan_vatankhah.jpg', NOW())
    ON CONFLICT DO NOTHING;

    -- 6. Əməkdaşlar (Personnel)
    -- 1. Elşən Qurbanov (no image)
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Elşən', 'Qurbanov', 'Mahmud oğlu', 'eli.gourban@aztu.edu.az', '(012) 525 24 06', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_degree, created_at) VALUES
    (w_id, 'az', 'Beynəlxalq layihələrin idarə olunması sektoruna əlavə iş yeri üzrə 0,5 ştat müdiri', 'PhD', NOW()),
    (w_id, 'en', 'Head of International Project Division', 'PhD', NOW());

    -- 2. Mənzər Məmmədli
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, profile_image, created_at)
    VALUES (dept_code, 'Mənzər', 'Məmmədli', 'Yunus qızı', 'manzar.mammadli@aztu.edu.az', '(012) 539 13 48 / 1243', '/media/prod/departments/bex/manzar_mammadli.jpg', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Beynəlxalq əməkdaşlıq və mübadilə sektorunun müdiri', NOW()),
    (w_id, 'en', 'Head of International Cooperation and Exchange Division', NOW());

    -- 3. Sevinc Absalamlı
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, profile_image, created_at)
    VALUES (dept_code, 'Sevinc', 'Absalamlı', 'Rahib qızı', 'sevinj.absalamli@aztu.edu.az', '(012) 538 94 14 / 1241', '/media/prod/departments/bex/sevinc_absalamli.jpg', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Əcnəbi tələbələrin qəbulu sektorunun müdiri', NOW()),
    (w_id, 'en', 'Head of International Students Admissions Division', NOW());

    -- 4. Müşviq Mehbalıyev
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, profile_image, created_at)
    VALUES (dept_code, 'Müşviq', 'Mehbalıyev', 'Tərməmməd oğlu', 'mushvig.mehbaliyev@aztu.edu.az', '(012) 538 94 14 / 1245', '/media/prod/departments/bex/mushviq_mehbaliyev.jpg', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Əcnəbi tələbələrin qəbulu üzrə baş mütəxəssis', NOW()),
    (w_id, 'en', 'Senior Specialist for Admission of Foreign Students', NOW());

    -- 5. Cavanşir Həsənov
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, profile_image, created_at)
    VALUES (dept_code, 'Cavanşir', 'Həsənov', 'Məhəmmədhəsən oğlu', 'hasanov.cavanshir@aztu.edu.az', '(012) 538 94 14', '/media/prod/departments/bex/hasanov_cavanshir.jpg', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Əcnəbi tələbələrin qeydiyyatı və miqrasiya məsələləri üzrə mütəxəssis', NOW()),
    (w_id, 'en', 'Specialist in Foreign Student Registration and Migration Issues', NOW());

    -- 6. Aysel Bədəlova (no image)
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Aysel', 'Bədəlova', 'İlqar qızı', 'aysel.badalova@aztu.edu.az', '(012) 539 13 48 / 1244', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Beynəlxalq əməkdaşlıq və mübadilə üzrə baş mütəxəssis', NOW()),
    (w_id, 'en', 'Senior Specialist for International Cooperation and Exchange', NOW());

    -- 7. Nabat Cabbarova (no image)
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Nabat', 'Cabbarova', 'Eldar qızı', 'nabat.cabbarova@aztu.edu.az', '(012) 525 24 06 / 1242', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Beynəlxalq layihələr üzrə baş mütəxəssis', NOW()),
    (w_id, 'en', 'Senior Specialist for International Projects', NOW());

END $$;
