-- ============================================================
-- Keyfiyyətin Təminatı Şöbəsi / Quality Assurance Department
-- department_code: 'quality_assurance'
-- ============================================================

BEGIN;

-- ── 1. Department base record ───────────────────────────────
INSERT INTO departments (department_code, created_at)
VALUES ('quality_assurance', NOW())
ON CONFLICT (department_code) DO NOTHING;


-- ── 2. Department translations ──────────────────────────────
INSERT INTO departments_tr (department_code, lang_code, department_name, about_html, created_at)
VALUES
(
    'quality_assurance',
    'az',
    'Keyfiyyətin Təminatı Şöbəsi',
    '<p>Azərbaycan Texniki Universitetinin Keyfiyyətin Təminatı Şöbəsi universitetdə təhsil, tədris, elmi-tədqiqat və idarəetmə fəaliyyətlərinin keyfiyyətinin təmin edilməsi, davamlı inkişafın dəstəklənməsi və beynəlxalq standartlara uyğunluğun təmin olunması məqsədilə fəaliyyət göstərən struktur bölmədir.</p><p>Şöbə universitetdə keyfiyyət təminatı mexanizmlərinin qurulmasını və tətbiqini təşkil edir, müvafiq siyasət və prosedurların hazırlanmasını, icrasını və monitorinqini həyata keçirir. Eyni zamanda, struktur bölmələrin fəaliyyətinin qiymətləndirilməsi, akademik proqramların müasir tələblərə uyğunluğunun təmin edilməsi və institusional effektivliyin artırılması istiqamətində sistemli tədbirlər görür.</p><p>Keyfiyyətin Təminatı Şöbəsi akkreditasiya proseslərinin təşkili və koordinasiyası, daxili nəzarət və audit mexanizmlərinin tətbiqi, maraqlı tərəflərin məmnunluğunun öyrənilməsi və təhlili, eləcə də əldə olunan nəticələr əsasında davamlı təkmilləşmə proseslərinin həyata keçirilməsində aparıcı rol oynayır.</p><p>Şöbə öz fəaliyyətində Azərbaycan Respublikasının qanunvericiliyini, universitetin nizamnaməsini və müvafiq normativ-hüquqi aktları rəhbər tutur.</p>',
    NOW()
),
(
    'quality_assurance',
    'en',
    'Quality Assurance Department',
    '<p>The Quality Assurance Department of Azerbaijan Technical University is a structural unit operating with the primary objective of ensuring the quality of education, teaching, research, and administrative activities, fostering continuous improvement, and maintaining compliance with international standards.</p><p>The Department is responsible for the establishment and implementation of quality assurance mechanisms across the university, as well as for the development, execution, and monitoring of relevant policies and procedures. It also undertakes systematic measures aimed at evaluating the performance of structural units, ensuring the alignment of academic programmes with contemporary requirements, and enhancing overall institutional effectiveness.</p><p>Furthermore, the Quality Assurance Department plays a leading role in the organization and coordination of accreditation processes, the implementation of internal control and audit mechanisms, the assessment and analysis of stakeholder satisfaction, and the execution of continuous improvement processes based on the findings obtained.</p><p>In its operations, the Department is guided by the legislation of the Republic of Azerbaijan, the University''s charter, and other relevant regulatory and legal frameworks.</p>',
    NOW()
)
ON CONFLICT (department_code, lang_code) DO UPDATE
SET department_name = EXCLUDED.department_name,
    about_html      = EXCLUDED.about_html,
    updated_at      = NOW();


-- ── 3. Objectives ───────────────────────────────────────────
DELETE FROM department_objectives WHERE department_code = 'quality_assurance';

