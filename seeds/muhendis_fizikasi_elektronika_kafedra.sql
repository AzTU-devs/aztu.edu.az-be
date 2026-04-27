-- ============================================================
-- "Mühəndis fizikası və elektronika" kafedrası — Full DB Import
-- cafedra_code: 'engineering-physics'
-- faculty_code: '805984'
-- ============================================================

BEGIN;

-- ── 1. Cafedra base record ──────────────────────────────────
INSERT INTO cafedras (
    faculty_code,
    cafedra_code,
    bachelor_programs_count,
    master_programs_count,
    phd_programs_count,
    international_collaborations_count,
    laboratories_count,
    projects_patents_count,
    industrial_collaborations_count,
    sdgs,
    created_at
) VALUES (
    '805984',
    'engineering-physics',
    1, 2, 1, 10, 9, 11, 2,
    '[6, 7]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'engineering-physics',
    'az',
    'Mühəndis fizikası və elektronika kafedrası',
    '<p>Mühəndis fizikası və elektronika kafedrası Azərbaycan Texniki Universitetinin (AzTU) Elmi Şurasının 3 fevral 2021-ci il tarixli qərarı ilə yaradılmışdır. Kafedranın əsas məqsədi mühəndis fizikası, elektronika və müasir texnologiyalar sahələrində yüksək ixtisaslı mütəxəssislərin hazırlanmasıdır.</p><p>Kafedranın missiyası fundamental fizika biliklərini mühəndis yanaşması ilə birləşdirərək analitik düşüncəyə malik, innovativ texnologiyalarla işləmə bacarığı olan müasir mühəndislər yetişdirməkdir. Elmi-tədqiqat fəaliyyəti yarımkeçiricilər, kompozit və nanomateriallar, optoelektronika və bərpa olunan enerji texnologiyaları kimi aktual sahələri əhatə edir.</p>',
    NOW()
),
(
    'engineering-physics',
    'en',
    'Department of Engineering Physics and Electronics',
    '<p>The Department of Engineering Physics and Electronics was established by the decision of the Scientific Council of the Azerbaijan Technical University (AzTU) dated February 3, 2021. The main objective of the department is to train highly qualified specialists in the fields of engineering physics, electronics, and modern technologies.</p><p>The mission of the department is to combine fundamental knowledge of physics with an engineering approach in order to educate modern engineers who possess analytical thinking skills and the ability to work with innovative technologies. Its research activities cover emerging fields such as semiconductors, composite and nanomaterials, optoelectronics, and renewable energy technologies.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'engineering-physics';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('engineering-physics', 1, NOW()),
    ('engineering-physics', 2, NOW()),
    ('engineering-physics', 3, NOW()),
    ('engineering-physics', 4, NOW()),
    ('engineering-physics', 5, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Müasir Tədris Proqramları', 'Mühəndis fizikası və elektronika sahəsində innovativ və beynəlxalq standartlara uyğun tədris proqramlarının hazırlanması.'),
    (2, 'Nəzəriyyə və Təcrübənin İnteqrasiyası', 'Tələbələrin nəzəri biliklərinin praktik tətbiqlərlə inteqrasiyası və peşəkar bacarıqların inkişafı.'),
    (3, 'Elmi Tədqiqatlar', 'Yeni nəsil yarımkeçiricilərin və nanokompozit materialların sintezi və fiziki xassələrinin tədqiqi.'),
    (4, 'Sənaye Əməkdaşlığı', 'Sənaye müəssisələri ilə əməkdaşlıq çərçivəsində yüksəkixtisaslı kadr hazırlığının təşkili.'),
    (5, 'İnnovativ Həllər', 'Enerji sistemləri və elektron texnologiyalar sahəsində innovativ və səmərəli həllərin işlənib hazırlanması.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Modern Curricula', 'Development of innovative and internationally aligned curricula in engineering physics and electronics.'),
    (2, 'Theory and Practice Integration', 'Integration of students’ theoretical knowledge with practical applications and professional skill development.'),
    (3, 'Scientific Research', 'Synthesis and investigation of physical properties of next-generation semiconductors and nanocomposite materials.'),
    (4, 'Industry Collaboration', 'Organization of specialist training in cooperation with industrial enterprises and research institutions.'),
    (5, 'Innovative Solutions', 'Development of efficient solutions in the fields of energy systems and electronic technologies.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'engineering-physics',
        'Mətanət', 'Mehrabova', 'Əhməd qızı',
        'metanet.mehrabova@aztu.edu.az',
        '+994 12 538 33 83 daxili 1320',
        'V korpus, 203 otaq',
        NOW()
    ) ON CONFLICT (cafedra_code) DO UPDATE
    SET first_name   = EXCLUDED.first_name,
        last_name    = EXCLUDED.last_name,
        father_name  = EXCLUDED.father_name,
        email        = EXCLUDED.email,
        phone        = EXCLUDED.phone,
        room_number  = EXCLUDED.room_number,
        updated_at   = NOW()
    RETURNING id
)
INSERT INTO cafedra_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, scientific_research_fields, created_at)
SELECT id, 'az',
    'Fizika elmləri doktoru',
    'Dosent',
    '<p>Mətanət Mehrabova Əhməd – fizika elmləri doktoru, dosent, bərk cisimlər fizikası, yarımkeçiricilər fizikası və radiasiya materialşünaslığı üzrə ixtisaslaşmış alimdir. O, 300-dən çox elmi məqalənin, 3 kitabın və 2 patentin müəllifidir.</p><p>Onun elmi tədqiqatlarının əsas istiqamətlərinə yarımkeçiricilər və onlar əsasında strukturların nəzəri və eksperimental tədqiqatları, polimerlər və kompozit materialların fiziki xassələrinin tədqiqi daxildir. Hazırda Mühəndis fizikası və elektronika kafedrasının müdiri vəzifəsində çalışır.</p>',
    '["Yarımkeçirici materiallar və strukturlar", "Radiasiya materialşünaslığı", "Mikro və nanoelektronika", "Bərk cism fizikası", "Polimer və kompozit materiallar", "Hesablama modelləşdirilməsi"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Physical Sciences (DSc)',
    'Associate Professor',
    '<p>Matanat Ahmad Mehrabova is a Doctor of Physical Sciences (DSc), Associate Professor, and a scholar specializing in solid-state physics, semiconductor physics, and radiation materials science. She is the author of more than 300 scientific articles, 3 books, and 2 patents.</p><p>Her main research areas include theoretical and experimental studies of semiconductors, investigation of the physical properties of polymers and composite materials, and radiation effects on materials. Currently, she serves as the Head of the Department of Engineering Physics and Electronics.</p>',
    '["Semiconductor materials and structures", "Radiation study of materials", "Micro- and nanoelectronics", "Solid state physics", "Polymer and composite materials", "Computational modeling"]'::jsonb,
    NOW()
