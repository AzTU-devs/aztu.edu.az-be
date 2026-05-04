-- Press Service (Mətbuat xidməti) Seed Data
DO $$
DECLARE
    dept_code VARCHAR(50) := 'press_service';
    obj_id INT;
    func_id INT;
    dir_id INT;
    w_id INT;
BEGIN
    -- 1. Departament
    INSERT INTO departments (department_code, created_at)
    VALUES (dept_code, NOW())
    ON CONFLICT (department_code) DO NOTHING;

    -- 2. Departament Tərcümələri (Haqqında)
    INSERT INTO departments_tr (department_code, lang_code, department_name, about_html, created_at)
    VALUES
    (dept_code, 'az', 'Mətbuat xidməti',
    '<p>Mətbuat xidməti AzTU-nun fəaliyyəti barədə məlumatların ictimaiyyətə operativ və düzgün şəkildə çatdırılmasını təmin edir. Xidmət kütləvi informasiya vasitələri ilə əlaqələrin təşkilini və koordinasiyasını həyata keçirir.</p><p>Mətbuat xidməti həmçinin qurumun imicinin formalaşdırılması və qorunması istiqamətində mühüm rol oynayır. Bu məqsədlə ictimai rəyin öyrənilməsi, media monitorinqi və kommunikasiya strategiyalarının hazırlanması həyata keçirilir.</p><p><strong>Əlaqə:</strong> metbuat@aztu.edu.az</p>', NOW()),
    (dept_code, 'en', 'Press Service',
    '<p>The Press Service of AzTU ensures the timely and accurate dissemination of information about the university''s activities to the public. It organizes and coordinates relations with mass media.</p><p>The Press Service also plays an important role in shaping and protecting the institution''s image. To this end, it carries out public opinion research, media monitoring, and the development of communication strategies.</p><p><strong>Contact:</strong> metbuat@aztu.edu.az</p>', NOW())
    ON CONFLICT (department_code, lang_code) DO NOTHING;

    -- 3. Məqsəd (Objective)
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES
    (obj_id, 'az', 'Qurumun fəaliyyəti barədə məlumatların ictimaiyyətə operativ, dəqiq və şəffaf şəkildə çatdırılmasını təmin etmək, kütləvi informasiya vasitələri ilə səmərəli əməkdaşlıq qurmaq və ictimaiyyətlə əlaqələri gücləndirmək.', NOW()),
    (obj_id, 'en', 'To ensure the timely, accurate, and transparent communication of institutional information, strengthen cooperation with mass media, and enhance public relations.', NOW());

    -- 4. Əsas funksiyaları (Core Functions)
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Kütləvi informasiya vasitələri ilə əlaqələrin təşkili və koordinasiyası.', NOW()),
    (func_id, 'en', 'Coordination of relations with mass media.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Qurumun fəaliyyəti ilə bağlı rəsmi məlumatların və press-relizlərin hazırlanması və yayılması.', NOW()),
    (func_id, 'en', 'Preparation and dissemination of official statements and press releases.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Media sorğularının cavablandırılması.', NOW()),
    (func_id, 'en', 'Handling media inquiries.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Mətbuat konfranslarının, brifinqlərin təşkili.', NOW()),
    (func_id, 'en', 'Organization of press conferences and briefings.', NOW());

    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES
    (func_id, 'az', 'Qurumun fəaliyyətinə dair media monitorinqinin aparılması və təhlili.', NOW()),
    (func_id, 'en', 'Media monitoring and analysis.', NOW());

    -- 5. Mətbuat katibi (Press Secretary - stored as Director)
    INSERT INTO department_directors (department_code, first_name, last_name, room_number, profile_image, created_at)
    VALUES (dept_code, 'Sevinc', 'İsgəndərova', '1-ci korpus, 204-cü otaq', '/media/prod/departments/press/sevinc_isgenderova.jpg', NOW())
    RETURNING id INTO dir_id;

    INSERT INTO department_director_tr (director_id, lang_code, bio, created_at)
    VALUES
    (dir_id, 'az',
    'İsgəndərova Sevinc Zülfüqar qızı Bakı Dövlət Universitetinin Jurnalistika fakültəsinin jurnalist ixtisasını, Azərbaycan Respublikasının Prezidenti yanında Dövlət İdarəçilik Akademiyasının İnzibati idarəetmə fakültəsinin menecment ixtisasını bitirib. Jurnalistika sahəsində 21 illik təcrübəyə malikdir. O müxtəlif vaxtlarda “Space” televiziyasının xəbərlər departamentində müxbir, “Siqnal” və “Abituriyent” verilişlərinin aparıcısı, Prezident müxbiri, AZƏRTAC-ın Multimedia və video xəbər şöbəsinin redaktoru, müxtəlif xəbər saytlarında layihə rəhbəri vəzifələrində çalışıb. Hazırda AzTU-nun Mətbuat xidmətinin mətbuat katibidir.', NOW()),
    (dir_id, 'en',
    'Isgandarova Sevinc Zulfugar graduated from the Faculty of Journalism at Baku State University, majoring in Journalism, and from the Faculty of Administrative Management at the Academy of Public Administration under the President of the Republic of Azerbaijan, majoring in Management. She has 21 years of experience in the field of journalism. Throughout her career, she has worked as a reporter in the News Department of "Space" TV, presenter of the programs "Signal" and "Abituriyent," presidential correspondent, editor of the Multimedia and Video News Department of AZERTAC, and project manager at various news websites. She is currently working as the Press Secretary of the Press Service of Azerbaijan Technical University (AzTU).', NOW());

    -- Mətbuat katibi əlaqə (also as worker contact)
    INSERT INTO department_workers (department_code, first_name, last_name, email, phone, profile_image, created_at)
    VALUES (dept_code, 'Sevinc', 'İsgəndərova', 'sevinc.isgenderova@aztu.edu.az', '1020 (1-ci korpus, 204-cü otaq)', '/media/prod/departments/press/sevinc_isgenderova.jpg', NOW())
    RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Mətbuat katibi', NOW()),
    (w_id, 'en', 'Press Secretary', NOW());

    -- 6. Əməkdaşlar (Staff)
    -- 1. Ülkər Abdullayeva (no image provided)
    INSERT INTO department_workers (department_code, first_name, last_name, email, created_at)
    VALUES (dept_code, 'Ülkər', 'Abdullayeva', 'ulker.abdullayeva@aztu.edu.az', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Dizayner', NOW()),
    (w_id, 'en', 'Designer', NOW());

    -- 2. Araz Məmmədov
    INSERT INTO department_workers (department_code, first_name, last_name, email, profile_image, created_at)
    VALUES (dept_code, 'Araz', 'Məmmədov', 'araz.mammadov@aztu.edu.az', '/media/prod/departments/press/mammadov_araz.jpg', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES
    (w_id, 'az', 'Fotoqraf', NOW()),
    (w_id, 'en', 'Photographer', NOW());

END $$;
