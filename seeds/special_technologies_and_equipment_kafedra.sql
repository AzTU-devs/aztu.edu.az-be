-- ============================================================
-- "Xüsusi texnologiyalar və avadanlıqlar" kafedrası — Full DB Import
-- cafedra_code: 'special_technologies_and_equipment'
-- faculty_code: 'XTT'
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
    'XTT',
    'special_technologies_and_equipment',
    1, 3, 2, 2, 3, 7, 1,
    '[9, 4, 8, 17]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'special_technologies_and_equipment',
    'az',
    'Xüsusi texnologiyalar və avadanlıqlar kafedrası',
    '<p>Azərbaycan Texniki Universiteti nəzdində fəaliyyət göstərən Xüsusi texnologiyalar və avadanlıqlar kafedrası 1990-cı ildə "Nəqliyyat maşınqayırma texnologiyası" kafedrası kimi yaradılmış, sonrakı illərdə bir neçə dəfə yenidən təşkil olunaraq 2016-cı ildən hazırkı adla fəaliyyət göstərir.</p><p>Kafedrada maşınqayırma, xüsusi texnologiyalar və avadanlıqlar sahəsi üzrə bakalavr və magistr hazırlığı həyata keçirilir. Tədris prosesi müasir texnologiyalara əsaslanır və tələbələrə texnoloji proseslərin təşkili, avadanlıqların istismarı və bərpa üsulları üzrə biliklər verilir.</p><p>Kafedranın nəzdində "Diffuziya metallaşdırma", "Tribotexnika" və "Alətlər və avadanlıqlar" laboratoriyaları fəaliyyət göstərir, maşın hissələrinin bərpası və etibarlılığı sahəsində elmi-tədqiqat işləri aparılır.</p><p>Kafedranın əsas məqsədi innovativ tədris metodlarının tətbiqi, elm və istehsalatın inteqrasiyası, həmçinin yüksək ixtisaslı mühəndis kadrların hazırlanmasıdır.</p>',
    NOW()
),
(
    'special_technologies_and_equipment',
    'en',
    'Department of Special Technologies and Equipment',
    '<p>The Department of Special Technologies and Equipment, operating under Azerbaijan Technical University, was established in 1990 as the "Transport Machine-Building Technology" department, and after several reorganizations in subsequent years, has been operating under its current name since 2016.</p><p>The department offers bachelor''s and master''s level training in machine-building, special technologies, and equipment. The teaching process is based on modern technologies, and students are provided with knowledge on the organization of technological processes, operation of equipment, and restoration methods.</p><p>The "Diffusion Metallization", "Tribotechnics", and "Tools and Equipment" laboratories operate under the department, where scientific research is conducted in the field of restoration and reliability of machine parts.</p><p>The main goal of the department is the application of innovative teaching methods, the integration of science and production, as well as the training of highly qualified engineering personnel.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'special_technologies_and_equipment';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('special_technologies_and_equipment', 1, NOW()),
    ('special_technologies_and_equipment', 2, NOW()),
    ('special_technologies_and_equipment', 3, NOW()),
    ('special_technologies_and_equipment', 4, NOW()),
    ('special_technologies_and_equipment', 5, NOW()),
    ('special_technologies_and_equipment', 6, NOW()),
    ('special_technologies_and_equipment', 7, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Maşınqayırma və xüsusi təyinatlı avadanlıqlar',   'Maşınqayırma və xüsusi təyinatlı avadanlıqların istehsal texnologiyalarının öyrədilməsi və inkişafı'),
    (2, 'Etibarlılıq və bərpa texnologiyaları',            'Maşın və mexanizmlərin etibarlılığı, təmiri və bərpası texnologiyalarının tədqiqi'),
    (3, 'Diffuziya metallaşdırma və səth mühəndisliyi',    'Diffuziya metallaşdırma və səth mühəndisliyi sahəsində elmi-tədqiqat işlərinin aparılması'),
    (4, 'Tribotexnika',                                     'Tribotexnika (sürtünmə və yeyilmə prosesləri) üzrə araşdırmalar'),
    (5, 'Avtomatlaşdırma və layihələndirmə',               'Müasir istehsalat proseslərinin layihələndirilməsi və avtomatlaşdırılması'),
    (6, 'Tədris-elm-istehsalat inteqrasiyası',             'Tədris, elm və istehsalat arasında inteqrasiyanın təmin edilməsi'),
    (7, 'Kadr hazırlığı',                                   'Sənaye və müdafiə təyinatlı sahələr üçün yüksək ixtisaslı mühəndis kadrların hazırlanması')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Machine-building and special-purpose equipment',   'Teaching and development of production technologies for machine-building and special-purpose equipment'),
    (2, 'Reliability and restoration technologies',         'Research on technologies for the reliability, repair, and restoration of machines and mechanisms'),
    (3, 'Diffusion metallization and surface engineering',  'Conducting scientific research in the field of diffusion metallization and surface engineering'),
    (4, 'Tribotechnics',                                     'Research on tribotechnics (friction and wear processes)'),
    (5, 'Automation and design',                             'Design and automation of modern production processes'),
    (6, 'Education-science-industry integration',            'Ensuring integration between education, science, and industry'),
    (7, 'Personnel training',                                'Training of highly qualified engineering personnel for industrial and defense-related fields')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'special_technologies_and_equipment',
        'Ələkbər', 'Hüseynov', 'Güləhməd oğlu',
        'yadigar.imamverdiyev@aztu.edu.az',
        '+994 50 999 75 72',
        'IV korpus, 315-ci otaq',
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
    'Texnika elmləri doktoru',
    'Professor',
    '<p>Texnika elmləri doktoru, professor Ə.G. Hüseynov Azərbaycan Texniki Universiteti nəzdində fəaliyyət göstərən Xüsusi texnologiyalar və avadanlıqlar kafedrasının rəhbəridir. O, maşınqayırma, təmir texnologiyaları və səth mühəndisliyi sahəsində tanınmış alim və mütəxəssislərdən biridir.</p><p>Ə.G. Hüseynov uzun illər elmi-pedaqoji fəaliyyətlə məşğul olmuş, ali təhsil sistemində yüksək ixtisaslı mühəndis kadrların hazırlanmasına mühüm töhfələr vermişdir. Onun elmi maraq dairəsinə maşınların etibarlılığı, hissələrin bərpası texnologiyaları, diffuziya metallaşdırma və tribotexnika sahələri daxildir.</p><p>Alim bir sıra dərslik, dərs vəsaiti və monoqrafiyaların müəllifidir. Xüsusilə "Maşınların təmir texnologiyası" dərsliyi və səth mühəndisliyi üzrə elmi əsərləri geniş istifadə olunur. Onun rəhbərliyi ilə magistr və doktorantlar hazırlanmış, müxtəlif elmi-tədqiqat işləri həyata keçirilmişdir.</p><p>Professor Ə.G. Hüseynov hazırda kafedranın elmi və tədris fəaliyyətinə rəhbərlik edir, müasir texnologiyaların tətbiqi və elm–təhsil–istehsalat əlaqələrinin inkişafı istiqamətində fəaliyyət göstərir.</p>',
    '["Maşın və mexanizmlərin etibarlılığının artırılması və texnoloji təminatı", "Maşın hissələrinin təmir və bərpa texnologiyaları", "Diffuziya metallaşdırma və səth mühəndisliyi", "Tribotexnika (sürtünmə, aşınma və yağlanma prosesləri)", "Bərpa olunmuş və möhkəmləndirilmiş səthlərin emal texnologiyaları"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Technical Sciences',
    'Professor',
    '<p>Doctor of Technical Sciences, Professor A.G. Huseynov is the head of the Department of Special Technologies and Equipment operating under Azerbaijan Technical University. He is one of the well-known scholars and specialists in the field of machine-building, repair technologies, and surface engineering.</p><p>A.G. Huseynov has been engaged in scientific-pedagogical activity for many years and has made significant contributions to the training of highly qualified engineering personnel in the higher education system. His scientific interests include machine reliability, parts restoration technologies, diffusion metallization, and tribotechnics.</p><p>He is the author of numerous textbooks, teaching aids, and monographs. In particular, his textbook "Machine Repair Technology" and his scientific works on surface engineering are widely used. Under his supervision, master''s and doctoral students have been trained, and various scientific research projects have been carried out.</p><p>Professor A.G. Huseynov currently leads the scientific and educational activities of the department and works towards the application of modern technologies and the development of science-education-industry relations.</p>',
    '["Improvement of the reliability of machines and mechanisms and their technological support", "Technologies for the repair and restoration of machine parts", "Diffusion metallization and surface engineering", "Tribotechnics (friction, wear, and lubrication processes)", "Processing technologies of restored and strengthened surfaces"]'::jsonb,
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
    SELECT id, '14:00–17:00', NOW()
    FROM cafedra_directors WHERE cafedra_code = 'special_technologies_and_equipment'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Çərşənbə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Wednesday',      NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1977', '1982', NOW() FROM cafedra_directors WHERE cafedra_code = 'special_technologies_and_equipment'
UNION ALL
SELECT id, '1983', '1987', NOW() FROM cafedra_directors WHERE cafedra_code = 'special_technologies_and_equipment'
UNION ALL
SELECT id, '2008', '2012', NOW() FROM cafedra_directors WHERE cafedra_code = 'special_technologies_and_equipment';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'special_technologies_and_equipment')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bakalavr + Magistr',                'Moskva Dövlət Aqrar Mühəndislər Universiteti'),
    (2, 'Elmlər namizədi (PhD)',             'Moskva Dövlət Aqrar Mühəndislər Universiteti'),
    (3, 'Elmlər doktoru (DSc)',              'Moskva Dövlət İnformatika və Cihazqayırma Akademiyası')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bachelor + Master',                 'Moscow State Agrarian Engineering University'),
    (2, 'Candidate of Sciences (PhD)',       'Moscow State Agrarian Engineering University'),
    (3, 'Doctor of Sciences (DSc)',          'Moscow State Academy of Informatics and Instrument-Making')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'special_technologies_and_equipment';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('special_technologies_and_equipment', 'Vaqif',   'Abbasov',    'Abbas oğlu',     'vaqif.abbasov@aztu.edu.az',     '+994 50 357 06 79', NOW()),  -- 1
    ('special_technologies_and_equipment', 'Fariz',   'Əmirov',     'Qaçay oğlu',     'fariz.amirov@aztu.edu.az',      '+994 77 317 31 79', NOW()),  -- 2
    ('special_technologies_and_equipment', 'Rasim',   'Bəşirov',    'Cavad oğlu',     'rasim_agma@aztu.edu.az',        '+994 50 212 22 73', NOW()),  -- 3
    ('special_technologies_and_equipment', 'Şövqi',   'Əsədov',     'Nayib oğlu',     'shovqi.esedov@aztu.edu.az',     '+994 50 668 29 74', NOW()),  -- 4
    ('special_technologies_and_equipment', 'Elçin',   'Rzayev',     'Davud oğlu',     'elchin_rzayev@aztu.edu.az',     '+994 55 662 88 06', NOW()),  -- 5
    ('special_technologies_and_equipment', 'Çingiz',  'Məmmədov',   'Mirzəmməd oğlu', 'cingiz.memmedov@aztu.edu.az',   '+994 51 599 93 45', NOW()),  -- 6
    ('special_technologies_and_equipment', 'Vüsal',   'Civişov',    'Faiq oğlu',      'vusal.civishov@aztu.edu.az',    '+994 55 229 95 05', NOW()),  -- 7
    ('special_technologies_and_equipment', 'Ramiz',   'Veysov',     'Əkbər oğlu',     'ramiz.veysov@aztu.edu.az',      '+994 50 330 67 77', NOW()),  -- 8
    ('special_technologies_and_equipment', 'Esmira',  'Astanova',   'Rafiq qızı',     'e.astanova@aztu.edu.az',        '+994 50 394 97 39', NOW()),  -- 9
    ('special_technologies_and_equipment', 'Teymur',  'Abdullayev', 'Qüdrət oğlu',    'teymur.abdullayev@aztu.edu.az', '+994 50 631 19 00', NOW()),  -- 10
    ('special_technologies_and_equipment', 'Azad',    'Kərimov',    'Feyruz oğlu',    'azasd.kerimov@aztu.edu.az',     '+994 50 524 57 54', NOW()),  -- 11
    ('special_technologies_and_equipment', 'Fərid',   'Hüseynli',   'Sabir oğlu',     'farid.huseynli@aztu.edu.az',    '+994 50 961 47 25', NOW())   -- 12
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının məsləhətçi-professoru', 'Professor',          't.e.d.'),
    (2,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının professoru',            'Professor',          't.e.d.'),
    (3,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının professoru',            'Professor',          't.e.d.'),
    (4,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının dosenti',               'Dosent',             't.f.d.'),
    (5,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının dosenti',               'Dosent',             't.e.n.'),
    (6,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının dosenti',               'Dosent',             't.f.d.'),
    (7,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının dosenti',               'Dosent',             't.f.d.'),
    (8,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının baş müəllimi',          NULL::varchar,        NULL::varchar),
    (9,  'Xüsusi texnologiyalar və avadanlıqlar kafedrasının baş müəllimi',          NULL,                 NULL),
    (10, 'Xüsusi texnologiyalar və avadanlıqlar kafedrasının baş müəllimi',          NULL,                 NULL),
    (11, 'Xüsusi texnologiyalar və avadanlıqlar kafedrasının assistenti',            NULL,                 NULL),
    (12, 'Xüsusi texnologiyalar və avadanlıqlar kafedrasının assistenti',            NULL,                 NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Consultant-Professor at the Department of Special Technologies and Equipment', 'Professor',           'Doctor of Technical Sciences'),
    (2,  'Professor at the Department of Special Technologies and Equipment',            'Professor',           'Doctor of Technical Sciences'),
    (3,  'Professor at the Department of Special Technologies and Equipment',            'Professor',           'Doctor of Technical Sciences'),
    (4,  'Associate Professor at the Department of Special Technologies and Equipment',  'Associate Professor', 'PhD in Technical Sciences'),
    (5,  'Associate Professor at the Department of Special Technologies and Equipment',  'Associate Professor', 'Candidate of Technical Sciences'),
    (6,  'Associate Professor at the Department of Special Technologies and Equipment',  'Associate Professor', 'PhD in Technical Sciences'),
    (7,  'Associate Professor at the Department of Special Technologies and Equipment',  'Associate Professor', 'PhD in Technical Sciences'),
    (8,  'Senior Lecturer at the Department of Special Technologies and Equipment',      NULL::varchar,         NULL::varchar),
    (9,  'Senior Lecturer at the Department of Special Technologies and Equipment',      NULL,                  NULL),
    (10, 'Senior Lecturer at the Department of Special Technologies and Equipment',      NULL,                  NULL),
    (11, 'Assistant at the Department of Special Technologies and Equipment',            NULL,                  NULL),
    (12, 'Assistant at the Department of Special Technologies and Equipment',            NULL,                  NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
