
BEGIN;

-- 1. Insert Faculty
INSERT INTO faculties (
    faculty_code, 
    bachelor_programs_count, 
    master_programs_count, 
    phd_programs_count, 
    international_collaborations_count, 
    laboratories_count, 
    projects_patents_count, 
    industrial_collaborations_count, 
    created_at
) VALUES (
    'transport_logistics', 
    3, 0, 0, 0, 0, 0, 0, 
    NOW()
);

-- 2. Insert Faculty Translations
INSERT INTO faculties_tr (faculty_code, lang_code, faculty_name, about_text, created_at)
VALUES 
(
    'transport_logistics', 
    'az', 
    'Nəqliyyat və logistika fakültəsi', 
    'Nəqliyyat və logistika fakültəsi 1950-ci ildən fəaliyyətə başlayıb. 1950-ci ildə Azərbaycan Politexnik İnstitutu (indiki Azərbaycan Texniki Universiteti) fəaliyyətə başladığı zaman bu fakültə Mexanika adlanıb. Sonralar fakültənin adı dəyişdirilərək Avtonəqliyyat, Avtomexanika, Dəmir yolu nəqliyyatı və Nəqliyyat adlanıb. 2019-cu ildən fakültə Nəqliyyat və logistika adı ilə fəaliyyət göstərir. Təhsil azərbaycan və rus dillərində aparılır. Fakültənin nəzdində 2 kafedra fəaliyyət göstərir: • Nəqliyyat logistikası və hərəkətin təhlükəsizliyi; • Nəqliyyat texnikası və idarəetmə texnologiyaları. Hazırda fakültənin nəzdində fəaliyyət göstərən 2 kafedrada 3 ixtisas üzrə bakalavr səviyyəsində kadr hazırlığı həyata keçirilir.', 
    NOW()
),
(
    'transport_logistics', 
    'en', 
    'Faculty of Transport and Logistics', 
    'The Faculty of Transport and Logistics has been operational since 1950. When the Azerbaijan Polytechnic Institute (current Azerbaijan Technical University) was established in 1950, this faculty was originally named the Faculty of Mechanics. Later, the faculty underwent several name changes, being called Automobile Transport, Automotive Mechanics, Railway Transport, and Transport. Since 2019, the faculty has been operating under the name Faculty of Transport and Logistics. Education is conducted in both Azerbaijani and Russian languages. There are 2 departments operating within the faculty: • Transport Logistics and Traffic Safety • Transport Engineering and Management Technologies Currently, these two departments provide undergraduate education in 3 specialized fields.', 
    NOW()
);

