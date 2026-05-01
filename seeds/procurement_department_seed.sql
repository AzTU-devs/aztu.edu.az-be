-- Procurement Department (Satınalma təchizat şöbəsi) Seed Data
DO $$
DECLARE
    dept_code VARCHAR(50) := 'procurement_department';
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
    (dept_code, 'az', 'Satınalma təchizat şöbəsi', 
    '<p>Azərbaycan Texniki Universitetinin (AzTU) Satınalma təchizat şöbəsi universitetin inzibati və əməliyyat fəaliyyətlərinin fasiləsiz və səmərəli təmin olunmasında mühüm rol oynayır. Departament universitetin ehtiyac duyduğu mal, xidmət və avadanlıqların şəffaf, effektiv və qanunvericiliyə uyğun şəkildə satın alınmasını təşkil edən mərkəzi struktur vahid kimi çıxış edir.</p><p>Şöbə bütün struktur bölmələrlə sıx əməkdaşlıq edərək ehtiyacların düzgün müəyyənləşdirilməsi, satınalma prosesinin planlaşdırılması, tender və təkliflərin qiymətləndirilməsi, müqavilələrin bağlanması və icrasına nəzarət mərhələlərində kompleks dəstək göstərir.</p><p>Eyni zamanda, yerli və beynəlxalq təchizatçılarla əməkdaşlıqlar qurur, rəqabətli mühit yaradır və maliyyə resurslarından səmərəli istifadəni təmin edir. Satınalma proseslərində şəffaflıq, hesabatlılıq və operativlik prinsiplərinə əsaslanaraq universitetin davamlı inkişafına töhfə verir.</p><p>Şöbə öz fəaliyyəti ilə AzTU-nun maddi-texniki bazasının gücləndirilməsinə, tədris və tədqiqat fəaliyyətlərinin yüksək səviyyədə təşkilinə və ümumi institusional effektivliyin artırılmasına xidmət edir.</p>', NOW()),
    (dept_code, 'en', 'Procurement Department', 
    '<p>The Procurement Department of Azerbaijan Technical University (AzTU) plays a key role in ensuring the continuous and efficient operation of the university’s administrative and operational activities. The department serves as a central structural unit responsible for organizing the procurement of goods, services, and equipment required by the university in a transparent, efficient, and legally compliant manner.</p><p>The department works in close collaboration with all structural units to accurately identify needs and provides comprehensive support throughout all stages of the procurement process, including planning, tendering, bid evaluation, contract conclusion, and contract execution monitoring.</p><p>At the same time, it establishes partnerships with local and international suppliers, fosters a competitive environment, and ensures the efficient use of financial resources. By adhering to the principles of transparency, accountability, and efficiency, the department contributes to the sustainable development of the university.</p><p>Through its activities, the department supports strengthening AzTU’s material and technical base, enhancing the quality of teaching and research activities, and improving overall institutional effectiveness.</p>', NOW())
    ON CONFLICT (department_code, lang_code) DO NOTHING;

    -- 3. Məqsədlər (Objectives)
    -- Objective 1
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Şəffaf satınalma mühitinin təmin edilməsi: Bütün satınalma proseslərinin açıq, ədalətli və qanunvericiliyə uyğun həyata keçirilməsini təmin etmək.', NOW()),
    (obj_id, 'en', 'Ensuring a transparent procurement environment: To guarantee that all procurement processes are conducted openly, fairly, and in compliance with legislation.', NOW());
    -- Objective 2
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Ehtiyacların effektiv planlaşdırılması: Struktur bölmələrin tələblərini düzgün analiz edərək optimal satınalma planlarının hazırlanmasını təmin etmək.', NOW()),
    (obj_id, 'en', 'Effective needs planning: To analyze the requirements of structural units and ensure the preparation of optimal procurement plans.', NOW());
    -- Objective 3
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Maliyyə resurslarından səmərəli istifadə: Keyfiyyət və qiymət balansını qorumaqla xərclərin optimallaşdırılmasına nail olmaq.', NOW()),
    (obj_id, 'en', 'Efficient use of financial resources: To optimize costs while maintaining a balance between quality and price.', NOW());
    -- Objective 4
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Təchizatçı bazasının genişləndirilməsi: Etibarlı yerli və beynəlxalq təchizatçılarla əməkdaşlığı inkişaf etdirmək.', NOW()),
    (obj_id, 'en', 'Expansion of the supplier base: To develop cooperation with reliable local and international suppliers.', NOW());
    -- Objective 5
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Proseslərin optimallaşdırılması: Satınalma prosedurlarını təkmilləşdirmək və rəqəmsallaşdırma vasitəsilə operativliyi artırmaq.', NOW()),
    (obj_id, 'en', 'Process optimization: To improve procurement procedures and increase efficiency through digitalization.', NOW());
    -- Objective 6
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 6, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Peşəkar inkişafın təşviqi: Satınalma sahəsində çalışan əməkdaşların bilik və bacarıqlarını artırmaq üçün təlimlər təşkil etmək.', NOW()),
    (obj_id, 'en', 'Promotion of professional development: To organize training programs aimed at enhancing the knowledge and skills of procurement staff.', NOW());

    -- 4. Əsas Funksiyalar (Core Functions)
    -- Function 1
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Satınalma planlaşdırılması: Universitetin illik və cari ehtiyaclarına uyğun satınalma planlarının hazırlanması.', NOW()),
    (func_id, 'en', 'Procurement planning: Preparation of annual and current procurement plans in line with university needs.', NOW());
    -- Function 2
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Tender və təkliflərin idarə olunması: Tenderlərin təşkili, təkliflərin toplanması və obyektiv meyarlar əsasında qiymətləndirilməsi.', NOW()),
    (func_id, 'en', 'Tender and bid management: Organization of tenders, collection of bids, and evaluation based on objective criteria.', NOW());
    -- Function 3
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Müqavilələrin hazırlanması və idarə olunması: Təchizatçılarla müqavilələrin hazırlanması, bağlanması və icrasına nəzarət.', NOW()),
    (func_id, 'en', 'Contract preparation and management: Drafting, concluding, and monitoring contracts with suppliers.', NOW());
    -- Function 4
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Bazar araşdırması: Qiymət təhlili və bazar araşdırmaları apararaq ən uyğun təkliflərin müəyyən edilməsi.', NOW()),
    (func_id, 'en', 'Market research: Conducting price analysis and market research to identify the most suitable offers.', NOW());
    -- Function 5
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Təchizatçı münasibətlərinin idarə olunması: Mövcud və potensial təchizatçılarla uzunmüddətli əməkdaşlıqların qurulması və inkişaf etdirilməsi.', NOW()),
    (func_id, 'en', 'Supplier relationship management: Establishing and developing long-term cooperation with existing and potential suppliers.', NOW());
    -- Function 6
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 6, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Uyğunluq və nəzarət: Satınalma fəaliyyətlərinin hüquqi və normativ tələblərə uyğunluğunun təmin edilməsi.', NOW()),
    (func_id, 'en', 'Compliance and control: Ensuring that procurement activities comply with legal and regulatory requirements.', NOW());
    -- Function 7
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 7, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Logistika və təhvil-təslim nəzarəti: Alınan məhsul və xidmətlərin vaxtında və düzgün şəkildə təhvil alınmasına nəzarət.', NOW()),
    (func_id, 'en', 'Logistics and delivery control: Monitoring the timely and accurate delivery of procured goods and services.', NOW());

    -- 5. Şöbə Müdiri (Director)
    INSERT INTO department_directors (department_code, first_name, last_name, father_name, room_number, created_at)
    VALUES (dept_code, 'Vüsal', 'Hüseynov', 'Qədir', '2-ci korpus, 304-cü otaq', NOW())
    RETURNING id INTO dir_id;

    INSERT INTO department_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, created_at)
    VALUES 
    (dir_id, 'az', NULL, NULL, 
    'Vüsal Hüseynov Qədir oğlu — 2015-2021-ci illərdə İqtisadiyyat Nazirliyinin İqtisadi İslahatlar Elmi Tədqiqat İnstitutunda Baş mütəxəssis vəzifəsində çalışmışdır. 2021-ci ilin noyabr ayından AzTU-da müxtəlif vəzifələrdə, o cümlədən Maliyyə və İqtisadiyyat şöbəsində Baş mütəxəssis, Təsərrüfat hissəsinin müdiri və Maddi qiymətlilərin idarə edilməsi şöbəsinin müdiri kimi fəaliyyət göstərmişdir. 2021-ci ilin fevral ayından İqtisadiyyat və statistika kafedrasının müəllimidir. 2025-ci ilin avqust ayından Satınalma təchizat şöbəsinin müdiri vəzifəsində çalışır.', NOW()),
    (dir_id, 'en', NULL, NULL, 
    'Vusal Huseynov Gadir — Served as a Chief Specialist at the Economic Reforms Research Institute of the Ministry of Economy from 2015 to 2021. Since November 2021, he has held various positions at AzTU, including Chief Specialist in the Finance and Economics Department, Head of Administrative Services, and Head of the Asset Management Department. He has been a lecturer at the Department of Economics and Statistics since February 2021. Since August 2025, he has been serving as the Head of the Procurement Department.', NOW());

    -- Təhsil
    -- Bakalavr
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '2011', '2015', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES 
    (edu_id, 'az', 'Bakalavr, Menecment (Alman Proqramı)', 'Azərbaycan Dövlət Aqrar Universiteti', NOW()),
    (edu_id, 'en', 'Bachelor, Management (German Program)', 'Azerbaijan State Agrarian University', NOW());
    -- Magistr
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '2017', '2019', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES 
    (edu_id, 'az', 'Magistr, Beynəlxalq İqtisadi Münasibətlər (MBA)', 'Odlar Yurdu Universiteti', NOW()),
    (edu_id, 'en', 'Master, International Economic Relations (MBA)', 'Odlar Yurdu University', NOW());
    -- Doktorantura
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '2024', NULL, NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES 
    (edu_id, 'az', 'Doktorantura, Finansal Ekonomi', 'Doğuş Universiteti (Türkiyə)', NOW()),
    (edu_id, 'en', 'PhD Candidate, Financial Economics', 'Dogus University (Turkey)', NOW());

    -- 6. Əməkdaşlar (Personnel)
    -- 1. Günay Paşayeva
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Günay', 'Paşayeva', 'Tofiq qızı', 'gunay.pashayeva@aztu.edu.az', '+994 55 591 24 18 (Otaq: 206)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', NOW()), (w_id, 'en', 'Specialist', NOW());

    -- 2. Aypara Qurbanova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Aypara', 'Qurbanova', 'Həmzəli qızı', 'aypara.qurbanova@aztu.edu.az', '+994 55 252 41 13 (Otaq: 206)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Mütəxəssis', NOW()), (w_id, 'en', 'Specialist', NOW());

END $$;
