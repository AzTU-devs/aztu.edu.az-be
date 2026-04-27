-- ============================================================
-- Mühəndis riyaziyyatı və süni intellekt kafedrası — Full DB Import
-- cafedra_code: 'engineering_mathematics_artificial_intelligence'
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
    'engineering_mathematics_artificial_intelligence',
    1, 2, 0, 4, 0, 3, 4,
    '[9, 8, 4, 17]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'engineering_mathematics_artificial_intelligence',
    'az',
    'Mühəndis riyaziyyatı və süni intellekt kafedrası',
    '<p>Azərbaycan Texniki Universitetinin ilk kafedralarından olan "Ali riyaziyyat" kafedrası 1950-ci ildə fəaliyyətə başlayıb.</p><p>1976-cı ildə professor Kərim Abdulxaliq oğlu Kərimovun təşəbbüsü ilə "Tətbiqi və hesablama riyaziyyatı" kafedrası yaradılıb. Sonra bu kafedra "Tətbiqi riyaziyyat" adlandırılıb. Daha sonra kafedra "Riyaziyyat-2" adı altında fəaliyyətə başlayıb.</p><p>2001-ci ildə "Riyaziyyat-1" və "Riyaziyyat-2" kafedraları birləşdirilərək "Riyaziyyat" kafedrası adlandırılıb. 2019-cu ildə kafedranın adı yenidən dəyişilərək "Mühəndis riyaziyyatı" kafedrası adlandırılıb.</p><p>2021-ci ildə universitetdə struktur dəyişikliyi ilə əlaqədar olaraq "İnformasiya texnologiyaları və proqramlaşdırma" və "Mühəndis riyaziyyatı" kafedraları birləşdirilərək onların bazasında "Mühəndis riyaziyyatı və süni intellekt" kafedrası yaradılıb.</p><p>Kafedrada bakalavr və magistr (10 ixtisaslaşma) səviyyələrində 3 ixtisas üzrə kadr hazırlanır.</p><p>Kafedranın əsas məqsədi mühəndis riyaziyyatı, proqram mühəndisliyi və süni intellekt sistemləri üzrə tədris olunan fənlərdə elmi-praktiki problemləri aradan qaldırmaq məqsədi ilə dünyanın nüfuzlu universitetlərinin təcrübəsindən faydalanmaq və kafedranın əməkdaşları ilə birgə tələbələri, magistrantları və doktorantları istər yerli, istərsə də xarici qrant layihələrinə cəlb etməkdir.</p>',
    NOW()
),
(
    'engineering_mathematics_artificial_intelligence',
    'en',
    'Department of Engineering Mathematics and Artificial Intelligence',
    '<p>The "Higher Mathematics" department, one of the first departments of Azerbaijan Technical University, started its activity in 1950.</p><p>In 1976, on the initiative of Professor Karim Abdulkhaliq oglu Karimov, the "Applied and Computational Mathematics" department was established. Later, this department was renamed "Applied Mathematics". Subsequently, the department began operating under the name "Mathematics-2".</p><p>In 2001, the "Mathematics-1" and "Mathematics-2" departments were merged and named the "Mathematics" department. In 2019, the department was renamed again to the "Engineering Mathematics" department.</p><p>In 2021, due to the structural changes at the university, the "Information Technologies and Programming" and "Engineering Mathematics" departments were merged, and on their basis, the "Engineering Mathematics and Artificial Intelligence" department was established.</p><p>The department prepares specialists in 3 specialties at the bachelor''s and master''s (10 specializations) levels.</p><p>The main goal of the department is to benefit from the experience of the world''s prestigious universities in order to solve scientific-practical problems in the subjects taught in engineering mathematics, software engineering and artificial intelligence systems, and to involve students, master''s students and doctoral students, together with the department''s staff, in both local and international grant projects.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'engineering_mathematics_artificial_intelligence';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('engineering_mathematics_artificial_intelligence', 1, NOW()),
    ('engineering_mathematics_artificial_intelligence', 2, NOW()),
    ('engineering_mathematics_artificial_intelligence', 3, NOW()),
    ('engineering_mathematics_artificial_intelligence', 4, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Texniki sistemlərin idarə edilməsi',                          'İnformasiyanın məhdudluğu şəraitində texniki sistemlərin idarə edilməsi metod və alqoritmlərinin işlənməsi'),
    (2, 'Korporativ informasiya təhlükəsizliyi',                      'Korporativ informasiya sistemlərində və bulud (Cloud Computing) texnologiyalarından istifadədə təhlükəsizliyinin təmin olunması metodlarının işlənməsi'),
    (3, 'Süni intellekt və intellektual proqram məhsulları',          'Süni intellekt (Artificial Intelligence) və intellektual proqram (Software) məhsullarının elmi-praktiki problemləri'),
    (4, 'Böyük verilənlər və intellektual analiz',                    'Böyük verilənlər (Big Data) və verilənlərin intellektual analizi (Data mining) texnologiyalarının perspektivləri və işlənilməsi problemləri')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Control of technical systems',                                'Development of methods and algorithms for controlling technical systems under conditions of limited information'),
    (2, 'Corporate information security',                              'Development of methods for ensuring security in corporate information systems and cloud computing technologies'),
    (3, 'Artificial intelligence and software products',               'Scientific-practical problems of artificial intelligence (AI) and intelligent software products'),
    (4, 'Big data and intelligent analysis',                           'Prospects and development challenges of big data and data mining technologies')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'engineering_mathematics_artificial_intelligence',
        'Atif', 'Namazov', 'Akif oğlu',
        'atif.namazov@aztu.edu.az',
        '+994 70 601 55 61',
        'Bina 6, 4-cü mərtəbə, otaq 409',
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
    'Riyaziyyat üzrə fəlsəfə doktoru (PhD)',
    'Dosent',
    '<p>Namazov Atif Akif oğlu 1993-2004-cü illərdə Gəncə şəhəri 37 saylı tamorta məktəbdə orta təhsilini alıb. O, 2004-2008-ci illərdə Bakı Dövlət Universitetinin Mexanika-riyaziyyat fakültəsində bakalavriat səviyyəsi üzrə, 2009-2011-ci illərdə həmin fakültədə magistratura səviyyəsi üzrə təhsil alıb.</p><p>2023-cü ildə riyaziyyat üzrə fəlsəfə doktoru elmi adını alıb. 2012-2013-cü illərdə Müdafiə Sənaye Nazirliyinin "Alov" zavodunda mühəndis-proqramçı vəzifəsində çalışıb. 2013-2019-cu illərdə Bakı Dövlət Universitetinin Tətbiqi Riyaziyyat Elmi Tədqiqat İnstitutunda kiçik elmi işçi, 2019-2023-cü illərdə isə elmi işçi kimi fəaliyyət göstərib.</p><p>2019-2023-cü illərdə Azərbaycan Texniki Universitetinin "Mühəndis riyaziyyatı və süni intellekt" kafedrasında 0,5 ştat baş müəllim vəzifəsində işləyib, 2023-cü ildən isə həmin kafedrada 0,5 ştat dosent vəzifəsində çalışır.</p><p>50-dən çox elmi metodik işin müəllifidir. Bunlardan 13 elmi məqaləsi beynəlxalq elmi bazalarda, o cümlədən "Scopus" və "Web of Science" bazalarında indekslənən jurnallarda dərc olunmuşdur. 2023-cü ildən etibarən Azərbaycan Texniki Universitetinin "Mühəndis riyaziyyatı və süni intellekt" kafedrasının müdiri vəzifəsini icra edir.</p>',
    '["Qeyri xətti dinamiki proseslərin riyazi modellərinin qurulması", "Adi diferensial tənliklər və xüsusi törəməli diferensial tənliklər", "Optimal idarəetmə məsələlərinin riyazi modelləşdirilməsi və proqramlarının işlədilməsi", "Süni intellekt"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'PhD in Mathematics',
    'Associate Professor',
    '<p>Atif Akif oglu Namazov received his secondary education at school No. 37 in Ganja city from 1993 to 2004. He studied at the bachelor''s level at the Faculty of Mechanics and Mathematics of Baku State University from 2004 to 2008, and at the master''s level at the same faculty from 2009 to 2011.</p><p>In 2023, he received the academic degree of Doctor of Philosophy in Mathematics. From 2012 to 2013, he worked as an engineer-programmer at the "Alov" factory of the Ministry of Defense Industry. From 2013 to 2019, he worked as a junior researcher, and from 2019 to 2023 as a researcher at the Institute of Applied Mathematics Research of Baku State University.</p><p>From 2019 to 2023, he worked as a 0.5 rate senior lecturer at the "Engineering Mathematics and Artificial Intelligence" department of Azerbaijan Technical University, and since 2023, he has been working as a 0.5 rate associate professor at the same department.</p><p>He is the author of more than 50 scientific methodological works. Of these, 13 scientific articles have been published in journals indexed in international scientific databases, including "Scopus" and "Web of Science". Since 2023, he has been serving as the head of the "Engineering Mathematics and Artificial Intelligence" department of Azerbaijan Technical University.</p>',
    '["Construction of mathematical models of nonlinear dynamic processes", "Ordinary differential equations and partial differential equations", "Mathematical modeling and programming of optimal control problems", "Artificial intelligence"]'::jsonb,
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
    FROM cafedra_directors WHERE cafedra_code = 'engineering_mathematics_artificial_intelligence'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Çərşənbə, Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Wednesday, Friday',       NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '2004', '2008', NOW() FROM cafedra_directors WHERE cafedra_code = 'engineering_mathematics_artificial_intelligence'
UNION ALL
SELECT id, '2009', '2011', NOW() FROM cafedra_directors WHERE cafedra_code = 'engineering_mathematics_artificial_intelligence'
UNION ALL
SELECT id, '2014', '2018', NOW() FROM cafedra_directors WHERE cafedra_code = 'engineering_mathematics_artificial_intelligence';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'engineering_mathematics_artificial_intelligence')
    ORDER BY id DESC
    LIMIT 3
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bakalavr (Riyaziyyat)',                                                          'Bakı Dövlət Universiteti'),
    (2, 'Magistr (Diferensial və inteqral tənliklər)',                                    'Bakı Dövlət Universiteti'),
    (3, 'Doktorantura (Sistemli analizin riyazi problemləri)',                             'Bakı Dövlət Universiteti, Tətbiqi Riyaziyyat Elmi Tədqiqat İnstitutu')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bachelor''s (Mathematics)',                                                       'Baku State University'),
    (2, 'Master''s (Differential and Integral Equations)',                                  'Baku State University'),
    (3, 'Doctorate (Mathematical Problems of Systems Analysis)',                            'Baku State University, Institute of Applied Mathematics Research')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'engineering_mathematics_artificial_intelligence';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Fəxri professor
    ('engineering_mathematics_artificial_intelligence', 'Nizami',      'Şıxəliyev',       'İsmayıl oğlu',       'nizami.shixeliyev@aztu.edu.az',       '+994 51 575 05 00',  NOW()),  -- 1
    -- Dosentlər
    ('engineering_mathematics_artificial_intelligence', 'Taleh',       'Şirinov',          'Voraşil oğlu',       'taleh.sirinov@aztu.edu.az',           '+994 50 357 60 71',  NOW()),  -- 2
    ('engineering_mathematics_artificial_intelligence', 'Həsən',       'Vəliyev',          'Paşa oğlu',          'veliyev.hesen@aztu.edu.az',           '+994 77 311 28 71',  NOW()),  -- 3
    ('engineering_mathematics_artificial_intelligence', 'Sahib',       'Piriyev',          'Aydın oğlu',         'sahib.piriyev@aztu.edu.az',           '+994 50 642 84 50',  NOW()),  -- 4
    ('engineering_mathematics_artificial_intelligence', 'Əlabbas',     'Haxıyev',          'Seydi oğlu',         'alabbas.haxiyev@aztu.edu.az',         '+994 70 380 09 53',  NOW()),  -- 5
    ('engineering_mathematics_artificial_intelligence', 'Firudin',     'Məmmədov',         'Osman oğlu',         'firudin.memmedov@aztu.edu.az',        '+994 50 413 99 50',  NOW()),  -- 6
    ('engineering_mathematics_artificial_intelligence', 'Fikrət',      'Məsimov',          'Əbülfət oğlu',       'fikret.mesimov@aztu.edu.az',          '+994 50 323 61 15',  NOW()),  -- 7
    ('engineering_mathematics_artificial_intelligence', 'Rəna',        'Əmirova',          'Ağamir qızı',        'rena.amirova@aztu.edu.az',            '+994 77 756 22 29',  NOW()),  -- 8
    ('engineering_mathematics_artificial_intelligence', 'Təbriz',      'Şəmiyev',          'Musa oğlu',          'tebriz.shamiyev@aztu.edu.az',         '+994 50 344 78 84',  NOW()),  -- 9
    ('engineering_mathematics_artificial_intelligence', 'Mehman',      'Şahverdiyev',      'Ələkbər oğlu',       'mehman.shahverdiyev@aztu.edu.az',     '+994 55 586 99 77',  NOW()),  -- 10
    ('engineering_mathematics_artificial_intelligence', 'Mənsur',      'İslamov',          'Mövlud oğlu',        'mensur.islamov@aztu.edu.az',          '+994 55 726 50 49',  NOW()),  -- 11
    ('engineering_mathematics_artificial_intelligence', 'Ruhiyyə',     'Zamanova',         'Bülbül qızı',        'ruhiyye.zamanova@aztu.edu.az',        '+994 50 678 77 23',  NOW()),  -- 12
    ('engineering_mathematics_artificial_intelligence', 'Güldəstə',    'Məmmədova',        'Akif qızı',          'guldeste.memmedova@aztu.edu.az',      '+994 55 612 65 20',  NOW()),  -- 13
    ('engineering_mathematics_artificial_intelligence', 'Aygün',       'Məmmədzadə',       'Malik qızı',         'aygun.mammadzada@aztu.edu.az',        '+994 50 514 30 34',  NOW()),  -- 14
    ('engineering_mathematics_artificial_intelligence', 'Azadə',       'Tahirova',         'Cəmşid qızı',       'azade.tahirova@aztu.edu.az',          '+994 50 641 00 30',  NOW()),  -- 15
    ('engineering_mathematics_artificial_intelligence', 'Vaqif',       'Yusifov',          'Həmid oğlu',         'vaqif.yusifov@aztu.edu.az',           '+994 50 512 04 22',  NOW()),  -- 16
    ('engineering_mathematics_artificial_intelligence', 'Rəna',        'İsmayılova',       'Əşrəf qızı',        'rana.ismayilova@aztu.edu.az',          '+994 55 894 92 82',  NOW()),  -- 17
    ('engineering_mathematics_artificial_intelligence', 'Oqtay',       'Əzizov',           'Qiyas oğlu',         'oqtay.azizov@aztu.edu.az',            '+994 50 624 57 79',  NOW()),  -- 18
    ('engineering_mathematics_artificial_intelligence', 'Günel',       'Eyvazlı',          'Mübariz qızı',       'gunel.eyvazli@aztu.edu.az',           '+994 55 901 99 07',  NOW()),  -- 19
    -- Baş müəllimlər
    ('engineering_mathematics_artificial_intelligence', 'Mövsüm',      'Əliyev',           'Əliqulu oğlu',       'movsum.eliyev@aztu.edu.az',           '+994 50 421 53 51',  NOW()),  -- 20
    ('engineering_mathematics_artificial_intelligence', 'Fizuli',      'Əzimov',           'Murad oğlu',         'fizuli.azimov@aztu.edu.az',           '+994 55 371 09 97',  NOW()),  -- 21
    ('engineering_mathematics_artificial_intelligence', 'Mülayim',     'Rizvanova',        'Mehdi qızı',         'mulayim.rizvanova@aztu.edu.az',       '+994 50 709 05 35',  NOW()),  -- 22
    ('engineering_mathematics_artificial_intelligence', 'Dürdanə',     'Abdullayeva',      'Əmir qızı',          'durdane.abdullayeva.68@aztu.edu.az',  '+994 50 337 42 17',  NOW()),  -- 23
    ('engineering_mathematics_artificial_intelligence', 'Rasim',       'Həşimov',          'Hümbət oğlu',        'rasim.hasimov@aztu.edu.az',           '+994 50 397 73 75',  NOW()),  -- 24
    ('engineering_mathematics_artificial_intelligence', 'Türkanə',     'Qəhrəmanlı',       'Barat qızı',         'turkane.qehramanli@aztu.edu.az',      '+994 55 902 61 27',  NOW()),  -- 25
    ('engineering_mathematics_artificial_intelligence', 'Rəfayıl',     'Əhmədov',          'Əlio oğlu',          'rafael.ahmedov@aztu.edu.az',          '+994 55 206 81 15',  NOW()),  -- 26
    ('engineering_mathematics_artificial_intelligence', 'Aynur',       'Rəsulzadə',        'Fizuli qızı',        'resulzadeaynur@aztu.edu.az',          '+994 51 893 86 92',  NOW()),  -- 27
    -- Assistentlər
    ('engineering_mathematics_artificial_intelligence', 'Aytən',       'Məmmədli',         'Rəhman qızı',        'ayten.memmedli@aztu.edu.az',          '+994 77 307 21 81',  NOW()),  -- 28
    ('engineering_mathematics_artificial_intelligence', 'Aydan',       'Hömmətova',        'Səməd qızı',         'aydan.hommatova@aztu.edu.az',         '+994 55 868 74 38',  NOW()),  -- 29
    ('engineering_mathematics_artificial_intelligence', 'Çinarə',      'Ağaməmmədova',     'Nail qızı',          'cinara.qenberova@aztu.edu.az',        '+994 51 805 55 15',  NOW()),  -- 30
    ('engineering_mathematics_artificial_intelligence', 'Çingiz',      'Hacızadə',         'Arif oğlu',          'chingiz.hacizade@aztu.edu.az',        '+994 50 440 83 93',  NOW()),  -- 31
    ('engineering_mathematics_artificial_intelligence', 'Tuti',        'Abdullayeva',      'Tehran qızı',        'tuti.abdullayeva@aztu.edu.az',        '+994 55 251 01 15',  NOW()),  -- 32
    ('engineering_mathematics_artificial_intelligence', 'Fatimə',      'Həsənli',          'Əbülfət qızı',       'fatime.hesenli@aztu.edu.az',          '+994 70 854 14 41',  NOW()),  -- 33
    ('engineering_mathematics_artificial_intelligence', 'Abdurahman',  'Vaqifli',          'Vüqar oğlu',         'abdurahman.vagifli@aztu.edu.az',      '+994 77 590 54 63',  NOW()),  -- 34
    ('engineering_mathematics_artificial_intelligence', 'Günel',       'Babanlı',          'Fəxrəddin qızı',     'gunel.babanli@aztu.edu.az',           '+994 70 203 73 77',  NOW()),  -- 35
    ('engineering_mathematics_artificial_intelligence', 'Zülfiyyə',    'Əliyeva',          'Mehman qızı',        'zulfiyya.aliyeva@aztu.edu.az',        '+994 50 611 62 37',  NOW()),  -- 36
    -- Müəllim köməkçiləri
    ('engineering_mathematics_artificial_intelligence', 'Aygün',       'Abdullayeva',      'Niyazi qızı',        'aygun.abdullayeva@aztu.edu.az',       '+994 50 510 67 51',  NOW()),  -- 37
    ('engineering_mathematics_artificial_intelligence', 'Çingiz',      'Ələkbərov',        'Araz oğlu',          'chingiz.alakbarov@aztu.edu.az',       '+994 55 631 36 63',  NOW()),  -- 38
    -- Kargüzar
    ('engineering_mathematics_artificial_intelligence', 'Afət',        'Cəfərova',         'Məmməd qızı',        'afet.cafarova@aztu.edu.az',           '+994 55 600 56 27',  NOW())   -- 39
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Fəxri professor
    (1,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, fəxri professor',   'Fəxri professor',  'f.r.e.n.'),
    -- Dosentlər
    (2,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (3,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (4,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'r.ü.f.d.'),
    (5,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (6,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (7,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (8,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           't.e.n.'),
    (9,  'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (10, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (11, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (12, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'r.ü.f.d.'),
    (13, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (14, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'r.ü.f.d.'),
    (15, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (16, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (17, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'r.ü.f.d.'),
    (18, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'f.r.e.n.'),
    (19, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, dosent',            'Dosent',           'r.ü.f.d.'),
    -- Baş müəllimlər
    (20, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, baş müəllim',       NULL,               NULL),
    (21, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, baş müəllim',       NULL,               NULL),
    (22, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, baş müəllim',       NULL,               NULL),
    (23, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, baş müəllim',       NULL,               NULL),
    (24, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, baş müəllim',       NULL,               NULL),
    (25, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, baş müəllim',       NULL,               NULL),
    (26, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, baş müəllim',       NULL,               NULL),
    (27, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, baş müəllim',       NULL,               NULL),
    -- Assistentlər
    (28, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    (29, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    (30, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    (31, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    (32, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    (33, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    (34, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    (35, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    (36, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, assistent',         NULL,               NULL),
    -- Müəllim köməkçiləri
    (37, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, müəllim köməkçisi', NULL,               NULL),
    (38, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, müəllim köməkçisi', NULL,               NULL),
    -- Kargüzar
    (39, 'Mühəndis riyaziyyatı və süni intellekt kafedrası, kargüzar',          NULL,               NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Honorary Professor
    (1,  'Department of Engineering Mathematics and Artificial Intelligence, Honorary Professor',    'Honorary Professor',   'Candidate of Physical-Mathematical Sciences'),
    -- Associate Professors
    (2,  'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (3,  'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (4,  'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'PhD in Mathematics'),
    (5,  'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (6,  'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (7,  'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (8,  'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Technical Sciences'),
    (9,  'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (10, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (11, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (12, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'PhD in Mathematics'),
    (13, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (14, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'PhD in Mathematics'),
    (15, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (16, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (17, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'PhD in Mathematics'),
    (18, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'Candidate of Physical-Mathematical Sciences'),
    (19, 'Department of Engineering Mathematics and Artificial Intelligence, Associate Professor',   'Associate Professor',  'PhD in Mathematics'),
    -- Senior Lecturers
    (20, 'Department of Engineering Mathematics and Artificial Intelligence, Senior Lecturer',       NULL,                   NULL),
    (21, 'Department of Engineering Mathematics and Artificial Intelligence, Senior Lecturer',       NULL,                   NULL),
    (22, 'Department of Engineering Mathematics and Artificial Intelligence, Senior Lecturer',       NULL,                   NULL),
    (23, 'Department of Engineering Mathematics and Artificial Intelligence, Senior Lecturer',       NULL,                   NULL),
    (24, 'Department of Engineering Mathematics and Artificial Intelligence, Senior Lecturer',       NULL,                   NULL),
    (25, 'Department of Engineering Mathematics and Artificial Intelligence, Senior Lecturer',       NULL,                   NULL),
    (26, 'Department of Engineering Mathematics and Artificial Intelligence, Senior Lecturer',       NULL,                   NULL),
    (27, 'Department of Engineering Mathematics and Artificial Intelligence, Senior Lecturer',       NULL,                   NULL),
    -- Assistants
    (28, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    (29, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    (30, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    (31, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    (32, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    (33, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    (34, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    (35, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    (36, 'Department of Engineering Mathematics and Artificial Intelligence, Assistant',             NULL,                   NULL),
    -- Teaching Assistants
    (37, 'Department of Engineering Mathematics and Artificial Intelligence, Teaching Assistant',    NULL,                   NULL),
    (38, 'Department of Engineering Mathematics and Artificial Intelligence, Teaching Assistant',    NULL,                   NULL),
    -- Clerk
    (39, 'Department of Engineering Mathematics and Artificial Intelligence, Clerk',                 NULL,                   NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
