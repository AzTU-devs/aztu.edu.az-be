-- ============================================================
-- Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası — Full DB Import
-- cafedra_code: 'machine_design_mechatronics_industrial_technologies'
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
    'machine_design_mechatronics_industrial_technologies',
    4, 4, 3, 29, 7, 22, 5,
    '[2, 4, 7, 9, 11, 12]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'machine_design_mechatronics_industrial_technologies',
    'az',
    'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası',
    '<p>"Maşın dizaynı, mexatronika və sənaye texnologiyaları" kafedrası Azərbaycan Texniki Universitetində aparılan struktur islahatları çərçivəsində 2025-ci ildə "Maşın dizaynı və sənaye texnologiyaları" kafedrası ilə "Mexatronika" kafedrasının birləşdirilməsi nəticəsində yaradılmışdır. Kafedra müasir mühəndislik sahələrində təhsil və elmi-tədqiqat fəaliyyətinin inkişafını təmin edən mühüm akademik struktur bölmələrindən biri kimi fəaliyyət göstərir.</p><p>Kafedranın formalaşması və inkişafı uzunmüddətli tarixi mərhələləri əhatə edir. Onun elmi və pedaqoji əsasları 1950-ci ildə yaradılmış "Mexanizmlər nəzəriyyəsi, maşın detalları və yükqaldırıcı-nəqledici mexanizmlər" kafedrasına, eləcə də "Tərsimi həndəsə və qrafika" kafedrasına söykənir. Daha sonra, 1961-ci ildə fəaliyyətə başlayan "İstehsal proseslərinin avtomatlaşdırılması və hesablama texnikası" kafedrası da bu istiqamətdə mühüm rol oynamış, mühəndislik təhsilinin və elmi tədqiqatların inkişafına əhəmiyyətli töhfələr vermişdir.</p><p>Kafedranın təşkil olunduğu bazada müxtəlif ixtisaslaşmış struktur bölmələri formalaşmış, onların fəaliyyəti nəticəsində maşınşünaslıq, mexatronika və robototexnika, proseslərin avtomatlaşdırılması və müxtəlif sənaye texnologiyaları sahələrində güclü elmi-pedaqoji məktəblər yaranmışdır.</p><p>Hazırda kafedra Azərbaycan Texniki Universitetinin ən böyük və yüksək elmi potensiala malik struktur bölmələrindən biri kimi fəaliyyət göstərir. Kafedrada çoxsaylı yüksək ixtisaslı elmi-pedaqoji kadrlar çalışır və bu potensial müasir mühəndislik problemlərinin həlli, innovativ texnologiyaların tətbiqi və rəqabətqabiliyyətli mütəxəssislərin hazırlanması istiqamətində mühüm rol oynayır.</p>',
    NOW()
),
(
    'machine_design_mechatronics_industrial_technologies',
    'en',
    'Department of Machine Design, Mechatronics and Industrial Technologies',
    '<p>The Department of Machine Design, Mechatronics and Industrial Technologies was established in 2025 as part of the structural reforms conducted at Azerbaijan Technical University, resulting from the merger of the "Machine Design and Industrial Technologies" and "Mechatronics" departments. The department operates as one of the key academic units ensuring the advancement of education and scientific research in modern engineering fields.</p><p>The formation and development of the department encompass long-term historical stages. Its scientific and pedagogical foundations are rooted in the "Theory of Mechanisms, Machine Components, and Hoisting-Transporting Mechanisms" department, as well as the "Descriptive Geometry and Graphics" department, both established in 1950. Subsequently, the "Automation of Production Processes and Computing Technology" department, which began its activities in 1961, played a vital role in this direction, making significant contributions to the development of engineering education and scientific research.</p><p>Various specialized structural units have been formed based on the department''s foundation. Through their activities, strong scientific-pedagogical schools have emerged in the fields of machine science, mechatronics and robotics, process automation, and various industrial technologies.</p><p>Currently, the department functions as one of the largest structural divisions of Azerbaijan Technical University, possessing high scientific potential. A large number of highly qualified scientific-pedagogical personnel work at the department, and this potential plays a crucial role in solving modern engineering problems, applying innovative technologies, and training competitive specialists.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'machine_design_mechatronics_industrial_technologies';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('machine_design_mechatronics_industrial_technologies', 1, NOW()),
    ('machine_design_mechatronics_industrial_technologies', 2, NOW()),
    ('machine_design_mechatronics_industrial_technologies', 3, NOW()),
    ('machine_design_mechatronics_industrial_technologies', 4, NOW()),
    ('machine_design_mechatronics_industrial_technologies', 5, NOW()),
    ('machine_design_mechatronics_industrial_technologies', 6, NOW()),
    ('machine_design_mechatronics_industrial_technologies', 7, NOW()),
    ('machine_design_mechatronics_industrial_technologies', 8, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Müasir və beynəlxalq standartlara uyğun tədris proqramlarının hazırlanması və tətbiqi',
        'Mexatronika və robototexnika, proseslərin avtomatlaşdırılması, qida mühəndisliyi və sənaye mühəndisliyi sahələri üzrə müasir və beynəlxalq standartlara uyğun tədris proqramlarının hazırlanması və tətbiqi'),
    (2, 'Yüksək ixtisaslı kadrların hazırlanması',
        'Sənaye və dövlət qurumları ilə əməkdaşlıq çərçivəsində praktiki bacarıqlara malik bakalavriatura, magistratura və doktorantura səviyyələrində yüksək ixtisaslı kadrların hazırlanması'),
    (3, 'Fundamental və tətbiqi tədqiqatların həyata keçirilməsi',
        'Maşın dizaynı, maşın və mexanizmlər nəzəriyyəsi, mühəndis qrafikası, idarəetmə və sənaye avtomatlaşdırılması, mexatronika və robototexnika, eləcə də müxtəlif sənaye texnologiyaları istiqamətləri üzrə fundamental və tətbiqi tədqiqatların həyata keçirilməsi'),
    (4, 'Müasir mühəndis proqram təminatların və innovativ təlim metodlarının tətbiqi',
        'Tədris prosesində müasir mühəndis proqram təminatların və innovativ təlim metodlarının tətbiq olunması'),
    (5, 'Tələbələrin elmi-tədqiqat fəaliyyətinə cəlb edilməsi',
        'Tələbələrin elmi-tədqiqat fəaliyyətinə cəlb edilməsi, onların yaradıcılıq və analitik bacarıqlarının inkişaf etdirilməsi'),
    (6, 'Sənaye müəssisələri ilə əməkdaşlığın genişləndirilməsi',
        'Sənaye müəssisələri ilə əməkdaşlığın genişləndirilməsi və praktiki layihələrin yerinə yetirilməsi'),
    (7, 'İnnovativ layihələrin hazırlanması',
        'İnnovativ layihələrin hazırlanması və mühəndislik sahəsində yeni texnoloji həllərin tətbiqinin təşviq edilməsi'),
    (8, 'Beynəlxalq əməkdaşlıq çərçivəsində birgə elmi-tədqiqat işləri',
        'Beynəlxalq əməkdaşlıq çərçivəsində birgə elmi-tədqiqat işlərinin yerinə yetirilməsi, tələbə və müəllim mobilliyinin təmin edilməsi')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Development and implementation of modern curriculum',
        'Development and implementation of modern curriculum in line with international standards in the fields of mechatronics and robotics, process automation, food engineering, and industrial engineering'),
    (2, 'Training of highly qualified personnel',
        'Training of highly qualified personnel at the bachelor''s, master''s, and doctoral levels with practical skills through cooperation with industrial enterprises and government agencies'),
    (3, 'Conducting fundamental and applied research',
        'Conducting fundamental and applied research in machine design, theory of machines and mechanisms, engineering graphics, control and industrial automation, mechatronics and robotics, as well as various industrial technologies'),
    (4, 'Application of modern engineering software and innovative teaching methods',
        'Application of modern engineering software and innovative teaching methods within the educational process'),
    (5, 'Involving students in scientific-research activities',
        'Involving students in scientific-research activities and developing their creative and analytical skills'),
    (6, 'Expanding cooperation with industrial enterprises',
        'Expanding cooperation with industrial enterprises and executing practical projects'),
    (7, 'Development of innovative projects',
        'Development of innovative projects and promotion of new technological solutions in the field of engineering'),
    (8, 'Joint scientific-research work within international cooperation',
        'Execution of joint scientific-research work within the framework of international cooperation, and ensuring student and faculty mobility')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'machine_design_mechatronics_industrial_technologies',
        'İsa', 'Xəlilov', 'Əli oğlu',
        'khalilov@aztu.edu.az',
        '+994 12 525 24 06',
        'I-III korpus, 217-ci otaq',
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
    '<p>Xəlilov İsa Əli oğlu — texnika elmləri doktoru, professor, maşınşünaslıq sahəsində ixtisaslaşmış alim və pedaqoqdur. O, uzun illərdir maşınşünaslıq, tətbiqi mexanika, maşınların etibarlığı, konstruksiyaetmənin əsasları istiqamətlərində elmi və pedaqoji fəaliyyət göstərir. Alimin elmi tədqiqatlarının əsas istiqamətlərinə maşın intiqallarının sistemli analizi, muftaların seçilməsinin nəzəri əsasları və mexaniki sistemlərin etibarlılığının artırılması daxildir. Bu sahələr üzrə apardığı tədqiqatlar mühəndislik elminin inkişafına mühüm töhfələr vermiş, nəticələri nüfuzlu elmi nəşrlərdə dərc olunmuşdur.</p><p>Xəlilov İ.Ə. pedaqoji fəaliyyətində müasir mühəndislik yanaşmalarını tətbiq edərək tələbələrin analitik düşünmə qabiliyyətinin formalaşdırılmasına, onların elmi-tədqiqat fəaliyyətinə cəlb olunmasına və yüksək ixtisaslı mühəndis kadrların hazırlanmasına xüsusi önəm verir. Hazırda o, Azərbaycan Texniki Universitetində "Maşın dizaynı, mexatronika və sənaye texnologiyaları" kafedrasının müdiri vəzifəsində çalışır. Eyni zamanda universitetin elmi və ictimai həyatında fəal iştirak edir, Dissertasiya Şurasının üzvüdür. O, 170-dən çox elmi-texniki və metodik əsərin müəllifidir. Bu əsərlərə 1 monoqrafiya, 3 dərslik, 4 dərs vəsaiti, 20 elmi-metodik məcmuə və 2 texniki lüğət kitabı daxildir. Alimin elmi məqalələrinin bir qismi beynəlxalq WoS və SCOPUS bazalarında indekslənmişdir. Elmi və pedaqoji fəaliyyətinə görə 2011 və 2015-ci illərdə Azərbaycan Respublikası Təhsil Nazirliyinin Fəxri fərmanı ilə təltif olunmuş, 2020-ci ildə isə "Əməkdar müəllim" fəxri adına layiq görülmüşdür.</p>',
    '["Maşın intiqallarının sistemli analizi", "Muftaların seçilməsi əsaslarının işlənməsi", "Maşın mexanizmlərinin analizi və sintezi", "Mexaniki sistemlərin etibarlılığı və effektivliyi"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Technical Sciences',
    'Professor',
    '<p>Khalilov Isa Ali oglu — Doctor of Technical Sciences, Professor, is a scientist and educator specializing in the field of machine science. For many years, he has been engaged in scientific and pedagogical activities in the areas of machine science, applied mechanics, machine reliability, and the fundamentals of design. The main directions of the scientist''s research include the systemic analysis of machine drives, the theoretical foundations of coupling selection, and increasing the reliability of mechanical systems. His research in these fields has made significant contributions to the development of engineering science, and his results have been published in prestigious scientific journals.</p><p>In his pedagogical activity, I.A. Khalilov applies modern engineering approaches, placing special importance on the formation of students'' analytical thinking abilities, their involvement in scientific research, and the training of highly qualified engineering personnel. Currently, he serves as the Head of the Department of "Machine Design, Mechatronics, and Industrial Technologies" at the Azerbaijan Technical University. At the same time, he actively participates in the scientific and social life of the university and is a member of the Dissertation Council. He is the author of more than 170 scientific-technical and methodical works, including 1 monograph, 3 textbooks, 4 study guides, 20 scientific-methodical collections, and 2 technical dictionaries. A portion of the scientist''s research articles is indexed in the international Web of Science and SCOPUS databases. For his scientific and pedagogical activities, he was awarded the Honorary Decree of the Ministry of Education of the Republic of Azerbaijan in 2011 and 2015, and in 2020, he was honored with the title of "Honored Teacher."</p>',
    '["Systematic analysis of machine drives", "Development of the foundations for coupling selection", "Analysis and synthesis of machine mechanisms", "Reliability and efficiency of mechanical systems"]'::jsonb,
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
    SELECT id, '12:00–13:00', NOW()
    FROM cafedra_directors WHERE cafedra_code = 'machine_design_mechatronics_industrial_technologies'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Çərşənbə axşamı, Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Tuesday, Friday',          NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1978', '1983', NOW() FROM cafedra_directors WHERE cafedra_code = 'machine_design_mechatronics_industrial_technologies'