-- 3. Insert Faculty Directions of Action
WITH direction_ids AS (
    INSERT INTO faculty_directions_of_action (faculty_code, display_order, created_at)
    VALUES 
    ('transport_logistics', 1, NOW()),
    ('transport_logistics', 2, NOW()),
    ('transport_logistics', 3, NOW()),
    ('transport_logistics', 4, NOW()),
    ('transport_logistics', 5, NOW()),
    ('transport_logistics', 6, NOW()),
    ('transport_logistics', 7, NOW()),
    ('transport_logistics', 8, NOW()),
    ('transport_logistics', 9, NOW()),
    ('transport_logistics', 10, NOW()),
    ('transport_logistics', 11, NOW()),
    ('transport_logistics', 12, NOW()),
    ('transport_logistics', 13, NOW()),
    ('transport_logistics', 14, NOW()),
    ('transport_logistics', 15, NOW()),
    ('transport_logistics', 16, NOW()),
    ('transport_logistics', 17, NOW()),
    ('transport_logistics', 18, NOW()),
    ('transport_logistics', 19, NOW()),
    ('transport_logistics', 20, NOW())
    RETURNING id
)
INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, created_at)
SELECT id, 'az', title, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM direction_ids
) d JOIN (
    VALUES 
    (1, 'Logistika və nəqliyyat texnologiyaları mühəndisliyi'),
    (2, 'Nəqliyyat logistikası'),
    (3, 'Şəhər nəqliyyat şəbəkəsi və nəqliyyat xidmətinin təşkili'),
    (4, 'Nəqliyyat xidmətləri üçün böhran və risklərin idarə edilməsi'),
    (5, 'Nəqliyyatda daşımalar və menecment (avtomobil nəqliyyatı üzrə)'),
    (6, 'Beynəlxalq daşımalar'),
    (7, 'Yol hərəkətinin təşkili və təhlükəsizliyi'),
    (8, 'Nəqliyyat əməliyyatlarının intellektual idarə edilməsi'),
    (9, 'Yol-nəqliyyat hadisələrinin ekspertizası'),
    (10, 'Yol hərəkətinin təşkilinin texniki nizamlama vasitələri'),
    (11, 'Yol şəraitləri və hərəkətin təhlükəsizliyi'),
    (12, 'Nəqliyyat axınları nəzəriyyəsi'),
    (13, 'Avtomobil yolları'),
    (14, 'Dəmir yolları'),
    (15, 'Nəqliyyatda daşımalar və menecment (dəmiryol nəqliyyatı üzrə)'),
    (16, 'Dəmir yolu təsərrüfatı və onun istismarı'),
    (17, 'Lokomotiv və vaqon təsərrüfatı'),
    (18, 'Avtomobil nəqliyyatında texniki servisin təşkili'),
    (19, 'Elektrik və hibrid nəqliyyat vasitələri'),
    (20, 'Avtomobil texnikası və istismar')
) v(row_num, title) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM direction_ids
) d JOIN (
    VALUES 
    (1, 'Logistics and transport technologies engineering'),
    (2, 'Transport logistics'),
    (3, 'Organization of urban transport networks and transport services'),
    (4, 'Crisis and risk management in transport services'),
    (5, 'Transportation and management in transport (automobile transport)'),
    (6, 'International transportation'),
    (7, 'Organization and safety of road transportation'),
    (8, 'Intelligent management of transport operations'),
    (9, 'Expertise of transport incidents'),
    (10, 'Technical regulation means of traffic organization'),
    (11, 'Road conditions and traffic safety'),
    (12, 'Theory of transport flows'),
    (13, 'Highways'),
    (14, 'Railways'),
    (15, 'Transportation and management in transport (railway transport)'),
    (16, 'Railway economy and its operation'),
    (17, 'Locomotive and wagon economy'),
    (18, 'Organization of technical service in automobile of transport'),
    (19, 'Electric and hybrid transport vehicles'),
    (20, 'Automobile engineering and operation')
) v(row_num, title) ON d.row_num = v.row_num;

