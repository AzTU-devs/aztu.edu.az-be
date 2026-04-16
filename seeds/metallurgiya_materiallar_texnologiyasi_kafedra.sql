-- ============================================================
-- Metallurgiya və materiallar texnologiyası kafedrası — Full DB Import
-- cafedra_code: 'metallurgy_materials_technology'
-- faculty_code: 'MMF'
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
    'MMF',
    'metallurgy_materials_technology',
    3, 3, 2, 10, 5, 4, 5,
    '[4, 8, 9, 12]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'metallurgy_materials_technology',
    'az',
    'Metallurgiya və materiallar texnologiyası kafedrası',
    '<p>"Metallurgiya və materiallar texnologiyası" kafedrası Azərbaycanın sənaye inkişafı ilə sıx bağlı olaraq formalaşmış və uzunmüddətli elmi-pedaqoji ənənələrə malik olan aparıcı akademik strukturlardan biridir. Kafedranın əsası 1967-ci ildə Azərbaycan Respublikasında metallurgiya və maşınqayırma sənayesinin sürətli inkişafı nəticəsində yüksəkixtisaslı mühəndis-metallurqlara artan tələbatın ödənilməsi məqsədilə qoyulmuşdur.</p><p>Müxtəlif dövrlərdə kafedraya tanınmış alimlər rəhbərlik etmişdir. Uzun illər kafedraya professor Rəhim Şükürov rəhbərlik etmiş, sonrakı illərdə professor Sübhan Namazov rəhbər olmuş, professor Aqil Babayev isə bu vəzifəni icra etmişdir.</p><p>Hazırda kafedrada yüksək ixtisaslı professor-müəllim heyəti fəaliyyət göstərir. Kafedra fəaliyyət göstərdiyi dövr ərzində zəngin laboratoriya bazası formalaşdırmışdır. Metalloqrafiya, termiki emal, qaynaq, tökmə və mexaniki xassələrin tədqiqi üzrə müasir laboratoriyalar yaradılmış və daim inkişaf etdirilmişdir.</p><p>Kafedranın elmi-pedaqoji fəaliyyəti nəticəsində yüzlərlə elmi məqalə, dərslik və dərs vəsaiti nəşr olunmuş, çoxsaylı ixtiralar və patentlər əldə edilmişdir. Eyni zamanda kafedra beynəlxalq elmi əməkdaşlıq əlaqələrini genişləndirərək müxtəlif ölkələrin elmi-tədqiqat mərkəzləri ilə birgə layihələr həyata keçirir.</p>',
    NOW()
),
(
    'metallurgy_materials_technology',
    'en',
    'Department of Metallurgy and Materials Technology',
    '<p>The Department of "Metallurgy and Materials Technology" is one of the leading academic units with long-standing scientific and pedagogical traditions, formed in close connection with the industrial development of Azerbaijan. The department was established in 1967 in response to the growing demand for highly qualified metallurgical engineers driven by the rapid development of the metallurgical and machine-building industries in the Republic of Azerbaijan.</p><p>At different periods the department has been led by distinguished scholars. For many years it was headed by Professor Rahim Shukurov, in subsequent years it was led by Professor Subhan Namazov, while Professor Agil Babayev served in this position.</p><p>Currently, the department is staffed by a highly qualified academic faculty. Throughout its activity the department has developed a strong laboratory infrastructure. Modern laboratories in metallography, heat treatment, welding, casting, and mechanical properties testing have been established and continuously improved.</p><p>As a result of its scientific and educational activities hundreds of scientific articles, textbooks, and teaching materials have been published and numerous inventions and patents have been obtained. At the same time the department actively expands its international scientific cooperation by implementing joint projects with research centers from various countries.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'metallurgy_materials_technology';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('metallurgy_materials_technology', 1, NOW()),
    ('metallurgy_materials_technology', 2, NOW()),
    ('metallurgy_materials_technology', 3, NOW()),
    ('metallurgy_materials_technology', 4, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Yüksəkixtisaslı kadr hazırlığı və tədris materiallarının hazırlanması',
        'Yüksəkixtisaslı kadr hazırlığı, müasir tədris metodlarının tətbiqi və ixtisas fənləri üzrə tədris materiallarının hazırlanması'),
    (2, 'Metallurgiya və materialşünaslıq sahəsində elmi tədqiqatlar',
        'Qara və əlvan metallurgiya, materialşünaslıq və termiki emal prosesləri, tökmə və qaynaq texnologiyaları, səth möhkəmləndirilməsi, həmçinin yüksəkmöhkəm ərintilər, ovuntu metallurgiyası və kompozit materialların işlənməsi'),
    (3, 'Sənaye ilə əməkdaşlıq və innovativ texnologiyaların tətbiqi',
        'Neft-qaz və maşınqayırma sahələri üçün materialların işlənməsi, avadanlıqların etibarlılığının artırılması, innovativ texnologiyaların tətbiqi və yerli sənaye müəssisələri ilə birgə layihələrin həyata keçirilməsi'),
    (4, 'Beynəlxalq elmi əməkdaşlıq',
        'Xarici universitet və elmi-tədqiqat institutları ilə birgə layihələrin həyata keçirilməsi, beynəlxalq elmi tədbirlərdə iştirak və birgə nəşrlər ilə akademik mübadilə proqramları')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Training of highly qualified specialists and development of educational materials',
        'Training of highly qualified specialists, application of modern teaching methods and development of educational materials for specialized courses'),
    (2, 'Scientific research in metallurgy and materials science',
        'Research in ferrous and non-ferrous metallurgy, materials science and heat treatment processes, casting and welding technologies, surface strengthening, as well as the development of high-strength alloys, powder metallurgy, and composite materials'),
    (3, 'Industry collaboration and implementation of innovative technologies',
        'Development of materials for oil and gas and machine-building industries, improvement of equipment reliability, implementation of innovative technologies and execution of joint projects with local industrial enterprises'),
    (4, 'International scientific cooperation',
        'Implementation of joint projects with foreign universities and research institutes, participation in international scientific events and engagement in joint publications and academic exchange programs')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'metallurgy_materials_technology',
        'Səyami', 'Hüseynov', 'Sənani oğlu',
        'sayami.huseynov@aztu.edu.az',
        '+994 12 525 24 06 (daxili: 2420)',
        'IV korpus, 106-cı otaq',
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
    'Texnika üzrə fəlsəfə doktoru',
    'Dosent',
    '<p>Hüseynov Səyami Sənani oğlu – texnika üzrə fəlsəfə doktoru, dosent, materialşünaslıq və yeni materialların texnologiyası sahəsində ixtisaslaşmış alimdir. O, materialşünaslıq, metallurgiya və materiallar texnologiyası istiqamətində elmi-pedaqoji fəaliyyət göstərir.</p><p>Onun apardığı elmi-tədqiqat işlərinin nəticələri nüfuzlu elmi nəşrlərdə dərc olunmuş, 50-dən çox yerli və beynəlxalq elmi məqalə, konfrans materialı, patent, monoqrafiya və dərs vəsaitinin müəllifidir.</p><p>Səyami Hüseynov Erasmus Mundus EMINENCE II layihəsi çərçivəsində Polşanın Poznan şəhərində yerləşən Adam Mickiewicz Universitetində postdoktorant tədqiqatçı kimi fəaliyyət göstərmişdir. O, elmi-pedaqoji fəaliyyətində materialşünaslıq sahəsində müasir tədqiqat metodlarının tətbiqi əsasında yüksəkixtisaslı gənc mütəxəssislərin hazırlanmasına və onların elmi-tədqiqat fəaliyyətinə cəlb olunmasına xüsusi əhəmiyyət verir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin "Metallurgiya və materiallar texnologiyası" kafedrasının müdiri vəzifəsində çalışır.</p>',
    '["Ovuntu metallurgiyası", "Forma yaddaşlı ərintilər", "Kompozit materiallar", "Yüksək entropiyalı ərintilər"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'PhD in Technical Sciences',
    'Associate Professor',
    '<p>Sayami Sanani Huseynov is a PhD in technical sciences, associate professor and a specialist in materials science and the technology of new materials. He is actively engaged in scientific and pedagogical activities in the fields of materials science, metallurgy and materials technology.</p><p>The results of his research have been published in reputable scientific journals and he is the author of more than 50 local and international scientific articles, conference proceedings, patents, monographs and teaching materials.</p><p>Within the framework of the Erasmus Mundus EMINENCE II project, Sayami Huseynov conducted postdoctoral research at Adam Mickiewicz University in Poznan, Poland. In his academic work he places particular emphasis on training highly qualified young specialists through the application of modern research methods in materials science and on actively involving them in research activities.</p><p>Currently he serves as the head of the Department of "Metallurgy and Materials Technology" at Azerbaijan Technical University.</p>',
    '["Powder metallurgy", "Shape memory alloys", "Composite materials", "High-entropy alloys"]'::jsonb,
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
    SELECT id, '09:00–17:30', NOW()
    FROM cafedra_directors WHERE cafedra_code = 'metallurgy_materials_technology'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi – Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday – Friday',      NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '2000', '2004', NOW() FROM cafedra_directors WHERE cafedra_code = 'metallurgy_materials_technology'