WITH objective_ids AS (
    INSERT INTO department_objectives (department_code, display_order, created_at)
    VALUES
    ('quality_assurance', 1, NOW()),
    ('quality_assurance', 2, NOW()),
    ('quality_assurance', 3, NOW()),
    ('quality_assurance', 4, NOW()),
    ('quality_assurance', 5, NOW()),
    ('quality_assurance', 6, NOW())
    RETURNING id
),
objective_numbered AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM objective_ids
)
INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at)
SELECT id, 'az', html_content, NOW() FROM objective_numbered o JOIN (
    VALUES
    (1, '<p>Universitetdə keyfiyyət təminatı sisteminin formalaşdırılması və davamlı inkişafının təmin edilməsi.</p>'),
    (2, '<p>Tədris, elmi-tədqiqat və inzibati fəaliyyətlərin keyfiyyətinin yüksəldilməsi və institusional effektivliyin artırılması.</p>'),
    (3, '<p>Akademik proqramların və təhsil prosesinin mövcud təhsil standartlarına və əmək bazarının tələblərinə uyğunluğunun təmin edilməsi.</p>'),
    (4, '<p>Universitetin milli və beynəlxalq akkreditasiya tələblərinə uyğun fəaliyyətinin təşkili və bu istiqamətdə davamlı monitorinqin həyata keçirilməsi.</p>'),
    (5, '<p>Maraqlı tərəflərin məmnunluq səviyyəsinin ölçülməsi və nəticələr əsasında idarəetmə qərarlarının qəbuluna dəstək verilməsi.</p>'),
    (6, '<p>Keyfiyyətin təmin olunması sahəsində innovativ yanaşmaların tətbiqi və davamlı təkmilləşmə mədəniyyətinin formalaşdırılması.</p>')
) v(row_num, html_content) ON o.row_num = v.row_num
UNION ALL
SELECT id, 'en', html_content, NOW() FROM objective_numbered o JOIN (
    VALUES
    (1, '<p>Establishing and ensuring the continuous development of a comprehensive quality assurance system within the university.</p>'),
    (2, '<p>Enhancing the quality of teaching, research, and administrative activities, while increasing overall institutional effectiveness.</p>'),
    (3, '<p>Ensuring that academic programmes and the educational process are aligned with current educational standards and labour market demands.</p>'),
    (4, '<p>Organizing the university''s operations in compliance with national and international accreditation requirements and conducting continuous monitoring in this regard.</p>'),
    (5, '<p>Measuring stakeholder satisfaction levels and supporting evidence-based managerial decision-making based on the results obtained.</p>'),
    (6, '<p>Promoting the adoption of innovative approaches in quality assurance and fostering a culture of continuous improvement.</p>')
) v(row_num, html_content) ON o.row_num = v.row_num;


-- ── 4. Core functions ───────────────────────────────────────
DELETE FROM department_core_functions WHERE department_code = 'quality_assurance';

