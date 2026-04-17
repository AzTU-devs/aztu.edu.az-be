-- ============================================================
-- Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası — Full DB Import
-- cafedra_code: 'transport_logistics_traffic_safety'
-- faculty_code: 'transport_logistics'
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
    'transport_logistics',
    'transport_logistics_traffic_safety',
    3, 2, 0, 4, 0, 0, 0,
    '[9, 12, 4, 8]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'transport_logistics_traffic_safety',
    'az',
    'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası',
    '<p>"Nəqliyyat logistikası və hərəkətin təhlükəsizliyi" kafedrası universitetin mühüm elmi-tədris struktur bölmələrindən biridir və nəqliyyat, logistika və yol hərəkətinin təhlükəsizliyi sahələrində yüksək ixtisaslı mütəxəssislərin hazırlanmasını həyata keçirir.</p><p>Kafedra 1978-ci ildə Avtomobillər kafedrasının bazasında "Avtomobil nəqliyyatının istismarı və yol hərəkətinin təhlükəsizliyi" adı ilə yaradılmışdır. Sonralar kafedranın adı "Avtomobil daşımalarının və yol hərəkətinin təşkili" kimi dəyişdirilmiş, 2019-cu ildən etibarən isə "Nəqliyyat logistikası və hərəkətin təhlükəsizliyi" kafedrası adlandırılmışdır.</p><p>Kafedranın əsas məqsədi nəqliyyat logistikası, nəqliyyatın təşkili və idarə olunması, nəqliyyat sistemləri və yol hərəkətinin təhlükəsizliyi sahələrində nəzəri biliklərə və praktiki bacarıqlara malik mütəxəssislər yetişdirməkdir. Tədris prosesində müasir tədris metodlarından, laboratoriya avadanlıqlarından və beynəlxalq təcrübədən istifadə olunur.</p><p>Kafedrada həyata keçirilən tədris proqramları milli və beynəlxalq təhsil standartlarına uyğun şəkildə təşkil olunur və mövcud akkreditasiya tələblərinə cavab verir. Bu istiqamətdə Almaniyanın keyfiyyət təminatı agentliyi olan AQAS tərəfindən kafedrada tədris olunan ixtisas proqramları üzrə beynəlxalq akkreditasiya prosesi həyata keçirilmişdir.</p><p>Kafedrada elmi-tədqiqat fəaliyyəti əsas və prioritet istiqamətlərdən biridir. Kafedranın professor-müəllim heyəti müxtəlif elmi layihələrdə iştirak edir, beynəlxalq və respublika səviyyəli elmi jurnallarda məqalələr dərc etdirir, elmi konfrans və seminarlarda fəal məruzələrlə çıxış edir.</p>',
    NOW()
),
(
    'transport_logistics_traffic_safety',
    'en',
    'Department of Transport Logistics and Traffic Safety',
    '<p>The "Transport Logistics and Traffic Safety" department is one of the important scientific-educational structural units of the university and carries out the training of highly qualified specialists in the fields of transport, logistics, and road traffic safety.</p><p>The department was established in 1978 on the basis of the Automobiles Department under the name "Operation of Automobile Transport and Road Traffic Safety." Later, the department was renamed to "Organization of Automobile Transportation and Road Traffic," and since 2019, it has been called the "Transport Logistics and Traffic Safety" department.</p><p>The main goal of the department is to train specialists with theoretical knowledge and practical skills in the fields of transport logistics, organization and management of transport, transport systems, and road traffic safety. Modern teaching methods, laboratory equipment, and international experience are used in the educational process.</p><p>The educational programs implemented at the department are organized in accordance with national and international educational standards and meet existing accreditation requirements. In this direction, the international accreditation process for specialty programs taught at the department has been carried out by AQAS, the German quality assurance agency.</p><p>Scientific research activity is one of the main and priority directions at the department. The department''s faculty participates in various scientific projects, publishes articles in international and national scientific journals, and actively presents reports at scientific conferences and seminars.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'transport_logistics_traffic_safety';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('transport_logistics_traffic_safety', 1, NOW()),
    ('transport_logistics_traffic_safety', 2, NOW()),
    ('transport_logistics_traffic_safety', 3, NOW()),
    ('transport_logistics_traffic_safety', 4, NOW()),
    ('transport_logistics_traffic_safety', 5, NOW()),
    ('transport_logistics_traffic_safety', 6, NOW()),
    ('transport_logistics_traffic_safety', 7, NOW()),
    ('transport_logistics_traffic_safety', 8, NOW()),
    ('transport_logistics_traffic_safety', 9, NOW()),
    ('transport_logistics_traffic_safety', 10, NOW()),
    ('transport_logistics_traffic_safety', 11, NOW()),
    ('transport_logistics_traffic_safety', 12, NOW()),
    ('transport_logistics_traffic_safety', 13, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1,  'Logistika və nəqliyyat texnologiyaları mühəndisliyi',              'Logistika və nəqliyyat texnologiyaları sahəsində mühəndis kadrların hazırlanması'),
    (2,  'Nəqliyyat logistikası (Transport logistics)',                       'Nəqliyyat logistikası sahəsində tədris və tədqiqat işlərinin aparılması'),
    (3,  'Şəhər nəqliyyat şəbəkəsi və nəqliyyat xidmətinin təşkili',       'Şəhər nəqliyyat şəbəkələrinin planlaşdırılması və nəqliyyat xidmətinin təşkili'),
    (4,  'Nəqliyyat xidmətləri üçün böhran və risklərin idarə edilməsi',    'Nəqliyyat sahəsində böhran vəziyyətlərinin idarə edilməsi və risklərin qiymətləndirilməsi'),
    (5,  'Nəqliyyatda daşımalar və menecment',                               'Avtomobil nəqliyyatı üzrə daşımaların təşkili və menecment'),
    (6,  'Beynəlxalq daşımalar',                                            'Beynəlxalq yük və sərnişin daşımalarının təşkili'),
    (7,  'Yol hərəkətinin təşkili və təhlükəsizliyi',                       'Yol hərəkətinin təşkili, nizamlanması və təhlükəsizliyinin təmin edilməsi'),
    (8,  'Nəqliyyat əməliyyatlarının intellektual idarə edilməsi',          'Ağıllı nəqliyyat sistemləri vasitəsilə nəqliyyat əməliyyatlarının idarə edilməsi'),
    (9,  'Yol-nəqliyyat hadisələrinin ekspertizası',                         'Yol-nəqliyyat hadisələrinin avtotexniki ekspertizası və təhlili'),
    (10, 'Yol hərəkətinin təşkilinin texniki nizamlama vasitələri',          'Yol hərəkətinin texniki vasitələrlə nizamlanması'),
    (11, 'Yol şəraitləri və hərəkətin təhlükəsizliyi',                      'Yol şəraitlərinin qiymətləndirilməsi və hərəkət təhlükəsizliyinin təmin edilməsi'),
    (12, 'Nəqliyyat axınları nəzəriyyəsi',                                  'Nəqliyyat axınlarının nəzəri əsaslarının tədqiqi və modelləşdirilməsi'),
    (13, 'Avtomobil yolları',                                                'Avtomobil yollarının layihələndirilməsi, tikintisi və istismarı')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1,  'Logistics and transport technology engineering',                    'Training of engineering personnel in the field of logistics and transport technologies'),
    (2,  'Transport logistics',                                              'Conducting teaching and research activities in the field of transport logistics'),
    (3,  'Urban transport network and transport service organization',        'Planning of urban transport networks and organization of transport services'),
    (4,  'Crisis and risk management for transport services',                'Management of crisis situations and risk assessment in the transport sector'),
    (5,  'Transportation and management in transport',                       'Organization of transportation and management in automobile transport'),
    (6,  'International transportation',                                     'Organization of international freight and passenger transportation'),
    (7,  'Traffic organization and safety',                                  'Organization, regulation, and ensuring of road traffic safety'),
    (8,  'Intelligent management of transport operations',                   'Management of transport operations through intelligent transport systems'),
    (9,  'Road traffic accident expertise',                                  'Auto-technical expertise and analysis of road traffic accidents'),
    (10, 'Technical regulation means of traffic organization',               'Regulation of road traffic through technical means'),
    (11, 'Road conditions and traffic safety',                               'Assessment of road conditions and ensuring traffic safety'),
    (12, 'Theory of transport flows',                                        'Research and modeling of theoretical foundations of transport flows'),
    (13, 'Automobile roads',                                                 'Design, construction, and operation of automobile roads')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'transport_logistics_traffic_safety',
        'Razim', 'Bayramov', 'Paşa oğlu',
        'razim.bayramov@aztu.edu.az',
        '+994 50 315 36 72',
        'Bina 5, 5-ci mərtəbə, otaq 503',
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
    'Texnika elmləri namizədi (PhD)',
    'Dosent',
    '<p>Bayramov Razim Paşa oğlu 1959-cu ildə anadan olub. 1976-cı ildə orta məktəbi fərqlənmə ilə bitirərək, Ç. İldırım adına Azərbaycan Politexnik İnstituna (indiki AzTU) daxil olmuşdur. 1981-ci ildə həmin institutun Avtomobil nəqliyyatı fakültəsini fərqlənmə diplomu ilə bitirərək, yol hərəkəti üzrə mühəndis ixtisasına yiyələnib.</p><p>1981-ci ildən Azərbaycan Politexnik institutunun "Avtomobil daşımaları və yol hərəkətinin təşkili" kafedrasında assistent kimi əmək fəaliyyətinə başlamışdır. 1986-cı ildə müsabiqədən keçərək baş müəllim vəzifəsinə seçilib. 1991-ci ildə namizədlik dissertasiyasını müdafiə edərək texnika elmləri namizədi elmi adını alıb. 1993-cü ildə həmin kafedranın dosenti vəzifəsinə seçilib. 2017-ci il 3 iyuldan "Nəqliyyat logistikası və hərəkətin təhlükəsizliyi" kafedrasının müdiri vəzifəsinə seçilib.</p><p>100-dən çox elmi-metodiki əsərin, 2 dərs vəsaitinin və 6 dərsliyin, xaricdə nəşr olunan 3 məqələnin və 3 konfrans materiallarının müəllifi və həmmüəllifidir. H-indeksi 3-dür. 2019-cu ildə "Qabaqcıl təhsil işçisi" fəxri döş nişanı ilə, 2020-ci ildə Azərbaycan Respublikası Prezidentinin Fərmanı ilə Əməkdar mühəndis fəxri adına layiq görülüb.</p>',
    '["Yol hərəkətinin təşkili və təhlükəsizliyi", "Nəqliyyat logistikası və təchizat zəncirinin idarə edilməsi", "Multimodal və beynəlxalq daşımaların təşkili", "Ağıllı nəqliyyat sistemləri (ITS) və nəqliyyat mühəndisliyi", "Yol-nəqliyyat hadisələrinin avtotexniki ekspertizası", "Nəqliyyat vasitələrinin konstruksiya təhlükəsizliyi", "Nəqliyyat axınları nəzəriyyəsi və modelləşdirilməsi"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Candidate of Technical Sciences (PhD)',
    'Associate Professor',
    '<p>Razim Pasha Bayramov was born in 1959. In 1976, he graduated from secondary school with honors and entered the Azerbaijan Polytechnic Institute named after Ch. Ildirim (now AzTU). In 1981, he graduated from the Automobile Transport Faculty of the same institute with honors, obtaining a degree in road traffic engineering.</p><p>Since 1981, he started his career as an assistant at the "Organization of Automobile Transportation and Road Traffic" department of the Azerbaijan Polytechnic Institute. In 1986, he was elected to the position of senior lecturer through a competitive process. In 1991, he defended his candidate dissertation and received the scientific degree of Candidate of Technical Sciences. In 1993, he was elected to the position of Associate Professor of the same department. Since July 3, 2017, he has been elected as the Head of the "Transport Logistics and Traffic Safety" department.</p><p>He is the author and co-author of more than 100 scientific-methodological works, 2 textbook aids and 6 textbooks, 3 articles published abroad, and 3 conference materials. His H-index is 3. In 2019, he was awarded the honorary badge "Advanced Education Worker," and in 2020, by the Decree of the President of the Republic of Azerbaijan, he was awarded the honorary title of Honored Engineer.</p>',
    '["Traffic organization and safety", "Transport logistics and supply chain management", "Organization of multimodal and international transportation", "Intelligent transport systems (ITS) and transport engineering", "Auto-technical expertise of road traffic accidents", "Structural safety of vehicles", "Theory and modeling of transport flows"]'::jsonb,
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
    FROM cafedra_directors WHERE cafedra_code = 'transport_logistics_traffic_safety'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Çərşənbə, Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Wednesday, Friday',       NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1976', '1981', NOW() FROM cafedra_directors WHERE cafedra_code = 'transport_logistics_traffic_safety'
