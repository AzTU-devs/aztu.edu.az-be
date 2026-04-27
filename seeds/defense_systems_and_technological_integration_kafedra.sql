-- ============================================================
-- "Müdafiə sistemləri və texnoloji inteqrasiya" kafedrası — Full DB Import
-- cafedra_code: 'defense_systems_and_technological_integration'
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
    'defense_systems_and_technological_integration',
    46, 10, 0, 0, 3, 1, 0,
    '[9, 4, 8, 17]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'defense_systems_and_technological_integration',
    'az',
    'Müdafiə sistemləri və texnoloji inteqrasiya kafedrası',
    '<p>"Müdafiə sistemləri və texnoloji inteqrasiya" kafedrası Azərbaycan Texniki Universitetinin 05 iyul 2025-ci il tarixli qərarı ilə ləğv olunmuş "Radioelektron və aerokosmik sistemlər" və "Xüsusi təyinatlı material və vasitələr" kafedrasının əsasında "Xüsusi Texnika və Texnologiya" fakültəsinin tərkibində hərbi təyinatlı yüksək ixtisaslı mühəndis kadrlarının hazırlanması məqsədilə yaradılmışdır.</p><p>Kafedranın əsas məqsədi müasir müdafiə sənayesinin inkişafı üçün zəruri olan yüksək ixtisaslı mühəndis kadrların hazırlanması, eyni zamanda qabaqcıl texnologiyaların tədrisi və tətbiqinin təmin edilməsidir.</p><p>AzTU-da radioelektronika sahəsində yüksək ixtisaslı mütəxəssislərin çatışmazlığını nəzərə alaraq, elmi-pedaqoji kadrlardan və hazırda Müdafiə Sənayesi Nazirliyi (MSN) və hərbi təyinatlı ali məktəblərdə tədrislə məşğul olan və Müdafiə Nazirliyi (MN)-də bu istiqamətdə çalışmış mütəxəssislər yeni yaradılan kafedraya cəlb olunmuşdur.</p><p>Kafedrada keçirilən bütün fənlər imkan verir ki, Yeni Nəsil Mühəndislər yetişsin, onlar strateji və yüksək texnoloji sahələrdə rəqabətqabiliyyətli ixtisascı kimi özlərini göstərsin. Kafedranın məzunları müdafiə sənayesi müəssisələri, aerokosmik və aviasiya şirkətləri, aerodinamik tədqiqat mərkəzləri, eləcə də yüksək texnoloji istehsalat sahələrində fəaliyyət göstərə bilirlər.</p><p>Bakalavr ixtisasları: XTB 050102 "Hərbi rabitə vasitələri mühəndisliyi", XTB 050103 "Optotexnika mühəndisliyi", XTB 050104 "Pirotexniki və partladıcı vasitələrinin mühəndisliyi", XTB 050107 "Sistem mühəndisliyi", 050601 "Aerokosmik mühəndislik". Magistratura ixtisası: 7010003 "Xüsusi rabitə vasitələri mühəndisliyi".</p>',
    NOW()
),
(
    'defense_systems_and_technological_integration',
    'en',
    'Department of Defense Systems and Technological Integration',
    '<p>The Department of "Defense Systems and Technological Integration" was established within the Faculty of Special Equipment and Technology at Azerbaijan Technical University based on the abolished departments of "Radioelectronic and Aerospace Systems" and "Special-Purpose Materials and Means," in accordance with the decision dated July 5, 2025. Its purpose is to train highly qualified engineering personnel for military applications.</p><p>The main objective of the department is to prepare highly qualified engineering specialists necessary for the development of the modern defense industry, as well as to ensure the teaching and application of advanced technologies.</p><p>Considering the shortage of highly qualified specialists in the field of radioelectronics at AzTU, scientific and pedagogical staff, as well as specialists currently working in the Ministry of Defense Industry and higher military educational institutions, and those who have previously worked in this field within the Ministry of Defense, have been involved in the newly established department.</p><p>The courses taught at the department enable the training of a new generation of engineers, allowing them to establish themselves as competitive specialists in strategic and high-tech fields. Graduates of this department can be employed in defense industry enterprises, aerospace and aviation companies, aerodynamic research centers, as well as in high-tech manufacturing sectors.</p><p>Bachelor''s specialties: XTB 050102 "Military Communication Systems Engineering", XTB 050103 "Optotechnics Engineering", XTB 050104 "Pyrotechnic and Explosive Devices Engineering", XTB 050107 "Systems Engineering", 050601 "Aerospace Engineering". Master''s specialty: 7010003 "Special Communication Systems Engineering".</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'defense_systems_and_technological_integration';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('defense_systems_and_technological_integration', 1, NOW()),
    ('defense_systems_and_technological_integration', 2, NOW()),
    ('defense_systems_and_technological_integration', 3, NOW()),
    ('defense_systems_and_technological_integration', 4, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Müdafiə sistemlərinin layihələndirilməsi, istehsalı və istismarı', 'Tələbələr müdafiə təyinatlı texniki sistemlərin layihələndirilməsi, konstruksiyası və istismar xüsusiyyətləri üzrə nəzəri biliklər və praktiki bacarıqlar əldə edirlər. Məqsəd milli müdafiə sənayesinin tələblərinə cavab verən peşəkar mühəndislərin hazırlanmasıdır.'),
    (2, 'Texnoloji inteqrasiya və innovativ mühəndislik həlləri',           'Qabaqcıl elmi-texniki nailiyyətlərin sənaye və istehsalat proseslərinə tətbiqini, yeni texnologiyaların mühəndislik fəaliyyətinə inteqrasiyasını və innovativ yanaşmaların inkişafını əhatə edir.'),
    (3, 'Elmi-tədqiqat fəaliyyətinin genişləndirilməsi',                    'Tədris prosesində müasir texnologiyaların tətbiqi və elmi-tədqiqat fəaliyyətinin genişləndirilməsi prioritet istiqamətdir.'),
    (4, 'Sənaye ilə əməkdaşlığın inkişaf etdirilməsi',                      'Müdafiə Sənayesi Nazirliyi və hərbi təyinatlı ali təhsil müəssisələri ilə əməkdaşlıq tədris prosesinin praktiki yönümlülüyünün artırılmasına və tələbələrin real sənaye mühiti ilə tanışlığına imkan yaradır.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Design, production, and operation of defense systems',              'Within this area, students acquire theoretical knowledge and practical skills related to the design, construction, and operational characteristics of defense-related technical systems. The goal is to train professional engineers who meet the requirements of the national defense industry.'),
    (2, 'Technological integration and innovative engineering solutions',    'This area covers the application of advanced scientific and technological achievements to industrial and production processes, the integration of new technologies into engineering activities, and the development of innovative approaches.'),
    (3, 'Expansion of scientific research activities',                        'The application of modern technologies in the educational process and the expansion of research activities is a priority direction.'),
    (4, 'Development of cooperation with industry',                           'Collaboration with the Ministry of Defense Industry and military-oriented higher education institutions enhances the practical orientation of the educational process and provides students with exposure to the real industrial environment.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'defense_systems_and_technological_integration',
        'Uğurlu', 'Nadirov', 'Məhəmməd oğlu',
        'ugurlu.nadirov@aztu.edu.az',
        '+994 55 512 77 58',
        'III korpus, K222-ci otaq',
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
    '<p>Nadirov Uğurlu Məhəmməd oğlu texnika elmləri doktoru, professor. Maşınqayırma texnologiyası sahəsi üzrə ixtisaslaşmış alimdir. O, elmi-pedaqoji fəaliyyətində maşınqayırma məmulatlarının istehsal keyfiyyətinin təmin edilməsi, istehsal keyfiyyəti ilə istismar göstəriciləri arasında qarşılıqlı əlaqələrin elmi əsaslarla idarə olunması, eləcə də istehsal sahələrinin layihələndirilməsi və dizaynı istiqamətlərində fundamental və tətbiqi tədqiqatlar aparır.</p><p>Alimin elmi tədqiqatlarının əsas istiqamətlərinə maşınqayırma məmulatlarının keyfiyyət göstəricilərinin kəmiyyətcə qiymətləndirilməsi metod və texnologiyalarının işlənib hazırlanması daxildir. Bu sahədə əldə etdiyi elmi nəticələr nüfuzlu beynəlxalq və yerli elmi jurnallarda dərc olunmuş, maşınqayırma texnologiyası sahəsinin nəzəri və praktiki inkişafına mühüm töhfələr vermişdir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin "Müdafiə sistemləri və texnoloji inteqrasiya" kafedrasının müdiri vəzifəsində çalışır.</p><p>O, 118 elmi əsərin müəllifidir. Onların sırasına 1 patent, 1 monoqrafiya, 2 dərslik, 5 dərs vəsaiti və 3 metodiki göstəriş daxildir. Məqalələri Amerika Birləşmiş Ştatları, Rusiya, Türkiyə, Braziliya, Hindistan, Belarusiya və Ukrayna kimi ölkələrin nüfuzlu beynəlxalq elmi jurnallarında dərc olunmuşdur.</p><p>Müxtəlif illərdə beynəlxalq elmi əməkdaşlıq çərçivəsində xarici ölkələrdə elmi ezamiyyətlərdə olmuşdur. Belə ki, 1995-ci ildə Türkiyənin Bilkent Universitetində, 2002-ci ildə isə Gebze Texniki Universitetində elmi tədqiqat fəaliyyətini həyata keçirmişdir.</p><p>Cisco Systems Networking Academy proqramı üzrə "IT Essentials: PC Hardware and Software" kursunu tamamlayaraq müvafiq instruktur sertifikatı əldə etmişdir.</p>',
    '["Maşınqayırma məmulatlarının keyfiyyət göstəricilərinin kəmiyyətcə qiymətləndirilməsi nəzəriyyəsi və metodları", "İstehsal keyfiyyəti ilə istismar (etibarlılıq, davamlılıq, dəqiqlik) göstəriciləri arasında qarşılıqlı əlaqələrin modelləşdirilməsi və idarə olunması", "Maşınqayırmada keyfiyyətin idarə edilməsi sistemləri və optimallaşdırma üsulları", "Maşınqayırma sahələrində layihələndirmə və istehsal sistemlərinin dizaynı", "Texnoloji proseslərin rəqəmsallaşdırılması və avtomatlaşdırılması", "İstehsal proseslərində çoxparametrli keyfiyyət qiymətləndirilməsi və monitorinqi", "Müasir istehsal texnologiyalarında (CNC, CAD/CAM sistemləri) keyfiyyətin təmin edilməsi üsulları", "Kompüter qrafikası və 3D modelləşdirmə texnologiyalarının maşınqayırma məmulatlarının layihələndirilməsi və vizuallaşdırılmasında tətbiqi", "CAD sistemlərində texnoloji obyektlərin parametrik modelləşdirilməsi və optimallaşdırılması"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Technical Sciences',
    'Professor',
    '<p>Nadirov Ughurlu Mammad oghlu is a Doctor of Technical Sciences and a professor. He is a specialist in the field of machine-building technology. In his scientific and pedagogical work, he conducts fundamental and applied research on ensuring the production quality of machine-building products, scientifically managing the relationships between production quality and operational performance, and designing and planning production facilities.</p><p>The main focus of his scientific research includes developing methods and technologies for the quantitative evaluation of the quality indicators of machine-building products. The results of his work have been published in prestigious international and national scientific journals and have made significant contributions to both the theoretical and practical development of machine-building technology.</p><p>Currently, he serves as the head of the Department of "Defense Systems and Technological Integration" at the Azerbaijan Technical University.</p><p>He is the author of 118 scientific works, including 1 patent, 1 monograph, 2 textbooks, 5 teaching aids, and 3 methodological guidelines. His articles have been published in respected international scientific journals in the United States, Russia, Turkey, Brazil, India, Belarus, and Ukraine.</p><p>Over the years, he has participated in scientific trips abroad within the framework of international scientific collaboration. Notably, in 1995, he conducted research at Bilkent University in Turkey, and in 2002, at Gebze Technical University.</p><p>He completed the "IT Essentials: PC Hardware and Software" course under the Cisco Systems Networking Academy program and obtained the corresponding instructor certification.</p>',
    '["Theory and methods for quantitative evaluation of quality indicators of machine-building products", "Modeling and management of relationships between production quality and operational performance (reliability, durability, accuracy)", "Quality management systems and optimization methods in machine-building", "Design and planning of production systems in machine-building", "Digitalization and automation of technological processes", "Multivariate quality evaluation and monitoring in production processes", "Methods for ensuring quality in modern production technologies (CNC, CAD/CAM systems)", "Application of computer graphics and 3D modeling technologies in the design and visualization of machine-building products", "Parametric modeling and optimization of technological objects in CAD systems"]'::jsonb,
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
    VALUES
    ((SELECT id FROM cafedra_directors WHERE cafedra_code = 'defense_systems_and_technological_integration'), '10:00–13:00', NOW()),
    ((SELECT id FROM cafedra_directors WHERE cafedra_code = 'defense_systems_and_technological_integration'), '14:00–17:00', NOW())
    RETURNING id, time_range
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', CASE time_range WHEN '10:00–13:00' THEN 'Bazar ertəsi' ELSE 'Çərşənbə' END, NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', CASE time_range WHEN '10:00–13:00' THEN 'Monday'        ELSE 'Wednesday' END, NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1983', '1990', NOW() FROM cafedra_directors WHERE cafedra_code = 'defense_systems_and_technological_integration'
UNION ALL
SELECT id, '1984', '1986', NOW() FROM cafedra_directors WHERE cafedra_code = 'defense_systems_and_technological_integration'
UNION ALL
SELECT id, '1994', '1998', NOW() FROM cafedra_directors WHERE cafedra_code = 'defense_systems_and_technological_integration'
UNION ALL
SELECT id, '2014', '2019', NOW() FROM cafedra_directors WHERE cafedra_code = 'defense_systems_and_technological_integration';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'defense_systems_and_technological_integration')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bakalavr + Magistr (fərqlənmə diplomu)',            'Azərbaycan Politexnik İnstitutu'),
    (2, 'Hərbi xidmət',                                      '—'),
    (3, 'Elmlər namizədi (t.e.n.)',                          'Azərbaycan Texniki Universiteti'),
    (4, 'Elmlər doktoru (t.e.d.)',                           'Azərbaycan Texniki Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bachelor + Master (with distinction)',              'Azerbaijan Polytechnic Institute'),
    (2, 'Military service',                                  '—'),
    (3, 'Candidate of Sciences (PhD in Technical Sciences)', 'Azerbaijan Technical University'),
    (4, 'Doctor of Sciences (DSc in Technical Sciences)',    'Azerbaijan Technical University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'defense_systems_and_technological_integration';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('defense_systems_and_technological_integration', 'Bayram',     'İbrahimov',    'Qənimət oğlu',   'bayram.ibrahimov@aztu.adu.az',      '+994 70 649 07 79', NOW()),  -- 1
    ('defense_systems_and_technological_integration', 'Vaqif',      'Məhərrəmov',   'Əli oğlu',       'vaqif.maharramov@aztu.edu.az',     '+994 50 644 47 76', NOW()),  -- 2
    ('defense_systems_and_technological_integration', 'Əsəd',       'Rüstəmov',     'Rüstəm oğlu',    'esed.rustamov@aztu.edu.az',        '+994 50 388 44 82', NOW()),  -- 3
    ('defense_systems_and_technological_integration', 'Mehman',     'Binnətov',     'Fərhad oğlu',    'mehman.binnetov@aztu.edu.az',      '+994 50 603 75 25', NOW()),  -- 4
    ('defense_systems_and_technological_integration', 'Zəfər',      'İsmayılov',    'Ələsgər oğlu',   'zefer.alesker@aztu.edu.az',        '+994 50 631 21 82', NOW()),  -- 5
    ('defense_systems_and_technological_integration', 'Yalçın',     'İsayev',       'Sabir oğlu',     'yalchin.isayev@aztu.edu.az',       '+994 70 277 43 81', NOW()),  -- 6
    ('defense_systems_and_technological_integration', 'Çərkəz',     'Yusubov',      'Əsgər oğlu',     'cerkez.yusubov@aztu.adu.az',       '+994 50 220 40 72', NOW()),  -- 7
    ('defense_systems_and_technological_integration', 'Həbibulla',  'Beydullayev',  'Ziyəddin oğlu',  'hebibulla.beydullayev@aztu.edu.az','+994 55 602 67 98', NOW()),  -- 8
    ('defense_systems_and_technological_integration', 'Əliqismət',  'Mehdiyev',     'Əbiş oğlu',      'aliqismet.mehdiyev@aztu.edu.az',   '+994 50 372 02 64', NOW()),  -- 9
    ('defense_systems_and_technological_integration', 'Qadir',      'Qafarov',      'Arzu oğlu',      'qadir.qafarov@aztu.edu.az',        '+994 55 590 68 06', NOW()),  -- 10
    ('defense_systems_and_technological_integration', 'Malik',      'Əliyev',       'Etibar oğlu',    'malik.aliyev@aztu.edu.az',         '+994 55 560 12 08', NOW()),  -- 11
    ('defense_systems_and_technological_integration', 'Amin',       'Mamedov',      'Afət oğlu',      'amin.mamedov@aztu.edu.az',         '+994 70 806 70 51', NOW()),  -- 12
    ('defense_systems_and_technological_integration', 'Muxtar',     'Əzizullayev',  'Qalib oğlu',     'mukhtar.azizullayev@aztu.edu.az',  '+994 55 705 86 62', NOW()),  -- 13
    ('defense_systems_and_technological_integration', 'Aygün',      'Həmidova',     'Akif qızı',      'aygun.hemidova@aztu.edu.az',       '+994 50 456 11 25', NOW()),  -- 14
    ('defense_systems_and_technological_integration', 'Rial',       'Hümmətov',     'Mübariz oğlu',   'rial.himmetov@aztu.edu.az',        '+994 55 388 04 03', NOW()),  -- 15
    ('defense_systems_and_technological_integration', 'Gülyanaq',   'Əfqanlı',      'Ələddin qızı',   'gulyanaq.afqanli@aztu.edu.az',     '+994 50 604 78 88', NOW())   -- 16
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının tədqiqatçı-professoru', 'Professor',   't.e.d.'),
    (2,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının məsləhətçi-professoru', 'Professor',   'f.r.e.d.'),
    (3,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının professoru',            'Professor',   't.ü.f.d.'),
    (4,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının dosenti',               'Dosent',      't.e.n.'),
    (5,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının dosenti',               'Dosent',      't.ü.f.d.'),
    (6,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının dosenti',               'Dosent',      'h.e.f.d.'),
    (7,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının dosenti',               'Dosent',      't.e.n.'),
    (8,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının baş müəllimi',          NULL::varchar, NULL::varchar),
    (9,  'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının baş müəllimi',          NULL,          NULL),
    (10, 'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının baş müəllimi',          NULL,          NULL),
    (11, 'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının assistenti',            NULL,          NULL),
    (12, 'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının assistenti',            NULL,          NULL),
    (13, 'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının assistenti',            NULL,          NULL),
    (14, 'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının kargüzarı',             NULL,          NULL),
    (15, 'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının müəllim köməkçisi',     NULL,          NULL),
    (16, 'Müdafiə sistemləri və texnoloji inteqrasiya kafedrasının müəllim köməkçisi',     NULL,          NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Research Professor at the Department of Defense Systems and Technological Integration',   'Professor',           'Doctor of Technical Sciences'),
    (2,  'Advisory Professor at the Department of Defense Systems and Technological Integration',   'Professor',           'Doctor of Physical and Mathematical Sciences'),
    (3,  'Professor at the Department of Defense Systems and Technological Integration',            'Professor',           'PhD in Technical Sciences'),
    (4,  'Associate Professor at the Department of Defense Systems and Technological Integration',  'Associate Professor', 'Candidate of Technical Sciences'),
    (5,  'Associate Professor at the Department of Defense Systems and Technological Integration',  'Associate Professor', 'PhD in Technical Sciences'),
    (6,  'Associate Professor at the Department of Defense Systems and Technological Integration',  'Associate Professor', 'PhD in Economic Sciences'),
    (7,  'Associate Professor at the Department of Defense Systems and Technological Integration',  'Associate Professor', 'Candidate of Technical Sciences'),
    (8,  'Senior Lecturer at the Department of Defense Systems and Technological Integration',      NULL::varchar,         NULL::varchar),
    (9,  'Senior Lecturer at the Department of Defense Systems and Technological Integration',      NULL,                  NULL),
    (10, 'Senior Lecturer at the Department of Defense Systems and Technological Integration',      NULL,                  NULL),
    (11, 'Assistant at the Department of Defense Systems and Technological Integration',            NULL,                  NULL),
    (12, 'Assistant at the Department of Defense Systems and Technological Integration',            NULL,                  NULL),
    (13, 'Assistant at the Department of Defense Systems and Technological Integration',            NULL,                  NULL),
    (14, 'Clerk at the Department of Defense Systems and Technological Integration',                NULL,                  NULL),
    (15, 'Teaching Assistant at the Department of Defense Systems and Technological Integration',  NULL,                  NULL),
    (16, 'Teaching Assistant at the Department of Defense Systems and Technological Integration',  NULL,                  NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
