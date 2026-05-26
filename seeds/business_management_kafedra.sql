-- ============================================================
-- "Biznesin idarə edilməsi" kafedrası — Full DB Import
-- cafedra_code: 'business_management'
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
    'business_management',
    3, 1, 0, 10, 0, 0, 8,
    '[4, 9, 12]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'business_management',
    'az',
    'Biznesin idarə edilməsi kafedrası',
    '<p>Biznesin idarə edilməsi kafedrası Azərbaycan Texniki Universitetinin (AzTU) rektorunun əmri ilə 10 yanvar 2025-ci ildə Yüksək Təhsil İnstitunun nəzdində yaradılmışdır. 09 iyul 2025-ci il tarixində AzTU rektorunun əmri Kafedra Yüksək Təhsil İnstitutunun tərkibindən Sənaye iqtisadiyyatı və menecment fakültəsinin tərkibinə verilmişdir. Kafedra tələbələrə müasir biznes və marketinq bacarıqları qazandırmağı, real biznes problemlərinin üzərində çalışmaqla praktiki bacarıqların inkişafını biznes sahəsində aktual mövzuların araşdırılmasını, sahibkarlığın təşviqi və əmək bazarına uyğun mütəxəssis hazırlamağı qarşısına məqsəd qoymuşdur.</p><p>Kafedranın missiyası müasir bilik və bacarıqlara malik, etik dəyərlərə sadiq, innovativ düşüncəli, və rəqabətqabiliyyətli mütəxəssislər hazırlamaqdır. Kafedra elmi tədqiqatlar apararaq cəmiyyətin sosial-iqtisadi inkişafına töhfə verməyi hədəfləməkdədir.</p><p>Biznesin idarə edilməsi kafedrası təhsil, elmi-tədqiqat və biznes mühiti ilə əməkdaşlığın vəhdət təşkil etdiyi müasir və inklüziv akademik ekosistemin formalaşdırılmasına yönəlmişdir. Marketinq, biznes analitikası, istehlakçı davranışları, sosial media marketinqi sahibkarlıq və karyera planlaması istiqamətlərində həyata keçirilən təşəbbüslər vasitəsilə nəzəri biliklərin praktik tətbiqlərə çevrilməsi təmin olunur. Müasir biznes trendləri, innovativ yanaşmalar və əmək bazarının tələbləri nəzərə alınaraq tələbələrin peşəkar inkişafı, biznes bacarıqları və rəqabətqabiliyyətli karyera quruculuğu dəstəklənir.</p>',
    NOW()
),
(
    'business_management',
    'en',
    'Department of Business Management',
    '<p>The Department of Business Management was established under the Higher Education Institute by the order of the Rector of Azerbaijan Technical University (AzTU) on January 10, 2025. By the order of the AzTU Rector dated July 9, 2025, the department was transferred from the Higher Education Institute to the Faculty of Industrial Economics and Management. The department aims to equip students with modern business and marketing skills, to develop practical abilities by working on real business problems, to research current topics in the field of business, to promote entrepreneurship, and to train specialists suited to the labor market.</p><p>The mission of the department is to train specialists with modern knowledge and skills, committed to ethical values, innovative thinking, and competitiveness. The department aims to contribute to the socio-economic development of society by conducting scientific research.</p><p>The Department of Business Management is focused on forming a modern and inclusive academic ecosystem in which education, scientific research, and cooperation with the business environment are combined. Through initiatives carried out in the directions of marketing, business analytics, consumer behavior, social media marketing, entrepreneurship, and career planning, the transformation of theoretical knowledge into practical applications is ensured. Taking into account modern business trends, innovative approaches, and the demands of the labor market, students'' professional development, business skills, and competitive career building are supported.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'business_management';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('business_management', 1, NOW()),
    ('business_management', 2, NOW()),
    ('business_management', 3, NOW()),
    ('business_management', 4, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Müasir tədris proqramları',          'Biznesin idarə edilməsi, marketinq və sahibkarlıq üzrə müasir və beynəlxalq standartlara uyğun tədris proqramlarının hazırlanması və tətbiqi.'),
    (2, 'Bazar araşdırmaları və elmi tədqiqatlar', 'Müxtəlif biznes sahələri üzrə bazar araşdırmaları, marketinq strategiyaları və idarəetmə modelləri istiqamətində elmi tədqiqatların aparılması və innovativ həllərin işlənməsi.'),
    (3, 'Karyera və liderlik inkişafı',       'Karyera planlaması, liderlik və şəxsi inkişaf sahələrində metod və yanaşmaların inkişaf etdirilməsi.'),
    (4, 'Karyerayönümlü mütəxəssis hazırlığı','Şirkətlər və təşkilatlarla əməkdaşlıq çərçivəsində praktiki bacarıqlara malik, karyera yönümlü mütəxəssislərin hazırlanması.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Modern curricula',                       'Development and implementation of curricula in business management, marketing, and entrepreneurship in line with modern and international standards.'),
    (2, 'Market research and scientific studies', 'Conducting market research, scientific studies in marketing strategies and management models across various business fields, and developing innovative solutions.'),
    (3, 'Career and leadership development',      'Development of methods and approaches in the fields of career planning, leadership, and personal development.'),
    (4, 'Career-oriented specialist training',    'Training of career-oriented specialists with practical skills within the framework of cooperation with companies and organizations.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'business_management',
        'Oqtay', 'Quliyev', 'Qulu oğlu',
        'oktay.guliyev@aztu.edu.az',
        '+994 50 556 30 33',
        'I korpus, 428-ci otaq',
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
    'iqtisad üzrə fəlsəfə doktoru',
    'dosent',
    '<p>Quliyev Oqtay Qulu oğlu — iqtisad üzrə fəlsəfə doktoru, dosent, marketinq, istehlakçı davranışları sahəsi üzrə ixtisaslaşmış alimdir. O, marketinq istiqamətində elmi və pedaqoji fəaliyyət göstərir.</p><p>Onun elmi tədqiqatlarının əsas istiqamətlərinə istehlakçı davranışları, marketinq tədqiqatları və sosial media marketinqi daxildir. Bu sahələr üzrə apardığı tədqiqatların nəticələri nüfuzlu elmi jurnallarda dərc olunmuş və marketinq sahəsinin inkişafına mühüm töhfə vermişdir.</p><p>Quliyev O. Q. pedaqoji fəaliyyətində istehlakçı davranışları, marketinq tədqiqatları sahəsində tədqiqatlar apararaq tələbələrin analitik və tənqidi düşünmə bacarıqlarının inkişafına, eləcə də gənc mütəxəssislərin hazırlanması və elmi-tədqiqat fəaliyyətinə cəlb olunmasına xüsusi önəm verir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin Biznesin idarə edilməsi kafedrasının müdiri vəzifəsində çalışır.</p><p>O, 20-dən çox elmi məqalənin müəllifi, 2 kitabın həmmüəllifi və 2 kitabın elmi redaktorudur. Son iki ildə KOBİA-nın 10-dan çox tədqiqatını həyata keçirmişdir.</p>',
    '["Marketinq", "Marketinq tədqiqatları", "İstehlakçı davranışları", "Rəqəmsal marketinq", "Sosial media marketinq"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'PhD in Economics',
    'Associate Professor',
    '<p>Guliyev Oktay Gulu oglu is a PhD in Economics, Associate Professor, and a scholar specialized in marketing and consumer behavior. He carries out scientific and pedagogical activities in the field of marketing.</p><p>The main directions of his scientific research include consumer behavior, marketing research, and social media marketing. The results of his research in these areas have been published in prestigious scientific journals and have made significant contributions to the development of the marketing field.</p><p>In his pedagogical activity, Guliyev O.Q. pays special attention to the development of students'' analytical and critical thinking skills through research in consumer behavior and marketing studies, as well as to the training of young specialists and their involvement in scientific research activities.</p><p>Currently, he serves as the head of the Department of Business Management of Azerbaijan Technical University.</p><p>He is the author of more than 20 scientific articles, co-author of 2 books, and scientific editor of 2 books. Over the past two years, he has carried out more than 10 studies for SMBDA (KOBİA).</p>',
    '["Marketing", "Marketing research", "Consumer behavior", "Digital marketing", "Social media marketing"]'::jsonb,
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
    FROM cafedra_directors WHERE cafedra_code = 'business_management'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Çərşənbə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Wednesday',      NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '2000', '2004', NOW() FROM cafedra_directors WHERE cafedra_code = 'business_management'
UNION ALL
SELECT id, '2005', '2007', NOW() FROM cafedra_directors WHERE cafedra_code = 'business_management'
UNION ALL
SELECT id, '2007', '2012', NOW() FROM cafedra_directors WHERE cafedra_code = 'business_management';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'business_management')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bakalavr (Biznesin idarə edilməsi)',                    'Azərbaycan Dövlət İqtisad Universiteti'),
    (2, 'Magistratura (İstehsalın idarə edilməsi və marketinq)', 'Türkiyə Respublikası Sakarya Universiteti'),
    (3, 'Doktorantura (İstehsalın idarə edilməsi və marketinq)', 'Türkiyə Respublikası Sakarya Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bachelor''s (Business Management)',                  'Azerbaijan State University of Economics'),
    (2, 'Master''s (Production Management and Marketing)',    'Sakarya University, Republic of Türkiye'),
    (3, 'Doctorate (Production Management and Marketing)',    'Sakarya University, Republic of Türkiye')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'business_management';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('business_management', 'Sədaqət', 'Əbdurəhmanova', 'Əyyub qızı',     'sedaqet.abdurahmanova@aztu.edu.az', '+994 50 391 72 82', NOW()),  -- 1
    ('business_management', 'Samirə',  'Əhmədova',      'Raqif qızı',     'ehmedova.samire@aztu.edu.az',       '+994 50 209 02 62', NOW()),  -- 2
    ('business_management', 'Lalə',    'Neymətova',     'Tofiq qızı',     'lale.neymetova@aztu.edu.az',        '+994 51 303 85 58', NOW()),  -- 3
    ('business_management', 'Rəşad',   'Əliyev',        'Yavər oğlu',     'rashad.aliyev@aztu.edu.az',         '+994 50 256 62 62', NOW()),  -- 4
    ('business_management', 'Ceyhun',  'Haciyev',       'Gülməmməd oğlu', 'ceyhun.hajiyev@aztu.edu.az',        '+994 50 245 33 63', NOW()),  -- 5
    ('business_management', 'Natiq',   'Məmmədov',      'Oqtay oğlu',     'natig.mammadov@aztu.edu.az',        '+994 55 639 84 00', NOW()),  -- 6
    ('business_management', 'Aytən',   'Məmmədova',     'Alxan qızı',     'aytan.mammadova@aztu.edu.az',       '+994 50 604 00 16', NOW()),  -- 7
    ('business_management', 'Gülər',   'Quliyeva',      'Şahin qızı',     'gular.guliyeva@aztu.edu.az',        '+994 50 505 53 15', NOW()),  -- 8
    ('business_management', 'Aygün',   'Şirin',         'Nəriman qızı',   'aygun.shirin@aztu.edu.az',          '+994 55 517 41 43', NOW()),  -- 9
    ('business_management', 'Pərvin',  'Hacıyeva',      'Xaqani qızı',    'Parvin.haciyeva@aztu.edu.az',       '+994 50 303 94 81', NOW()),  -- 10
    ('business_management', 'Fəxri',   'Əbilov',        'Tərlan oğlu',    'fakhri.abilov@aztu.edu.az',         '+994 55 208 21 22', NOW()),  -- 11
    ('business_management', 'Günel',   'Şahmarova',     'Şahvələd qızı',  'gunel.shahmarova@aztu.edu.az',      '+994 50 261 38 16', NOW()),  -- 12
    ('business_management', 'Elvira',  'Cəbrayılzadə',  'Vüqar qızı',     'elvira.jabrailzade@aztu.edu.az',    '+994 50 382 69 17', NOW())   -- 13
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Biznesin idarə edilməsi kafedrasının dosenti',            'Dosent', 'i.e.n.'),
    (2,  'Biznesin idarə edilməsi kafedrasının dosenti',            'Dosent', 'i.f.d.'),
    (3,  'Biznesin idarə edilməsi kafedrasının dosenti',            'Dosent', 'i.f.d.'),
    (4,  'Biznesin idarə edilməsi kafedrasının dosenti',            'Dosent', 'i.f.d.'),
    (5,  'Biznesin idarə edilməsi kafedrasının dosenti',            'Dosent', 'i.f.d.'),
    (6,  'Biznesin idarə edilməsi kafedrasının baş müəllimi',       NULL::varchar, NULL::varchar),
    (7,  'Biznesin idarə edilməsi kafedrasının baş müəllimi',       NULL,          NULL),
    (8,  'Biznesin idarə edilməsi kafedrasının baş müəllimi',       NULL,          NULL),
    (9,  'Biznesin idarə edilməsi kafedrasının baş müəllimi',       NULL,          NULL),
    (10, 'Biznesin idarə edilməsi kafedrasının 0.5 ştat baş müəllimi', NULL,       NULL),
    (11, 'Biznesin idarə edilməsi kafedrasının müəllimi',           NULL,          NULL),
    (12, 'Biznesin idarə edilməsi kafedrasının 0.5 ştat assistenti',NULL,          NULL),
    (13, 'Biznesin idarə edilməsi kafedrasının kargüzarı',          NULL,          NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Associate Professor at the Department of Business Management',          'Associate Professor', 'Candidate of Economic Sciences'),
    (2,  'Associate Professor at the Department of Business Management',          'Associate Professor', 'PhD in Economics'),
    (3,  'Associate Professor at the Department of Business Management',          'Associate Professor', 'PhD in Economics'),
    (4,  'Associate Professor at the Department of Business Management',          'Associate Professor', 'PhD in Economics'),
    (5,  'Associate Professor at the Department of Business Management',          'Associate Professor', 'PhD in Economics'),
    (6,  'Senior Lecturer at the Department of Business Management',              NULL::varchar,         NULL::varchar),
    (7,  'Senior Lecturer at the Department of Business Management',              NULL,                  NULL),
    (8,  'Senior Lecturer at the Department of Business Management',              NULL,                  NULL),
    (9,  'Senior Lecturer at the Department of Business Management',              NULL,                  NULL),
    (10, 'Senior Lecturer (0.5 rate) at the Department of Business Management',   NULL,                  NULL),
    (11, 'Lecturer at the Department of Business Management',                     NULL,                  NULL),
    (12, 'Assistant (0.5 rate) at the Department of Business Management',         NULL,                  NULL),
    (13, 'Clerk at the Department of Business Management',                        NULL,                  NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
