-- ============================================================
-- "Humanitar fənlər" kafedrası — Full DB Import
-- cafedra_code: 'humanities'
-- faculty_code: '257378'
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
    '257378',
    'humanities',
    0, 0, 0, 5, 0, 0, 3,
    '[4, 16, 17]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'humanities',
    'az',
    'Humanitar fənlər kafedrası',
    '<p>Humanitar fənlər kafedrası Azərbaycan Texniki Universiteti (AzTU) Elmi Şurasının 03 fevral 2021-ci il tarixli qərarı ilə Azərbaycan dili və pedaqogika və İctimai fənlər kafedralarının birləşdirilməsi əsasında bu iki kafedranın bazasında yaradılmışdır. Kafedra humanitar yönümlü fəaliyyət istiqamətində təhsil və elmi-tədqiqat üzrə əhəmiyyətli töhfə verməyi qarşısına məqsəd qoymuşdur.</p><p>Kafedranın missiyası innovativ və kreativ düşüncəyə malik, analitik bacarıqları inkişaf etmiş, müasir tələblərə uyğun effektiv həllər təqdim edə bilən yüksək ixtisaslı mütəxəssislərin hazırlanmasına köməklik göstərməkdir.</p><p>Kafedra ümumuniversitet kafedrası olaraq bütün fakültələrin tədris prosesində iştirak edir və kafedranın tərkibinə daxil olan fənlər universitet üzrə hazırlanan bütün ixtisaslarda tədris olunur.</p>',
    NOW()
),
(
    'humanities',
    'en',
    'Department of Humanities',
    '<p>The Department of Humanities was established on the basis of the merger of the Departments of Azerbaijani Language and Pedagogy and Social Sciences by the decision of the Scientific Council of Azerbaijan Technical University (AzTU) dated February 03, 2021. The Department aims to make a significant contribution to education and scientific research in the direction of humanitarian activities.</p><p>The mission of the Department is to assist in the preparation of highly qualified specialists with innovative and creative thinking, developed analytical skills, and able to provide effective solutions in accordance with modern requirements.</p><p>As a university-wide department, the Department participates in the educational process of all faculties and the subjects included in the Department are taught in all specialties prepared at the University.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'humanities';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('humanities', 1, NOW()),
    ('humanities', 2, NOW()),
    ('humanities', 3, NOW()),
    ('humanities', 4, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Müasir tədris proqramları',                'İxtisaslar üzrə müasir və beynəlxalq standartlara uyğun tədris proqramlarının hazırlanması və tətbiqi.'),
    (2, 'Vətəndaş və şəxsiyyət formalaşdırılması', 'Azərbaycan xalqı və dövləti qarşısında öz məsuliyyətini dərk edən, müstəqil və yaradıcı düşünən, milli-mənəvi və ümumbəşəri dəyərləri qoruyan və inkişaf etdirən vətəndaşların yetişdirilməsi.'),
    (3, 'Mütəxəssis hazırlığı və əməkdaşlıq',      'Sənaye və dövlət qurumları ilə əməkdaşlıq çərçivəsində təşəbbüsləri və yenilikləri qiymətləndirməyi bacaran, nəzəri və praktiki biliklərə malik mütəxəssislərin hazırlanması.'),
    (4, 'Milli təhlükəsizlik yönümlü tədqiqatlar',  'Kafedranın profilinə uyğun olaraq ölkənin milli təhlükəsizliyinin təmin edilməsi məqsədilə vətəndaş yetişdirilməsi istiqamətində elmi tədqiqatların aparılması.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Modern curricula',                         'Preparation and implementation of educational programs in accordance with modern and international standards in specialties.'),
    (2, 'Formation of citizens and personalities', 'Education of citizens who understand their responsibility to the people and state of Azerbaijan, think independently and creatively, and protect national-spiritual values.'),
    (3, 'Specialist training and cooperation',     'Preparation of specialists who are able to evaluate initiatives and innovations within the framework of cooperation with industry and state institutions.'),
    (4, 'Security-oriented research',               'Conducting scientific research in the direction of educating citizens in order to ensure the national security of the country.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'humanities',
        'Həbib', 'Mirzəyev', 'Adil oğlu',
        'habib.mirzayev@aztu.edu.az',
        '+994 50 523 14 18',
        'II korpus, K318-ci otaq',
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
    'Filologiya üzrə fəlsəfə doktoru',
    'Dosent',
    '<p>Həbib Adil oğlu Mirzəyev — filologiya üzrə fəlsəfə doktoru, dosent, filologiya sahəsi üzrə ixtisaslaşmış alimdir. O, mövcud bütün ixtisaslar istiqamətində elmi-pedaqoji fəaliyyət göstərir.</p><p>Onun elmi tədqiqatlarının əsas istiqamətlərinə Azərbaycan dili və ədəbiyyatı, ictimai və pedaqoji istiqamətlər daxildir. Bu sahələr üzrə apardığı tədqiqatların nəticələri nüfuzlu elmi jurnallarda dərc olunmuş və humanitar sahənin inkişafına mühüm töhfə vermişdir.</p><p>H.A.Mirzəyev pedaqoji fəaliyyətində müasir interaktiv təlim metodlarını tətbiq edərək Azərbaycan xalqı və dövləti qarşısında öz məsuliyyətini dərk edən, azad, müstəqil və yaradıcı düşünən, geniş dünyagörüşünə malik gənc mütəxəssislərin hazırlanmasına xüsusi önəm verir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin Humanitar fənlər kafedrasının müdiri vəzifəsində çalışır. O, 200-ə qədər elmi məqalənin və 9 kitabın müəllifidir.</p>',
    '["Azərbaycan dili", "Dilçilik və terminologiya", "Dil və üslubiyyat", "Dil və janr məsələri"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Philosophy in Philology',
    'Associate Professor',
    '<p>Habib Adil oglu Mirzayev is a doctor of philosophy in philology, associate professor, a scientist specializing in philology. He carries out scientific and pedagogical activities in all specialties.</p><p>The main directions of his scientific research include Azerbaijani language and literature, sociological and pedagogical directions. The results of his research in these areas have been published in prestigious scientific journals and have made a significant contribution to the development of the humanitarian field.</p><p>Applying modern interactive teaching methods in his pedagogical activity, H.A. Mirzayev attaches special importance to the preparation of young specialists who understand their responsibility to the people and state of Azerbaijan, think freely, independently and creatively.</p><p>Currently, he works as the head of the Department of Humanitarian Sciences at Azerbaijan Technical University. He is the author of up to 200 scientific articles and 9 books.</p>',
    '["Azerbaijani language", "Linguistics and terminology", "Language and stylistics", "Language and genre issues"]'::jsonb,
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
    FROM cafedra_directors WHERE cafedra_code = 'humanities'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Çərşənbə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Wednesday',         NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1980', '1984', NOW() FROM cafedra_directors WHERE cafedra_code = 'humanities'
UNION ALL
SELECT id, '1997', '2001', NOW() FROM cafedra_directors WHERE cafedra_code = 'humanities'
UNION ALL
SELECT id, '2012', '2012', NOW() FROM cafedra_directors WHERE cafedra_code = 'humanities';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'humanities')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Ali təhsil',                                  'Azərbaycan Dövlət Pedaqoji Universiteti'),
    (2, 'Elmlər namizədi (PhD)',                       'AMEA Nəsimi adına Dilçilik İnstitutu'),
    (3, 'Elmlər doktoru (DSc)',                        'AMEA Nəsimi adına Dilçilik İnstitutu')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Higher Education',                            'Azerbaijan State Pedagogical University'),
    (2, 'Candidate of Sciences (PhD)',                 'Nasimi Institute of Linguistics, ANAS'),
    (3, 'Doctor of Sciences (DSc)',                    'Nasimi Institute of Linguistics, ANAS')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'humanities';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('humanities', 'Qabil',      'Hüseynov',      'İsmixan oğlu',  'qabil.hüseynov@aztu.edu.az',      '+994 50 312 46 50', NOW()),  -- 1
    ('humanities', 'Əyyub',      'Kərimov',       'Sevdim oğlu',   'eyyub.kerimov@aztu.edu.az',       '+994 50 317 01 49', NOW()),  -- 2
    ('humanities', 'Akif',       'Nağı',          'Qazax oğlu',    'nagi.akif@aztu.edu.az',           '+994 77 315 22 78', NOW()),  -- 3
    ('humanities', 'Gülşən',     'Rzayeva',       'Fikrət qızı',   'gulshen.rzayeva@aztu.edu.az',     '+994 55 997 62 82', NOW()),  -- 4
    ('humanities', 'İsrail',     'Məhərrəmov',    'Bəhram oğlu',   'israil.meherremov@aztu.edu.az',    '+994 50 520 70 14', NOW()),  -- 5
    ('humanities', 'Afaq',       'Zeynalova',     'Məmməd',        'afaq.zeynalova@aztu.edu.az',      '+994 50 704 77 15', NOW()),  -- 6
    ('humanities', 'İsmayıl',    'İsmayılov',     'Yolçu oğlu',    'ismayil.ismayilov@aztu.edu.az',    '+994 50 318 18 10', NOW()),  -- 7
    ('humanities', 'Nailə',      'Şirinova',      'Fuad qızı',     'naile.shirinova@aztu.edu.az',     '+994 55 607 87 31', NOW()),  -- 8
    ('humanities', 'Lalə',       'Piriyeva',      'Zakir qızı',    'lale.piriyeva@aztu.edu.az',       '+994 50 892 44 20', NOW()),  -- 9
    ('humanities', 'Aynur',      'Fərəcova',      'Aydın qızı',    'aynur.ferecova@aztu.edu.az',      '+994 50 305 00 03', NOW()),  -- 10
    ('humanities', 'Nərminə',    'İsayeva',       'Şüa qızı',      'narmina.isayeva@aztu.edu.az',     '+994 50 321 10 89', NOW()),  -- 11
    ('humanities', 'Şəfiqə',     'Məhərrəmova',   'Mütəllim qızı', 'shafiga.meherremova@aztu.edu.az',  '+994 50 577 48 98', NOW()),  -- 12
    ('humanities', 'Pərvin',     'Abdullabəyova', 'Yaqub qızı',    'pervin.abdullabeyova@aztu.edu.az', '+994 50 680 98 38', NOW()),  -- 13
    ('humanities', 'Vüsalə',     'Cəfər-zadə',    'Nofəl qızı',    'vusale.jafar-zade@aztu.edu.az',   '+994 55 512 38 90', NOW()),  -- 14
    ('humanities', 'Güntəkin',   'Musayeva',      'Qəzənfər qızı', 'guntekin.musayeva@aztu.edu.az',    '+994 55 208 42 45', NOW()),  -- 15
    ('humanities', 'Arzu',       'Xəlilzadə',     'Cahid qızı',    'arzuxelilzade89@gmail.com',       '+994 70 509 56 59', NOW()),  -- 16
    ('humanities', 'Sonaxanım',  'İmamova',       'Qurban qızı',   'sonaxanim.imamova@aztu.edu.az',   '+994 50 442 96 71', NOW()),  -- 17
    ('humanities', 'Zarina',     'Tağıyeva',      'Lukyanova',     'zarina.tagiyeva@aztu.edu.az',     '+994 55 741 39 21', NOW()),  -- 18
    ('humanities', 'Zeynəb',     'Məmmədzadə',    'Sərxan qızı',   'zeyneb.memmedzade@aztu.edu.az',   '+994 51 725 79 06', NOW()),  -- 19
    ('humanities', 'Günəş',      'Nuriyeva',      'Nizami qızı',   'gunesh.nuriyeva@aztu.edu.az',     '+994 50 821 98 21', NOW()),  -- 20
    ('humanities', 'Rəna',       'Nəcəfova',      'Həsənağa qızı', 'rena.nacafova@aztu.edu.az',       '+994 55 278 90 72', NOW()),  -- 21
    ('humanities', 'Nurdan',     'Əsədova',       'Rufulla qızı',  'nurdan.asadov@aztu.edu.az',       '+994 51 430 60 24', NOW()),  -- 22
    ('humanities', 'Xuraman',    'Qurbanova',     'Fəxrəddin qızı','khuraman.gurbanova@aztu.edu.az',  '+994 50 346 05 25', NOW())   -- 23
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Humanitar fənlər kafedrasının professoru',   'Professor', 'Fəlsəfə elmləri doktoru'),
    (2,  'Humanitar fənlər kafedrasının professoru',   'Professor', 'Fəlsəfə elmləri doktoru'),
    (3,  'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Tarix üzrə fəlsəfə doktoru'),
    (4,  'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (5,  'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Tarix üzrə fəlsəfə doktoru'),
    (6,  'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (7,  'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (8,  'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Fəlsəfə üzrə fəlsəfə doktoru'),
    (9,  'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (10, 'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (11, 'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (12, 'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (13, 'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (14, 'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (15, 'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Filologiya üzrə fəlsəfə doktoru'),
    (16, 'Humanitar fənlər kafedrasının dosenti',    'Dosent',    'Tarix üzrə fəlsəfə doktoru'),
    (17, 'Humanitar fənlər kafedrasının baş müəllimi', NULL,       NULL),
    (18, 'Humanitar fənlər kafedrasının baş müəllimi', NULL,       NULL),
    (19, 'Humanitar fənlər kafedrasının baş müəllimi', NULL,       NULL),
    (20, 'Humanitar fənlər kafedrasının baş müəllimi', NULL,       'doktorant'),
    (21, 'Humanitar fənlər kafedrasının müəllimi',     NULL,       'doktorant'),
    (22, 'Humanitar fənlər kafedrasının müəllimi',     NULL,       'doktorant'),
    (23, 'Humanitar fənlər kafedrasının kargüzarı',    NULL,       'doktorant')
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Professor of the Department of Humanities',          'Professor',           'Doctor of Philosophy'),
    (2,  'Professor of the Department of Humanities',          'Professor',           'Doctor of Philosophy'),
    (3,  'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in History'),
    (4,  'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (5,  'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in History'),
    (6,  'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (7,  'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (8,  'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philosophy'),
    (9,  'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (10, 'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (11, 'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (12, 'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (13, 'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (14, 'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (15, 'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in Philology'),
    (16, 'Associate Professor of the Department of Humanities','Associate Professor', 'PhD in History'),
    (17, 'Head teacher of the Department of Humanities',       NULL,                  NULL),
    (18, 'Head teacher of the Department of Humanities',       NULL,                  NULL),
    (19, 'Senior lecturer of the Department of Humanities',    NULL,                  NULL),
    (20, 'Senior Lecturer of the Department of Humanities',    NULL,                  'PhD student'),
    (21, 'Lecturer of the Department of Humanities',           NULL,                  'PhD student'),
    (22, 'Lecturer of the Department of Humanities',           NULL,                  'PhD student'),
    (23, 'Clerk of the Department of Humanities',              NULL,                  'PhD student')
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