UNION ALL
SELECT id, '1986', '1991', NOW() FROM cafedra_directors WHERE cafedra_code = 'transport_logistics_traffic_safety';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'transport_logistics_traffic_safety')
    ORDER BY id DESC
    LIMIT 2
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bakalavr/Mühəndis (Avtomobil nəqliyyatı)', 'Azərbaycan Politexnik İnstitutu (indiki AzTU)'),
    (2, 'Texnika elmləri namizədi (PhD)',              'Azərbaycan Texniki Universiteti (AzTU)')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bachelor/Engineer (Automobile Transport)',          'Azerbaijan Polytechnic Institute (now AzTU)'),
    (2, 'Candidate of Technical Sciences (PhD)',             'Azerbaijan Technical University (AzTU)')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers (professors, associate professors, senior lecturers, assistants, clerk) ──
DELETE FROM cafedra_workers WHERE cafedra_code = 'transport_logistics_traffic_safety';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Professors (t.e.d.)
    ('transport_logistics_traffic_safety', 'Şamil',       'Heydərov',       'Hilal oğlu',          'heydarov.shamil@aztu.edu.az',         '+994 10 387 02 02',  NOW()),  -- 1
    ('transport_logistics_traffic_safety', 'Akif',        'Cahangirov',     'Əli oğlu',            'akif.cahangirov@aztu.edu.az',         '+994 50 210 3958',   NOW()),  -- 2
    ('transport_logistics_traffic_safety', 'Fuad',        'Həsənov',        'Fazil oğlu',          'hasanov.fuad@aztu.edu.az',            '+994 55 350 93 99',  NOW()),  -- 3
    -- Associate Professors (dosentlər)
    ('transport_logistics_traffic_safety', 'Əlləz',       'Əliyəv',         'Hacıəhməd oğlu',     'allaz.aliyev@aztu.edu.az',            '+994 50 327 27 92',  NOW()),  -- 4
    ('transport_logistics_traffic_safety', 'Fuad',        'Daşdəmirov',     'Səmid oğlu',          'fuad.dashdamirov@aztu.edu.az',        '+994 50 300 99 73',  NOW()),  -- 5
    ('transport_logistics_traffic_safety', 'Allahverdi',  'Şərifov',        'Camal oğlu',          'sharifov.allahverdi@aztu.edu.az',     '+994 50 346 57 66',  NOW()),  -- 6
    -- Senior Lecturers (Baş müəllimlər) — Əsas
    ('transport_logistics_traffic_safety', 'Yaşar',       'Mahmudov',       'Əli oğlu',            'yashar.mahmudov@aztu.edu.az',         '+994 55 713 08 08',  NOW()),  -- 7
    ('transport_logistics_traffic_safety', 'Nəsir',       'Nəcəfov',        'Sabir oğlu',          'necefov.nesir@aztu.edu.az',           '+994 70 662 04 06',  NOW()),  -- 8
    ('transport_logistics_traffic_safety', 'Elməddin',    'Salayev',        'Mübərrəd oğlu',      'elmeddin.salayev@aztu.edu.az',        '+994 55 568 37 63',  NOW()),  -- 9
    -- Assistants (Əsas)
    ('transport_logistics_traffic_safety', 'Arzu',        'Məmmədov',       'Arif oğlu',           'arzu.mammadov@aztu.edu.az',           '+994 55 858 15 81',  NOW()),  -- 10
    ('transport_logistics_traffic_safety', 'Hüsəyn',      'Əliyəv',         'Vaqif oğlu',          'huseyn.aliyev@aztu.edu.az',           '+994 51 740 49 11',  NOW()),  -- 11
    ('transport_logistics_traffic_safety', 'İbrahim',     'Məcidli',        'Rahib oğlu',          'ibrahim.majidli@aztu.edu.az',         '+994 99 376 02 18',  NOW()),  -- 12
    -- Senior Lecturers (Baş müəllimlər) — Daxili əvəzçiliklə
    ('transport_logistics_traffic_safety', 'Sahib',       'Əsgərov',        'Azər oğlu',           'sahib.asgarov@aztu.edu.az',           '+994 77 520 33 22',  NOW()),  -- 13
    -- Senior Lecturers (Baş müəllimlər) — Əvəzçiliklə
    ('transport_logistics_traffic_safety', 'Çingiz',      'Rəhimov',        'Həşim oğlu',          'chingiz.rahimov@aztu.edu.az',         '+994 70 216 16 85',  NOW()),  -- 14
    ('transport_logistics_traffic_safety', 'İlham',       'Hüsəynov',       'Dilqəm oğlu',        'ilham.huseynov@aztu.edu.az',          '+994 51 303 01 83',  NOW()),  -- 15
    ('transport_logistics_traffic_safety', 'Ramin',       'Abdullayev',     'Rauf oğlu',           'ramin.abdullayev@aztu.edu.az',        '+994 55 311 55 22',  NOW()),  -- 16
    ('transport_logistics_traffic_safety', 'Naridə',      'Zülfüqarova',    'Qaçay qızı',          'narida.zulfuqarova@aztu.edu.az',      '+994 51 468 56 62',  NOW()),  -- 17
    ('transport_logistics_traffic_safety', 'Nicat',       'Rəhimli',        'Vidadi oğlu',         'nicat.rehimli@aztu.edu.az',           '+994 55 418 00 65',  NOW()),  -- 18
    ('transport_logistics_traffic_safety', 'Vüsal',       'Əliyəv',         'Nürəddin oğlu',       'vusal.aliyev@aztu.edu.az',            '+994 77 277 77 01',  NOW()),  -- 19
    -- Senior Lecturers (Baş müəllimlər) — Daxili əvəzçiliklə (continued)
    ('transport_logistics_traffic_safety', 'Sevinc',      'Abdinzadə',      'Məhərrəm qızı',      'sevinc.abdinzade@aztu.edu.az',        '+994 51 777 27 85',  NOW()),  -- 20
    ('transport_logistics_traffic_safety', 'Məmməd',      'Məmmədov',       'Qurban oğlu',         'mammad.mammadov@aztu.edu.az',         '+994 51 526 66 41',  NOW()),  -- 21
    ('transport_logistics_traffic_safety', 'Turan',       'Verdiyəv',       'Şəmsi oğlu',          'turan.verdiyev@aztu.edu.az',          '+994 50 762 80 62',  NOW()),  -- 22
    ('transport_logistics_traffic_safety', 'Mahir',       'Mustafayəv',     'Mustafa oğlu',        'mahir.mustafayev@aztu.edu.az',        '+994 51 615 62 55',  NOW()),  -- 23
    ('transport_logistics_traffic_safety', 'Ülvi',        'Cavadlı',        'Yusif oğlu',          'ulvi.cavadli@aztu.edu.az',            '+994 77 343 00 81',  NOW()),  -- 24
    -- Senior Lecturers (Baş müəllimlər) — Əvəzçiliklə (continued)
    ('transport_logistics_traffic_safety', 'Mirmahmud',   'Əhmədov',        'Mirəhməd oğlu',       'mirmahmud.ehmedov@aztu.edu.az',       '+994 55 835 01 64',  NOW()),  -- 25
    ('transport_logistics_traffic_safety', 'Əli',         'Quliyəv',        'Şəmsəddin oğlu',      'ali.quliyev@aztu.edu.az',             '+994 50 322 56 21',  NOW()),  -- 26
    -- Assistants — Daxili əvəzçiliklə
    ('transport_logistics_traffic_safety', 'Yaşar',       'İsrəfilov',      'Mirbağır oğlu',       'yashar.israfilov@aztu.edu.az',        '+994 55 645 14 13',  NOW()),  -- 27
    -- Assistants — Əvəzçiliklə
    ('transport_logistics_traffic_safety', 'Sərxan',      'Məcidov',        'Mahmudəli oğlu',      'serxan.mecidov@aztu.edu.az',          '+994 70 676 80 95',  NOW()),  -- 28
    -- Clerk (Kargüzar)
    ('transport_logistics_traffic_safety', 'Rəna',        'Əliyeva',        'Rəvan qızı',          'rena.eliyeva@aztu.edu.az',            '+994 50 723 62 848', NOW())   -- 29
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Professors
    (1,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, məsləhətçi professor',           'Professor',  't.e.d.'),
    (2,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, professor (0.5 şt.)',             'Professor',  't.e.d.'),
    (3,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, professor',                       'Professor',  't.e.d.'),
    -- Associate Professors
    (4,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, dosent (1.5 şt.)',               'Dosent',     't.e.n.'),
    (5,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, dosent (0.5 şt., daxili əvəzçiliklə)', 'Dosent', 't.f.d.'),
    (6,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, dosent (0.5 şt., daxili əvəzçiliklə)', 'Dosent', 't.f.d.'),
    -- Senior Lecturers (Əsas)
    (7,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim',                    NULL,         NULL),
    (8,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim',                    NULL,         NULL),
    (9,  'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim',                    NULL,         NULL),
    -- Assistants (Əsas)
    (10, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, assistent',                      NULL,         NULL),
    (11, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, assistent',                      NULL,         NULL),
    (12, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, assistent (0.5 şt.)',            NULL,         NULL),
    -- Senior Lecturers (Daxili əvəzçiliklə)
    (13, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., daxili əvəzçiliklə)', NULL, NULL),
    -- Senior Lecturers (Əvəzçiliklə)
    (14, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., əvəzçiliklə)', NULL,    NULL),
    (15, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., əvəzçiliklə)', NULL,    NULL),
    (16, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., əvəzçiliklə)', NULL,    NULL),
    (17, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., əvəzçiliklə)', NULL,    NULL),
    (18, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., əvəzçiliklə)', NULL,    NULL),
    (19, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., əvəzçiliklə)', NULL,    NULL),
    -- Senior Lecturers (Daxili əvəzçiliklə continued)
    (20, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., daxili əvəzçiliklə)', NULL, NULL),
    (21, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., daxili əvəzçiliklə)', NULL, NULL),
    (22, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., daxili əvəzçiliklə)', NULL, NULL),
    (23, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., daxili əvəzçiliklə)', NULL, NULL),
    (24, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., daxili əvəzçiliklə)', NULL, NULL),
    -- Senior Lecturers (Əvəzçiliklə continued)
    (25, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., əvəzçiliklə)', NULL,    NULL),
    (26, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, baş müəllim (0.5 şt., əvəzçiliklə)', NULL,    NULL),
    -- Assistants (Daxili əvəzçiliklə)
    (27, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, assistent (0.5 şt., daxili əvəzçiliklə)', NULL, NULL),
    -- Assistants (Əvəzçiliklə)
    (28, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, assistent (0.5 şt., əvəzçiliklə)', NULL,       NULL),
    -- Clerk
    (29, 'Nəqliyyat logistikası və hərəkətin təhlükəsizliyi kafedrası, kargüzar',                       NULL,         NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Professors
    (1,  'Department of Transport Logistics and Traffic Safety, Consulting Professor',                     'Professor',           'D.Tech.Sci.'),
    (2,  'Department of Transport Logistics and Traffic Safety, Professor (0.5 rate)',                      'Professor',           'D.Tech.Sci.'),
    (3,  'Department of Transport Logistics and Traffic Safety, Professor',                                 'Professor',           'D.Tech.Sci.'),
    -- Associate Professors
    (4,  'Department of Transport Logistics and Traffic Safety, Associate Professor (1.5 rate)',            'Associate Professor', 'PhD'),
    (5,  'Department of Transport Logistics and Traffic Safety, Associate Professor (0.5 rate, internal)',  'Associate Professor', 'D.Phil.Sci.'),
    (6,  'Department of Transport Logistics and Traffic Safety, Associate Professor (0.5 rate, internal)',  'Associate Professor', 'D.Phil.Sci.'),
    -- Senior Lecturers (Main)
    (7,  'Department of Transport Logistics and Traffic Safety, Senior Lecturer',                           NULL,                  NULL),
    (8,  'Department of Transport Logistics and Traffic Safety, Senior Lecturer',                           NULL,                  NULL),
    (9,  'Department of Transport Logistics and Traffic Safety, Senior Lecturer',                           NULL,                  NULL),
    -- Assistants (Main)
    (10, 'Department of Transport Logistics and Traffic Safety, Assistant',                                 NULL,                  NULL),
    (11, 'Department of Transport Logistics and Traffic Safety, Assistant',                                 NULL,                  NULL),
    (12, 'Department of Transport Logistics and Traffic Safety, Assistant (0.5 rate)',                      NULL,                  NULL),
    -- Senior Lecturers (Internal part-time)
    (13, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, internal)',      NULL,                  NULL),
    -- Senior Lecturers (External part-time)
    (14, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, part-time)',     NULL,                  NULL),
    (15, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, part-time)',     NULL,                  NULL),
    (16, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, part-time)',     NULL,                  NULL),
    (17, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, part-time)',     NULL,                  NULL),
    (18, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, part-time)',     NULL,                  NULL),
    (19, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, part-time)',     NULL,                  NULL),
    -- Senior Lecturers (Internal part-time continued)
    (20, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, internal)',      NULL,                  NULL),
    (21, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, internal)',      NULL,                  NULL),
    (22, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, internal)',      NULL,                  NULL),
    (23, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, internal)',      NULL,                  NULL),
    (24, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, internal)',      NULL,                  NULL),
    -- Senior Lecturers (External part-time continued)
    (25, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, part-time)',     NULL,                  NULL),
    (26, 'Department of Transport Logistics and Traffic Safety, Senior Lecturer (0.5 rate, part-time)',     NULL,                  NULL),
    -- Assistants (Internal part-time)
    (27, 'Department of Transport Logistics and Traffic Safety, Assistant (0.5 rate, internal)',             NULL,                  NULL),
    -- Assistants (External part-time)
    (28, 'Department of Transport Logistics and Traffic Safety, Assistant (0.5 rate, part-time)',            NULL,                  NULL),
    -- Clerk
    (29, 'Department of Transport Logistics and Traffic Safety, Clerk',                                     NULL,                  NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