UNION ALL
SELECT id, '2004', '2006', NOW() FROM cafedra_directors WHERE cafedra_code = 'metallurgy_materials_technology'
UNION ALL
SELECT id, '2006', '2009', NOW() FROM cafedra_directors WHERE cafedra_code = 'metallurgy_materials_technology'
UNION ALL
SELECT id, '2013', '2018', NOW() FROM cafedra_directors WHERE cafedra_code = 'metallurgy_materials_technology';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'metallurgy_materials_technology')
    ORDER BY id DESC
    LIMIT 4
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bakalavr',                          'Azərbaycan Dövlət Neft Akademiyası'),
    (2, 'Magistr',                           'Azərbaycan Dövlət Neft Akademiyası'),
    (3, 'Fəlsəfə doktoru (PhD)',            'Azərbaycan Dövlət Neft Akademiyası'),
    (4, 'Elmlər doktoru (DSc)',              'Azərbaycan Texniki Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bachelor''s degree',                'Azerbaijan State Oil Academy'),
    (2, 'Master''s degree',                  'Azerbaijan State Oil Academy'),
    (3, 'Doctor of Philosophy (PhD)',        'Azerbaijan State Oil Academy'),
    (4, 'Doctor of Sciences (DSc)',          'Azerbaijan Technical University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'metallurgy_materials_technology';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Professors (professorlar)
    ('metallurgy_materials_technology', 'Sübhan',     'Namazov',        'Nadir oğlu',         'subhan.namazov@aztu.edu.az',         '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 1
    ('metallurgy_materials_technology', 'Rəhim',      'Şükürov',        'İzzət oğlu',         'rehim.shukurov@aztu.edu.az',         '+994 12 525 24 06 (daxili: 2240)',  NOW()),  -- 2
    ('metallurgy_materials_technology', 'Arif',        'Məmmədov',       'Tapdıq oğlu',        'arif.memmedov@aztu.edu.az',          '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 3
    ('metallurgy_materials_technology', 'Emel',        'Yıldız',         'Mustafa qızı',       'emel.yildiz@aztu.edu.az',            '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 4
    ('metallurgy_materials_technology', 'Xudaverdi',   'Kərimov',        'Kazım oğlu',         'khudaverdi.karimov@aztu.edu.az',     '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 5
    ('metallurgy_materials_technology', 'Rafiq',       'Hüseynov',       'Qurban oğlu',        'rafiq.huseynov@aztu.edu.az',         '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 6
    ('metallurgy_materials_technology', 'Aqil',        'Babayev',        'İsa oğlu',           'aqil.babayev@aztu.edu.az',           '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 7
    -- Associate Professors (dosentlər)
    ('metallurgy_materials_technology', 'Muxtar',      'Hüseynov',       'Çərkəz oğlu',        'muxtar.huseynov@aztu.edu.az',        '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 8
    ('metallurgy_materials_technology', 'Akif',        'Mənsimov',       'Cavad oğlu',          'akif.mensimov@aztu.edu.az',          '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 9
    ('metallurgy_materials_technology', 'Nailə',       'Mirbabayeva',    'Rəhim qızı',         'naile.mirbabayeva@aztu.edu.az',      '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 10
    ('metallurgy_materials_technology', 'İlham',       'Əliyev',         'Alxan oğlu',          'ilham.aliyev@aztu.edu.az',           '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 11
    ('metallurgy_materials_technology', 'Ramiz',       'Həsənli',        'Kamandar oğlu',       'ramiz.hesenli@aztu.edu.az',          '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 12
    ('metallurgy_materials_technology', 'Səidə',       'Cəfərova',       'Allahverdi qızı',     'seide.ceferova@aztu.edu.az',         '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 13
    ('metallurgy_materials_technology', 'Füzuli',      'Rəsulov',        'Rəsul oğlu',          'fuzuli.resulov@aztu.edu.az',         '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 14
    ('metallurgy_materials_technology', 'Səyyadə',     'Süleymanova',    'Nizami qızı',         'seyyade.suleymanova@aztu.edu.az',    '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 15
    ('metallurgy_materials_technology', 'İlhamə',      'Həmdullayeva',   'Həmdulla qızı',       'ilhame.hemdullayeva@aztu.edu.az',    '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 16
    ('metallurgy_materials_technology', 'Nizami',       'Poladov',        'Qədim oğlu',          'nizami_poladov@aztu.edu.az',         '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 17
    ('metallurgy_materials_technology', 'Zənurə',      'Namazova',       'Əsgər qızı',          'zenure.namazova@aztu.edu.az',        '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 18
    -- Senior Lecturers (baş müəllimlər)
    ('metallurgy_materials_technology', 'Lalə',        'Əzimova',        'Hacıağa qızı',        'lale.ezimova@aztu.edu.az',           '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 19
    ('metallurgy_materials_technology', 'Taleh',       'Tağıyev',        'Əyyam oğlu',          'taleh.taqiyev@aztu.edu.az',          '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 20
    ('metallurgy_materials_technology', 'Bəturə',      'Musurzayeva',    'Bəybala qızı',        'beture.musurzayeva@aztu.edu.az',     '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 21
    ('metallurgy_materials_technology', 'Günal',       'Hüseynova',      'Malik qızı',          'gunal.huseynova@aztu.edu.az',        '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 22
    -- Assistants (assistentlər)
    ('metallurgy_materials_technology', 'Kamil',       'Məmmədov',       'Ramiz oğlu',          'kamil.memmedov@aztu.edu.az',         '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 23
    ('metallurgy_materials_technology', 'İslam',       'Əlyarzadə',      'Sabir oğlu',          'islam.alyarzade@aztu.edu.az',        '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 24
    -- Teaching Assistants (müəllim köməkçiləri)
    ('metallurgy_materials_technology', 'Sevinc',      'Heybətova',      'Adil qızı',           'sevinc.heybetova@aztu.edu.az',       '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 25
    ('metallurgy_materials_technology', 'Aysel',       'Hüseynova',      'İnsafəli qızı',       'aysel.huseynova@aztu.edu.az',        '+994 12 525 24 06 (daxili: 2241)',  NOW()),  -- 26
    -- Clerk (kargüzar)
    ('metallurgy_materials_technology', 'Könül',       'Qocayeva',       'Ənvər qızı',          'konul.gocayeva@aztu.edu.az',         '+994 12 525 24 06 (daxili: 2241)',  NOW())   -- 27
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Professors
    (1,  'Metallurgiya və materiallar texnologiyası kafedrası, professor',              'Professor',  't.e.d.'),
    (2,  'Metallurgiya və materiallar texnologiyası kafedrası, məsləhətçi professor',   'Professor',  't.e.n.'),
    (3,  'Metallurgiya və materiallar texnologiyası kafedrası, məsləhətçi professor',   'Professor',  't.e.d.'),
    (4,  'Metallurgiya və materiallar texnologiyası kafedrası, tədqiqatçı professor',   NULL,         't.e.d.'),
    (5,  'Metallurgiya və materiallar texnologiyası kafedrası, tədqiqatçı professor',   NULL,         't.e.d.'),
    (6,  'Metallurgiya və materiallar texnologiyası kafedrası, professor',              'Professor',  't.e.d.'),
    (7,  'Metallurgiya və materiallar texnologiyası kafedrası, professor',              'Dosent',     't.e.n.'),
    -- Associate Professors
    (8,  'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  'Dosent',  't.e.n.'),
    (9,  'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  NULL,      't.e.n.'),
    (10, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  'Dosent',  't.e.n.'),
    (11, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  NULL,      't.e.n.'),
    (12, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  'Dosent',  't.e.n.'),
    (13, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  'Dosent',  't.e.n.'),
    (14, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  'Dosent',  't.e.n.'),
    (15, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  'Dosent',  't.e.n.'),
    (16, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  'Dosent',  't.e.n.'),
    (17, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  'Dosent',  't.ü.f.d.'),
    (18, 'Metallurgiya və materiallar texnologiyası kafedrası, dosent',  NULL,      't.ü.f.d.'),
    -- Senior Lecturers
    (19, 'Metallurgiya və materiallar texnologiyası kafedrası, baş müəllim',  NULL,  NULL),
    (20, 'Metallurgiya və materiallar texnologiyası kafedrası, baş müəllim',  NULL,  NULL),
    (21, 'Metallurgiya və materiallar texnologiyası kafedrası, baş müəllim',  NULL,  NULL),
    (22, 'Metallurgiya və materiallar texnologiyası kafedrası, baş müəllim',  NULL,  NULL),
    -- Assistants
    (23, 'Metallurgiya və materiallar texnologiyası kafedrası, assistent',    NULL,  't.ü.f.d.'),
    (24, 'Metallurgiya və materiallar texnologiyası kafedrası, assistent',    NULL,  NULL),
    -- Teaching Assistants
    (25, 'Metallurgiya və materiallar texnologiyası kafedrası, müəllim köməkçisi',  NULL,  NULL),
    (26, 'Metallurgiya və materiallar texnologiyası kafedrası, müəllim köməkçisi',  NULL,  NULL),
    -- Clerk
    (27, 'Metallurgiya və materiallar texnologiyası kafedrası, kargüzar',           NULL,  NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Professors
    (1,  'Department of Metallurgy and Materials Technology, Professor',              'Professor',             't.e.d.'),
    (2,  'Department of Metallurgy and Materials Technology, Advisory Professor',     'Professor',             't.e.n.'),
    (3,  'Department of Metallurgy and Materials Technology, Advisory Professor',     'Professor',             't.e.d.'),
    (4,  'Department of Metallurgy and Materials Technology, Research Professor',     NULL,                    't.e.d.'),
    (5,  'Department of Metallurgy and Materials Technology, Research Professor',     NULL,                    't.e.d.'),
    (6,  'Department of Metallurgy and Materials Technology, Professor',              'Professor',             't.e.d.'),
    (7,  'Department of Metallurgy and Materials Technology, Professor',              'Associate Professor',   't.e.n.'),
    -- Associate Professors
    (8,  'Department of Metallurgy and Materials Technology, Associate Professor',    'Associate Professor',   't.e.n.'),
    (9,  'Department of Metallurgy and Materials Technology, Associate Professor',    NULL,                    't.e.n.'),
    (10, 'Department of Metallurgy and Materials Technology, Associate Professor',    'Associate Professor',   't.e.n.'),
    (11, 'Department of Metallurgy and Materials Technology, Associate Professor',    NULL,                    't.e.n.'),
    (12, 'Department of Metallurgy and Materials Technology, Associate Professor',    'Associate Professor',   't.e.n.'),
    (13, 'Department of Metallurgy and Materials Technology, Associate Professor',    'Associate Professor',   't.e.n.'),
    (14, 'Department of Metallurgy and Materials Technology, Associate Professor',    'Associate Professor',   't.e.n.'),
    (15, 'Department of Metallurgy and Materials Technology, Associate Professor',    'Associate Professor',   't.e.n.'),
    (16, 'Department of Metallurgy and Materials Technology, Associate Professor',    'Associate Professor',   't.e.n.'),
    (17, 'Department of Metallurgy and Materials Technology, Associate Professor',    'Associate Professor',   't.ü.f.d.'),
    (18, 'Department of Metallurgy and Materials Technology, Associate Professor',    NULL,                    't.ü.f.d.'),
    -- Senior Lecturers
    (19, 'Department of Metallurgy and Materials Technology, Senior Lecturer',        NULL,                    NULL),
    (20, 'Department of Metallurgy and Materials Technology, Senior Lecturer',        NULL,                    NULL),
    (21, 'Department of Metallurgy and Materials Technology, Senior Lecturer',        NULL,                    NULL),
    (22, 'Department of Metallurgy and Materials Technology, Senior Lecturer',        NULL,                    NULL),
    -- Assistants
    (23, 'Department of Metallurgy and Materials Technology, Assistant',              NULL,                    't.ü.f.d.'),
    (24, 'Department of Metallurgy and Materials Technology, Assistant',              NULL,                    NULL),
    -- Teaching Assistants
    (25, 'Department of Metallurgy and Materials Technology, Teaching Assistant',     NULL,                    NULL),
    (26, 'Department of Metallurgy and Materials Technology, Teaching Assistant',     NULL,                    NULL),
    -- Clerk
    (27, 'Department of Metallurgy and Materials Technology, Administrative Clerk',   NULL,                    NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