UNION ALL
SELECT id, '1984', '1987', NOW() FROM cafedra_directors WHERE cafedra_code = 'machine_design_mechatronics_industrial_technologies'
UNION ALL
SELECT id, '2007', '2012', NOW() FROM cafedra_directors WHERE cafedra_code = 'machine_design_mechatronics_industrial_technologies';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'machine_design_mechatronics_industrial_technologies')
    ORDER BY id DESC
    LIMIT 3
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Mühəndis-mexanik',                 'Azərbaycan Politexnik İnstitutu (indiki Azərbaycan Texniki Universiteti)'),
    (2, 'Elmlər namizədi (PhD)',            'Azərbaycan Texniki Universiteti'),
    (3, 'Elmlər doktoru (DSc)',             'Azərbaycan Texniki Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Mechanical Engineer',                              'Azerbaijan Polytechnic Institute (currently Azerbaijan Technical University)'),
    (2, 'Candidate of Sciences (PhD)',                      'Azerbaijan Technical University'),
    (3, 'Doctor of Sciences (DSc)',                         'Azerbaijan Technical University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'machine_design_mechatronics_industrial_technologies';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Professors (professorlar)
    ('machine_design_mechatronics_industrial_technologies', 'Rasim',       'Əlizadə',       'İsmayıl oğlu',     'rasima@aztu.edu.az',                  '+994 50-679-59-65',  NOW()),  -- 1
    ('machine_design_mechatronics_industrial_technologies', 'Orxan',       'Əfəndiyev',      'Ziyəddin',          'orxan.efendiyev@aztu.edu.az',         '+994 55-222-70-00',  NOW()),  -- 2
    ('machine_design_mechatronics_industrial_technologies', 'Bəyalı',     'Əhmədov',        'Bəhcət',            'ahmedov.beyali@aztu.edu.az',          '+994 70-233-44-82',  NOW()),  -- 3
    ('machine_design_mechatronics_industrial_technologies', 'İftixar',    'Çələbi',         'Qurbanəli',         'i_chalabi@aztu.edu.az',               '+994 51-850-26-01',  NOW()),  -- 4
    ('machine_design_mechatronics_industrial_technologies', 'Uğurlu',     'Nadirov',        'Məhəmməd',          'ugurlu.nadirov@aztu.edu.az',          '+994 55-512-77-58',  NOW()),  -- 5
    -- Associate Professors (dosentlər)
    ('machine_design_mechatronics_industrial_technologies', 'Manafaddin', 'Namazov',        'Bəşir',             'manafeddin.namazov@aztu.edu.az',      '+994 50-346-57-07',  NOW()),  -- 6
    ('machine_design_mechatronics_industrial_technologies', 'Əhməd',     'İmanov',         'Süleyman',          'ehmed.imanov@aztu.edu.az',            '+994 10-308-70-90',  NOW()),  -- 7
    ('machine_design_mechatronics_industrial_technologies', 'Savalan',    'Kərimov',        'Xanlar',            'savalan.kerimov@aztu.edu.az',         '+994 50-630-99-13',  NOW()),  -- 8
    ('machine_design_mechatronics_industrial_technologies', 'Vahid',      'Fərhadov',       'Qara',              'vahid.farhadov@aztu.edu.az',          '+994 55-750-16-39',  NOW()),  -- 9
    ('machine_design_mechatronics_industrial_technologies', 'Əzizağa',   'Əzizov',         'Ağahüseyn',         'ezizaga.ezizov@aztu.edu.az',          '+994 50-611-12-71',  NOW()),  -- 10
    ('machine_design_mechatronics_industrial_technologies', 'Ramiz',      'Əhmədov',        'Mürsəl',            'ramizahmadov@aztu.edu.az',            '+994 50-424-58-67',  NOW()),  -- 11
    ('machine_design_mechatronics_industrial_technologies', 'Rəfail',    'Eyyubov',        'Həmid',             'rafayil.eyyubov@aztu.edu.az',         '+994 50-451-30-49',  NOW()),  -- 12
    ('machine_design_mechatronics_industrial_technologies', 'İmran',     'Yolçuyev',       'Alı',               'imran_yolchuyev@aztu.edu.az',         '+994 50-346-46-72',  NOW()),  -- 13
    ('machine_design_mechatronics_industrial_technologies', 'Firuz',      'Məmmədov',       'Həbibulla',         'firuz.memmedov@aztu.edu.az',          '+994 70-877-75-07',  NOW()),  -- 14
    ('machine_design_mechatronics_industrial_technologies', 'Eldar',      'Əliyev',         'Abbas',             'eldar.aliyev@aztu.edu.az',            '+994 50-317-03-08',  NOW()),  -- 15
    ('machine_design_mechatronics_industrial_technologies', 'Rəşid',     'Qasımov',        'Cümşüd',            'reshid.qasimov@aztu.edu.az',          '+994 50-610-54-88',  NOW()),  -- 16
    ('machine_design_mechatronics_industrial_technologies', 'Şahin',     'Çərkəsov',       'Böyükağa',          'cerkesov.sahin@aztu.edu.az',          '+994 55-578-37-02',  NOW()),  -- 17
    ('machine_design_mechatronics_industrial_technologies', 'Şahid',     'Yusubov',        'Tahir',             'shahidyusub@aztu.edu.az',             '+994 50-331-58-52',  NOW()),  -- 18
    ('machine_design_mechatronics_industrial_technologies', 'Zakir',      'Qələndərov',     'Səlvər',            'zakir.qelenderov@aztu.edu.az',        '+994 55-635-82-30',  NOW()),  -- 19
    ('machine_design_mechatronics_industrial_technologies', 'Fərrux',    'Məmmədov',       'Qara',              'mamedov.ferrux@aztu.edu.az',          '+994 50-312-67-71',  NOW()),  -- 20
    ('machine_design_mechatronics_industrial_technologies', 'Xalidə',    'Hacıyeva',       'Əbdülqafar',        'xalida.haciyeva@aztu.edu.az',         '+994 99-745-82-12',  NOW()),  -- 21
    ('machine_design_mechatronics_industrial_technologies', 'Afaq',       'Məmmədova',      'Tofiq',             'afaq.mammadova@aztu.edu.az',          '+994 50-332-48-78',  NOW()),  -- 22
    ('machine_design_mechatronics_industrial_technologies', 'Qoşqar',    'Rəsulov',        'Nəriman',           'qoshqarrasul@aztu.edu.az',            '+994 51-700-09-06',  NOW()),  -- 23
    ('machine_design_mechatronics_industrial_technologies', 'Bəhruz',    'Əhmədov',        'Cabbar',            'ahmedov_bahruz@aztu.edu.az',          '+994 55-766-36-83',  NOW()),  -- 24
    ('machine_design_mechatronics_industrial_technologies', 'Elsəvər',   'Fərzəliyev',     'Baba',              'elsever.ferzeliyev@aztu.edu.az',      '+994 77-403-00-26',  NOW()),  -- 25
    ('machine_design_mechatronics_industrial_technologies', 'Günəş',     'Nəsrullayeva',   'Məzahir',           'gunash.nasrullayeva@aztu.edu.az',     '+994 50-357-07-37',  NOW()),  -- 26
    ('machine_design_mechatronics_industrial_technologies', 'Mehriban',   'Yusifova',       'Rauf',              'mehriban.yusifova@aztu.edu.az',       '+994 55-743-67-34',  NOW()),  -- 27
    -- Senior Lecturers (baş müəllimlər)
    ('machine_design_mechatronics_industrial_technologies', 'Nadir',      'Məmmədov',       'Müzəffər',          'nadir.memmedov@aztu.edu.az',          '+994 70-361-78-38',  NOW()),  -- 28
    ('machine_design_mechatronics_industrial_technologies', 'Asif',       'Qasımov',        'Yusif',             'asif.qasimov@aztu.edu.az',            '+994 50-341-60-16',  NOW()),  -- 29
    ('machine_design_mechatronics_industrial_technologies', 'Səmayə',    'Bağırova',       'Əli',               'semaye.bagirova@aztu.edu.az',         '+994 50-734-54-34',  NOW()),  -- 30
    ('machine_design_mechatronics_industrial_technologies', 'Yasəmən',   'Əfəndiyeva',     'Firudin',           'yasemen.efendiyeva@aztu.edu.az',      '+994 70-599-02-75',  NOW()),  -- 31
    ('machine_design_mechatronics_industrial_technologies', 'Sevinc',     'Əliyeva',        'Niyazi',            'sevinc.eliyeva@aztu.edu.az',          '+994 55-680-02-49',  NOW()),  -- 32
    ('machine_design_mechatronics_industrial_technologies', 'Anar',       'Hacıyev',        'Babaqədir',         'anar.hajiyev@aztu.edu.az',            '+994 50-873-06-80',  NOW()),  -- 33
    ('machine_design_mechatronics_industrial_technologies', 'Bəhruz',    'Cəbrayılov',     'Cəlal',             'behruz.jabrayilov@aztu.edu.az',       '+994 10-525-11-46',  NOW()),  -- 34
    ('machine_design_mechatronics_industrial_technologies', 'Şəbnəm',   'İsmayılova',     'Vidadi',            'shebinem.ismayilova@aztu.edu.az',     '+994 70-350-54-43',  NOW()),  -- 35
    ('machine_design_mechatronics_industrial_technologies', 'Səkinəxanım', 'İsayeva',      'Namiq',             'sakinakhanim.isayeva@aztu.edu.az',    '+994 77-523-50-78',  NOW()),  -- 36
    ('machine_design_mechatronics_industrial_technologies', 'Aliyə',     'Qocayeva',       'Burxan',            'aliya.gojayeva@aztu.edu.az',          '+994 55-268-99-59',  NOW()),  -- 37
    ('machine_design_mechatronics_industrial_technologies', 'Nicat',      'Məjlumov',       'Bəşir oğlu',       'mecnunovnicat63@aztu.edu.az',         '+994 51-367-04-59',  NOW()),  -- 38
    ('machine_design_mechatronics_industrial_technologies', 'Zaur',       'Aşirov',         'Paşa',              'zaurashirov@aztu.edu.az',             '+994 70-928-53-99',  NOW()),  -- 39
    -- Assistants (assistentlər)
    ('machine_design_mechatronics_industrial_technologies', 'İlkin',     'Əliyev',         'İdris',             'ilkin.aliyev@aztu.edu.az',            '+994 50-966-19-99',  NOW()),  -- 40
    ('machine_design_mechatronics_industrial_technologies', 'Ayçillər',  'Aslanova',       'Telman',            'ayciller.aslanova@aztu.edu.az',       '+994 51-658-50-30',  NOW()),  -- 41
    ('machine_design_mechatronics_industrial_technologies', 'Vüqar',     'Hüseynov',       'Hicran',            'vugar.huseynov@aztu.edu.az',          '+994 55-321-64-46',  NOW()),  -- 42
    ('machine_design_mechatronics_industrial_technologies', 'Bibixanım', 'Cabbarlı',       'Rəvayət qızı',     'bibikhanim.jabbarli@aztu.edu.az',     '+994 51-397-40-63',  NOW()),  -- 43
    -- Teaching Assistants (müəllim köməkçiləri)
    ('machine_design_mechatronics_industrial_technologies', 'Sevda',      'Adgözəlova',     'Ağakərim',          'sevda.adgezalova@aztu.edu.az',        '+994 50-419-30-43',  NOW()),  -- 44
    ('machine_design_mechatronics_industrial_technologies', 'Leyla',      'Aslanova',       'Hafiz',             'leyla@aztu.edu.az',                   '+994 70-292-02-84',  NOW()),  -- 45
    ('machine_design_mechatronics_industrial_technologies', 'Südabə',    'Quliyeva',       'Fərhad',            'sudaba.quliyeva@aztu.edu.az',         '+994 50-497-14-62',  NOW()),  -- 46
    ('machine_design_mechatronics_industrial_technologies', 'Natəvan',   'Sultanova',      'Əli',               'natavan.sultanova@aztu.edu.az',       '+994 55-597-04-61',  NOW()),  -- 47
    ('machine_design_mechatronics_industrial_technologies', 'Nərmin',    'Əliyeva',        'Bəysəfa',           'narmin.aliyeva@aztu.edu.az',          '+994 70-961-55-95',  NOW()),  -- 48
    -- Clerk (kargüzar)
    ('machine_design_mechatronics_industrial_technologies', 'Lalə',      'Fərzəliyeva',    'Bədəl',             'lale.ferzeliyeva@aztu.edu.az',        '+994 55-871-72-23',  NOW())   -- 49
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Professors
    (1,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, məsləhətçi professor',  'Professor',              't.e.d.'),
    (2,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, məsləhətçi professor',  'Professor',              't.e.d.'),
    (3,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, professor',             'Professor',              't.e.d.'),
    (4,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, tədqiqatçı-professor',  'Tədqiqatçı-professor',   't.e.d.'),
    (5,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, professor',             'Professor',              't.e.d.'),
    -- Associate Professors
    (6,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (7,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (8,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (9,  'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (10, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (11, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (12, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 'f.r.e.n.'),
    (13, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.f.d.'),
    (14, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (15, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (16, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (17, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (18, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (19, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.f.d.'),
    (20, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (21, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 'f.r.e.n.'),
    (22, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (23, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.ü.f.d.'),
    (24, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.f.d.'),
    (25, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 't.e.n.'),
    (26, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 'i.f.d.'),
    (27, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, dosent',  'Dosent', 'b.f.d.'),
    -- Senior Lecturers
    (28, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  NULL,          NULL),
    (29, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  NULL,          NULL),
    (30, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  NULL,          NULL),
    (31, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  NULL,          NULL),
    (32, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  NULL,          NULL),
    (33, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  NULL,          NULL),
    (34, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  'Doktorant',   NULL),
    (35, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  'Doktorant',   NULL),
    (36, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  'Doktorant',   NULL),
    (37, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  'Doktorant',   NULL),
    (38, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  'Doktorant',   NULL),
    (39, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, baş müəllim',  'Doktorant',   NULL),
    -- Assistants
    (40, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, assistent',    NULL,          NULL),
    (41, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, assistent',    NULL,          NULL),
    (42, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, assistent',    NULL,          NULL),
    (43, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, assistent',    'Doktorant',   NULL),
    -- Teaching Assistants
    (44, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, müəllim köməkçisi',  NULL,    NULL),
    (45, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, müəllim köməkçisi',  NULL,    NULL),
    (46, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, müəllim köməkçisi',  NULL,    NULL),
    (47, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, müəllim köməkçisi',  NULL,    NULL),
    (48, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, müəllim köməkçisi',  NULL,    NULL),
    -- Clerk
    (49, 'Maşın dizaynı, mexatronika və sənaye texnologiyaları kafedrası, kargüzar',          NULL,    NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Professors
    (1,  'Department of Machine Design, Mechatronics and Industrial Technologies, Consultant Professor',  'Professor',            't.e.d.'),
    (2,  'Department of Machine Design, Mechatronics and Industrial Technologies, Consultant Professor',  'Professor',            't.e.d.'),
    (3,  'Department of Machine Design, Mechatronics and Industrial Technologies, Professor',             'Professor',            't.e.d.'),
    (4,  'Department of Machine Design, Mechatronics and Industrial Technologies, Research Professor',    'Research Professor',   't.e.d.'),
    (5,  'Department of Machine Design, Mechatronics and Industrial Technologies, Professor',             'Professor',            't.e.d.'),
    -- Associate Professors
    (6,  'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (7,  'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (8,  'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (9,  'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (10, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (11, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (12, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  'f.r.e.n.'),
    (13, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.f.d.'),
    (14, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (15, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (16, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (17, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (18, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (19, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.f.d.'),
    (20, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (21, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  'f.r.e.n.'),
    (22, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (23, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.ü.f.d.'),
    (24, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.f.d.'),
    (25, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  't.e.n.'),
    (26, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  'i.f.d.'),
    (27, 'Department of Machine Design, Mechatronics and Industrial Technologies, Associate Professor',   'Associate Professor',  'b.f.d.'),
    -- Senior Lecturers
    (28, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       NULL,                   NULL),
    (29, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       NULL,                   NULL),
    (30, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       NULL,                   NULL),
    (31, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       NULL,                   NULL),
    (32, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       NULL,                   NULL),
    (33, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       NULL,                   NULL),
    (34, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       'PhD Student',          NULL),
    (35, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       'PhD Student',          NULL),
    (36, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       'PhD Student',          NULL),
    (37, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       'PhD Student',          NULL),
    (38, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       'PhD Student',          NULL),
    (39, 'Department of Machine Design, Mechatronics and Industrial Technologies, Senior Lecturer',       'PhD Student',          NULL),
    -- Assistants
    (40, 'Department of Machine Design, Mechatronics and Industrial Technologies, Assistant',             NULL,                   NULL),
    (41, 'Department of Machine Design, Mechatronics and Industrial Technologies, Assistant',             NULL,                   NULL),
    (42, 'Department of Machine Design, Mechatronics and Industrial Technologies, Assistant',             NULL,                   NULL),
    (43, 'Department of Machine Design, Mechatronics and Industrial Technologies, Assistant',             'PhD Student',          NULL),
    -- Teaching Assistants
    (44, 'Department of Machine Design, Mechatronics and Industrial Technologies, Teaching Assistant',    NULL,                   NULL),
    (45, 'Department of Machine Design, Mechatronics and Industrial Technologies, Teaching Assistant',    NULL,                   NULL),
    (46, 'Department of Machine Design, Mechatronics and Industrial Technologies, Teaching Assistant',    NULL,                   NULL),
    (47, 'Department of Machine Design, Mechatronics and Industrial Technologies, Teaching Assistant',    NULL,                   NULL),
    (48, 'Department of Machine Design, Mechatronics and Industrial Technologies, Teaching Assistant',    NULL,                   NULL),
    -- Clerk
    (49, 'Department of Machine Design, Mechatronics and Industrial Technologies, Clerk',                NULL,                   NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