-- 4. Insert Faculty Director
WITH director_insert AS (
    INSERT INTO faculty_directors (
        faculty_code, first_name, last_name, father_name, email, phone, room_number, created_at
    ) VALUES (
        'transport_logistics', 'Allahverdi', 'Şərifov', 'Camal', 'sharifov.allahverdi@aztu.edu.az', '+994 12 539 1251', 'V korpus, 403-cü otaq', NOW()
    ) RETURNING id
)
INSERT INTO faculty_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, scientific_research_fields, created_at)
SELECT id, 'az', 'Texnika üzrə fəlsəfə doktoru', 'dosent', 'Şərifov Allahverdi Camal oğlu - texnika üzrə fəlsəfə doktoru, dosent, hərəkətin təhlükəsizliyi və nəqliyyat logistikası üzrə ixtisaslaşmış alimdir. O, yollarda hərəkətin təhlükəsizliyi və yol-nəqliyyat hadisələrinin baş vermə riskləri istiqamətində elmi və pedaqoji fəaliyyət göstərir. Onun elmi tədqiqatlarının əsas istiqamətlərinə hərəkət təhlükəsizliyi, nəqliyyat vasitələrinin təhlükəsizliyi, yol-nəqliyyat hadisələrinin baş verməsinə təsir edən parametrlərin qiymətləndirilməsi, nəqliyyat logistikası və hərərkət şəraitində yaranan risklər daxildir Bu sahələr üzrə apardığı tədqiqatların nəticələri nüfuzlu elmi jurnallarda dərc olunmuş və nəqliyyat sahəsinin inkişafına töhfə vermişdir. Şərifov A.C. pedaqoji fəaliyyətində müasir yanaşmaları tətbiq edərək tələbələrin analitik və tənqidi düşünmə bacarıqlarının inkişafına, eləcə də gənc mütəxəssislərin hazırlanması və elmi-tədqiqat fəaliyyətinə cəlb olunmasına xüsusi önəm verir. Hazırda o, Azərbaycan Texniki Universitetinin Nəqliyyat və logistika fakültəsində dekan vəzifəsində çalışır. O, 62 dərc olunmuş elmi məqalənin (11 məqalə xarici jurnallarda dərc edilmişdir), 1 dərsliyin, 1 dərs vəsaitinin, 20 fənn proqramının və 2 metodik göstərişin müəllifidir. Həmçinin Azərbaycan Gənclər Fondunun “Tələbə sükanı”, “CRENG (Erasmus +K2) Crisis and risk engineering for transport services” magistr, “İctimai xidmətlərin əhatəliliyinin və keyfiyyətinin artırılması üçün qərar qəbul etmə mexanizmlərinin işlənməsi (pilot olaraq Abşeron və Qobustan rayonunun nəqliyyat sektorunun timsalında)”, “Azərbaycan Respublikasının şəhərlərində şəhərdaxili mobillik (hərəkətlilik) planının hazırlanması (Biləsuvar şəhərinin)” layihələrində iştirak etmişdir.', '["Hərəkət təhlükəsizliyi", "Nəqliyyat vasitələrinin təhlükəsizliyi", "Nəqliyyat logistikası", "Nəqliyyatda yaranan risklər", "Nəqliyyatda tətbiq olunan yeni texnologiylar"]', NOW() FROM director_insert
UNION ALL
SELECT id, 'en', 'Ph.D. in Engineering', 'Associate Professor', 'Allahverdi Camal oghlu Sharifov – Ph.D. in Engineering, Associate Professor, is a scholar specializing in Traffic Safety and Transportation Logistics. He conducts scientific and pedagogical activities in the fields of traffic safety and the risk assessment of road traffic incidents. The primary focus of his research includes traffic safety, vehicle safety, evaluation of parameters influencing the occurrence of road traffic accidents, transportation logistics, and risks arising in traffic conditions. The results of his studies in these areas have been published in reputable scientific journals and have contributed to the advancement of the transportation sector. In his pedagogical activities, Sharifov applies modern approaches to foster students’ analytical and critical thinking skills, as well as to prepare young specialists and involve them in scientific research activities. Currently, he serves as the Dean of the Faculty of Transport and Logistics at Azerbaijan Technical University. He is the author of 62 published scientific articles (11 of which are in international journals), 1 textbook, 1 teaching aid, 20 course programs, and 2 methodological guidelines. Additionally, he has participated in projects such as the Azerbaijan Youth Foundation’s “Student Steering Wheel”, “CRENG (Erasmus+ K2) Crisis and Risk Engineering for Transport Services” Master’s program, “Development of Decision-Making Mechanisms to Enhance the Coverage and Quality of Public Services (Pilot Project in the Transport Sector of Absheron and Gobustan Districts)”, and “Preparation of Urban Mobility (Mobility) Plan in the Cities of the Republic of Azerbaijan.', '["Traffic Safety", "Vehicle Safety", "Transportation Logistics", "Risks arising in Transportation", "Emerging Technologies in Transportation"]', NOW() FROM director_insert;

-- 5. Insert Director Working Hours
WITH working_hour_insert AS (
    INSERT INTO faculty_director_working_hours (director_id, time_range, created_at)
    SELECT id, '14:00–17:00', NOW() FROM faculty_directors WHERE faculty_code = 'transport_logistics'
    RETURNING id
)
INSERT INTO faculty_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Çərşənbə axşamı, Çərşənbə, Cümə axşamı', NOW() FROM working_hour_insert
UNION ALL
SELECT id, 'en', 'Tuesday, Wednesday, Thursday', NOW() FROM working_hour_insert;

