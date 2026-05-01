-- Research and Development Department (Tədqiqat və inkişaf departamenti) Seed Data
DO $$
DECLARE
    dept_code VARCHAR(50) := 'research_dev_department';
    dir_id INT;
    edu_id INT;
    w_id INT;
    obj_id INT;
    func_id INT;
BEGIN
    -- 1. Departament
    INSERT INTO departments (department_code, created_at)
    VALUES (dept_code, NOW())
    ON CONFLICT (department_code) DO NOTHING;

    -- 2. Departament Tərcümələri (Haqqında)
    INSERT INTO departments_tr (department_code, lang_code, department_name, about_html, created_at)
    VALUES 
    (dept_code, 'az', 'Tədqiqat, İnkişaf və Reputasiya Departamenti', 
    '<p>Azərbaycan Texniki Universitetinin (AzTU) Tədqiqat, İnkişaf və Reputasiya Departamenti universitetin elmi, akademik və institusional inkişafında aparıcı rol oynayır. Departament tədqiqat fəaliyyətlərinin dəstəklənməsi, innovasiyanın təşviqi və universitetin milli və beynəlxalq səviyyədə akademik nüfuzunun gücləndirilməsi üçün mərkəzi platforma kimi çıxış edir.</p><p>Departament müəllim heyətinə, tədqiqatçılara və tələbələrə tədqiqat prosesinin bütün mərhələlərində ideyanın formalaşdırılmasından layihənin planlaşdırılması, icrası və uğurla tamamlanmasına qədər dəstək göstərir. Eyni zamanda, qrant müraciətlərinin hazırlanması, tədqiqat imkanlarına çıxış və akademik-sənaye əməkdaşlıqlarının qurulmasına yardım edir.</p><p>İnterdisiplinar əməkdaşlığı və tədqiqat nəticələrinin praktik tətbiqini təşviq etməklə departament innovasiya, texnologiya transferi və davamlı inkişafın gücləndirilməsinə töhfə verir. Bununla yanaşı, strateji təşəbbüslər, akademik şəbəkələşmə və milli və beynəlxalq qurumlarla əməkdaşlıq vasitəsilə AzTU-nun tanınması, təsiri və reputasiyasının artırılması istiqamətində fəaliyyət göstərir.</p>', NOW()),
    (dept_code, 'en', 'Research, Development and Reputation Department', 
    '<p>The Research, Development and Reputation Department at Azerbaijan Technical University (AzTU) plays a leading role in advancing the university’s scientific, academic, and institutional excellence. The department serves as a central platform for supporting research initiatives, encouraging innovation, and strengthening the university’s academic reputation at both national and international levels.</p><p>The department provides guidance and support to faculty members, researchers, and students throughout all stages of the research process, from idea development and project planning to implementation and successful completion. It also assists in grant proposal preparation, access to research opportunities, and the development of collaborative academic and industrial partnerships.</p><p>By promoting interdisciplinary cooperation and practical application of research outcomes, the department contributes to the growth of innovation, technology transfer, and sustainable development. At the same time, it works to enhance the visibility, impact, and reputation of AzTU through strategic initiatives, academic networking, and engagement with national and international institutions.</p>', NOW())
    ON CONFLICT (department_code, lang_code) DO UPDATE 
    SET department_name = EXCLUDED.department_name, about_html = EXCLUDED.about_html, updated_at = NOW();

    -- 3. Məqsədlər (Objectives)
    -- Objective 1
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Elmi mühitin təşviqi: Müəllim və tələbələrin tədqiqat, innovasiya və bilik yaradılmasında aktiv iştirakını təşviq etmək.', NOW()),
    (obj_id, 'en', 'Promote a Research Culture: Encourage faculty members and students to actively engage in research, innovation, and knowledge creation.', NOW());
    -- Objective 2
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Layihələrin inkişafına dəstək: Tədqiqatçılara maliyyə imkanlarının müəyyənləşdirilməsi, rəqabətqabiliyyətli qrant müraciətlərinin hazırlanması və layihələrin effektiv idarə olunmasında kömək etmək.', NOW()),
    (obj_id, 'en', 'Support Project Development: Assist researchers in identifying funding opportunities, preparing competitive grant proposals, and effectively managing research projects.', NOW());
    -- Objective 3
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Akademik görünürlüğün artırılması: Beynəlxalq nüfuzlu jurnallarda nəşrləri və milli və beynəlxalq konfranslarda iştirakı dəstəkləmək.', NOW()),
    (obj_id, 'en', 'Enhance Academic Visibility: Support publication in reputable international journals and participation in national and international conferences.', NOW());
    -- Objective 4
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Universitetin reputasiyasının gücləndirilməsi: Yüksək keyfiyyətli elmi nəticələrin təşviqi, beynəlxalq əməkdaşlıqların genişləndirilməsi və reytinqlərdə irəliləyiş vasitəsilə AzTU-nun milli və beynəlxalq nüfuzunu artırmaq.', NOW()),
    (obj_id, 'en', 'Strengthen Institutional Reputation: Enhance the national and international standing of AzTU by promoting high-quality research outputs, increasing academic visibility, supporting global collaborations, and contributing to university rankings and recognition.', NOW());
    -- Objective 5
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'İnterdisiplinar əməkdaşlığın təşviqi: Müxtəlif sahələri birləşdirən və mürəkkəb elmi-texnoloji problemləri həll etməyə yönəlmiş layihələri dəstəkləmək.', NOW()),
    (obj_id, 'en', 'Foster Interdisciplinary Collaboration: Promote research initiatives that integrate multiple disciplines to address complex scientific and technological challenges.', NOW());
    -- Objective 6
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 6, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'Peşəkar inkişaf fəaliyyətlərinin təşkili: Tədqiqat bacarıqlarını və akademik kompetensiyaları gücləndirmək üçün təlimlər, seminarlar və workshoplar təşkil etmək.', NOW()),
    (obj_id, 'en', 'Organize Professional Development Activities: Conduct workshops, seminars, and training programs to strengthen research skills and academic competencies.', NOW());

    -- 4. Əsas Funksiyalar (Core Functions)
    -- Func 1
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Qrant və layihə dəstəyi: Rəqabətqabiliyyətli tədqiqat layihələrinin hazırlanması və milli və beynəlxalq maliyyə mənbələrinin cəlb olunmasında dəstək göstərmək.', NOW()),
    (func_id, 'en', 'Grant and Proposal Support: Provide guidance in preparing competitive research proposals and securing national and international funding.', NOW());
    -- Func 2
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Tərəfdaşlıqların inkişafı: Yerli və beynəlxalq sənaye, tədqiqat mərkəzləri və universitetlərlə əməkdaşlıqlar qurmaq və inkişaf etdirmək.', NOW()),
    (func_id, 'en', 'Partnership Development: Build and maintain collaborations with industry, research institutions, and universities at both local and global levels.', NOW());
    -- Func 3
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Tədqiqat infrastrukturu və resursların idarə olunması: Laboratoriyalara, müasir avadanlıqlara və akademik resurslara, o cümlədən tezis və nəşrlərə çıxışı təmin etmək.', NOW()),
    (func_id, 'en', 'Research Infrastructure Management: Ensure access to laboratories, advanced equipment, and digital academic resources, including theses and publications.', NOW());
    -- Func 4
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'Etika və uyğunluğa nəzarət: Bütün tədqiqat fəaliyyətlərinin etik, hüquqi və normativ tələblərə uyğun həyata keçirilməsini təmin etmək.', NOW()),
    (func_id, 'en', 'Ethics and Compliance Management: Oversee adherence to ethical standards, legal frameworks, and regulatory requirements in all research activities.', NOW());
    -- Func 5
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'İnnovasiya və texnologiya transferi: Patentlərin əldə olunması, tədqiqat nəticələrinin kommersiyalaşdırılması və tətbiqi innovasiyanın təşviqi.', NOW()),
    (func_id, 'en', 'Innovation and Technology Transfer: Support patent applications, commercialization of research outcomes, and the promotion of applied innovation.', NOW());

    -- 5. Şöbə Müdiri (Director)
    INSERT INTO department_directors (department_code, first_name, last_name, father_name, room_number, created_at)
    VALUES (dept_code, 'Bəxtiyar', 'Bədəlov', '', 'Tel: +994 125252406 (Ext.1150)', NOW())
    ON CONFLICT (department_code) DO UPDATE SET first_name = EXCLUDED.first_name, updated_at = NOW()
    RETURNING id INTO dir_id;

    INSERT INTO department_director_tr (director_id, lang_code, scientific_degree, bio, created_at)
    VALUES 
    (dir_id, 'az', 'Beynəlxalq Münasibətlər üzrə fəlsəfə doktoru (PhD)', 
    'Email: bakhtiyar.badalov@aztu.edu.az | Bəxtiyar Bədəlov ali təhsil, elmi innovasiya və qlobal akademik əməkdaşlıq sahəsində geniş təcrübəyə malik beynəlxalq münasibətlər üzrə mütəxəssisdir. O, Bakı Dövlət Universitetində Beynəlxalq Münasibətlər üzrə fəlsəfə doktoru (PhD) dərəcəsinə, həmçinin İsveçin Lund Universitetində Siyasi Elmlər üzrə magistr dərəcəsinə malikdir və Avropa məsələləri üzrə ixtisaslaşmışdır. Hazırda o, Azərbaycan Texniki Universitetində Tədqiqat və İnkişaf Departamentinin rəhbəri vəzifəsində çalışır. Bu vəzifədə o, universitetin elmi-tədqiqat strategiyasını formalaşdırır, innovasiya ekosistemlərinin inkişafını sürətləndirir və akademiya, sənaye, eləcə də beynəlxalq tərəfdaşlarla səmərəli əməkdaşlıqlar qurur.', NOW()),
    (dir_id, 'en', 'PhD in International Relations', 
    'Email: bakhtiyar.badalov@aztu.edu.az | Bakhtiyar Badalov is an international relations expert with extensive experience in higher education, research innovation, and global academic cooperation. He holds a PhD in International Relations from Baku State University and a Master’s degree in Political Science from Lund University (Sweden), specializing in European Affairs. He currently serves as Head of the Research and Development Department at Azerbaijan Technical University, where he drives institutional research strategy, advances innovation ecosystems, and builds high-impact partnerships between academia, industry, and international stakeholders.', NOW())
    ON CONFLICT (director_id, lang_code) DO UPDATE SET bio = EXCLUDED.bio, updated_at = NOW();

    -- Təhsil (Director)
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '2020', 'Present', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES 
    (edu_id, 'az', 'Beynəlxalq Münasibətlər üzrə fəlsəfə doktoru (PhD)', 'Bakı Dövlət Universiteti', NOW()),
    (edu_id, 'en', 'Doctor of Philosophy (PhD) in International Relations', 'Baku State University', NOW());

    -- 6. Əməkdaşlar (Personnel)
    -- 1. Kəmalə Təhməzova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Kəmalə', 'Təhməzova', 'Tariyel qızı', 'tehmezova.kemale@aztu.edu.az', '+99412-538-94-16', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Tədqiqatların koordinasiyası üzrə mütəxəssis', NOW()), (w_id, 'en', 'Specialist in Research Coordination', NOW());

    -- 2. Natəvan Babayeva
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Natəvan', 'Babayeva', 'Xəzair qızı', 'natavan.babayeva@aztu.edu.az', '+99412-538-94-16', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Reytinq performanslarının qiymətləndirilməsi üzrə mütəxəssis', NOW()), (w_id, 'en', 'Rating performance assessment specialist', NOW());

    -- 3. Fatma Tağıyeva
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Fatma', 'Tağıyeva', 'Rahib qızı', 'fatma.tagiyeva@aztu.edu.az', '+99412-538-94-16', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Akademik inkişaf üzrə mütəxəssis', NOW()), (w_id, 'en', 'Academic Development Specialist', NOW());

    -- 4. Nərgiz İsmayılova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Nərgiz', 'İsmayılova', 'Zülfüqar qızı', 'nargiz.ismayilova@aztu.edu.az', '+99412-538-94-16', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Beynəlxalq tədqiqat əməkdaşlıqı üzrə koordinator', NOW()), (w_id, 'en', 'International Research Collaboration Coordinator', NOW());

END $$;
