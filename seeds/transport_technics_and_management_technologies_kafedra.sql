-- ============================================================
-- "Nəqliyyat texnikası və idarəetmə texnologiyaları" kafedrası — Full DB Import
-- cafedra_code: 'transport_technics_and_management_technologies'
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
    'transport_technics_and_management_technologies',
    1, 5, 2, 10, 5, 1, 10,
    '[9, 10, 11, 12]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'transport_technics_and_management_technologies',
    'az',
    'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrası',
    '<p>"Nəqliyyat texnikası və idarəetmə texnologiyaları" kafedrası 2021-ci ildə "Avtomobil texnikası" və "Dəmiryol nəqliyyatının istismarı" kafedralarının birləşdirilməsi ilə yaradılmışdır. "Avtomobil texnikası" kafedrası isə 2015-ci ildə "Daxili yanma mühərrikləri və avtotraktorlar" və "Avtomobil nəqliyyatı vasitələri" kafedralarının bazasında yaradılmışdır.</p><p>"Avtomobil nəqliyyatı vasitələri" kafedrası 1940-cı ildə Azərbaycan Sənaye İnstitutunda "Avtomobil istismarı" kafedrası adı ilə fəaliyyətə başlamış, 1950-ci ildə Azərbaycan Politexnik İnstitutu yaradıldıqda onun tərkibinə daxil edilmişdir.</p><p>Azərbaycan Politexnik İnstitutunda 1962-ci ildə "İstilik texnikası və istilik mühərrikləri" adı ilə yaradılmış kafedra, sonrakı illərdə "Daxili yanma mühərrikləri və soyuducu maşınlar" adı ilə fəaliyyət göstərmiş və 1997-ci ildən "Daxili yanma mühərrikləri və avtotraktorlar" kafedrası adlandırılmışdır.</p><p>"Dəmiryol nəqliyyatının istismarı" kafedrası AzTU-da 1997-ci ildə "Dəmiryol nəqliyyatı" fakültəsi ilə eyni zamanda yaradılmış, sonrakı illərdə "Nəqliyyat və logistika" fakültəsinin tərkibinə daxil edilmişdir.</p><p>"Nəqliyyat texnikası və idarəetmə texnologiyaları" kafedrasının missiyası, müasir avtomobil və dəmiryol nəqliyyat texnikası və onların istismarı sahəsində dərin texniki biliklərini qabaqcıl İT həlləri və idarəetmə sistemləri ilə inteqrasiya edə bilən yeni nəsil mühəndislərin hazırlanmasıdır.</p><p>Kafedranın missiyası üç sahəni əhatə edir — <strong>Təhsil:</strong> Avtomobil və dəmiryolu nəqliyyatının texniki vasitələri mühəndislərinin, onların intellektual texnologiya tənzimləyicilərinin və nəqliyyat texnikasının avtomatlaşdırma və idarəetmə mühəndis-menecer kadrlarının hazırlanması. <strong>Texnologiya:</strong> Avtomobil və dəmiryolu nəqliyyat vasitələrinin və avadanlıqlarının tədqiqi, yaradılması, istehsalı, tətbiqi və istismarı. <strong>İdarəetmə:</strong> Dəqiq işləyən nəqliyyat texnikası sistemləri yaratmaq üçün İT texnologiyalarından, riyazi və fiziki modelləşdirmədən və optimallaşdırma metodlarından istifadə.</p>',
    NOW()
),
(
    'transport_technics_and_management_technologies',
    'en',
    'Department of Transport Technics and Management Technologies',
    '<p>The department of "Transport technics and management technologies" was established in 2021 through the merger of the departments of "Automobile technics" and "Exploitation of railway transport". The department of "Automobile technics" itself had previously been founded in 2015 on the basis of the departments of "Internal combustion engines and autotractors" and "Automobile transport vehicles".</p><p>The Department of "Automobile transport vehicles" traces its origins back to 1940, when it was initially established under the name "Automobile exploitation" at the Azerbaijan Industrial Institute. In 1950, following the establishment of the Azerbaijan Polytechnic Institute, the department became part of its academic structure.</p><p>In 1962, the department of "Heat technics and thermal engines" was founded at the Azerbaijan Polytechnic Institute. In subsequent years, it operated under the name "Internal combustion engines and refrigeration machines," and since 1997, it has been known as the department of "Internal combustion engines and autotractors."</p><p>The Department of "Exploitation of railway transport" was established at Azerbaijan Technical University in 1997 simultaneously with the creation of the faculty of "Railway transport." In later years, it became part of the faculty of "Transport and logistics."</p><p>The mission of the Department of "Transport technics and management technologies" is to educate a new generation of engineers capable of integrating advanced technical knowledge in modern automobile and railway transport systems with cutting-edge IT solutions and management technologies.</p><p>The Department''s mission encompasses three core areas — <strong>Education:</strong> To prepare highly qualified engineers in the field of automobile and railway transport technics engineering, including specialists in intelligent technological regulation systems, as well as engineer-managers in the automation and management of transport technologies. <strong>Technology:</strong> To conduct research, create, production, implementation, and operation of automobile and railway transport vehicles and equipment. <strong>Management:</strong> To apply information technologies, mathematical and physical modeling, and optimization methods in order to create efficient and reliable transport technics systems.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'transport_technics_and_management_technologies';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('transport_technics_and_management_technologies', 1, NOW()),
    ('transport_technics_and_management_technologies', 2, NOW()),
    ('transport_technics_and_management_technologies', 3, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'İnnovasiya yönümlü',  'Perspektiv nəqliyyat texnikasının təhlükəsizliyini, səmərəliliyini və ekoloji tələblərə uyğunluğunu təmin etmək üçün intellektual idarəetmə sistemlərini dizayn və tətbiq edə bilən yüksək ixtisaslı mütəxəssislərin hazırlanması.'),
    (2, 'Təcrübə yönümlü',     'Nəqliyyat texnikası avadanlıqlarının və idarəetmə sistemlərinin istehsalı, istismarı, texniki xidməti və rəqəmsal transformasiyası sahələrini mütəxəssis kadrlarla təmin etmək.'),
    (3, 'Elmi-tədqiqat yönümlü','Müasir nəqliyyat texnikasının qabaqcıl nümunələrinin yaradılması və tədqiqi, onların rəqəmsal idarəetməsinin yaradılması sahəsində elmi biliklərin və qlobal nəqliyyat infrastrukturunun idarəetməsinin inkişafı üçün innovativ idarəetmə texnologiyalarının hazırlanması.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Innovation-oriented', 'To educate highly qualified specialists capable of designing and implementing intelligent control systems that ensure the safety, efficiency, and environmental sustainability of next-generation transport technologies.'),
    (2, 'Practice-oriented',   'To supply the transport sector with skilled professionals in the areas of production, operation, maintenance, and digital transformation of transport technics equipment and control systems.'),
    (3, 'Research-oriented',   'To conduct advanced research and development on modern transport technologies, including the creation and study of innovative transport systems, the development of their digital control mechanisms, and the advancement of scientific knowledge and innovative management technologies for global transport infrastructure.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'transport_technics_and_management_technologies',
        'Nicat', 'Zöhrabov', 'Rəsul oğlu',
        'nicatzohrabov@aztu.edu.az',
        '+994 12 525 24 06 (daxili 2120)',
        'V korpus, K407-ci otaq',
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
    'Texnika üzrə fəlsəfə doktoru (PhD)',
    'Dosent',
    '<p>Zöhrabov Nicat Rəsul oğlu — texnika elmləri üzrə fəlsəfə doktoru, dosent, nəqliyyatda daşımaların təşkili və idarə edilməsi sahəsi üzrə ixtisaslaşmış alimdir. O, daşımaların təşkili və idarə edilməsi istiqamətində elmi və pedaqoji fəaliyyət göstərir.</p><p>Onun elmi tədqiqatlarının əsas istiqamətlərinə nəqliyyatda daşımaların təşkili və idarə edilməsi, daşıma texnologiyaları, beynəlxalq nəqliyyat dəhlizləri, müasir nəqliyyat texnologiyaları daxildir. Bu sahələr üzrə apardığı tədqiqatların nəticələri nüfuzlu elmi jurnallarda dərc olunmuşdur.</p><p>Zöhrabov N.R. pedaqoji fəaliyyətində nəqliyyatda müasir daşıma texnologiyalarının tətbiq sahələrini aşılayaraq tələbələrin nəzəri və təcrübi bacarıqlarının inkişafına, vətənpərvər ruhda yetişməsinə, eləcə də gənc mütəxəssislərin hazırlanması və elmi-tədqiqat fəaliyyətinə cəlb olunmasına xüsusi diqqət yetirir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin "Nəqliyyat texnikası və idarəetmə texnologiyaları" kafedrasının müdiri vəzifəsində çalışır.</p><p>O, 70-ə yaxın elmi əsərin, 1 kollektiv monoqrafiyanın, 2 dərsliyin və 6 dərs vəsaitinin, xaricdə nəşr olunan 5 məqalənin və 4 konfrans materialının müəllifi və ya həmmüəllifidir, həmçinin respublikanın müxtəlif şəhərlərinin mobillik (hərəkətlilik) planın hazırlanması sahəsində dövlət layihələrinin fəal icraçısı olmuşdur.</p><p>2018-2021-ci illərdə Erasmus K+2 (Crisis and Risks Engineering for transport services (CRENG)) layihəsinin iştirakçısı olub.</p>',
    '["Daşıma texnologiyaları", "Sərnişin daşımaları", "Konteyner daşımaları", "Logistik texnologiyalar", "Logistik infrastruktur"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Ph.D. in Technical Sciences',
    'Associate Professor',
    '<p>Zohrabov Nijat Rasul is a Ph.D. (Tech.), Associate Professor, specializing in the field of organization of transportation and management. He carries out scientific and pedagogical activities in the field of transportation organization and management.</p><p>The main areas of his scientific research include transportation organization and management, transportation technologies, international transport corridors, and modern transport technologies. The results of his research in these areas have been published in prestigious scientific journals.</p><p>In his pedagogical activity, Zohrabov N.R. pays special attention to the development of students'' theoretical and practical skills, their patriotic upbringing, as well as the training of young specialists and their involvement in scientific and research activities, instilling in them the areas of application of modern transportation technologies in transport.</p><p>Currently, he works as the head of the Department of "Transport Technics and Management Technologies" of the Azerbaijan Technical University.</p><p>He is the author or co-author of about 70 scientific works, 1 collective monograph, 2 textbooks and 6 teaching aids, 5 articles published abroad and 4 conference materials, and was also an active executor of state projects in the field of developing mobility plans for various cities of the republic.</p><p>In 2018-2021, he was a participant in the Erasmus K+2 (Crisis and Risks Engineering for transport services (CRENG)) project.</p>',
    '["Transportation technologies", "Passenger transportation", "Container transportation", "Logistics technologies", "Logistics infrastructure"]'::jsonb,
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
    SELECT id, '15:00–17:00', NOW()
    FROM cafedra_directors WHERE cafedra_code = 'transport_technics_and_management_technologies'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Çərşənbə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Wednesday', NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1995', '1999', NOW() FROM cafedra_directors WHERE cafedra_code = 'transport_technics_and_management_technologies'
UNION ALL
SELECT id, '1999', '2001', NOW() FROM cafedra_directors WHERE cafedra_code = 'transport_technics_and_management_technologies'
UNION ALL
SELECT id, '2012', '2016', NOW() FROM cafedra_directors WHERE cafedra_code = 'transport_technics_and_management_technologies';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'transport_technics_and_management_technologies')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bakalavr',                                         'Azərbaycan Texniki Universiteti'),
    (2, 'Magistr',                                          'Azərbaycan Texniki Universiteti'),
    (3, 'Texnika elmləri üzrə fəlsəfə doktoru (PhD)',       'Azərbaycan Texniki Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bachelor',                                          'Azerbaijan Technical University'),
    (2, 'Master',                                            'Azerbaijan Technical University'),
    (3, 'Doctor of Philosophy (PhD) in Technical Sciences',  'Azerbaijan Technical University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'transport_technics_and_management_technologies';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('transport_technics_and_management_technologies', 'Heybətulla', 'Əhmədov',       'Mabud oğlu',     'heybetahmed@aztu.edu.az',         '+994 50 378 55 80', NOW()),  -- 1
    ('transport_technics_and_management_technologies', 'Ziyafət',    'Kərimov',       'Xeyrulla oğlu',  'kerimov.z@aztu.edu.az',           NULL,                 NOW()),  -- 2
    ('transport_technics_and_management_technologies', 'Qasım',      'Manafov',       'Cabar oğlu',     'qmanafov@aztu.edu.az',            '+994 50 355 74 39', NOW()),  -- 3
    ('transport_technics_and_management_technologies', 'Ramin',      'Aslanov',       'Məmməd oğlu',    'ramin.aslanov@aztu.edu.az',       '+994 51 215 23 73', NOW()),  -- 4
    ('transport_technics_and_management_technologies', 'Azad',       'Babayev',       'Məmməd oğlu',    'azad.babayev@aztu.edu.az',        '+994 50 363 43 18', NOW()),  -- 5
    ('transport_technics_and_management_technologies', 'Mirhəmid',   'Həmidov',       'Mirheydər oğlu', 'mirhemid.hemidov@aztu.edu.az',    '+994 50 374 50 99', NOW()),  -- 6
    ('transport_technics_and_management_technologies', 'Elşən',      'Manafov',       'Kamil oğlu',     'elshen.manafov@aztu.edu.az',      '+994 55 741 79 39', NOW()),  -- 7
    ('transport_technics_and_management_technologies', 'Qəzənfər',   'Axundov',       'Nəsrulla oğlu',  'qezenfer.axundov@aztu.edu.az',    '+994 55 868 62 30', NOW()),  -- 8
    ('transport_technics_and_management_technologies', 'Məsud',      'Rüstəmbəyov',   'Ənvər oğlu',     'masud.rustambayov@aztu.edu.az',   '+994 70 363 06 94', NOW()),  -- 9
    ('transport_technics_and_management_technologies', 'Qurban',     'Qocayev',       'Müzəffər oğlu',  'qurbanqo@aztu.edu.az',            '+994 50 304 63 07', NOW()),  -- 10
    ('transport_technics_and_management_technologies', 'Röyal',      'Allahverdiyev', 'Şöhrət oğlu',    'royal.allahverdiyev@aztu.edu.az', '+994 77 431 31 33', NOW()),  -- 11
    ('transport_technics_and_management_technologies', 'İltifat',    'Məmmədli',      'İrşad oğlu',     'iltifat.memmedli@aztu.edu.az',    '+994 70 248 40 10', NOW()),  -- 12
    ('transport_technics_and_management_technologies', 'Faiq',       'Tağızadə',      'Fuad oğlu',      'faig.taghizadeh@aztu.edu.az',     '+994 50 794 65 96', NOW()),  -- 13
    ('transport_technics_and_management_technologies', 'Səbinə',     'Rəsulova',      'Əlimurad qızı',  'sabina.rasulova@aztu.edu.az',     '+994 70 341 33 36', NOW()),  -- 14
    ('transport_technics_and_management_technologies', 'İradə',      'Abasova',       'İslam qızı',     'irada.abbasova@aztu.edu.az',      '+994 50 664 46 55', NOW())   -- 15
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının məsləhətçi-professoru', 'Professor',   't.e.d.'),
    (2,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının professoru',            'Professor',   't.e.d.'),
    (3,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının dosenti',               'Dosent',      't.e.n.'),
    (4,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının dosenti',               'Dosent',      'r.ü.f.d.'),
    (5,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının dosenti',               'Dosent',      't.e.n.'),
    (6,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının dosenti',               'Dosent',      't.e.n.'),
    (7,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının dosenti',               'Dosent',      't.ü.f.d.'),
    (8,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının baş müəllimi',          NULL::varchar, NULL::varchar),
    (9,  'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının baş müəllimi',          NULL,          NULL),
    (10, 'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının baş müəllimi',          NULL,          NULL),
    (11, 'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının assistenti',            NULL,          NULL),
    (12, 'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının assistenti',            NULL,          NULL),
    (13, 'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının assistenti',            NULL,          NULL),
    (14, 'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının assistenti',            NULL,          NULL),
    (15, 'Nəqliyyat texnikası və idarəetmə texnologiyaları kafedrasının kargüzarı',             NULL,          NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Advisory Professor at the Department of Transport Technics and Management Technologies',   'Professor',           'Doctor of Technical Sciences'),
    (2,  'Professor at the Department of Transport Technics and Management Technologies',            'Professor',           'Doctor of Technical Sciences'),
    (3,  'Associate Professor at the Department of Transport Technics and Management Technologies',  'Associate Professor', 'Candidate of Technical Sciences'),
    (4,  'Associate Professor at the Department of Transport Technics and Management Technologies',  'Associate Professor', 'Ph.D. in Mathematics'),
    (5,  'Associate Professor at the Department of Transport Technics and Management Technologies',  'Associate Professor', 'Candidate of Technical Sciences'),
    (6,  'Associate Professor at the Department of Transport Technics and Management Technologies',  'Associate Professor', 'Candidate of Technical Sciences'),
    (7,  'Associate Professor at the Department of Transport Technics and Management Technologies',  'Associate Professor', 'Ph.D. in Technical Sciences'),
    (8,  'Senior Lecturer at the Department of Transport Technics and Management Technologies',      NULL::varchar,         NULL::varchar),
    (9,  'Senior Lecturer at the Department of Transport Technics and Management Technologies',      NULL,                  NULL),
    (10, 'Senior Lecturer at the Department of Transport Technics and Management Technologies',      NULL,                  NULL),
    (11, 'Assistant at the Department of Transport Technics and Management Technologies',            NULL,                  NULL),
    (12, 'Assistant at the Department of Transport Technics and Management Technologies',            NULL,                  NULL),
    (13, 'Assistant at the Department of Transport Technics and Management Technologies',            NULL,                  NULL),
    (14, 'Assistant at the Department of Transport Technics and Management Technologies',            NULL,                  NULL),
    (15, 'Administrative Assistant at the Department of Transport Technics and Management Technologies', NULL,              NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
