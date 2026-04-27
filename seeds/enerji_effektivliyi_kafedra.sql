-- ============================================================
-- "Enerji effektivliyi və yaşıl enerji texnologiyaları" kafedrası — Full DB Import
-- cafedra_code: 'energy-efficiency'
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
    'energy-efficiency',
    3, 3, 2, 4, 6, 15, 7,
    '[7, 11, 13]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'energy-efficiency',
    'az',
    'Enerji effektivliyi və yaşıl enerji texnologiyaları kafedrası',
    '<p>Enerji effektivliyi və yaşıl enerji texnologiyaları kafedrası Azərbaycan Texniki Universitetinin (AzTU) Elmi Şurasının 09 fevral 2021-ci il tarixli qərarı ilə Hidravlika və istilik texnikası və Elektroenergetika və Elektrik Təchizatı Sistemləri kafedralarının birləşməsi əsasında yaradılmışdır.</p><p>Kafedranın strateji məqsədi enerji səmərəliliyi, bərpa olunan enerji mənbələri və dayanıqlı enerji texnologiyaları sahəsində yüksək səviyyəli təhsil və elmi-tədqiqat fəaliyyətinin həyata keçirilməsini təmin etməkdir. Dayanıqlı enerji sistemlərinin inkişafına töhfə verən yüksək ixtisaslı mütəxəssislərin hazırlanması əsas prioritet istiqamətlərdən biridir.</p>',
    NOW()
),
(
    'energy-efficiency',
    'en',
    'Department of Energy Efficiency and Green Energy Technologies',
    '<p>The Department of Energy Efficiency and Green Energy Technologies was established by the decision of the Scientific Council of Azerbaijan Technical University (AzTU) on February 9, 2021, through the merger of the Departments of Hydraulics and Heat Engineering and Electric Power Engineering and Power Supply Systems.</p><p>The strategic goal of the department is to ensure high-level education and scientific research activities in the field of energy efficiency, renewable energy sources, and sustainable energy technologies. The preparation of highly qualified specialists contributing to the development of sustainable energy systems is defined as one of the main priority areas.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'energy-efficiency';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('energy-efficiency', 1, NOW()),
    ('energy-efficiency', 2, NOW()),
    ('energy-efficiency', 3, NOW()),
    ('energy-efficiency', 4, NOW()),
    ('energy-efficiency', 5, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Tədris Prosesinin Təşkili', 'Bakalavr, magistr və doktorantların hazırlanması istiqamətində müasir tədris prosesini təşkil etmək.'),
    (2, 'Elmi-Tədqiqat Fəaliyyəti',  'Enerji səmərəliliyi və yaşıl texnologiyalar sahəsində aktual elmi araşdırmaların aparılması.'),
    (3, 'Metodik Təminat',           'Tədris olunan fənlər üzrə müasir tələblərə cavab verən proqram və vəsaitlərin hazırlanması.'),
    (4, 'Təcrübələrin Təşkili',      'İstehsalat və elmi-pedaqoji təcrübələrin yüksək səviyyədə təşkilini təmin etmək.'),
    (5, 'İdarəetmə və İnnovasiya',   'Effektiv idarəetməni və təhsildə yeni texnologiyaların tətbiqini rəhbər tutmaq.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Organization of Teaching',   'Organizing a modern educational process for the preparation of bachelors, masters, and PhD students.'),
    (2, 'Scientific Research',        'Conducting relevant scientific research in the field of energy efficiency and green technologies.'),
    (3, 'Methodological Support',     'Preparation of programs and manuals that meet modern requirements for the subjects taught.'),
    (4, 'Organization of Internship', 'Ensuring the organization of high-level industrial and scientific-pedagogical internships.'),
    (5, 'Management and Innovation',  'Guiding effective management and the application of new technologies in education.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'energy-efficiency',
        'Vaqif', 'Həsənov', 'Hajan oğlu',
        'vagif.hasanov@aztu.edu.az',
        '+994 12 539 14 32',
        'V korpus, 303-cü otaq',
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
    '<p>Həsənov Vaqif Hajan oğlu — texnika elmləri doktoru, professor istilik texnikasının nəzəri əsasları və istilik energetikası sahəsi üzrə ixtisaslaşmış alimdir. O, yaşıl enerji texnologiyaları, istilik texnikası, termodinamika və istilik energetikası istiqamətində elmi və pedaqoji fəaliyyət göstərir.</p><p>O, 250-dən çox elmi əsərin, o cümlədən 16 kitabın və dərs vəsaitinin, 2 monoqrafiyanın və 3 ixtiranın müəllifidir. 2019-cu ildən AAK-ın Texnika elmləri bölməsi üzrə Ekspert şurasının üzvüdür.</p>',
    '["İstilik texnikasının nəzəri əsasları", "İstilik energetikası", "Maddənin hal tənlikləri və faza keçidləri", "Enerji effektivliyi və texnoloji yeniliklər", "Mayelərin istili-fiziki xassələrinin tədqiqi"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Technical Sciences',
    'Professor',
    '<p>Vagif Hajan oglu Hasanov is a doctor of technical sciences and a professor specializing in the theoretical foundations of heat engineering and heat power engineering. He conducts scientific and pedagogical activities in green energy technologies, heat engineering, thermodynamics, and heat power engineering.</p><p>He is the author of more than 250 scientific works, including 16 books and manuals, 2 monographs, and 3 inventions. Since 2019, he has been a member of the Expert Council on Technical Sciences of the Higher Attestation Commission.</p>',
    '["Theoretical foundations of heat engineering", "Heat power engineering", "Equations of state and phase transitions", "Energy efficiency and technological innovations", "Study of thermo-physical properties of fluids"]'::jsonb,
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
    SELECT id, '09:00–17:30', NOW() FROM cafedra_directors WHERE cafedra_code = 'energy-efficiency'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi - Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday - Friday',     NOW() FROM wh_insert;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1981', '1986', NOW() FROM cafedra_directors WHERE cafedra_code = 'energy-efficiency'
UNION ALL
SELECT id, '1992', '1994', NOW() FROM cafedra_directors WHERE cafedra_code = 'energy-efficiency'
UNION ALL
SELECT id, '2014', '2014', NOW() FROM cafedra_directors WHERE cafedra_code = 'energy-efficiency';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'energy-efficiency')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Ali təhsil (Bakalavr + Magistr)', 'Azərbaycan Texniki Universiteti'),
    (2, 'Elmlər namizədi (PhD)',           'Azərbaycan Texniki Universiteti'),
    (3, 'Elmlər doktoru (DSc)',            'Azərbaycan Texniki Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Higher Education (Bachelor + Master)', 'Azerbaijan Technical University'),
    (2, 'Candidate of Sciences (PhD)',          'Azerbaijan Technical University'),
    (3, 'Doctor of Sciences (DSc)',             'Azerbaijan Technical University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'energy-efficiency';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('energy-efficiency', 'Nurəli',    'Yusifbəyli',  'Adil oğlu',     'nuraliyusifbeyli@aztu.edu.az',  NULL,                NOW()),
    ('energy-efficiency', 'Misirxan',  'Talıbov',     'Atduxan oğlu',  'misirxan.talibov@aztu.edu.az',   '+994 50 345 16 28', NOW()),
    ('energy-efficiency', 'Aydın',     'Muradəliyev', 'Zurab oğlu',    'aydinmuradaliyev@aztu.edu.az',  '+994 50 680 40 93', NOW()),
    ('energy-efficiency', 'Fuad',      'Məmmədov',    'Faiq oğlu',     'fuad.memmedov@aztu.edu.az',     '+994 50 525 69 90', NOW()),
    ('energy-efficiency', 'Adilə',     'Zeynalova',   'Bala-Ağa qızı', 'adile.zeynalova@aztu.edu.az',   '+994 50 320 92 38', NOW()),
    ('energy-efficiency', 'Rəna',      'Həmidova',    'Fəxrəddin qızı','rena81.qamidova@aztu.edu.az',   '+994 50 284 47 17', NOW()),
    ('energy-efficiency', 'Esmira',    'Məmmədova',   'Adil qızı',     'esmira.mammadova@aztu.edu.az',  '+994 77 317 71 28', NOW()),
    ('energy-efficiency', 'Naib',      'Hacıyev',     'İsmixan oğlu',  'naib.haciyev@aztu.edu.az',      '+994 55 662 12 55', NOW()),
    ('energy-efficiency', 'Validə',    'Mahmudova',   'Xankişi qızı',  'valida.mahmudova@aztu.edu.az',  '+994 70 585 10 05', NOW()),
    ('energy-efficiency', 'Aynur',     'Nəbiyeva',    'Xəlil qızı',    'aynur.nabiyeva@aztu.edu.az',    '+994 70 303 41 43', NOW()),
    ('energy-efficiency', 'Əhməd',     'Müslümov',    'Habil oğlu',    'ahmad.muslum@aztu.edu.az',     '+994 50 337 87 64', NOW()),
    ('energy-efficiency', 'Asif',      'Sadıqov',     'Bəhman oğlu',   'asif14.sadiq@aztu.edu.az',      '+994 55 225 57 48', NOW()),
    ('energy-efficiency', 'Ülviyyə',   'Nəsibova',    'Adil qızı',     'ulviyye.nasibova@aztu.edu.az',  '+994 70 614 14 78', NOW()),
    ('energy-efficiency', 'Ülkər',     'Əkbərova',    'Mübariz',       'ulker.ekberova@aztu.edu.az',    '+994 50 641 52 17', NOW()),
    ('energy-efficiency', 'Murad',     'Rzayev',      'Ağayar oğlu',   'murad.rzayev@aztu.edu.az',      '+994 50 707 97 81', NOW()),
    ('energy-efficiency', 'Movlanə',   'Ələkbərova',  'Şiraslan qızı', 'movlane.alakbarova@aztu.edu.az', NULL,                NOW()),
    ('energy-efficiency', 'Sevinc',    'Səfərova',    'Ədalət qızı',   'sevinc.seferova@aztu.edu.az',   NULL,                NOW()),
    ('energy-efficiency', 'Şəfəq',     'İbrahimova',  'Aqil',          'shafag.ibrahimova@aztu.edu.az', '+994 50 477 32 47', NOW()),
    ('energy-efficiency', 'Afilə',     'Əhmədova',    'Nuşravan qızı', 'ehmedova.afile@aztu.edu.az',    '+994 55 974 25 35', NOW())
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Kafedranın professoru', 'Professor', 't.e.d.'),
    (2,  'Kafedranın professoru', 'Professor', 't.e.d.'),
    (3,  'Kafedranın professoru', 'Professor', 't.e.d.'),
    (4,  'Kafedranın professoru', 'Professor', 't.e.d.'),
    (5,  'Kafedranın dosenti',    'Dosent',    't.e.n.'),
    (6,  'Kafedranın dosenti',    'Dosent',    't.e.n.'),
    (7,  'Kafedranın dosenti',    'Dosent',    't.e.n.'),
    (8,  'Kafedranın dosenti',    'Dosent',    't.e.n.'),
    (9,  'Kafedranın dosenti',    'Dosent',    't.e.n.'),
    (10, 'Kafedranın baş müəllimi', NULL,      NULL),
    (11, 'Kafedranın baş müəllimi', NULL,      NULL),
    (12, 'Kafedranın baş müəllimi', NULL,      NULL),
    (13, 'Kafedranın baş müəllimi', NULL,      NULL),
    (14, 'Kafedranın assistenti',  NULL,      NULL),
    (15, 'Kafedranın assistenti',  NULL,      NULL),
    (16, 'Kafedranın müəllim köməkçisi', NULL, NULL),
    (17, 'Kafedranın müəllim köməkçisi', NULL, NULL),
    (18, 'Kafedranın müəllim köməkçisi', NULL, NULL),
    (19, 'Kafedranın kargüzarı',   NULL,      NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Professor of Department',           'Professor',           'DSc in Technical Sciences'),
    (2,  'Professor of Department',           'Professor',           'DSc in Technical Sciences'),
    (3,  'Professor of Department',           'Professor',           'DSc in Technical Sciences'),
    (4,  'Professor of Department',           'Professor',           'DSc in Technical Sciences'),
    (5,  'Associate Professor of Department', 'Associate Professor', 'PhD in Technical Sciences'),
    (6,  'Associate Professor of Department', 'Associate Professor', 'PhD in Technical Sciences'),
    (7,  'Associate Professor of Department', 'Associate Professor', 'PhD in Technical Sciences'),
    (8,  'Associate Professor of Department', 'Associate Professor', 'PhD in Technical Sciences'),
    (9,  'Associate Professor of Department', 'Associate Professor', 'PhD in Technical Sciences'),
    (10, 'Senior Lecturer of Department',     NULL,                  NULL),
    (11, 'Senior Lecturer of Department',     NULL,                  NULL),
    (12, 'Senior Lecturer of Department',     NULL,                  NULL),
    (13, 'Senior Lecturer of Department',     NULL,                  NULL),
    (14, 'Assistant of Department',           NULL,                  NULL),
    (15, 'Assistant of Department',           NULL,                  NULL),
    (16, 'Teacher Assistant of Department',    NULL,                  NULL),
    (17, 'Teacher Assistant of Department',    NULL,                  NULL),
    (18, 'Teacher Assistant of Department',    NULL,                  NULL),
    (19, 'Clerk of Department',               NULL,                  NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
