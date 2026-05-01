-- Education Department (Tədris şöbəsi) Seed Data
DO $$
DECLARE
    dept_code VARCHAR(50) := 'education_department';
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
    (dept_code, 'az', 'Tədris şöbəsi', 
    '<p>Tədris şöbəsi öz fəaliyyətində Azərbaycan Respublikasının Konstitusiyasını, Azərbaycan Respublikasının "Təhsil haqqında", “Elm haqqında” Qanunlarını, digər müvafiq qanunvericilik aktlarını, Azərbaycan Respublikası Prezidentinin fərman və sərəncamlarını, Azərbaycan Respublikası Nazirlər Kabinetinin qərar və sərəncamlarını, “Avropa ali təhsil məkanında keyfiyyət təminatı üzrə standartlar və təlimatları” (ESG), Elm və Təhsil Nazirliyinin Kollegiya Qərarlarını, təlimatlarını, əmr və sərəncamlarını, digər normativ-hüquqi aktlarını, AzTU-nun və Elmi Şurasının qərarlarını, AzTU-nun rektorunun əmr və sərəncamlarını, təhsil, elm və innovasiyalar, inzibat-iqtisadi və sosial fəaliyyət sahələrində mövcud olan müvafiq normativ-hüquqi aktları, AzTU-nun Nizamnaməsini və Tədris şöbəsinin öz Əsasnaməsini rəhbər tutur.</p><p>Tədris şöbəsi öz vəzifələrini yerinə yetirərkən və hüquqlarını həyata keçirərkən AzTU-nun digər struktur bölmələri ilə qarşılıqlı əlaqədə fəaliyyət göstərir.</p>', NOW()),
    (dept_code, 'en', 'Education Department', 
    '<p>In its activities, the Education Department is guided by the Constitution of the Republic of Azerbaijan, the Laws of the Republic of Azerbaijan "On Education" and "On Science," other relevant legislative acts, decrees and orders of the President of the Republic of Azerbaijan, decisions and orders of the Cabinet of Ministers of the Republic of Azerbaijan, the "Standards and Guidelines for Quality Assurance in the European Higher Education Area" (ESG), Board Decisions, instructions, orders, and decrees of the Ministry of Science and Education, and other normative-legal acts. It also follows the decisions of the Scientific Council of TU Azerbaijan, orders and decrees of the Rector of TU Azerbaijan, relevant normative-legal acts existing in the fields of education, science and innovation, administrative-economic and social activities, as well as the Charter of TU Azerbaijan and its own Regulations.</p><p>The Education Department operates in coordination with other structural units of TU Azerbaijan while performing its duties and exercising its rights.</p>', NOW())
    ON CONFLICT (department_code, lang_code) DO NOTHING;

    -- 3. Fəaliyyət istiqamətləri (Objectives)
    -- Istiqamət 1
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'AzTU-da tədris prosesini səmərəli, mövcud standartlara uyğun təşkil edir və ona nəzarətin həyata keçirilməsini təmin edir', NOW()),
    (obj_id, 'en', 'Organizes the educational process at TU Azerbaijan efficiently and in accordance with current standards, ensuring the implementation of monitoring', NOW());
    -- Istiqamət 2
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'tədris prosesinin tədris ili üzrə planlaşdırılmasını təmin edir', NOW()),
    (obj_id, 'en', 'Ensures the planning of the educational process for the academic year', NOW());
    -- Istiqamət 3
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'AzTU-nun təhsil səviyyələrində tədrisın kredit sistemi ilə təşkili qaydalarının tələblərinə uyğunlaşdırılmasını və biliyin obyektiv qiymətləndirilməsini digər struktur bölmələrlə əlaqələndirilmiş formada təşkil və təmin edir', NOW()),
    (obj_id, 'en', 'Organizes and ensures the alignment of education at TU Azerbaijan levels with the requirements of the credit system and the objective assessment of knowledge in coordination with other structural units', NOW());
    -- Istiqamət 4
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'tədris prosesinin Dövlət təhsil standartlarına uyğun şəkildə təşkili və idarə olunmasına nəzarət edir', NOW()),
    (obj_id, 'en', 'Supervises the organization and management of the teaching process in accordance with State Education Standards', NOW());
    -- Istiqamət 5
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'tədris prosesin metodiki təminatının yaxşılaşdırıması ilə bağlı müvafiq tədbirlər görür', NOW()),
    (obj_id, 'en', 'Takes appropriate measures to improve the methodical support of the educational process', NOW());
    -- Istiqamət 6
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 6, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'tədris prosesinin təşkilı və idarə edilməsi ilə əlaqədar analitik-informasiya materiallarının işlənib hazırlanmasını təmin edir', NOW()),
    (obj_id, 'en', 'Ensures the preparation of analytical-information materials related to the organization and management of the educational process', NOW());
    -- Istiqamət 7
    INSERT INTO department_objectives (department_code, display_order, created_at) VALUES (dept_code, 7, NOW()) RETURNING id INTO obj_id;
    INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at) VALUES 
    (obj_id, 'az', 'qanunvericiliklə müəyyən edilmiş digər istiqamətlərdə fəaliyyət göstərir', NOW()),
    (obj_id, 'en', 'Operates in other directions determined by legislation', NOW());

    -- 4. Vəzifələr (Core Functions)
    -- Func 1
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 1, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'payız, yaz və yay semestrlərində tədrisi təşkil etmək', NOW()),
    (func_id, 'en', 'To organize teaching in the fall, spring, and summer semesters', NOW());
    -- Func 2
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 2, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'tədris ili üzrə akademik təqvimin və növbəti tədris ilinə hazırlıq haqqında əmrin tərtibinə və nəzərdə tutulan bütün tədbirlərın vaxtında yerinə yetirilməsinə nəzarət etmək', NOW()),
    (func_id, 'en', 'To supervise the preparation of the academic calendar and the order for preparation for the next academic year, ensuring all planned activities are completed on time', NOW());
    -- Func 3
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 3, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'dərs cədvəllərini hazırlayıb təsdiq üçün rəhbərliyə təqdim etmək', NOW()),
    (func_id, 'en', 'To prepare lesson schedules and submit them to management for approval', NOW());
    -- Func 4
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 4, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'ixtisas kafedraları ilə birlikdə bakalavriat və magistratura səviyyələri üzrə tədris standartlarına uyğun olaraq tədris planlarının tərtibinə nəzarət etmək', NOW()),
    (func_id, 'en', 'To supervise the preparation of curricula for undergraduate and graduate levels in accordance with educational standards, together with specialized departments', NOW());
    -- Func 5
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 5, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'tədris prosesinin təşkilində kafedralara və digər struktur bölmələrə metodiki yardım göstərmək və tədris ili üçün təsdiq olunmuş tədris planlarına riayət etməklə fakültə dekanlıqları tərəfindən tərtib edilmiş “İxtisaslar üzrə illik işçi tədris planları”nın düzgünlüyünü yoxlamaq', NOW()),
    (func_id, 'en', 'To provide methodical assistance to departments and other structural units in organizing the educational process and to verify the accuracy of "Annual Working Curricula by Specializations" prepared by faculty deaneries, ensuring compliance with approved plans', NOW());
    -- Func 6
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 6, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'təhsil proqramlarının reallaşdırılmasını həyata keçirən fakültə və kafedraların fəaliyyətini əlaqələndirmək', NOW()),
    (func_id, 'en', 'To coordinate the activities of faculties and departments implementing educational programs', NOW());
    -- Func 7
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 7, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'tədrisin keyfiyyətinin yaxşılaşdırılması ilə əlaqədar təkliflər vermək', NOW()),
    (func_id, 'en', 'To provide proposals for improving the quality of teaching', NOW());
    -- Func 8
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 8, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'kafedralar üzrə tədris yüklərini təsdiq olunması üçün qəbul edərkən tədris yüklərinə aid formaların düzgün tərtib olunmasına, akademik yükün əmək müqaviləsi əsasında çalışan və ya kənardan dəvət olunmuş əməkdaşlar arasında normalara uyğun bölüşdürülməsinə nəzarət etmək', NOW()),
    (func_id, 'en', 'To monitor the correct preparation of teaching load forms and ensure the academic workload is distributed among staff and guest lecturers according to norms', NOW());
    -- Func 9
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 9, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'tədris ili ərzində kafedraların ştatında olan və ya kənardan dəvət edilmiş əməkdaşlara saathesabı olaraq həvalə edilmiş dərs yükünü yoxlamaq və saathesabı əmr layihələrini hazırlamaq', NOW()),
    (func_id, 'en', 'To verify the hourly workload assigned to staff or guest lecturers during the academic year and prepare draft hourly payment orders', NOW());
    -- Func 10
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 10, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'ATİS proqram təminatının AzTU-da tətbiqi ilə əlaqədar sistemə daxil edilmiş məlumatların modullara uyğun olaraq işlənməsinə və düzgün formada yüklənməsinə ümumi nəzarət etmək', NOW()),
    (func_id, 'en', 'To provide general supervision over the processing and correct uploading of data into the ATIS software system at TU Azerbaijan according to specific modules', NOW());
    -- Func 11
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 11, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'AzTU-nu bitirən məzunlar haqqında hesabatları, ali təhsil haqqında diplomları və diploma əlavələri hazırlamaq', NOW()),
    (func_id, 'en', 'To prepare, register, and issue reports on graduates, higher education diplomas, and diploma supplements', NOW());
    -- Func 12
    INSERT INTO department_core_functions (department_code, display_order, created_at) VALUES (dept_code, 12, NOW()) RETURNING id INTO func_id;
    INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at) VALUES 
    (func_id, 'az', 'tələbə kontingentinin hərəkətinin müntəzəm dəqiqləşdirilməsini, qeydiyyatını və nəzarətini təşkili etmək', NOW()),
    (func_id, 'en', 'To organize the regular verification, registration, and monitoring of student contingent movements', NOW());

    -- 5. Şöbə Müdiri (Director)
    INSERT INTO department_directors (department_code, first_name, last_name, father_name, room_number, created_at)
    VALUES (dept_code, 'Ərəstun', 'Məmmədov', 'Salman oğlu', 'I korpus, 306-4', NOW())
    RETURNING id INTO dir_id;

    INSERT INTO department_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, created_at)
    VALUES 
    (dir_id, 'az', 'Texnika elmləri namizədi', 'dosent', 
    'Ərəstun Salman oğlu Məmmədov — 1990-cı ilin avqust ayından «Maşınqayırma texnologiyası» kafedrasına gənc mütəxəssis kimi stajkeçən-tədqiqatçı vəzifəsinə işə qəbul olunmuşdur. 1993-cü ilin yanvarından «Maşınqayırma texnologiyası» kafedrasında assistent, baş müəllim, 2000-ci ildən isə dosent vəzifəsində çalışır. 2005-2025-ci illər ərzində Maşınqayırma fakültəsinin dekanı, Tədris hissəsinin müdiri və Alman mühəndislik fakültəsinin dekanı vəzifələrini icra etmişdir. 01.2025-ci ildən AzTU-da Tədris şöbəsinin müdiridir. Ə.S.Məmmədov 70-dən çox elmi əsərin, o cümlədən 3 patent, 5 dərs vəsaiti və 1 metodiki göstəriş və 15 fənn proqramının müəllifidir. DAAD, TEMPUS və ERASMUS+ layihələri çərçivəsində Almaniya və Çexiyada elmi ezamiyyətlərdə olmuşdur. "Azərbaycan Respublikası qabaqcıl təhsil işçisi" döş nişanı ilə təltif edilmişdir.', NOW()),
    (dir_id, 'en', 'PhD in Technical Sciences', 'Associate Professor', 
    'Arastun Salman oglu Mammadov began his career in August 1990 at the "Machine Building Technology" department. Since January 1993, he has served as an assistant and senior lecturer, and since 2000, as an Associate Professor. Between 2005 and 2025, he held various positions including Dean of the Faculty of Machine Building, Head of the Teaching Unit, and Acting Dean of the German Faculty of Engineering. Since January 2025, he has been serving as the Head of the Education Department. Author of more than 70 scientific works, including 3 patents and 5 textbooks. He has conducted scientific missions in Germany and the Czech Republic through DAAD, TEMPUS, and ERASMUS+ projects. Awarded the "Advanced Education Worker of the Republic of Azerbaijan" badge.', NOW());

    -- Qəbul saatları
    INSERT INTO department_director_working_hours (director_id, time_range, created_at)
    VALUES (dir_id, '14:00÷15:30', NOW()) RETURNING id INTO wh_id;
    INSERT INTO department_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
    VALUES 
    (wh_id, 'az', 'Bazar ertəsi ÷ Cümə', NOW()),
    (wh_id, 'en', 'Monday – Friday', NOW());

    -- Təhsil
    -- Edu 1
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '1983', '1990', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES 
    (edu_id, 'az', 'mühəndis-mexanik (fərqlənmə)', 'Azərbaycan Texniki Universiteti', NOW()),
    (edu_id, 'en', 'Mechanical Engineer (Distinction)', 'Azerbaijan Technical University', NOW());
    -- Edu 2
    INSERT INTO department_director_educations (director_id, start_year, end_year, created_at) VALUES (dir_id, '1996', '1996', NOW()) RETURNING id INTO edu_id;
    INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at) VALUES 
    (edu_id, 'az', 'Texnika elmləri namizədi', 'AzTU', NOW()),
    (edu_id, 'en', 'PhD in Technical Sciences', 'AzTU', NOW());

    -- 6. Əməkdaşlar (Personnel)
    -- 1. Elnurə Cəfərova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Elnurə', 'Cəfərova', 'Qiyas qızı', 'elnure.ceferova@aztu.edu.az', '1503 (Otaq: 306-3)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Kurikulumun planlaşdırma meneceri', NOW()), (w_id, 'en', 'Curriculum Planning Manager', NOW());

    -- 2. Ülviyyə Əlləzova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Ülviyyə', 'Əlləzova', 'Nəzir qızı', 'ulviyye.ellezova@aztu.edu.az', '(Otaq: 306-3)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Tədris koordinatoru', NOW()), (w_id, 'en', 'Education Coordinator', NOW());

    -- 3. Cəmilə Abdurəhimova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Cəmilə', 'Abdurəhimova', 'İbrahim qızı', 'cemile.abdurahimova@aztu.edu.az', '1505 (Otaq: 306-3)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Akademik məlumat meneceri', NOW()), (w_id, 'en', 'Academic Information Manager', NOW());

    -- 4. Sevinc Mirzəyeva
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Sevinc', 'Mirzəyeva', 'Nazir qızı', 'sevinc.mirzeyeva@aztu.edu.az', '+994 12 538 34 41 (1506) Otaq: 306-5', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Akademik məlumatların idarə edilməsi mütəxəssisi', NOW()), (w_id, 'en', 'Academic Information Management Specialist', NOW());

    -- 5. Səkinə Allahverdiyeva
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Səkinə', 'Allahverdiyeva', 'Aslan qızı', 'sakina.allahverdiyeva@aztu.edu.az', '1501 (Otaq: 306-3)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Elektron Təhsil Sistemi (ETS) mütəxəssisi', NOW()), (w_id, 'en', 'Electronic Education System Specialist', NOW());

    -- 6. Kamil Əliyev
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Kamil', 'Əliyev', 'Rafət oğlu', 'kamil.aliyev.r@aztu.edu.az', '1504 (Otaq: 306-2)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Statistika mütəxəssisi', NOW()), (w_id, 'en', 'Statistical Specialist', NOW());

    -- 7. Günay Kərimova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Günay', 'Kərimova', 'Əjdər qızı', 'gunay.karimova@aztu.edu.az', '+994 12 538 34 41 (1506) Otaq: 306-5', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Sənədləşmə mütəxəssisi', NOW()), (w_id, 'en', 'Documentation Specialist', NOW());

    -- 8. Pərvanə Musayeva
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Pərvanə', 'Musayeva', 'Pərviz qızı', 'pervane.musayeva@aztu.edu.az', '(Otaq: 306-2)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Tələbə təhsil krediti mütəxəssisi', NOW()), (w_id, 'en', 'Student Education Loan Specialist', NOW());

    -- 9. Yaşar İsrəfilov
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Yaşar', 'İsrəfilov', 'Mirbağır oğlu', 'yasar.israfilov@aztu.edu.az', '(Otaq: 306-2)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'AOİTAS mütəxəssisi', NOW()), (w_id, 'en', 'Education System Specialist', NOW());

    -- 10. Ramin Rzayev
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Ramin', 'Rzayev', 'İlham oğlu', 'rzayevramin@aztu.edu.az', '1508 (Otaq: 306-2)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Dərs cədvəli və auditoriyaların idarə edilməsi meneceri', NOW()), (w_id, 'en', 'Course Schedule and Classroom Management Manager', NOW());

    -- 11. Aidə Cabarova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Aidə', 'Cabarova', 'Rafiq qızı', 'aida.cabarova@aztu.edu.az', '+994 12 538 34 41 (1507) Otaq: 306-5', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Dövlət nümunəli təhsil sənədləri mütəxəssisi', NOW()), (w_id, 'en', 'Specialist for State-Recognized Educational Documents', NOW());

    -- 12. Tahirə Təhməzova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Tahirə', 'Təhməzova', 'Rza qızı', 'tahira.tahmazova@aztu.edu.az', '(Otaq: 306-3)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Ştatdankənar xəttat', NOW()), (w_id, 'en', 'Freelance Calligrapher', NOW());

    -- 13. Xəyalə Quliyeva
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Xəyalə', 'Quliyeva', 'Əkbər qızı', 'khayala.guliyeva@aztu.edu.az', '(Otaq: 306-5)', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'Ştatdankənar xəttat', NOW()), (w_id, 'en', 'Freelance Calligrapher', NOW());

    -- 14. Ayçillər Aslanova
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES (dept_code, 'Ayçillər', 'Aslanova', 'Telman qızı', 'ayciller.aslanova@aztu.edu.az', '+994 12 538 45 61 (1502) Otaq: 306-3', NOW()) RETURNING id INTO w_id;
    INSERT INTO department_worker_tr (worker_id, lang_code, duty, created_at) VALUES 
    (w_id, 'az', 'SABAH proqramları koordinatoru', NOW()), (w_id, 'en', 'SABAH Programs Coordinator', NOW());

END $$;