FROM director_insert
ON CONFLICT (director_id, lang_code) DO UPDATE
SET scientific_degree          = EXCLUDED.scientific_degree,
    scientific_title           = EXCLUDED.scientific_title,
    bio                        = EXCLUDED.bio,
    scientific_research_fields = EXCLUDED.scientific_research_fields,
    updated_at                 = NOW();

-- Working hours
WITH wh_insert AS (
    INSERT INTO cafedra_director_working_hours (director_id, time_range, created_at)
    SELECT id, '14:00–17:00', NOW() FROM cafedra_directors WHERE cafedra_code = 'engineering-physics'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Çərşənbə, Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Wednesday, Friday', NOW() FROM wh_insert;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1981', '1986', NOW() FROM cafedra_directors WHERE cafedra_code = 'engineering-physics'
UNION ALL
SELECT id, '1988', '1992', NOW() FROM cafedra_directors WHERE cafedra_code = 'engineering-physics'
UNION ALL
SELECT id, '2014', '2018', NOW() FROM cafedra_directors WHERE cafedra_code = 'engineering-physics';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'engineering-physics')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Ali təhsil (Bakalavr + Magistr)', 'Bakı Dövlət Universiteti'),
    (2, 'Elmlər namizədi (PhD)',           'Kosmik Tədqiqatlar İnstitutu'),
    (3, 'Elmlər doktoru (DSc)',            'AMEA Radiasiya Problemləri İnstitutu')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Higher Education (Bachelor + Master)', 'Baku State University'),
    (2, 'Candidate of Sciences (PhD)',          'Institute of Space Research'),
    (3, 'Doctor of Sciences (DSc)',             'Institute of Radiation Problems, ANAS')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'engineering-physics';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('engineering-physics', 'Vəli',     'Hüseynov',      'Allahverdi oğlu', 'veli.huseynov@aztu.edu.az',   '+994 50 399 68 81', NOW()),
    ('engineering-physics', 'Çingiz',   'Əbilov',        'İldırım oğlu',    'chingiz.ebilov@aztu.edu.az',   '+994 50 346 96 02', NOW()),
    ('engineering-physics', 'Naxçıvan', 'Səfərov',       'Yusub oğlu',      'naxchivan.seferov@aztu.edu.az', '+994 50 458 65 96', NOW()),
    ('engineering-physics', 'Mehriban', 'Həsənova',      'Şirin qızı',      'mehriban.hesenova@aztu.edu.az','+994 50 310 97 17', NOW()),
    ('engineering-physics', 'Sevda',    'Qasımova',      'Rasim qızı',      'sevda.qasimova@aztu.edu.az',   '+994 55 828 79 74', NOW()),
    ('engineering-physics', 'Babakişi', 'Qaracayev',     'Qaraca oğlu',     'qaracayev.babakishi@aztu.edu.az','+994 50 648 18 48', NOW()),
    ('engineering-physics', 'Elmxan',   'Qurbanov',      'Mədəd oğlu',      'elmxan.qurbanov@aztu.edu.az',  '+994 50 631 20 23', NOW()),
    ('engineering-physics', 'Rəsul',    'Rəhimov',       'Səftər oğlu',     'rehimov_resul@aztu.edu.az',    '+994 50 317 07 80', NOW()),
    ('engineering-physics', 'Kamal',    'Gülməmmədov',   'Camal oğlu',      'kamal.gul@aztu.edu.az',        '+994 50 222 06 80', NOW()),
    ('engineering-physics', 'Şəfiqə',   'Mehdiyeva',     'Məhəmməd qızı',   'mehdiyeva_shafiga@aztu.edu.az','+994 50 501 29 59', NOW()),
    ('engineering-physics', 'Sevinc',   'Osmanova',      'Sərkər qızı',     'sevinc_osman@aztu.edu.az',     '+994 50 381 10 30', NOW()),
    ('engineering-physics', 'Nigar',    'Hüseynova',     'Tərxan qızı',     'nigar.huseynova@aztu.edu.az',  '+994 50 740 90 10', NOW()),
    ('engineering-physics', 'Şücayət',  'Zeynalov',      'Əmən oğlu',       'sucaet@aztu.edu.az',           '+994 55 829 73 72', NOW()),
    ('engineering-physics', 'Elçin',    'Mustafayev',    'Ramiz oğlu',      'elcin.mustafayev@aztu.edu.az', '+994 50 210 24 55', NOW()),
    ('engineering-physics', 'Sürəyya',  'Məmmədova',     'İsa qızı',        'memmedova_sureyya@aztu.edu.az','+994 50 543 48 05', NOW()),
    ('engineering-physics', 'Sevinc',   'Səfərova',      'İttifaq qızı',    'seferova_sevinc@aztu.edu.az',  '+994 55 405 90 08', NOW()),
    ('engineering-physics', 'Rafiq',    'Sadıqov',       'Mikayıl oğlu',    'rafiq.sadiqov@aztu.edu.az',   '+994 70 580 71 61', NOW()),
    ('engineering-physics', 'Günay',    'Xasməmmədova',  'Tofiq qızı',      'gunay.xasmemmedova@aztu.edu.az','+994 50 389 36 12', NOW()),
    ('engineering-physics', 'Elmira',   'Qasımova',      'Kərim qızı',      'elmira.qasimova@aztu.edu.az',  '+994 51 784 77 34', NOW()),
    ('engineering-physics', 'Aybəniz',  'Abdullayeva',   'Akif qızı',       'aybeniz.abdullayeva@aztu.edu.az','+994 50 295 58 78', NOW()),
    ('engineering-physics', 'İradə',    'İbrahimova',    'Cavad qızı',      'irade.ibrahimova@aztu.edu.az', '+994 50 332 88 60', NOW()),
    ('engineering-physics', 'Gülşən',   'Cəfərova',      'Salman qızı',     'g.jafarova@aztu.edu.az',       '+994 77 638 50 00', NOW()),
    ('engineering-physics', 'Fərhad',   'Kərimov',       'Şamil oğlu',      'ferhad.kerimov@aztu.edu.az',   '+994 70 498 57 34', NOW()),
    ('engineering-physics', 'Səyyarə',  'Sadıqova',      'Heydər qızı',     'seyyare.sadiqova@aztu.edu.az', '+994 77 731 18 31', NOW()),
    ('engineering-physics', 'Şərəfxanım', 'Əliyeva',      'Vaqif qızı',      'sharafxanim@aztu.edu.az',      '+994 55 478 09 99', NOW()),
    ('engineering-physics', 'Rəna',     'Məmmədli',      'Mirzə qızı',      'renamammadli@aztu.edu.az',     '+994 50 545 41 40', NOW()),
    ('engineering-physics', 'Sona',     'Hüseynova',     'Təhmasib qızı',   'sona.huseynova@aztu.edu.az',   '+994 99 309 06 90', NOW())
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Kafedranın professoru', 'Professor', 'f.r.e.d.'),
    (2,  'Kafedranın məsləhətçi professoru', 'Professor', 't.e.d.'),
    (3,  'Kafedranın professoru', 'Professor', 'p.ü.e.d.'),
    (4,  'Kafedranın professoru', 'Professor', 'f.ü.f.d.'),
    (5,  'Kafedranın professoru', 'Professor', 't.e.d.'),
    (6,  'Kafedranın dosenti',    'Dosent',    't.e.n.'),
    (7,  'Kafedranın dosenti',    'Dosent',    'f.r.e.n.'),
    (8,  'Kafedranın dosenti',    'Dosent',    't.e.n.'),
    (9,  'Kafedranın dosenti',    'Dosent',    'f.r.e.n.'),
    (10, 'Kafedranın dosenti',    'Dosent',    'p.e.n.'),
    (11, 'Kafedranın dosenti',    'Dosent',    'f.r.e.n.'),
    (12, 'Kafedranın dosenti',    'Dosent',    'f.r.e.n.'),
    (13, 'Kafedranın dosenti',    'Dosent',    'f.ü.f.d.'),
    (14, 'Kafedranın dosenti',    'Dosent',    'f.r.e.n.'),
    (15, 'Kafedranın dosenti',    'Dosent',    'f.r.e.n.'),
    (16, 'Kafedranın dosenti',    'Dosent',    'f.ü.f.d.'),
    (17, 'Kafedranın dosenti',    'Dosent',    'f.r.e.n.'),
    (18, 'Kafedranın dosenti',    'Dosent',    't.ü.f.d.'),
    (19, 'Kafedranın dosenti',    'Dosent',    'f.ü.f.d.'),
    (20, 'Kafedranın müəllimi',   NULL,       't.ü.f.d.'),
    (21, 'Kafedranın baş müəllimi', NULL,      NULL),
    (22, 'Kafedranın baş müəllimi', NULL,      'f.r.e.n.'),
    (23, 'Kafedranın baş müəllimi', NULL,      'f.r.e.n.'),
    (24, 'Kafedranın müəllim köməkçisi', NULL, NULL),
    (25, 'Kafedranın müəllimi',   NULL,       'f.ü.f.d.'),
    (26, 'Kafedranın müəllim köməkçisi', NULL, NULL),
    (27, 'Kafedranın kargüzarı',   NULL,       NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Professor of Department', 'Professor', 'DSc in Physics and Math'),
    (2,  'Consultant Professor',   'Professor', 'DSc in Technical Sciences'),
    (3,  'Professor of Department', 'Professor', 'DSc in Pedagogical Sciences'),
    (4,  'Professor of Department', 'Professor', 'PhD in Physics'),
    (5,  'Professor of Department', 'Professor', 'DSc in Technical Sciences'),
    (6,  'Associate Professor',    'Associate Professor', 'Candidate of Tech Sciences'),
    (7,  'Associate Professor',    'Associate Professor', 'DSc in Physics and Math'),
    (8,  'Associate Professor',    'Associate Professor', 'Candidate of Tech Sciences'),
    (9,  'Associate Professor',    'Associate Professor', 'DSc in Physics and Math'),
    (10, 'Associate Professor',    'Associate Professor', 'Candidate of Pedagogical Sciences'),
    (11, 'Associate Professor',    'Associate Professor', 'DSc in Physics and Math'),
    (12, 'Associate Professor',    'Associate Professor', 'Candidate of Physics and Math'),
    (13, 'Associate Professor',    'Associate Professor', 'PhD in Physics'),
    (14, 'Associate Professor',    'Associate Professor', 'Candidate of Physics and Math'),
    (15, 'Associate Professor',    'Associate Professor', 'Candidate of Physics and Math'),
    (16, 'Associate Professor',    'Associate Professor', 'PhD in Physics'),
    (17, 'Associate Professor',    'Associate Professor', 'Candidate of Physics and Math'),
    (18, 'Associate Professor',    'Associate Professor', 'PhD in Engineering'),
    (19, 'Associate Professor',    'Associate Professor', 'PhD in Physics'),
    (20, 'Lecturer of Department', NULL,        'PhD in Engineering'),
    (21, 'Senior Lecturer',        NULL,        NULL),
    (22, 'Senior Lecturer',        NULL,        'Candidate of Physics and Math'),
    (23, 'Senior Lecturer',        NULL,        'Candidate of Physics and Math'),
    (24, 'Teaching Assistant',     NULL,        NULL),
    (25, 'Teacher of Department',  NULL,        'PhD in Physics'),
    (26, 'Teaching Assistant',     NULL,        NULL),
    (27, 'Administrator',          NULL,        NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
