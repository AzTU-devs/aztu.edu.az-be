-- ============================================================
-- "Sənaye mühəndisliyi və davamlı iqtisadiyyat" kafedrası — Full DB Import
-- cafedra_code: 'industrial_engineering_and_sustainable_economy'
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
    'industrial_engineering_and_sustainable_economy',
    3, 3, 2, 10, 0, 0, 8,
    '[4, 8, 9, 12]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'industrial_engineering_and_sustainable_economy',
    'az',
    'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrası',
    '<p>Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrası Azərbaycan Texniki Universitetinin (AzTU) rektorunun 09 iyul 2025-ci il tarixli əmri ilə Sənaye iqtisadiyyatı və menecment fakültəsinin tərkibində İqtisadiyyat və statistika bazasında yaradılmışdır. Kafedra tələbələrə müasir idarəetmə və iqtisadi bacarıqları qazandırmağı, universitet-sənaye əməkdaşlığı əsasında çalışmaqla praktiki bacarıqların inkişafını, iqtisadiyyatın müxtəlif sahələrində aktual mövzuların araşdırılmasını, sahibkarlığın təşviqi və əmək bazarına uyğun mütəxəssis hazırlamağı qarşısına məqsəd qoymuşdur.</p><p>Kafedranın missiyası müasir bilik və bacarıqlara malik, etik dəyərlərə sadiq, innovativ düşüncəli və rəqabətqabiliyyətli mütəxəssislər hazırlamaqdır. Kafedra bir neçə istiqamətdə elmi tədqiqatlar apararaq cəmiyyətin sosial-iqtisadi inkişafına töhfə verməyi hədəfləməkdədir.</p><p>Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrası təhsil, elmi-tədqiqat və sənaye müəssisələri ilə əməkdaşlığın vəhdət təşkil etdiyi müasir və inklüziv akademik ekosistemin formalaşdırılmasına yönəlmişdir. Sənaye mühəndisliyi, davamlı iqtisadiyyat, dairəvi iqtisadiyyat, layihələrin idarə olunması, layihə menecmenti, insan resurslarının idarə olunması, innovasiya və dəyişikliklərin idarəedilməsi və digər istiqamətlərdə həyata keçirilən təşəbbüslər vasitəsilə nəzəri biliklərin praktik tətbiqlərə çevrilməsi təmin olunur. Müasir tələblər, innovativ yanaşmalar və əmək bazarının və sənayenin tələbləri nəzərə alınaraq tələbələrin peşəkar inkişafı, idarəetmə bacarıqları və rəqabətqabiliyyətli karyera quruculuğu dəstəklənir.</p>',
    NOW()
),
(
    'industrial_engineering_and_sustainable_economy',
    'en',
    'Department of Industrial Engineering and Sustainable Economy',
    '<p>The Department of Industrial Engineering and Sustainable Economy was established on the basis of the Economics and Statistics unit within the Faculty of Industrial Economics and Management by the order of the Rector of Azerbaijan Technical University (AzTU) dated July 9, 2025. The department aims to equip students with modern management and economic skills, to develop practical abilities through university-industry cooperation, to research current topics in various fields of the economy, to promote entrepreneurship, and to train specialists suited to the labor market.</p><p>The mission of the department is to train specialists with modern knowledge and skills, committed to ethical values, innovative thinking, and competitiveness. The department aims to contribute to the socio-economic development of society by conducting scientific research in several directions.</p><p>The Department of Industrial Engineering and Sustainable Economy is focused on forming a modern and inclusive academic ecosystem in which education, scientific research, and cooperation with industrial enterprises are combined. Through initiatives carried out in industrial engineering, sustainable economy, circular economy, project management, human resources management, innovation and change management, and other directions, the transformation of theoretical knowledge into practical applications is ensured. Taking into account modern requirements, innovative approaches, and the demands of the labor market and industry, students'' professional development, management skills, and competitive career building are supported.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'industrial_engineering_and_sustainable_economy';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('industrial_engineering_and_sustainable_economy', 1, NOW()),
    ('industrial_engineering_and_sustainable_economy', 2, NOW()),
    ('industrial_engineering_and_sustainable_economy', 3, NOW()),
    ('industrial_engineering_and_sustainable_economy', 4, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Müasir tədris proqramları',                'Sənaye mühəndisliyi, davamlı iqtisadiyyat, dairəvi iqtisadiyyat və idarəetmə üzrə müasir və beynəlxalq standartlara uyğun tədris proqramlarının hazırlanması və tətbiqi.'),
    (2, 'Sənaye ilə birgə elmi tədqiqatlar',        'Müxtəlif sənaye müəssisələri ilə birlikdə elmi araşdırmaların aparılması, iqtisadi və idarəetmə modellərinin qurulması istiqamətində elmi tədqiqatların aparılması və innovativ həllərin işlənməsi.'),
    (3, 'Metod və yanaşmaların inkişafı',          'Sənaye mühəndisliyi, layihələrin idarə olunması və dayanıqlı iqtisadiyyat sahələrində metod və yanaşmaların inkişaf etdirilməsi.'),
    (4, 'Karyerayönümlü mütəxəssis hazırlığı',      'Şirkətlər və təşkilatlarla əməkdaşlıq çərçivəsində praktiki bacarıqlara malik, karyera yönümlü mütəxəssislərin hazırlanması.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Modern curricula',                         'Development and implementation of curricula in industrial engineering, sustainable economy, circular economy, and management in line with modern and international standards.'),
    (2, 'Joint research with industry',             'Conducting scientific research together with various industrial enterprises, building economic and management models, and developing innovative solutions.'),
    (3, 'Development of methods and approaches',    'Development of methods and approaches in the fields of industrial engineering, project management, and sustainable economy.'),
    (4, 'Career-oriented specialist training',      'Training of career-oriented specialists with practical skills within the framework of cooperation with companies and organizations.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'industrial_engineering_and_sustainable_economy',
        'İlkin', 'Məhərrəmov', 'Ələddin oğlu',
        'ilkin.maharramov@aztu.edu.az',
        '+994 55 547 22 64',
        'I korpus, 423-cü otaq',
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
    'Riyaziyyat üzrə fəlsəfə doktoru',
    NULL,
    '<p>Məhərrəmov İlkin Ələddin oğlu — riyaziyyat üzrə fəlsəfə doktoru, optimal idarəetmə, hesablama riyaziyyatı, informasiyanın işlənməsi, data analitika sahələri üzrə ixtisaslaşmışdır. O, qeyd olunan istiqamətlərdə elmi və pedaqoji fəaliyyət göstərir.</p><p>Onun elmi tədqiqatlarının əsas istiqamətlərinə optimal idarəetmə məsələsi, riyazi modelin qurulması, informasiyanın işlənməsi daxildir. Bu sahələr üzrə apardığı tədqiqatların nəticələri nüfuzlu elmi jurnallarda dərc olunmuşdur.</p><p>Məhərrəmov İ.Ə. pedaqoji fəaliyyətində tələbələrin analitik və tənqidi düşünmə bacarıqlarının inkişafına, eləcə də gənc mütəxəssislərin hazırlanması və elmi-tədqiqat fəaliyyətinə cəlb olunmasına xüsusi önəm verir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının müdiri vəzifəsində çalışır.</p><p>O, 20-dən çox elmi məqalənin və konfrans materialının müəllifi, 1 kitabın həmmüəllifi, həmçinin təhsil sahəsində uğurlu fəaliyyətlə məşğuldur, Dövlət İmtahan Mərkəzinin ekspertidir.</p>',
    '["Optimal idarəetmə", "Sistemli analiz və informasiyanın işlənməsi", "Neftçıxarma prosesində optimallaşdırma məsələsi", "Data analitika və süni intellektin tətbiqləri", "Riyazi modelləşmə"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Ph.D. in Mathematics',
    NULL,
    '<p>Maharramov Ilkin Aladdin is a Ph.D. in Mathematics, specializing in optimal control, computational mathematics, information processing, and data analytics. He carries out scientific and pedagogical activities in these areas.</p><p>The main directions of his scientific research include optimal control problems, the construction of mathematical models, and information processing. The results of his research in these areas have been published in prestigious scientific journals.</p><p>In his pedagogical activity, Maharramov I.A. pays special attention to the development of students'' analytical and critical thinking skills, as well as the training of young specialists and their involvement in scientific research activities.</p><p>Currently, he serves as the head of the Department of Industrial Engineering and Sustainable Economy of Azerbaijan Technical University.</p><p>He is the author of more than 20 scientific articles and conference materials, co-author of 1 book, engaged in successful activity in the field of education, and an expert of the State Examination Center.</p>',
    '["Optimal control", "Systems analysis and information processing", "Optimization problems in oil extraction processes", "Data analytics and applications of artificial intelligence", "Mathematical modeling"]'::jsonb,
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
    FROM cafedra_directors WHERE cafedra_code = 'industrial_engineering_and_sustainable_economy'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Cümə axşamı', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Thursday',          NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '2005', '2009', NOW() FROM cafedra_directors WHERE cafedra_code = 'industrial_engineering_and_sustainable_economy'
UNION ALL
SELECT id, '2009', '2011', NOW() FROM cafedra_directors WHERE cafedra_code = 'industrial_engineering_and_sustainable_economy'
UNION ALL
SELECT id, '2017', '2021', NOW() FROM cafedra_directors WHERE cafedra_code = 'industrial_engineering_and_sustainable_economy';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'industrial_engineering_and_sustainable_economy')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bakalavr (Riyaziyyat)',                                                                 'Bakı Dövlət Universiteti'),
    (2, 'Magistratura (Hesablama Riyaziyyatı)',                                                  'Bakı Dövlət Universiteti'),
    (3, 'Doktorantura (Sistemli analiz, idarəetmə və informasiyanın işlənməsi)',                 'Bakı Dövlət Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bachelor''s (Mathematics)',                                                              'Baku State University'),
    (2, 'Master''s (Computational Mathematics)',                                                  'Baku State University'),
    (3, 'Doctorate (Systems Analysis, Management and Information Processing)',                    'Baku State University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'industrial_engineering_and_sustainable_economy';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('industrial_engineering_and_sustainable_economy', 'Ləman',     'Aslanzadə',     'Sərdar qızı',       'laman.aslanzada@aztu.edu.az',     '+994 50 430 30 69', NOW()),  -- 1
    ('industrial_engineering_and_sustainable_economy', 'Aynur',     'Qədimli',       'İbrahim qızı',      'aynur.gadimli@aztu.edu.az',       '+994 50 777 46 64', NOW()),  -- 2
    ('industrial_engineering_and_sustainable_economy', 'İlham',     'Aslanzadə',     'Alıcı oğlu',        'aslanzade.ilham@aztu.edu.az',     '+994 77 315 54 60', NOW()),  -- 3
    ('industrial_engineering_and_sustainable_economy', 'Əliheydər', 'Panəliyev',     'Vəliəhəd oğlu',     'aliheydar.panaliyev@aztu.edu.az', '+994 50 356 64 90', NOW()),  -- 4
    ('industrial_engineering_and_sustainable_economy', 'Cavid',     'Bədəlov',       'Əliyar oğlu',       'cavid.bedelov@aztu.edu.az',       '+994 50 642 36 49', NOW()),  -- 5
    ('industrial_engineering_and_sustainable_economy', 'Pərvanə',   'Məmmədova',     'Vaqif qızı',        'pervane.mammedova@aztu.edu.az',   '+994 55 387 06 10', NOW()),  -- 6
    ('industrial_engineering_and_sustainable_economy', 'Ramil',     'Quliyev',       'Hacırza oğlu',      'ramil.quliyev@aztu.edu.az',       '+994 55 219 50 40', NOW()),  -- 7
    ('industrial_engineering_and_sustainable_economy', 'Azət',      'Bağırova',      'Lətif qızı',        'azet.bagirova@aztu.edu.az',       '+994 55 684 01 99', NOW()),  -- 8
    ('industrial_engineering_and_sustainable_economy', 'Pərvin',    'Soltanlı',      'Sidqi qızı',        'pervin.soltanli@aztu.edu.az',     '+994 50 785 12 10', NOW()),  -- 9
    ('industrial_engineering_and_sustainable_economy', 'Xanım',     'Ağayeva',       'Yusif qızı',        'xanim.agayeva@aztu.edu.az',       '+994 55 227 14 87', NOW()),  -- 10
    ('industrial_engineering_and_sustainable_economy', 'Xəyalla',   'Əliyeva',       'Həsən qızı',        'xayalla.aliyeva@aztu.edu.az',     '+994 55 779 29 18', NOW()),  -- 11
    ('industrial_engineering_and_sustainable_economy', 'Bəxtiyar',  'Bədəlov',       'Laçın oğlu',        'baxtiyarov.baxtiyar@aztu.edu.az', '+994 55 575 58 78', NOW()),  -- 12
    ('industrial_engineering_and_sustainable_economy', 'Orxan',     'Vətənxah',      'Mirzağa oğlu',      'orxan.vatan@aztu.edu.az',         '+994 51 390 05 40', NOW()),  -- 13
    ('industrial_engineering_and_sustainable_economy', 'Arzu',      'Hüseynova',     'Doğru qızı',        'khumar.shiraliyeva@aztu.edu.az',  '+994 55 232 07 67', NOW()),  -- 14
    ('industrial_engineering_and_sustainable_economy', 'Şəhla',     'Qəhrəmanova',   'Şəki qızı',         'shahla.qahramanova@aztu.edu.az',  '+994 50 623 71 74', NOW()),  -- 15
    ('industrial_engineering_and_sustainable_economy', 'Mürşüd',    'Mehdiyev',      'Natiq oğlu',        'murshud.mehdiyev@aztu.edu.az',    '+994 50 688 84 82', NOW()),  -- 16
    ('industrial_engineering_and_sustainable_economy', 'Aynur',     'Babayeva',      'Nəbi qızı',         'aynur.babayeva@aztu.edu.az',      '+994 70 372 61 19', NOW()),  -- 17
    ('industrial_engineering_and_sustainable_economy', 'Aytən',     'Şıxaliyeva',    'Çingiz qızı',       'aytan.shikhaliyeva@aztu.edu.az',  '+994 55 571 55 33', NOW()),  -- 18
    ('industrial_engineering_and_sustainable_economy', 'Təranə',    'Səlifova',      'Şahvələt qızı',     'terane.salifova@aztu.edu.az',     '+994 50 443 48 33', NOW()),  -- 19
    ('industrial_engineering_and_sustainable_economy', 'Fariz',     'Məmmədov',      'Orucalı oğlu',      'fariz.mammadov@aztu.edu.az',      '+994 50 311 27 96', NOW()),  -- 20
    ('industrial_engineering_and_sustainable_economy', 'Aytən',     'Şıxıyeva',      'Ənvərpaşa qızı',    'aytan.shixiyeva@aztu.edu.az',     '+994 55 410 13 58', NOW()),  -- 21
    ('industrial_engineering_and_sustainable_economy', 'Anar',      'Muradov',       'Niyazi oğlu',       'anar.muradov@aztu.edu.az',        '+994 50 499 27 91', NOW()),  -- 22
    ('industrial_engineering_and_sustainable_economy', 'Kamran',    'Rəsulov',       'Ağaəli oğlu',       'kamran.resulov@aztu.edu.az',      '+994 50 361 26 26', NOW()),  -- 23
    ('industrial_engineering_and_sustainable_economy', 'Hafiz',     'Cəfərzadə',     'Elşad oğlu',        'hafiz.jafarzade@aztu.edu.az',     '+994 55 644 12 54', NOW()),  -- 24
    ('industrial_engineering_and_sustainable_economy', 'Əlabbas',   'Azadov',        'Ağarza oğlu',       'alabbas.azadov@aztu.edu.az',      '+994 51 880 16 06', NOW()),  -- 25
    ('industrial_engineering_and_sustainable_economy', 'Rəfael',    'Mərdiyev',      'Əli oğlu',          'rafael.mardiyev@aztu.edu.az',     '+994 55 202 93 83', NOW()),  -- 26
    ('industrial_engineering_and_sustainable_economy', 'Bəxtiyar',  'Hacızadə',      'Samir oğlu',        'bakhtiyar.hajizadeh@aztu.edu.az', '+994 998 19 65 00', NOW()),  -- 27
    ('industrial_engineering_and_sustainable_economy', 'Kənan',     'Məmmədov',      'Ələsgər oğlu',      'kenan.mammadov@aztu.edu.az',      '+994 50 244 00 91', NOW()),  -- 28
    ('industrial_engineering_and_sustainable_economy', 'Günel',     'Teymurova',     'Məmmədcamal qızı',  'gunel.teymurova@aztu.edu.az',     '+994 51 796 55 61', NOW())   -- 29
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının müəllim köməkçisi', NULL::varchar, NULL::varchar),
    (2,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının kargüzarı',         NULL,          NULL),
    (3,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının professoru',        'Professor',   'i.e.d.'),
    (4,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      NULL),
    (5,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      'i.f.d.'),
    (6,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      'i.f.d.'),
    (7,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      'i.f.d.'),
    (8,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      'i.e.n.'),
    (9,  'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (10, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      'i.f.d.'),
    (11, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (12, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (13, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (14, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının professoru',        'Professor',   'i.e.d.'),
    (15, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (16, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (17, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      NULL),
    (18, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (19, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      'Dosent',      NULL),
    (20, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      NULL),
    (21, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (22, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (23, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          'i.f.d.'),
    (24, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (25, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (26, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (27, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının baş müəllimi',      NULL,          NULL),
    (28, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      NULL),
    (29, 'Sənaye mühəndisliyi və davamlı iqtisadiyyat kafedrasının dosenti',           'Dosent',      't.f.d.')
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Teaching Assistant at the Department of Industrial Engineering and Sustainable Economy', NULL::varchar,         NULL::varchar),
    (2,  'Clerk at the Department of Industrial Engineering and Sustainable Economy',              NULL,                  NULL),
    (3,  'Professor at the Department of Industrial Engineering and Sustainable Economy',          'Professor',           'Doctor of Economic Sciences'),
    (4,  'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', NULL),
    (5,  'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', 'PhD in Economics'),
    (6,  'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', 'PhD in Economics'),
    (7,  'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', 'PhD in Economics'),
    (8,  'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', 'Candidate of Economic Sciences'),
    (9,  'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (10, 'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', 'PhD in Economics'),
    (11, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (12, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (13, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (14, 'Professor at the Department of Industrial Engineering and Sustainable Economy',          'Professor',           'Doctor of Economic Sciences'),
    (15, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (16, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (17, 'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', NULL),
    (18, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (19, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    'Associate Professor', NULL),
    (20, 'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', NULL),
    (21, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (22, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (23, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  'PhD in Economics'),
    (24, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (25, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (26, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (27, 'Senior Lecturer at the Department of Industrial Engineering and Sustainable Economy',    NULL,                  NULL),
    (28, 'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', NULL),
    (29, 'Associate Professor at the Department of Industrial Engineering and Sustainable Economy','Associate Professor', 'PhD in Technical Sciences')
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