-- 6. Insert Director Educations
WITH education_inserts AS (
    INSERT INTO faculty_director_educations (director_id, start_year, end_year, created_at)
    SELECT id, start_y, end_y, NOW() FROM faculty_directors d, (
        VALUES 
        ('2001', '2005'),
        ('2005', '2007'),
        ('2012', '2015'),
        ('2020', '2025')
    ) v(start_y, end_y) WHERE d.faculty_code = 'transport_logistics'
    RETURNING id
)
INSERT INTO faculty_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM education_inserts
) e JOIN (
    VALUES 
    (1, 'Bakalavr', 'Azərbaycan Texniki Universiteti'),
    (2, 'Magistratura', 'Azərbaycan Texniki Universiteti'),
    (3, 'Texnika üzrə fəlsəfə doktoru, dissertant', 'Azərbaycan Texniki Universiteti'),
    (4, 'Texnika üzrə elmlər doktoru, dissertant', 'Azərbaycan Texniki Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM education_inserts
) e JOIN (
    VALUES 
    (1, 'Bachelor''s Degree', 'Azerbaijan Technical University'),
    (2, 'Master''s Degree', 'Azerbaijan Technical University'),
    (3, 'Ph.D. in Engineering (Dissertation)', 'Azerbaijan Technical University'),
    (4, 'Doctor of Engineering Sciences (Dissertation)', 'Azerbaijan Technical University')
) v(row_num, degree, university) ON e.row_num = v.row_num;

-- 7. Insert Deputy Deans
WITH deputy_inserts AS (
    INSERT INTO faculty_deputy_deans (faculty_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES 
    ('transport_logistics', 'Mahir', 'Mustafayev', 'Mustafa', 'mahir.mustafayev@aztu.edu.az', '+994 51 615 62 55', NOW()),
    ('transport_logistics', 'Sevinc', 'Abdinzadə', 'Məhərrəm', 'sevinc.abdinzade@aztu.edu.az', '+994 51 777 27 85', NOW())
    RETURNING id
)
INSERT INTO faculty_deputy_dean_tr (deputy_dean_id, lang_code, duty, created_at)
SELECT id, 'az', duty, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM deputy_inserts
) d JOIN (
    VALUES 
    (1, 'Nəqliyyat və logistika fakültəsinin Tədris işləri üzrə dekan müavini'),
    (2, 'Nəqliyyat və logistika fakültəsinin Sosial məsələlər, ictimaiyyətlə əlaqələr və infrastrukur üzrə dekan müavini')
) v(row_num, duty) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM deputy_inserts
) d JOIN (
    VALUES 
    (1, 'Deputy Dean for Academic Affairs, Faculty of Transport and Logistics'),
    (2, 'Deputy Dean for Social Affairs Public Relations and Infrastructure of the Faculty of Transport and logistics')
) v(row_num, duty) ON d.row_num = v.row_num;

-- 8. Insert Faculty Workers (Academic Advisors)
WITH worker_inserts AS (
    INSERT INTO faculty_workers (faculty_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES 
    ('transport_logistics', 'Elzamin', 'Quliyev', 'Rəhman', 'elzaminquliyev@aztu.edu.az', '+994 70 719 19 07', NOW()),
    ('transport_logistics', 'Günel', 'Məmmədli', 'Əkbər', 'gunel.mammadli@aztu.edu.az', '+994 50 895 95 93', NOW())
    RETURNING id
)
INSERT INTO faculty_worker_tr (worker_id, lang_code, duty, created_at)
SELECT id, 'az', duty, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM worker_inserts
) w JOIN (
    VALUES 
    (1, 'Nəqliyyat və logistika fakültəsinin Akademik məsləhətçi'),
    (2, 'Nəqliyyat və logistika fakültəsinin Akademik məsləhətçi')
) v(row_num, duty) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM worker_inserts
) w JOIN (
    VALUES 
    (1, 'Academic tutor at the Faculty of Transport and Logistics'),
    (2, 'Academic tutor at the Faculty of Transport and Logistics')
) v(row_num, duty) ON w.row_num = v.row_num;

COMMIT;