WITH cf_ids AS (
    INSERT INTO department_core_functions (department_code, display_order, created_at)
    VALUES
    ('quality_assurance', 1, NOW()),
    ('quality_assurance', 2, NOW()),
    ('quality_assurance', 3, NOW()),
    ('quality_assurance', 4, NOW())
    RETURNING id
),
cf_numbered AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM cf_ids
)
INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at)
SELECT id, 'az', html_content, NOW() FROM cf_numbered c JOIN (
    VALUES
    (1, '<h4>Akkreditasiya və monitorinq</h4><ul><li>Universitetin və təhsil proqramlarının akkreditasiya tələblərinə uyğunluğunun təmin edilməsi;</li><li>İnstitusional və proqram akkreditasiyası üzrə özünütəhlil proseslərinin təşkili və həyata keçirilməsi;</li><li>Akkreditasiya nəticələri üzrə verilmiş tövsiyələrin icrasına nəzarətin həyata keçirilməsi;</li><li>Beynəlxalq akkreditasiya proseslərinin digər struktur bölmələrlə əlaqəli şəkildə təşkili və koordinasiyası;</li><li>Universitetin fəaliyyət istiqamətləri üzrə monitorinq mexanizmlərinin hazırlanması və tətbiqi;</li><li>Struktur bölmələrin fəaliyyətinin, təhsil proqramlarının və ümumi institusional fəaliyyətin monitorinqinin həyata keçirilməsi.</li></ul>'),
    (2, '<h4>Akademik keyfiyyətin qiymətləndirilməsi</h4><ul><li>Akademik proqramların və kurikulumların mütəmadi olaraq qiymətləndirilməsi və yenilənməsi;</li><li>Tədrisin effektivliyinin artırılması məqsədilə müvafiq təhlillərin aparılması;</li><li>Tələbələrin təlim nəticələrinin və akademik performans göstəricilərinin qiymətləndirilməsi;</li><li>Akademik və inzibati proseslər üzrə siyasət və prosedurların hazırlanması və təkmilləşdirilməsi;</li><li>Tədris və idarəetmə proseslərində keyfiyyət standartlarının tətbiqinə nəzarət;</li><li>Akademik və inzibati heyət üçün metodiki dəstək və təlimlərin təşkili.</li></ul>'),
    (3, '<h4>Məmnunluq və qiymətləndirmə</h4><ul><li>Təhsilalanlar, təhsil verənlər, məzunlar və digər maraqlı tərəflər arasında məmnunluq sorğularının təşkili;</li><li>Sorğu nəticələrinin təhlili və ümumiləşdirilməsi;</li><li>Akademik fəaliyyət, tələbə məmnuniyyəti və digər göstəricilər üzrə analitik hesabatların hazırlanması;</li><li>Əldə olunan nəticələr əsasında qərarların qəbuluna dəstək verilməsi;</li><li>Keyfiyyət göstəricilərinin qiymətləndirilməsi və inkişaf istiqamətlərinin müəyyən edilməsi.</li></ul>'),
    (4, '<h4>Audit</h4><ul><li>Universitet daxilində daxili nəzarət və audit mexanizmlərinin təşkili və həyata keçirilməsi;</li><li>Struktur bölmələrin fəaliyyətinin və icra vəziyyətinin yoxlanılması;</li><li>Daxili nəzarət tədbirləri çərçivəsində məlumatların toplanması, təhlili və qiymətləndirilməsi;</li><li>Aşkar edilmiş çatışmazlıqların aradan qaldırılması ilə bağlı təkliflərin hazırlanması;</li><li>Daxili nəzarət sisteminin təkmilləşdirilməsi istiqamətində tədbirlərin həyata keçirilməsi;</li><li>Zərurət yarandıqda təkrar audit və yoxlamaların aparılması.</li></ul>')
) v(row_num, html_content) ON c.row_num = v.row_num
UNION ALL
SELECT id, 'en', html_content, NOW() FROM cf_numbered c JOIN (
    VALUES
    (1, '<h4>Accreditation and Monitoring</h4><ul><li>Ensuring the university''s and academic programmes'' compliance with accreditation requirements;</li><li>Organizing and conducting self-assessment processes for institutional and programme accreditation;</li><li>Overseeing the implementation of recommendations arising from accreditation outcomes;</li><li>Organizing and coordinating international accreditation processes in close collaboration with relevant structural units;</li><li>Developing and implementing monitoring mechanisms across the university''s areas of activity;</li><li>Conducting systematic monitoring of structural units, academic programmes, and overall institutional performance.</li></ul>'),
    (2, '<h4>Academic Quality Assessment</h4><ul><li>Conducting regular evaluation and systematic revision of academic programmes and curricula;</li><li>Performing analytical assessments aimed at enhancing the effectiveness of teaching and learning processes;</li><li>Evaluating students'' learning outcomes and academic performance indicators;</li><li>Developing and refining policies and procedures governing academic and administrative processes;</li><li>Overseeing the implementation of quality standards in teaching and institutional management processes;</li><li>Providing methodological support and organizing professional development training for academic and administrative staff.</li></ul>'),
    (3, '<h4>Satisfaction and Evaluation</h4><ul><li>Organizing satisfaction surveys among students, academic staff, graduates, and other stakeholders;</li><li>Analyzing and synthesizing survey results;</li><li>Preparing analytical reports on academic performance, student satisfaction, and other key indicators;</li><li>Supporting decision-making processes based on the findings obtained;</li><li>Evaluating quality indicators and identifying strategic directions for further development.</li></ul>'),
    (4, '<h4>Audit</h4><ul><li>Organization and execution of internal control and audit mechanisms within the university;</li><li>Examination of the activities and performance status of structural units;</li><li>Collection, analysis, and evaluation of data within the framework of internal control procedures;</li><li>Preparation of recommendations aimed at eliminating identified deficiencies;</li><li>Implementation of measures to enhance and optimize the internal control system;</li><li>Conducting follow-up audits and inspections when necessary.</li></ul>')
) v(row_num, html_content) ON c.row_num = v.row_num;


