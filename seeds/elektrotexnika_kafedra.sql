-- ============================================================
-- "Elektrotexnika və elektrik avadanlığı" kafedrası — Full DB Import
-- cafedra_code: 'electrical-engineering'
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
    'electrical-engineering',
    2, 2, 1, 3, 5, 10, 5,
    '[7, 9, 12]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'electrical-engineering',
    'az',
    'Elektrotexnika və elektrik avadanlığı kafedrası',
    '<p>“Elektrotexnika” kafedrası ali təhsilin bakalavriat və magistratura pillələrində “Elektrik mühəndisliyi” və “Elektrik və elektronika mühəndisliyi” ixtisasları üzrə əsas aparıcı ixtisas kafedrasıdır.</p><p>Kafedra, müasir sənayenin ehtiyacı olan yüksək ixtisaslı mütəxəssislərin hazırlanması üçün bir çox sahələri əhatə edən çoxsaylı müxtəlif fənnlərin tədrisini həyata keçirir. Kafedranın tədris etdiyi fənlər, yüksək ixtisaslı mütəxəssislər tərəfindən azərbaycan, rus və ingilis dillərində tədris olunur.</p><p>Tədris olunan fənlər üzrə tədrisin keyfiyyətini artırmaq, tədris prossesinin səmərəliliyini yüksəltmək, o cümlədən, tələbələrimizin müxtəlif sahələr üzrə nəzəri biliklərlə yanaşı, həm də təcrübi vərdişlərini artırmaq məqsədi ilə mütəmadi olaraq Azərenerji ASC, Azərişıq ASC, Bakımetropoliteni QSC –nin Tədris Mərkəzlərində dual təlim aparılır.</p>',
    NOW()
),
(
    'electrical-engineering',
    'en',
    'Department of Electrical Engineering and Electrical Equipment',
    '<p>The "Electrical Engineering" department is the main leading specialty department for "Electrical Engineering" and "Electrical and Electronics Engineering" specialties at the undergraduate and graduate levels of higher education.</p><p>The department provides teaching of numerous various subjects covering many fields for the preparation of highly qualified specialists needed by modern industry. The subjects are taught by highly qualified specialists in Azerbaijani, Russian, and English languages.</p><p>In order to increase the quality of teaching and practical skills, dual training is regularly conducted at the Training Centers of Azerenerji OJSC, Azerishig OJSC, and Baku Metro CJSC, allowing students to apply theoretical knowledge in real production conditions.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'electrical-engineering';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('electrical-engineering', 1, NOW()),
    ('electrical-engineering', 2, NOW()),
    ('electrical-engineering', 3, NOW()),
    ('electrical-engineering', 4, NOW()),
    ('electrical-engineering', 5, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Tədris Prosesinin Təşkili', 'Müvaviq ixtisas və ixtisaslaşmalar üzrə bakalavr, magistr, doktorantların hazırlanması istiqamətində tədris prosesini təşkil etmək.'),
    (2, 'Elmi Araşdırmalar',           'Aktual elmi araşdırmaların aparılması və müasir tətəblərə cavab verən yüksək ixtisaslı kadrların hazırlanması.'),
    (3, 'Tədris-Metodiki İşlər',     'Tədris-metodiki ədəbiyyatların, o cümlədən, elektron dərsliklərin hazırlanmasını həyata keçirmək.'),
    (4, 'Təcrübələrin Təşkili',       'Bakalavriat səviyyəsində istehsalat, magistr səviyyəsində isə elmi tədqiqat və elmi-pedaqoji təcrübələrin təşkili.'),
    (5, 'İnnovativ Struktur',        'Kafedra daxilində yenilikçi (innovativ) strukturların yaradılmasına köməklik etmək.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Organization of Teaching',   'Organizing the educational process for the preparation of bachelors, masters, and PhD students in relevant specialties.'),
    (2, 'Scientific Research',        'Conducting relevant scientific research and preparing highly qualified personnel who meet modern requirements.'),
    (3, 'Methodological Work',        'Preparation of teaching-methodological literature, including electronic textbooks.'),
    (4, 'Organization of Internship', 'Organizing industrial internships at the undergraduate level, and research and pedagogical internships at the graduate level.'),
    (5, 'Innovative Structure',       'Assisting in the creation of innovative structures within the department.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'electrical-engineering',
        'Hikmət', 'Əliyev', 'Səxavəddin oğlu',
        'hikmetaliyev@aztu.edu.az',
        '+994 050 668 10 60',
        'IV korpus, otaq 309',
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
    'Fizika-riyaziyyat elmləri namizədi, Əməkdar mühəndis',
    'Dosent',
    '<p>Hikmət Səxavəddin oğlu Əliyev 1964-cü ildə Kürdəmir rayonunda anadan olub. 1989-cu ildə AzPİ-ni bitirib və ”mühəndis-elektrik“ ixtisasına yiyələnib.</p><p>1995-ci ildə Azərbaycan Elmlər Akademiyasının Fizika İnstitutunda namizədlik dissertasiyası müdafiə edərək fizika riyaziyyat elmləri namizədi alimlik dərəcəsini alıb. 2004-2008-ci illərdə “Elektrotexnika və Energetika” fakültəsinin dekanı vəzifəsində çalışıb.</p><p>2019-cu ilin oktyabr ayından “Elektrotexnika və elektrik avadanlığı” kafedrasının müdiri seçilib. 100-dən çox elmi əsərin müəllifidir. 2020-ci ildə “Əməkdar mühəndis” fəxri adı verilmişdir.</p>',
    '["Elektrotexnika", "Elektronika", "Yarımkeçiricilər və dielektriklər fizikası", "Yeni nəsil elektrotrxniki təyinatlı kompozisiya materiallarının işlənməsi", "Elektroenergetika", "Güc elektronikası", "Elektrik avadanlıqlarının sınaq və diaqnostikası"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'PhD in Physics and Mathematics, Honored Engineer',
    'Associate Professor',
    '<p>Hikmat Sakhavaddin oglu Aliyev was born in 1964. He graduated from AzPI in 1989 as an electrical engineer. He received his PhD from the Institute of Physics of the Azerbaijan Academy of Sciences in 1995.</p><p>He served as the Dean of the "Electrical Engineering and Energy" faculty from 2004-2008. Since 2019, he has been the head of the "Electrical Engineering and Electrical Equipment" department.</p><p>He is the author of more than 100 scientific works and was awarded the title of "Honored Engineer" in 2020 for his contributions to engineering education and development.</p>',
    '["Electrical Engineering", "Electronics", "Physics of Semiconductors and Dielectrics", "Development of New Generation Composite Materials", "Electric Power Engineering", "Power Electronics", "Testing and Diagnostics of Electrical Equipment"]'::jsonb,
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
    SELECT id, '12:00-13:00', NOW() FROM cafedra_directors WHERE cafedra_code = 'electrical-engineering'
    UNION ALL
    SELECT id, '14:00-15:00', NOW() FROM cafedra_directors WHERE cafedra_code = 'electrical-engineering'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', day_az, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM wh_insert
) w JOIN (
    VALUES (1, 'Bazar ertəsi, Cümə axşamı'), (2, 'Çərşənbə axşamı, Çərşənbə, Cümə')
) v(row_num, day_az) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', day_en, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM wh_insert
) w JOIN (
    VALUES (1, 'Monday, Thursday'), (2, 'Tuesday, Wednesday, Friday')
) v(row_num, day_en) ON w.row_num = v.row_num;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1982', '1989', NOW() FROM cafedra_directors WHERE cafedra_code = 'electrical-engineering'
UNION ALL
SELECT id, '1992', '1995', NOW() FROM cafedra_directors WHERE cafedra_code = 'electrical-engineering';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'electrical-engineering')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Ali təhsil (Bakalavr + Magistr)', 'Azərbaycan Texniki Universiteti'),
    (2, 'Elmlər namizədi (PhD)',           'AMEA Fizika İnstitutu')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Higher Education (Bachelor + Master)', 'Azerbaijan Technical University'),
    (2, 'Candidate of Sciences (PhD)',          'Institute of Physics, ANAS')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'electrical-engineering';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('electrical-engineering', 'Əyyar',     'Məmmədov',    'Təyyar oğlu',   'eyyar.memmedov@aztu.edu.az',  '+994 50 486 50 58', NOW()),
    ('electrical-engineering', 'Vasif',     'Neymətov',    'Aydın oğlu',    'vasif.neymatov@aztu.edu.az',  '+994 55 744 78 78', NOW()),
    ('electrical-engineering', 'Mehdi',     'Camalov',     'Əvəz oğlu',     'mehticamal@aztu.edu.az',      '+994 77 739 36 37', NOW()),
    ('electrical-engineering', 'Elmir',     'Bağırlı',     'Fəttah oğlu',   'elmir.bagirli@aztu.edu.az',   '+994 55 203 83 99', NOW()),
    ('electrical-engineering', 'Nicat',     'Hüseynov',    'Ramiz oğlu',    'nicat.huseynov@aztu.edu.az',  '+994 55 222 09 91', NOW()),
    ('electrical-engineering', 'Elçin',     'Kərimov',     'Əhməd oğlu',    'elchin.karimov@aztu.edu.az',  '+994 50 330 35 03', NOW()),
    ('electrical-engineering', 'Gülnarə',   'Hüseynova',   'Xanlar qızı',   'gulnare.huseynova@aztu.edu.az','+994 55 623 56 16', NOW()),
    ('electrical-engineering', 'Sevinc',    'Musayeva',    'Xanlar qızı',   'sevinc.musayeva@aztu.edu.az', '+994 50 388 21 82', NOW()),
    ('electrical-engineering', 'Əhməd',     'Məmmədov',    'Adil oğlu',     'Ahmad.mammadov@aztu.edu.az',  '+994 55 716 31 55', NOW()),
    ('electrical-engineering', 'Müsafir',   'Quliyev',     'Məzahir oğlu',  'Musafir.guliyev@aztu.edu.az', '+994 50 733 03 60', NOW()),
    ('electrical-engineering', 'Sabir',     'Bağırov',     'Ağabağır oğlu', 'sabir.bagirov@aztu.edu.az',   '+994 55 643 94 09', NOW()),
    ('electrical-engineering', 'Bəhruz',    'Sadıqlı',     'Məmməd oğlu',   'behruz.sadıqlı@aztu.edu.az',  '+994 55 643 94 09', NOW()),
    ('electrical-engineering', 'Xədicə',    'Əliyeva',     'Ramiz qızı',    'xedice.eliyeva@aztu.edu.az',  '+994 50 743 82 01', NOW()),
    ('electrical-engineering', 'Xanlar',    'Həşimov',     'Xamis oğlu',    'heshumov.x@16gmail.com',      '+994 50 531 81 90', NOW()),
    ('electrical-engineering', 'Nuridə',    'Zeynalova',   'Feyzulla qızı', 'nurida.zeynalova@aztu.edu.az','+994 55 710 51 36', NOW()),
    ('electrical-engineering', 'Simuzər',   'İsmayılova',  'Möylam qızı',   'simuzer.ismayilova@aztu.edu.az','+994 55 801 89 54', NOW()),
    ('electrical-engineering', 'Natella',   'Namazoba',    'Məhəddin qızı', 'natella.namazoba@aztu.edu.az','+994 55 655 35 85', NOW()),
    ('electrical-engineering', 'Sevda',     'Kazbekova',   'Ağamməd qızı',  'Sevda.kazbekova@aztu.edu.az', '+994 50 591 94 44', NOW()),
    ('electrical-engineering', 'Hikmət',    'Fəttayev',    'Varid oğlu',    'Hikmet.fettayev@aztu.edu.az', '+994 55 696 71 75', NOW()),
    ('electrical-engineering', 'Şamxal',    'Əliyev',      'Ramil oğlu',    'Shamkhal.aliyev@aztu.edu.az', '+994 99 891 96 98', NOW()),
    ('electrical-engineering', 'Samir',     'Yusifov',     'Pənah oğlu',    'Samir.yusifov@aztu.edu.az',   '+994 70 642 28 65', NOW()),
    ('electrical-engineering', 'Sara',      'Rzazadə',     'Elşad qızı',    NULL,                          '+994 70 642 28 65', NOW()),
    ('electrical-engineering', 'Günel',     'İbrahimli',   'Yaşar qızı',    'gunel.ibrahimli@aztu.edu.az', '+994 50 332 37 38', NOW()),
    ('electrical-engineering', 'Amalya',    'Alesgerova',  'Qışım qızı',    'amalya.alesgerova@aztu.edu.az','+994 50 326 11 76', NOW())
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Elektrotexnika kafedrasının baş müəllimi', NULL, NULL),
    (2,  'Elektrotexnika kafedrasının baş müəllimi', NULL, NULL),
    (3,  'Elektrotexnika kafedrasının baş müəllimi', NULL, NULL),
    (4,  'Elektrotexnika kafedrasının baş müəllimi', NULL, NULL),
    (5,  'Elektrotexnika kafedrasının baş müəllimi', NULL, NULL),
    (6,  'Elektrotexnika kafedrasının professoru', 'Professor', NULL),
    (7,  'Elektrotexnika kafedrasının dosenti',    'Dosent', 'f.r.ü.d.'),
    (8,  'Elektrotexnika kafedrasının dosenti',    'Dosent', NULL),
    (9,  'Elektrotexnika kafedrasının dosenti',    'Dosent', NULL),
    (10, 'Elektrotexnika kafedrasının dosenti',    'Dosent', NULL),
    (11, 'Elektrotexnika kafedrasının dosenti',    'Dosent', NULL),
    (12, 'Elektrotexnika kafedrasının dosenti',    'Dosent', NULL),
    (13, 'Elektrotexnika kafedrasının dosenti',    'Dosent', NULL),
    (14, 'Elektrotexnika kafedrasının dosenti',    'Dosent', 'f.r.e.n'),
    (15, 'Elektrotexnika kafedrasının dosenti',    'Dosent', NULL),
    (16, 'Elektrotexnika kafedrasının dosenti',    'Dosent', NULL),
    (17, 'Elektrotexnika kafedrasının baş müəllimi', NULL, NULL),
    (18, 'Elektrotexnika kafedrasının assistenti',  NULL, NULL),
    (19, 'Elektrotexnika kafedrasının assistenti',  NULL, NULL),
    (20, 'Elektrotexnika kafedrasının assistenti',  NULL, NULL),
    (21, 'Elektrotexnika kafedrasının assistenti',  NULL, NULL),
    (22, 'Elektrotexnika kafedrasının mühəndisi',   NULL, NULL),
    (23, 'Elektrotexnika kafedrasının müəllim köməkçisi', NULL, NULL),
    (24, 'Elektrotexnika kafedrasının kargüzarı',   NULL, NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Head teacher of Electrical Engineering department', NULL, NULL),
    (2,  'Head teacher of Electrical Engineering department', NULL, NULL),
    (3,  'Head teacher of Electrical Engineering department', NULL, NULL),
    (4,  'Head teacher of Electrical Engineering department', NULL, NULL),
    (5,  'Head teacher of Electrical Engineering department', NULL, NULL),
    (6,  'Professor of Electrical Engineering department', 'Professor', NULL),
    (7,  'Associate Professor of Electrical Engineering department', 'Associate Professor', 'PhD in Physics'),
    (8,  'Associate Professor of Electrical Engineering department', 'Associate Professor', NULL),
    (9,  'Associate Professor of Electrical Engineering department', 'Associate Professor', NULL),
    (10, 'Associate Professor of Electrical Engineering department', 'Associate Professor', NULL),
    (11, 'Associate Professor of Electrical Engineering department', 'Associate Professor', NULL),
    (12, 'Associate Professor of Electrical Engineering department', 'Associate Professor', NULL),
    (13, 'Associate Professor of Electrical Engineering department', 'Associate Professor', NULL),
    (14, 'Associate Professor of Electrical Engineering department', 'Associate Professor', 'PhD in Physics'),
    (15, 'Associate Professor of Electrical Engineering department', 'Associate Professor', NULL),
    (16, 'Associate Professor of Electrical Engineering department', 'Associate Professor', NULL),
    (17, 'Head teacher of Electrical Engineering department', NULL, NULL),
    (18, 'Assistant of Electrical Engineering department',  NULL, NULL),
    (19, 'Assistant of Electrical Engineering department',  NULL, NULL),
    (20, 'Assistant of Electrical Engineering department',  NULL, NULL),
    (21, 'Assistant of Electrical Engineering department',  NULL, NULL),
    (22, 'Engineer of Electrical Engineering department',   NULL, NULL),
    (23, 'Teacher Assistant of Electrical Engineering department', NULL, NULL),
    (24, 'Clerk of Electrical Engineering department',   NULL, NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
