-- ============================================================
-- Kompüter Texnologiyaları kafedrası — Full DB Import
-- cafedra_code: 'computer_technologies'
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
    'computer_technologies',
    2, 6, 1, 7, 3, 1, 3,
    '[4, 8, 9, 17]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'computer_technologies',
    'az',
    'Kompüter Texnologiyaları kafedrası',
    'Kompüter texnologiyaları kafedrası Azərbaycan Texniki Universitetinin (AzTU) Elmi Şurasının 22 fevral 2021-ci il tarixli qərarı ilə "Kompüter sistemləri və şəbəkələri" və "İnformasiya texnologiyaları və proqramlaşdırma" kafedralarının bazasında yaradılmışdır. Kafedra 12-18 dekabr 2025 tarixdə nüfuzlu AQAS (Təhsil Proqramlarının Akkreditasiyası Vasitəsilə Keyfiyyətə Təminat Agentliyi) Akkreditasiya üzrə Daimi Komissiyası tərəfindən uğurla akkreditasiyadan keçmiş "Kompüter mühəndisliyi" və "İnformasiya texnologiyaları" mühəndislik ixtisasları üzrə bakalavriat və magistratura səviyyələrində kadr hazırlığı həyata keçirir. Kompüter texnologiyaları kafedrası 31 mart 2026-cı tarixdə "Informatics Europe" Beynəlxalq təşkilatına üzv qəbul edilmişdir. Kafedra təhsil, tədqiqat və sənaye inteqrasiyasını təmin edən strateji mərkəzə çevrilməyi qarşısına məqsəd qoymuşdur. Kafedranın missiyası rəqəmsal iqtisadiyyatın tələblərinə uyğun, yüksək ixtisaslı, qlobal əmək bazarına hazır mütəxəssislər hazırlamaqdır. Kafedra müasir informasiya texnologiyaları üzrə yüksək ixtisaslı mütəxəssislərin hazırlanmasını təmin edir, eyni zamanda süni intellekt, bulud texnologiyaları və kompüter şəbəkələri kimi sahələrdə elmi araşdırmalar aparır. Praktiki bacarıqların inkişafı məqsədilə laboratoriya işləri, layihələr və real sektorla birgə fəaliyyətlər həyata keçirilir. Bununla yanaşı, beynəlxalq platformalar vasitəsilə akademik əməkdaşlıq genişləndirilir. Kafedra həmçinin innovasiya, startap fəaliyyəti və tədrisin keyfiyyətinin davamlı yüksəldilməsi istiqamətində sistemli iş aparır.',
    NOW()
),
(
    'computer_technologies',
    'en',
    'Department of Computer Technologies',
    'The Department of Computer Technologies was established by the decision of the Scientific Council of Azerbaijan Technical University (AzTU) dated February 22, 2021, based on the merger of the departments "Computer Systems and Networks" and "Information Technologies and Programming." The department provides education at both bachelor''s and master''s levels in the engineering specializations "Computer Engineering" and "Information Technologies," which successfully passed accreditation by the prestigious AQAS (Agentur für Qualitätssicherung durch Akkreditierung von Studiengängen) Standing Commission from December 12 to 18, 2025. The Department of Computer Technologies was admitted as a member of the international organization Informatics Europe on March 31, 2026. The department aims to evolve into a strategic center that ensures the integration of education, research, and industry. Its mission is to train highly qualified specialists in line with the requirements of the digital economy, who are competitive and well-prepared for the global labor market. The department ensures the training of highly qualified specialists in modern information technologies, while also conducting scientific research in areas such as artificial intelligence, cloud technologies, and computer networks. To develop practical skills, laboratory work, project-based learning, and collaborations with the real sector are actively implemented. In addition, academic cooperation is expanded through international platforms. The department also carries out systematic work aimed at innovation, startup activities, and the continuous improvement of teaching quality.',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'computer_technologies';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('computer_technologies', 1, NOW()),
    ('computer_technologies', 2, NOW()),
    ('computer_technologies', 3, NOW()),
    ('computer_technologies', 4, NOW()),
    ('computer_technologies', 5, NOW()),
    ('computer_technologies', 6, NOW()),
    ('computer_technologies', 7, NOW()),
    ('computer_technologies', 8, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Tədris fəaliyyəti',             'Müasir IT proqramlarının hazırlanması və tədrisi'),
    (2, 'Elmi-tədqiqat',                 'Süni intellekt, data analitika, şəbəkələr və s. sahələrdə araşdırmalar'),
    (3, 'Praktiki və laboratoriya işləri','Layihə əsaslı və tətbiqi təhsil'),
    (4, 'Sənaye ilə əməkdaşlıq',         'IT şirkətlərlə birgə layihələr və təcrübə proqramları'),
    (5, 'Beynəlxalq əlaqələr',           'ACM, Informatics Europe kimi proqram və təşkilatlarla əməkdaşlıq'),
    (6, 'Keyfiyyət təminatı',            'Tədris və idarəetmədə beynəlxalq standartların tətbiqi'),
    (7, 'İnnovasiya və startap fəaliyyəti','Yeni texnologiyaların və ideyaların təşviqi'),
    (8, 'Kadr hazırlığı',                'Bakalavr, magistr və doktorant səviyyəsində mütəxəssis yetişdirilməsi')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Teaching activities',           'Development and delivery of modern IT curricula'),
    (2, 'Research activities',           'Studies in artificial intelligence, data analytics, networks, etc.'),
    (3, 'Practical and laboratory work', 'Project-based and applied education'),
    (4, 'Industry collaboration',        'Joint projects and internship programs with IT companies'),
    (5, 'International relations',       'Cooperation with organizations and programs such as ACM and Informatics Europe'),
    (6, 'Quality assurance',             'Implementation of international standards in teaching and management'),
    (7, 'Innovation and startup activities','Promotion of new technologies and ideas'),
    (8, 'Human resource development',    'Training specialists at bachelor''s, master''s, and doctoral levels')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours ──────────────
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'computer_technologies',
        'Zəfər', 'Cəfərov', 'Əli oğlu',
        'zafar.cafarov@aztu.edu.az',
        '+994 77 302 39 80',
        '6-cı Bina, 5-ci mərtəbə, otaq №510',
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
    'Texnika elmləri namizədi',
    'Dosent',
    'Cəfərov Zəfər Əli oğlu — AzTU-nun Kompüter Texnologiyaları kafedrasının müdiridir. O, informasiya və telekommunikasiya texnologiyaları sahəsində ixtisaslaşmış mütəxəssisdir. 1980-1985-ci illərdə Azərbaycan Neft və Kimya İnstitutunun Tətbiqi riyaziyyat ixtisası üzrə ali təhsil almış, 1985-1993-cü illərdə Rusiya Federasiyasının Ulyanovsk şəhərindəki keçmiş Sovetlər Birliyi Hərbi Dəniz Donanması "MARS" elmi-istehsalat birliyində mühəndis, kiçik elmi-işçi, aparıcı mühəndis, sektor rəisi vəzifələrində çalışmışdır. Zəfər Cəfərov texnika elmləri namizədi dərəcəsinə və dosent elmi adına malikdir. Onun elmi fəaliyyət istiqamətlərinə server əsaslı telekommunikasiya texnologiyaları, verilənlərin analizi, maşın öyrənməsi və süni intellekt modelləri daxildir. O, 140-dan çox elmi məqalə, məruzə, dərs vəsaiti və metodik materialların müəllifidir. Zəfər Cəfərov eyni zamanda Informatics Europe və ACM kimi beynəlxalq təşkilatlarla əməkdaşlıq istiqamətində fəaliyyət göstərir. Hazırda o, kafedranın strateji inkişafı, müasir IT kurikulumlarının tətbiqi, elmi-tədqiqat fəaliyyətinin gücləndirilməsi və sənaye ilə inteqrasiyanın genişləndirilməsi istiqamətlərində çalışır.',
    '["Server əsaslı telekommunikasiya texnologiyaları", "Verilənlərin analizi", "Maşın öyrənməsi", "Süni intellekt modelləri"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Candidate of Technical Sciences',
    'Associate Professor',
    'Zafar Jafarov is the Head of the Department of Computer Technologies at AzTU. He is a specialist in the field of information and telecommunication technologies. He received his higher education in Applied Mathematics from the Azerbaijan Oil and Chemistry Institute during 1980–1985. From 1985 to 1993, he worked by state assignment in Ulyanovsk, Russian Federation, at the former Soviet Navy''s "MARS" Scientific-Production Association, holding positions as an engineer, junior researcher, leading engineer, and head of sector. Zafar Jafarov holds a PhD (Candidate of Technical Sciences) degree and the academic title of Associate Professor. His research interests include server-based telecommunication technologies, data analysis, machine learning, and artificial intelligence models. He is the author of more than 140 scientific articles, conference papers, textbooks, and methodological materials. He is also actively involved in collaboration with international organizations such as Informatics Europe and ACM. Currently, he is focused on the strategic development of the department, implementation of modern IT curricula, strengthening research activities, and expanding integration with industry.',
    '["Server-based telecommunication technologies", "Data analysis", "Machine learning", "Artificial intelligence models"]'::jsonb,
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
    FROM cafedra_directors WHERE cafedra_code = 'computer_technologies'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Çərşənbə, Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Wednesday, Friday',       NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;


-- ── 5. Workers (professors, associate professors, lecturers, assistants) ──
DELETE FROM cafedra_workers WHERE cafedra_code = 'computer_technologies';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Professors (t.e.d.)
    ('computer_technologies', 'Xəzail',   'Rzayev',       'Nurəddin oğlu',         'xezail.rzayev@aztu.edu.az',         '+994 50 312 95 28',  NOW()),  -- 1
    ('computer_technologies', 'Mehriban', 'Fəttahova',    'İsa qızı',              'mehriban.fettahova@aztu.edu.az',    '+994 55 277 19 69',  NOW()),  -- 2
    -- Associate Professors (dosentlər)
    ('computer_technologies', 'Şəhla',    'Hüseynzadə',   'Surxay qızı',           'shahla.huseynzade@aztu.edu.az',     '+994 50 388 70 59',  NOW()),  -- 3
    ('computer_technologies', 'Tükazban', 'Quliyeva',     'Dadaş qızı',            'kulieva_td@aztu.edu.az',            '+994 50 539 12 50',  NOW()),  -- 4
    ('computer_technologies', 'David',    'Nəsibov',      'Rəhman oğlu',           'david.nasib@aztu.edu.az',           '+994 55 362 90 15',  NOW()),  -- 5
    ('computer_technologies', 'Rauf',     'Mustafayev',   'Tofiq oğlu',            'rauf.mustafayev@aztu.edu.az',       '+994 55 880 32 35',  NOW()),  -- 6
    ('computer_technologies', 'Nizami',   'Cəfərov',      'Duman oğlu',            'nizami.ceferov@aztu.edu.az',        '+994 50 532 39 07',  NOW()),  -- 7
    ('computer_technologies', 'İradə',    'Rəhimova',     'Rəhim qızı',            'irade.rehimova@aztu.edu.az',        '+994 50 315 34 15',  NOW()),  -- 8
    ('computer_technologies', 'Natiq',    'Əhmədov',      'Bəhlul oğlu',           'natiq.ahmedov@aztu.edu.az',         '+994 50 314 17 41',  NOW()),  -- 9
    ('computer_technologies', 'Zirəddin', 'Qasımov',      'Əmirəhməd oğlu',        'zireddin.qasimov@aztu.edu.az',      '+994 70 599 04 84',  NOW()),  -- 10
    ('computer_technologies', 'Elman',    'İmaməliyev',   'Bəhlul oğlu',           'elman.imameliyev@aztu.edu.az',      '+994 50 233 10 53',  NOW()),  -- 11
    ('computer_technologies', 'Təranə',   'Qəhrəmanova',  'İbrahim',               'tarana.qahramanova@aztu.edu.az',    '+994 50 311 64 61',  NOW()),  -- 12
    ('computer_technologies', 'Nərgiz',   'Miriyeva',     'Seyidalı qızı',         'nargiz.miriyeva@aztu.edu.az',       '+994 70 557 67 07',  NOW()),  -- 13
    ('computer_technologies', 'Qafar',    'Atayev',       'Nəriman',               'gafar.atayev@aztu.edu.az',          '+994 55 543 60 33',  NOW()),  -- 14
    ('computer_technologies', 'Milana',   'Orucova',      'Yaqub qızı',            'milana.orucova@aztu.edu.az',        '+994 55 775 08 00',  NOW()),  -- 15
    ('computer_technologies', 'Sevinc',   'İsmayılova',   'Ramiz qızı',            'sevinc.ismayilova@aztu.edu.az',     '+994 50 349 92 02',  NOW()),  -- 16
    ('computer_technologies', 'Mətanət',  'Hüseynova',    'Vaqif qızı',            'metanet.huseynova@aztu.edu.az',     '+994 50 667 44 74',  NOW()),  -- 17
    -- Senior Lecturers (Baş müəllimlər)
    ('computer_technologies', 'Mübariz',  'Qənbərov',     'Məhəmmədəli oğlu',      'mubariz.qenberov@aztu.edu.az',      '+994 55 782 04 05',  NOW()),  -- 18
    ('computer_technologies', 'Sevinc',   'Əliyeva',      'Yasin qızı',            'sevinc.aliyeva@aztu.edu.az',        '+994 55 966 69 01',  NOW()),  -- 19
    ('computer_technologies', 'Xaliq',    'Əmiraslanov',  'Vəli oğlu',             'xaliq.emiraslanov@aztu.edu.az',     '+994 70 222 90 14',  NOW()),  -- 20
    ('computer_technologies', 'Kamran',   'Əbilov',       'Əli oğlu',              'kamran.ebilov@aztu.edu.az',         '+994 77 761 59 22',  NOW()),  -- 21
    ('computer_technologies', 'Şəhla',    'Əliyeva',      'Xanqulu qızı',          'shahla.aliyeva@aztu.edu.az',        '+994 55 471 07 86',  NOW()),  -- 22
    ('computer_technologies', 'Şəyastə',  'Həsənova',     'Fərhad qızı',           'shayasta.hasanova@aztu.edu.az',     '+994 50 622 49 39',  NOW()),  -- 23
    ('computer_technologies', 'Məryəm',   'Cavadova',     'İslam qızı',            'maryam.cavadova@aztu.edu.az',       '+994 70 532 99 50',  NOW()),  -- 24
    ('computer_technologies', 'Şəbnəm',   'Cəbiyeva',     'Şahlar qızı',           'cebiyeva.shebnem@aztu.edu.az',      '+994 50 274 00 10',  NOW()),  -- 25
    ('computer_technologies', 'Anar',     'İsmayılov',    'Ələkbər oğlu',          'anar.ismayilov@aztu.edu.az',        '+994 55 713 26 84',  NOW()),  -- 26
    ('computer_technologies', 'Əli',      'Xəlilov',      'İsa oğlu',              'ali.khalilov@aztu.edu.az',          '+994 55 858 01 51',  NOW()),  -- 27
    ('computer_technologies', 'Mehran',   'Hemmatyar',    'Mahmud oğlu',           'mehran.hematyar@aztu.edu.az',       '+994 50 603 84 38',  NOW()),  -- 28
    -- Assistants (assistentlər)
    ('computer_technologies', 'Nigar',    'Cəbrayilova',  'Davud qızı',            'nigar.cebrayilova@aztu.edu.az',     '+994 55 886 66 81',  NOW()),  -- 29
    ('computer_technologies', 'Bahar',    'Nəzərova',     'Çingiz qızı',           'bahar.nezerova@aztu.edu.az',        '+994 50 498 73 98',  NOW()),  -- 30
    ('computer_technologies', 'Validə',   'Məmmədova',    'Xəqani qızı',           'memmedova.valide@aztu.edu.az',      '+994 55 643 84 43',  NOW()),  -- 31
    -- Teachers (müəllimlər)
    ('computer_technologies', 'Əfsanə',   'Yusifzadə Qaraşlı', 'Səyyaf qızı',     'efsane.yusifzade@aztu.edu.az',      '+994 55 881 39 68',  NOW()),  -- 32
    ('computer_technologies', 'Leyla',    'Yusifli Heydərli', 'Səməd qızı',        'leylayusifova16@gmail.com',         '+994 77 311 00 98',  NOW()),  -- 33
    ('computer_technologies', 'Gülşən',   'Hüseynova',    'Baba qızı',             'gulshan.huseynova@aztu.edu.az',     '+994 55 673 79 74',  NOW()),  -- 34 (assistent)
    ('computer_technologies', 'Lamiə',    'Qurbanlı',     'Sənhan qızı',           'lamiya.gurbanli@aztu.edu.az',       '+994 51 936 65 27',  NOW()),  -- 35
    ('computer_technologies', 'Sədaqət',  'Abasova',      'Mirzəbaba qızı',        'sedaqet.abasova@aztu.edu.az',       '+994 51 558 41 79',  NOW()),  -- 36 (assistent)
    ('computer_technologies', 'Cəmilə',   'Abdurəhimova', 'İbrahim qızı',          'cemile.aliyeva@aztu.edu.az',        '+994 51 349 25 57',  NOW()),  -- 37
    ('computer_technologies', 'Nurlan',   'Arifzadə',     'Səhrad oğlu',           'nurlan.arifzade@aztu.edu.az',       '+994 50 985 49 40',  NOW()),  -- 38
    ('computer_technologies', 'Əsmər',    'Nəbiyeva',     'Namiq qızı',            'esmer.nebiyeva@aztu.edu.az',        '+994 70 770 70 17',  NOW()),  -- 39
    ('computer_technologies', 'Günel',    'Məmmədli',     'Mirzə qızı',            'gunel.memmedli@aztu.edu.az',        '+994 51 543 96 10',  NOW()),  -- 40
    -- Teaching Assistants (tədris köməkçiləri)
    ('computer_technologies', 'Samirə',   'Bayramova',    NULL,                    'samire.bayramova@aztu.edu.az',      '+994 51 975 67 88',  NOW()),  -- 41
    ('computer_technologies', 'Rəşadət',  'Fəttahova',    NULL,                    'rashadat.fattahova@aztu.edu.az',    '+994 55 777 89 79',  NOW())   -- 42
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Kompüter texnologiyaları kafedrası, professor',    'Professor', 't.e.d.'),
    (2,  'Kompüter texnologiyaları kafedrası, professor',    'Professor', 't.e.d.'),
    (3,  'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.d.'),
    (4,  'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (5,  'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    'f.r.e.n.'),
    (6,  'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (7,  'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (8,  'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (9,  'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (10, 'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (11, 'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (12, 'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    'f.r.e.n.'),
    (13, 'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    'f.r.e.n.'),
    (14, 'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (15, 'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (16, 'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.e.n.'),
    (17, 'Kompüter texnologiyaları kafedrası, dosent',       'Dosent',    't.ü.f.d.'),
    (18, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (19, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (20, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (21, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (22, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (23, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (24, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (25, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (26, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (27, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (28, 'Kompüter texnologiyaları kafedrası, Baş müəllim', NULL,        NULL),
    (29, 'Kompüter texnologiyaları kafedrası, assistent',       NULL, NULL),
    (30, 'Kompüter texnologiyaları kafedrası, assistent',       NULL, NULL),
    (31, 'Kompüter texnologiyaları kafedrası, assistent',       NULL, NULL),
    (32, 'Kompüter texnologiyaları kafedrası, müəllim',         NULL, NULL),
    (33, 'Kompüter texnologiyaları kafedrası, müəllim',         NULL, NULL),
    (34, 'Kompüter texnologiyaları kafedrası, assistent',       NULL, NULL),
    (35, 'Kompüter texnologiyaları kafedrası, müəllim',         NULL, NULL),
    (36, 'Kompüter texnologiyaları kafedrası, assistent',       NULL, NULL),
    (37, 'Kompüter texnologiyaları kafedrası, müəllim',         NULL, NULL),
    (38, 'Kompüter texnologiyaları kafedrası, müəllim',         NULL, NULL),
    (39, 'Kompüter texnologiyaları kafedrası, müəllim',         NULL, NULL),
    (40, 'Kompüter texnologiyaları kafedrası, müəllim',         NULL, NULL),
    (41, 'Kompüter texnologiyaları kafedrası, tədris köməkçisi',NULL, NULL),
    (42, 'Kompüter texnologiyaları kafedrası, tədris köməkçisi',NULL, NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Department of Computer Technologies, Professor',         'Professor',           't.e.d.'),
    (2,  'Department of Computer Technologies, Professor',         'Professor',           't.e.d.'),
    (3,  'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.d.'),
    (4,  'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (5,  'Department of Computer Technologies, Associate Professor','Associate Professor', 'f.r.e.n.'),
    (6,  'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (7,  'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (8,  'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (9,  'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (10, 'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (11, 'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (12, 'Department of Computer Technologies, Associate Professor','Associate Professor', 'f.r.e.n.'),
    (13, 'Department of Computer Technologies, Associate Professor','Associate Professor', 'f.r.e.n.'),
    (14, 'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (15, 'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (16, 'Department of Computer Technologies, Associate Professor','Associate Professor', 't.e.n.'),
    (17, 'Department of Computer Technologies, Associate Professor','Associate Professor', 't.ü.f.d.'),
    (18, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (19, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (20, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (21, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (22, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (23, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (24, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (25, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (26, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (27, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (28, 'Department of Computer Technologies, Senior Lecturer',   NULL,                  NULL),
    (29, 'Department of Computer Technologies, Assistant',          NULL, NULL),
    (30, 'Department of Computer Technologies, Assistant',          NULL, NULL),
    (31, 'Department of Computer Technologies, Assistant',          NULL, NULL),
    (32, 'Department of Computer Technologies, Teacher',            NULL, NULL),
    (33, 'Department of Computer Technologies, Teacher',            NULL, NULL),
    (34, 'Department of Computer Technologies, Assistant',          NULL, NULL),
    (35, 'Department of Computer Technologies, Teacher',            NULL, NULL),
    (36, 'Department of Computer Technologies, Assistant',          NULL, NULL),
    (37, 'Department of Computer Technologies, Teacher',            NULL, NULL),
    (38, 'Department of Computer Technologies, Teacher',            NULL, NULL),
    (39, 'Department of Computer Technologies, Teacher',            NULL, NULL),
    (40, 'Department of Computer Technologies, Teacher',            NULL, NULL),
    (41, 'Department of Computer Technologies, Teaching Assistant', NULL, NULL),
    (42, 'Department of Computer Technologies, Teaching Assistant', NULL, NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