-- ── 5. Director + translations + working hours + educations ──
-- Note: department_directors schema has no email/phone columns; contact
-- details for the head are preserved inside the bio HTML so no data is lost.
WITH director_insert AS (
    INSERT INTO department_directors (
        department_code,
        first_name, last_name, father_name,
        room_number,
        created_at
    ) VALUES (
        'quality_assurance',
        'Pərvanə', 'Mövsümova', 'Firdovsi qızı',
        'II korpus, 317-ci otaq',
        NOW()
    ) ON CONFLICT (department_code) DO UPDATE
    SET first_name  = EXCLUDED.first_name,
        last_name   = EXCLUDED.last_name,
        father_name = EXCLUDED.father_name,
        room_number = EXCLUDED.room_number,
        updated_at  = NOW()
    RETURNING id
)
INSERT INTO department_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, created_at)
SELECT id, 'az',
    'Dil nəzəriyyəsi üzrə fəlsəfə doktoru (PhD)',
    'Şöbə müdiri',
    '<p><strong>Əlaqə:</strong> parvana.movsumova@aztu.edu.az · +994 50 306 74 76 / +994 10 331 23 63 · II korpus, 317-ci otaq · Bazar ertəsi – Cümə (09:00–17:00)</p><p>Mövsümova Pərvanə Firdovsi qızı — dil nəzəriyyəsi və tərcümə sahəsində ixtisaslaşmış, keyfiyyət təminatı və ali təhsilin idarə olunması istiqamətində geniş təcrübəyə malik mütəxəssisdir. O, ali təhsil sistemində keyfiyyət təminatı, akkreditasiya və tədris prosesinin təkmilləşdirilməsi sahələrində elmi və inzibati fəaliyyət göstərir.</p><p>Onun peşəkar fəaliyyətinin əsas istiqamətlərinə ali təhsildə keyfiyyət təminatı sistemlərinin qurulması, daxili və xarici akkreditasiya proseslərinin təşkili, təhsil siyasətinin hazırlanması, monitorinq və qiymətləndirmə mexanizmlərinin tətbiqi, eləcə də beynəlxalq reytinq sistemləri ilə iş daxildir. Bu sahələr üzrə fəaliyyəti nəticəsində müxtəlif universitetlərdə keyfiyyət təminatı mexanizmlərinin inkişafına və beynəlxalq standartlara uyğunlaşdırılmasına mühüm töhfələr vermişdir.</p><p>Pərvanə Mövsümova pedaqoji fəaliyyətində müasir tədris metodlarını tətbiq edərək tələbəyönümlü yanaşmanın inkişafına, tədris prosesində innovativ üsulların tətbiqinə və müəllimlərin peşəkar inkişafına xüsusi diqqət yetirir. O, həmçinin təlim proqramlarının hazırlanması, tədris nəticələrinin qiymətləndirilməsi və akademik heyətin inkişafı istiqamətində aktiv fəaliyyət göstərir.</p><p>Hazırda o, Azərbaycan Texniki Universitetində Keyfiyyətin Təminatı şöbəsinin müdiri vəzifəsində çalışır və universitet səviyyəsində keyfiyyət təminatı siyasətinin formalaşdırılması və icrasına rəhbərlik edir.</p><p>Pərvanə Mövsümova uzun illər ərzində müxtəlif ali təhsil müəssisələrində rəhbər və müəllim kimi fəaliyyət göstərmiş, beynəlxalq akkreditasiya proseslərində, Erasmus+ proqramlarında və müxtəlif elmi-tədris layihələrində iştirak etmişdir. O, 20-dən çox elmi məqalənin və bir sıra tədris proqramlarının müəllifidir, həmçinin keyfiyyət təminatı və təhsil idarəçiliyi sahəsində ekspert kimi çıxış edir.</p>',
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'PhD in Linguistic Theory',
    'Head of Department',
    '<p><strong>Contact:</strong> parvana.movsumova@aztu.edu.az · +994 50 306 74 76 / +994 10 331 23 63 · II Building, Room 317 · Monday – Friday (09:00–17:00)</p><p>Parvana Movsumova Firdovsi is a specialist in the fields of linguistics and translation studies with extensive experience in quality assurance and higher education management. She is actively engaged in both academic and administrative work focused on quality assurance, accreditation, and the continuous improvement of teaching and learning processes in higher education institutions.</p><p>Her core areas of professional activity include the establishment of quality assurance systems in higher education, the organization of internal and external accreditation processes, the development of education policies, and the implementation of monitoring and evaluation mechanisms, as well as work with international ranking systems. Through her contributions in these domains, she has significantly supported the development and alignment of quality assurance frameworks in various universities with international standards.</p><p>In her pedagogical practice, Parvana Movsumova places strong emphasis on student-centered learning, the integration of innovative teaching methodologies, and the professional development of academic staff. She is also actively involved in the design of training programs, assessment of learning outcomes, and capacity building for faculty members.</p><p>She currently serves as the Head of the Quality Assurance Department at the Azerbaijan Technical University, where she leads the formulation and implementation of the university''s quality assurance policy.</p><p>Over the years, she has held leadership and teaching positions in several higher education institutions and has participated in international accreditation processes, Erasmus+ programs, and various academic and educational projects. She is the author of more than 20 scientific publications and several curricula, and she also acts as an expert in quality assurance and educational management.</p>',
    NOW()
