-- ============================================================
-- Kibertəhlükəsizlik kafedrası — Full DB Import
-- cafedra_code: 'cybersecurity'
-- faculty_code: 'information_technologies_telecommunications'
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
    'information_technologies_telecommunications',
    'cybersecurity',
    1, 5, 2, 7, 3, 1, 5,
    '[4, 9, 16]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'cybersecurity',
    'az',
    'Kibertəhlükəsizlik kafedrası',
    '<p>Kibertəhlükəsizlik kafedrası Azərbaycan Texniki Universiteti (AzTU) Elmi Şurasının 12 iyul 2022-ci il tarixli qərarı ilə yaradılmışdır. Kafedra regionda kibertəhlükəsizlik və informasiya təhlükəsizliyi sahəsində təhsil və elmi-tədqiqat üzrə qabaqcıl mərkəzə çevrilməyi qarşısına məqsəd qoymuşdur.</p><p>Kafedranın missiyası innovativ və kreativ düşüncəyə malik, analitik bacarıqları inkişaf etmiş, müasir texnologiyalar əsasında effektiv həllər təqdim edə bilən yüksək ixtisaslı mütəxəssislər hazırlamaqdır. Bu mütəxəssislər informasiya təhlükəsizliyi sahəsində yeni yanaşmaların formalaşdırılması və cəmiyyətin rəqəmsal təhlükəsizliyinin təmin edirlər.</p><p>Kafedra təhsil, elmi-tədqiqat və sənaye əməkdaşlığının vəhdət təşkil etdiyi müasir və inklüziv akademik mühitin formalaşdırılmasına çalışır. Böyük verilənlərin analizi, süni intellekt tətbiqləri, kibertəhlükəsizlik, IoT və smart sistemlərin təhlükəsizliyi, eləcə də texnoloji sahibkarlıq istiqamətində həyata keçirilən təşəbbüslər vasitəsilə nəzəri biliklərin praktik tətbiqlərə çevrilməsi təmin olunur.</p>',
    NOW()
),
(
    'cybersecurity',
    'en',
    'Department of Cybersecurity',
    '<p>The Department of Cybersecurity was established by the decision of the Academic Council of Azerbaijan Technical University (AzTU) on July 12, 2022. The department aims to become a leading center in the region for education and scientific research in the field of cybersecurity and information security.</p><p>The mission of the department is to train highly qualified specialists with innovative and creative thinking, well-developed analytical skills, who can provide effective solutions based on modern technologies. These specialists contribute to forming new approaches in the field of information security and ensuring the digital security of society.</p><p>The department strives to create a modern and inclusive academic environment that integrates education, scientific research, and industry collaboration. Through initiatives in big data analytics, artificial intelligence applications, cybersecurity, IoT and smart systems security, and technological entrepreneurship, theoretical knowledge is transformed into practical applications.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'cybersecurity';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('cybersecurity', 1, NOW()),
    ('cybersecurity', 2, NOW()),
    ('cybersecurity', 3, NOW()),
    ('cybersecurity', 4, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'İnformasiya təhlükəsizliyi üzrə tədris proqramlarının hazırlanması və tətbiqi',    'İnformasiya təhlükəsizliyi üzrə müasir və beynəlxalq standartlara uyğun tədris proqramlarının hazırlanması və tətbiqi'),
    (2, 'Praktiki bacarıqlara malik mütəxəssislərin hazırlanması',                           'Sənaye və dövlət qurumları ilə əməkdaşlıq çərçivəsində praktiki bacarıqlara malik mütəxəssislərin hazırlanması'),
    (3, 'Kritik informasiya infrastrukturunun qorunması',                                    'Kritik informasiya infrastrukturunun qorunması üçün metod və texnologiyaların inkişaf etdirilməsi'),
    (4, 'Elmi tədqiqatlar və innovativ həllər',                                              'Müxtəlif sektorlar üzrə informasiya təhlükəsizliyinin təmin edilməsi istiqamətində elmi tədqiqatların aparılması və innovativ həllərin işlənməsi')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Development and implementation of curricula in information security',               'Development and implementation of modern curricula aligned with international information security standards'),
    (2, 'Training of specialists with practical skills',                                     'Training of specialists with practical skills through collaboration with industry and government institutions'),
    (3, 'Protection of critical information infrastructure',                                 'Development of methods and technologies for the protection of critical information infrastructure'),
    (4, 'Scientific research and innovative solutions',                                      'Conducting scientific research and developing innovative solutions for information security across various sectors')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'cybersecurity',
        'Yadigar', 'İmamverdiyev', 'Nəsib oğlu',
        'yadigar.imamverdiyev@aztu.edu.az',
        '+994 12 539 08 24',
        'V korpus, K406-cı otaq',
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
    'Dosent',
    '<p>İmamverdiyev Yadigar Nəsib oğlu — texnika elmləri doktoru, dosent, informasiya təhlükəsizliyi və kriptoqrafiya sahəsi üzrə ixtisaslaşmış alimdir. O, informasiya təhlükəsizliyi və kibertəhlükəsizlik istiqamətində elmi və pedaqoji fəaliyyət göstərir.</p><p>Onun elmi tədqiqatlarının əsas istiqamətlərinə informasiya təhlükəsizliyi, tətbiqi kriptoqrafiya və kriptoanaliz, süni intellekt metodları və biometrik texnologiyalar daxildir. Bu sahələr üzrə apardığı tədqiqatların nəticələri nüfuzlu elmi jurnallarda dərc olunmuş və informasiya təhlükəsizliyi sahəsinin inkişafına mühüm töhfə vermişdir.</p><p>İmamverdiyev Y.N. pedaqoji fəaliyyətində müasir kibertəhlükəsizlik yanaşmalarını tətbiq edərək tələbələrin analitik və tənqidi düşünmə bacarıqlarının inkişafına, eləcə də gənc mütəxəssislərin hazırlanması və elmi-tədqiqat fəaliyyətinə cəlb olunmasına xüsusi önəm verir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin Kibertəhlükəsizlik kafedrasının müdiri vəzifəsində çalışır. O, 200-dən çox elmi məqalənin və 8 kitabın müəllifidir, həmçinin ölkədə ilk CERT komandasının yaradılmasında və biometrik identifikasiya sistemlərinin tətbiqi üzrə dövlət layihələrində aktiv iştirak etmişdir.</p>',
    '["Süni intellekt metodları", "Tətbiqi kriptoqrafiya", "Kibertəhlükəsizlik sistemləri", "İnformasiya sistemlərinin idarə edilməsi", "Kritik infrastrukturun təhlükəsizliyi", "Blokçeyn texnologiyaları"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Technical Sciences',
    'Associate Professor',
    '<p>Yadigar Nasib Imamverdiyev is a Doctor of Technical Sciences, Associate Professor, and a scientist specializing in information security and cryptography. He carries out scientific and pedagogical activities in the field of information security and cybersecurity.</p><p>His main research areas include information security, applied cryptography and cryptanalysis, artificial intelligence methods, and biometric technologies. The results of his research in these fields have been published in prestigious scientific journals and have made significant contributions to the development of the information security field.</p><p>In his pedagogical activities, Imamverdiyev Y.N. applies modern cybersecurity approaches, paying special attention to the development of students'' analytical and critical thinking skills, as well as the training of young specialists and their involvement in scientific research activities.</p><p>He currently serves as the Head of the Department of Cybersecurity at Azerbaijan Technical University. He is the author of more than 200 scientific articles and 8 books, and has actively participated in the creation of the country''s first CERT team and in state projects for the implementation of biometric identification systems.</p>',
    '["Artificial intelligence methods", "Applied cryptography", "Cybersecurity systems", "Information systems management", "Critical infrastructure security", "Blockchain technologies"]'::jsonb,
    NOW()
FROM director_insert
ON CONFLICT (director_id, lang_code) DO UPDATE
SET scientific_degree         = EXCLUDED.scientific_degree,
    scientific_title          = EXCLUDED.scientific_title,
    bio                       = EXCLUDED.bio,
    scientific_research_fields = EXCLUDED.scientific_research_fields,
    updated_at                = NOW();

-- Working hours
WITH wh_insert AS (
    INSERT INTO cafedra_director_working_hours (director_id, time_range, created_at)
    SELECT id, '14:00–17:00', NOW()
    FROM cafedra_directors WHERE cafedra_code = 'cybersecurity'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Çərşənbə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Wednesday',        NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1982', '1989', NOW() FROM cafedra_directors WHERE cafedra_code = 'cybersecurity'
UNION ALL
SELECT id, '2003', '2006', NOW() FROM cafedra_directors WHERE cafedra_code = 'cybersecurity'
UNION ALL
SELECT id, '2008', '2012', NOW() FROM cafedra_directors WHERE cafedra_code = 'cybersecurity';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'cybersecurity')
    ORDER BY id DESC
    LIMIT 3
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bakalavr və Magistr',              'Azərbaycan Dövlət Neft və Sənaye Universiteti'),
    (2, 'Elmlər namizədi (PhD)',            'AMEA İnformasiya Texnologiyaları İnstitutu'),
    (3, 'Elmlər doktoru (DSc)',             'AMEA İnformasiya Texnologiyaları İnstitutu')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bachelor''s and Master''s',                        'Azerbaijan State Oil and Industry University'),
    (2, 'Candidate of Sciences (PhD)',                      'Institute of Information Technology of ANAS'),
    (3, 'Doctor of Sciences (DSc)',                         'Institute of Information Technology of ANAS')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers (associate professors, senior lecturers, assistants) ──
DELETE FROM cafedra_workers WHERE cafedra_code = 'cybersecurity';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Associate Professors (dosentlər)
    ('cybersecurity', 'Samirə',   'Qəhrəmanova',  'Həsən qızı',      'samira.qahramanova@aztu.edu.az',  '+994 10-527-07-11',  NOW()),  -- 1
    ('cybersecurity', 'Natiq',    'Quliyev',       'Əliabbas oğlu',   'natiq.quliyev@aztu.edu.az',       '+994 70-323-37-36',  NOW()),  -- 2
    ('cybersecurity', 'Rəhilə',   'Sadıqova',      'Hidayət qızı',    'rahila.sadygova@aztu.edu.az',     '+994 70-623-31-18',  NOW()),  -- 3
    ('cybersecurity', 'Aydın',    'Hüseynov',      'Fridun oğlu',     'aydin.huseynov@aztu.edu.az',      '+994 70-386-76-77',  NOW()),  -- 4
    ('cybersecurity', 'Elşən',    'İbayev',        'Akif oğlu',       'elshen.ibayev@aztu.edu.az',       '+994 50-501-14-84',  NOW()),  -- 5
    ('cybersecurity', 'Təbriz',   'Cəfərov',       'Ramal oğlu',      'tabriz.cafarov@aztu.edu.az',      '+994 50-247-48-10',  NOW()),  -- 6
    -- Senior Lecturers (Baş müəllimlər)
    ('cybersecurity', 'Fərid',    'Qasımlı',       'Fikrət oğlu',     'farid.gasimli@aztu.edu.az',       '+994 50-403-07-44',  NOW()),  -- 7
    ('cybersecurity', 'İlahə',    'Qəhrəmanova',   'Həsən qızı',      'ilaha.qahramanova@aztu.edu.az',   '+994 50-418-57-30',  NOW()),  -- 8
    ('cybersecurity', 'Rahib',    'Ağababayev',     'Rəsul oğlu',      'rahib.agababayev@aztu.edu.az',    '+994 51-491-91-81',  NOW()),  -- 9
    -- Assistants (assistentlər)
    ('cybersecurity', 'Aynur',    'Məhərrəmova',   'Natiq qızı',      'aynur.meherremova@aztu.edu.az',   '+994 51-700-30-30',  NOW()),  -- 10
    ('cybersecurity', 'Nərmin',   'Məmmədova',      'Ləyaqət qızı',    'narmin.mammadova@aztu.edu.az',    '+994 51-526-86-87',  NOW()),  -- 11
    ('cybersecurity', 'Arzu',     'Babayeva',       'Ələm qızı',       'arzu.babayeva@aztu.edu.az',       '+994 51-430-05-74',  NOW()),  -- 12
    ('cybersecurity', 'Əzimə',    'Hüseynova',      'Şahin qızı',      'ezime.huseynova@aztu.edu.az',     '+994 51-649-82-98',  NOW()),  -- 13
    ('cybersecurity', 'Aytəkin',  'İbrahimova',     'Bəybala qızı',    'aytekin.ibrahimova@aztu.edu.az',  '+994 55-980-39-70',  NOW()),  -- 14
    ('cybersecurity', 'Qahirə',   'Əliyeva',        'Tehran qızı',     'qahire.vahidli@aztu.edu.az',      '+994 55-840-97-28',  NOW()),  -- 15
    ('cybersecurity', 'Pərişan',  'Quluzadə',       'Ceyhun qızı',     'perishan.guluzade@aztu.edu.az',   '+994 50-449-30-56',  NOW()),  -- 16
    ('cybersecurity', 'Cavad',    'Nəcəfli',        'Vaqif oğlu',      'cavad.necefli@aztu.edu.az',       '+994 51-340-19-24',  NOW()),  -- 17
    ('cybersecurity', 'Aydan',    'Arifli',         'Rauf qızı',       'aydan.arifli@aztu.edu.az',        '+994 55-439-72-28',  NOW()),  -- 18
    ('cybersecurity', 'Leyla',    'Orucova',        'Sənan qızı',      'leyla.orucova@aztu.edu.az',       '+994 50-679-72-34',  NOW()),  -- 19
    ('cybersecurity', 'Xumar',    'Şirəliyeva',     'Rəşad qızı',      'khumar.shiraliyeva@aztu.edu.az',  '+994 55-232-07-67',  NOW()),  -- 20
    ('cybersecurity', 'İnci',     'Abdullayeva',    'Tağı qızı',       'inci.abdullayeva@aztu.edu.az',    '+994 50-536-49-26',  NOW()),  -- 21
    ('cybersecurity', 'Azad',     'Fərzəliyev',     'Novruz oğlu',     'azad.farzaliyev@aztu.edu.az',     '+994 51-696-06-44',  NOW()),  -- 22
    ('cybersecurity', 'Ramidə',   'Səfərli',        'Elşən qızı',      'ramida.safarli@aztu.edu.az',      '+994 55-329-83-26',  NOW()),  -- 23
    ('cybersecurity', 'Adilə',    'Kərimova',       'Yadigar qızı',    'adila.karimova@aztu.edu.az',      '+994 51-821-54-17',  NOW()),  -- 24
    ('cybersecurity', 'Əli',      'Əliyev',         'Əbülfəz oğlu',    'ali.aliyev@aztu.edu.az',          '+994 50-253-49-53',  NOW()),  -- 25
    ('cybersecurity', 'Nigar',    'Məmmədzadə',     'Ərəstun qızı',    'nigar.mammadzade@aztu.edu.az',    '+994 50-493-21-24',  NOW()),  -- 26
    ('cybersecurity', 'Əminə',    'Abbasova',       'Elşad qızı',      'amina.abbasova@aztu.edu.az',      '+994 51-724-60-92',  NOW()),  -- 27
    ('cybersecurity', 'Samirə',   'Həsənova',       'Əfrasiyab qızı',  'samirahasanova75@gmail.com',      '+994 50-349-77-27',  NOW())   -- 28
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Associate Professors
    (1,  'Kibertəhlükəsizlik kafedrası, dosent',       'Dosent', 't.f.d.'),
    (2,  'Kibertəhlükəsizlik kafedrası, dosent',       'Dosent', 'f.r.e.n.'),
    (3,  'Kibertəhlükəsizlik kafedrası, dosent',       'Dosent', 'r.ü.f.d.'),
    (4,  'Kibertəhlükəsizlik kafedrası, dosent',       'Dosent', 't.e.n.'),
    (5,  'Kibertəhlükəsizlik kafedrası, dosent',       'Dosent', 'r.ü.f.d.'),
    (6,  'Kibertəhlükəsizlik kafedrası, dosent',       'Dosent', 'h.ü.f.d.'),
    -- Senior Lecturers
    (7,  'Kibertəhlükəsizlik kafedrası, baş müəllim',  NULL,     NULL),
    (8,  'Kibertəhlükəsizlik kafedrası, baş müəllim',  NULL,     NULL),
    (9,  'Kibertəhlükəsizlik kafedrası, baş müəllim',  NULL,     NULL),
    -- Assistants
    (10, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (11, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (12, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (13, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (14, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (15, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (16, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (17, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (18, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (19, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (20, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (21, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (22, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (23, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (24, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (25, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (26, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (27, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL),
    (28, 'Kibertəhlükəsizlik kafedrası, assistent',    NULL,     NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Associate Professors
    (1,  'Department of Cybersecurity, Associate Professor',  'Associate Professor', 't.f.d.'),
    (2,  'Department of Cybersecurity, Associate Professor',  'Associate Professor', 'f.r.e.n.'),
    (3,  'Department of Cybersecurity, Associate Professor',  'Associate Professor', 'r.ü.f.d.'),
    (4,  'Department of Cybersecurity, Associate Professor',  'Associate Professor', 't.e.n.'),
    (5,  'Department of Cybersecurity, Associate Professor',  'Associate Professor', 'r.ü.f.d.'),
    (6,  'Department of Cybersecurity, Associate Professor',  'Associate Professor', 'h.ü.f.d.'),
    -- Senior Lecturers
    (7,  'Department of Cybersecurity, Senior Lecturer',      NULL,                  NULL),
    (8,  'Department of Cybersecurity, Senior Lecturer',      NULL,                  NULL),
    (9,  'Department of Cybersecurity, Senior Lecturer',      NULL,                  NULL),
    -- Assistants
    (10, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (11, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (12, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (13, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (14, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (15, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (16, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (17, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (18, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (19, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (20, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (21, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (22, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (23, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (24, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (25, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (26, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (27, 'Department of Cybersecurity, Assistant',            NULL,                  NULL),
    (28, 'Department of Cybersecurity, Assistant',            NULL,                  NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