FROM director_insert
ON CONFLICT (director_id, lang_code) DO UPDATE
SET scientific_degree = EXCLUDED.scientific_degree,
    scientific_title  = EXCLUDED.scientific_title,
    bio               = EXCLUDED.bio,
    updated_at        = NOW();

-- Working hours
WITH wh_insert AS (
    INSERT INTO department_director_working_hours (director_id, time_range, created_at)
    SELECT id, '09:00–17:00', NOW()
    FROM department_directors WHERE department_code = 'quality_assurance'
    RETURNING id
)
INSERT INTO department_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi – Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday – Friday',    NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO department_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1999', '2003', NOW() FROM department_directors WHERE department_code = 'quality_assurance'
UNION ALL
SELECT id, '2003', '2006', NOW() FROM department_directors WHERE department_code = 'quality_assurance'
UNION ALL
SELECT id, '2020', '2024', NOW() FROM department_directors WHERE department_code = 'quality_assurance';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM (
        SELECT id FROM department_director_educations
        WHERE director_id = (SELECT id FROM department_directors WHERE department_code = 'quality_assurance')
        ORDER BY id ASC
        LIMIT 3
    ) sub
)
INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bakalavr (Avropaşünaslıq və beynəlxalq münasibətlər)', 'Azərbaycan Dillər Universiteti'),
    (2, 'Magistratura (Tərcümə nəzəriyyəsi və dillərarası əlaqə)', 'Gəncə Dövlət Universiteti'),
    (3, 'Doktorantura (Dil nəzəriyyəsi)', 'Azərbaycan Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bachelor''s (European Studies and International Relations)', 'Azerbaijan University of Languages'),
    (2, 'Master''s (Translation Theory and Interlingual Communication)', 'Ganja State University'),
    (3, 'PhD (Doctoral studies) in Linguistic Theory', 'Azerbaijan University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 6. Workers ──────────────────────────────────────────────
DELETE FROM department_workers WHERE department_code = 'quality_assurance';

WITH worker_inserts AS (
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('quality_assurance', 'Nərmin',  'Xasayeva',    'Pərviz qızı',  'narmin.xasayeva@aztu.edu.az',    '+994 55 698 70 07', NOW()),  -- 1
    ('quality_assurance', 'Afaq',    'İsmayılzadə', 'Rafiq qızı',   'afag.ismayilzade@aztu.edu.az',   '+994 50 654 96 64', NOW()),  -- 2
    ('quality_assurance', 'Həmidə',  'Həsənova',    'İmran qızı',   'hemide.hesenova@aztu.edu.az',    '+994 77 597 01 01', NOW()),  -- 3
    ('quality_assurance', 'Kənan',   'Zərbiyev',    'Mübariz oğlu', 'kenan.zarbiyev@aztu.edu.az',     '+994 70 560 00 62', NOW())   -- 4
    RETURNING id
),
worker_numbered AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM worker_inserts
)
INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM worker_numbered w JOIN (
    VALUES
    (1, 'Akademik keyfiyyətin qiymətləndirilməsi mütəxəssisi', NULL::varchar, NULL::varchar),
    (2, 'Akkreditasiya və monitorinq üzrə mütəxəssis',         NULL,          NULL),
    (3, 'Məmnunluq və qiymətləndirmə üzrə mütəxəssis',         NULL,          NULL),
    (4, 'Audit mütəxəssisi',                                    NULL,          NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM worker_numbered w JOIN (
    VALUES
    (1, 'Specialist in Academic Quality Assessment',       NULL::varchar, NULL::varchar),
    (2, 'Specialist in Accreditation and Monitoring',      NULL,          NULL),
    (3, 'Specialist in Satisfaction and Evaluation',       NULL,          NULL),
    (4, 'Audit Specialist',                                 NULL,          NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
