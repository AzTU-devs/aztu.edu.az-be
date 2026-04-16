-- Information Technologies and Telecommunications Faculty SQL Import Script
-- This script uses ON CONFLICT to prevent duplicate key errors and casts strings to JSONB.

BEGIN;

-- 1. Insert Faculty (Skip if exists)
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
    'information_technologies_telecommunications',
    7, 6, 0, 0, 0, 0, 0,
    NOW()
) ON CONFLICT (faculty_code) DO NOTHING;

-- 2. Insert Faculty Translations
INSERT INTO faculties_tr (faculty_code, lang_code, faculty_name, about_text, created_at)
VALUES
(
    'information_technologies_telecommunications',
    'az',
    'İnformasiya Texnologiyaları və Telekommunikasiya Fakültəsi',
    'İnformasiya Texnologiyaları və Telekommunikasiya fakültəsi ölkəmizdə sürətlə inkişaf edən rəqəmsal iqtisadiyyatın və telekommunikasiya sənayesinin yüksək ixtisaslı mühəndis kadrlarla təmin edilməsinə olan ehtiyacını qarşılamaq məqsədilə yaradılıb. Fakültənin əsası Azərbaycan Texniki Universitetində informasiya texnologiyaları, kompüter mühəndisliyi və telekommunikasiya istiqamətlərində aparılan mühəndis hazırlığının genişləndirilməsi zəruriliyindən irəli gələrək qoyulub. 1961-ci ildə Azərbaycan Politexnik İnstitutunda (indiki Azərbaycan Texniki Universiteti) Avtomatika və hesablama texnikası fakültəsi yaradılmışdır. Azərbaycan Texniki Universitetinin 05.02.2025-ci il tarixli Elmi Şurasının əmri ilə fakültənin adı dəyişdirilərək İnformasiya Texnologiyaları və Telekommunikasiya fakültəsi adlandırılmışdır. Fakültənin strukturu müasir tələblərə uyğun yenilənmiş, əmək bazarının ehtiyaclarına cavab verən geniş ixtisas spektri formalaşdırılmışdır. Bu dəyişikliklər nəticəsində fakültə hazırda informasiya texnologiyaları, telekommunikasiya sistemləri, kompüter mühəndisliyi və süni intellekt sahələrində yüksək ixtisaslı mütəxəssis hazırlığını həyata keçirən əsas mərkəzlərdən birinə çevrilmişdir. Fakültənin nəzdində 4 kafedra fəaliyyət göstərir: Kibertəhlükəsizlik; Kompüter texnologiyaları; Mühəndis riyaziyyatı və süni intellekt; Radiotexnika və telekommunikasiya. Hazırda fakültənin nəzdində fəaliyyət göstərən 4 kafedrada bakalavr təhsil səviyyəsində 7 ixtisas, magistr təhsil səviyyəsində isə 5 ixtisas üzrə kadr hazırlığı həyata keçirilir. Fakültədə bakalavr təhsil səviyyəsi üzrə ixtisas istiqamətləri: Kompüter elmləri, İnformasiya texnologiyaları, Kompüter mühəndisliyi, İnformasiya təhlükəsizliyi, Radiotexnika və telekommunikasiya mühəndisliyi, Proqram təminatı mühəndisliyi, Data Analitika. Fakültədə magistr təhsil səviyyəsi üzrə ixtisas istiqamətləri: Kompüter mühəndisliyi, İnformasiya texnologiyaları, İnformasiya təhlükəsizliyi, Kompüter elmləri, Radiotexnika və telekommunikasiya mühəndisliyi, Data elmləri. Tədris Azərbaycan, ingilis və rus dillərində aparılır. İnformasiya Texnologiyaları və Telekommunikasiya fakültəsi müasir rəqəmsal mühəndislik təhsilinin tələblərinə uyğun olaraq tələbələrə riyazi, proqramlaşdırma, informasiya sistemləri arxitekturası, şəbəkə texnologiyaları, süni intellekt, böyük verilənlər, kibertəhlükəsizlik, simsiz rabitə sistemləri, 5G/6G telekommunikasiya texnologiyaları, IoT (Internet of Things) və bulud texnologiyaları üzrə geniş nəzəri və praktiki biliklər təqdim edir. Tədris prosesi dual təhsil modelinə əsaslanır – tələbələr həm fakültənin müasir laboratoriyalarında, həm də real istehsalat mühitində təcrübə keçməklə tətbiqi biliklərini möhkəmləndirirlər. Fakültənin texnoloji şirkətlərlə əməkdaşlığı, startap mühiti, inkubasiya proqramları, beynəlxalq layihələrdə iştirak imkanları tələbələrin innovativ mühəndis kimi formalaşmasına əhəmiyyətli töhfə verir. İTT-nin nəzdində Kompüter mühəndisliyi, İnformasiya texnologiyaları, İnformasiya təhlükəsizliyi, Kompüter elmləri ixtisasları üzrə SABAH qrupları fəaliyyət göstərir. Fakültə xarici universitetlərlə akademik əlaqələrə malikdir və tələbələrə beynəlxalq mübadilə, həmçinin Ankara Universiteti ilə ikili diplom və sertifikatlaşdırma proqramlarında iştirak imkanı yaradır.',
    NOW()
),
(
    'information_technologies_telecommunications',
    'en',
    'Faculty of Information Technologies and Telecommunications',
    'The Faculty of Information Technologies and Telecommunications was established to meet the growing demand of the country''s rapidly developing digital economy and telecommunications industry for highly qualified engineering professionals. The foundation of the Faculty is rooted in the necessity to expand engineering education in the fields of information technologies, computer engineering, and telecommunications at Azerbaijan Technical University. In 1961, the Faculty of Automation and Computing Machinery was established at the Azerbaijan Polytechnic Institute (now Azerbaijan Technical University). By the decision of the Academic Council of Azerbaijan Technical University dated February 5, 2025, the Faculty was renamed as the Faculty of Information Technologies and Telecommunications. The structure of the Faculty has been modernized in accordance with contemporary requirements, and a wide range of specializations responding to labor market demands has been developed. As a result of these changes, the Faculty has become one of the leading centers for the training of highly qualified specialists in the fields of information technologies, telecommunication systems, computer engineering, and artificial intelligence. The Faculty comprises four departments: Cybersecurity; Computer Technologies; Engineering Mathematics and Artificial Intelligence; Radio Engineering and Telecommunications. Currently, the Faculty provides education through its four departments, offering training in 7 specialties at the undergraduate (bachelor''s) level and 5 specialties at the graduate (master''s) level. Undergraduate (Bachelor''s) Degree Programs: Computer Science, Information Technology, Computer Engineering, Information Security, Radio Engineering and Telecommunications Engineering, Software Engineering, Data Analytics. Graduate (Master''s) Degree Programs: Computer Engineering, Information Technology, Information Security, Computer Sciences, Radio Engineering and Telecommunications Engineering, Data Sciences. The language of instruction is Azerbaijani, English, and Russian. The Faculty of Information Technologies and Telecommunications provides students with comprehensive theoretical and practical knowledge in accordance with the requirements of modern digital engineering education. The curriculum covers a wide range of fields, including mathematics, programming, information systems architecture, network technologies, artificial intelligence, big data, cybersecurity, wireless communication systems, 5G/6G telecommunication technologies, the Internet of Things (IoT), and cloud technologies. The educational process is based on a dual education model, whereby students strengthen their applied knowledge through practical training both in the Faculty''s modern laboratories and in real industrial environments. The Faculty''s cooperation with technology companies, its startup ecosystem, incubation programs, and opportunities to participate in international projects make a significant contribution to the development of students as innovative engineers. SABAH groups are actively operating within the Faculty of Information Technologies and Telecommunications in the specialties of Computer Engineering, Information Technology, Information Security, and Computer Science. The Faculty maintains academic partnerships with foreign universities and provides students with opportunities for international exchange, as well as participation in dual degree program with Ankara University and the other certification programs.',
    NOW()
) ON CONFLICT (faculty_code, lang_code) DO UPDATE
SET faculty_name = EXCLUDED.faculty_name, about_text = EXCLUDED.about_text, updated_at = NOW();

-- 3. Insert Faculty Directions of Action (Clear old ones to prevent duplicates)
DELETE FROM faculty_directions_of_action WHERE faculty_code = 'information_technologies_telecommunications';

WITH direction_ids AS (
    INSERT INTO faculty_directions_of_action (faculty_code, display_order, created_at)
    VALUES
    ('information_technologies_telecommunications', 1, NOW()),
    ('information_technologies_telecommunications', 2, NOW()),
    ('information_technologies_telecommunications', 3, NOW()),
    ('information_technologies_telecommunications', 4, NOW()),
    ('information_technologies_telecommunications', 5, NOW()),
    ('information_technologies_telecommunications', 6, NOW()),
    ('information_technologies_telecommunications', 7, NOW()),
    ('information_technologies_telecommunications', 8, NOW()),
    ('information_technologies_telecommunications', 9, NOW()),
    ('information_technologies_telecommunications', 10, NOW()),
    ('information_technologies_telecommunications', 11, NOW())
    RETURNING id
)
INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, created_at)
SELECT id, 'az', title, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Riyaziyyat'),
    (2, 'Proqramlaşdırma'),
    (3, 'İnformasiya sistemləri arxitekturası'),
    (4, 'Şəbəkə texnologiyaları'),
    (5, 'Süni intellekt'),
    (6, 'Böyük verilənlər (Big Data)'),
    (7, 'Kibertəhlükəsizlik'),
    (8, 'Simsiz rabitə sistemləri'),
    (9, '5G/6G telekommunikasiya texnologiyaları'),
    (10, 'IoT (Internet of Things)'),
    (11, 'Bulud texnologiyaları')
) v(row_num, title) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Mathematics'),
    (2, 'Programming'),
    (3, 'Information Systems Architecture'),
    (4, 'Network Technologies'),
    (5, 'Artificial Intelligence'),
    (6, 'Big Data'),
    (7, 'Cybersecurity'),
    (8, 'Wireless Communication Systems'),
    (9, '5G/6G Telecommunication Technologies'),
    (10, 'Internet of Things (IoT)'),
    (11, 'Cloud Technologies')
) v(row_num, title) ON d.row_num = v.row_num;

-- 4. Insert Faculty Director (Dean)
WITH director_insert AS (
    INSERT INTO faculty_directors (
        faculty_code, first_name, last_name, father_name, email, phone, room_number, created_at
    ) VALUES (
        'information_technologies_telecommunications',
        'Leyla',
        'Məmmədova',
        'Məzdək',
        'leyla.mammadova@aztu.edu.az',
        '+994 12 525 24 06',
        '7-ci tədris binası, 617-ci otaq',
        NOW()
    ) ON CONFLICT (faculty_code) DO UPDATE
    SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name, father_name = EXCLUDED.father_name,
        email = EXCLUDED.email, phone = EXCLUDED.phone, room_number = EXCLUDED.room_number, updated_at = NOW()
    RETURNING id
)
INSERT INTO faculty_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, scientific_research_fields, created_at)
SELECT id, 'az', 'Fizika-riyaziyyat elmləri namizədi', 'Dosent',
'Məmmədova Leyla Məzdək qızı, fizika-riyaziyyat elmləri namizədi, dosent olaraq Azərbaycan Texniki Universitetinin İnformasiya Texnologiyaları və Telekommunikasiya fakültəsində elmi-pedaqoji fəaliyyət göstərir. Onun tədqiqat fəaliyyəti əsasən diferensial tənliklər, riyazi modelləşdirmə və optimallaşdırma sahələrini əhatə edir. Bununla yanaşı, son illərdə elmi maraq dairəsi genişlənərək süni intellekt, data analitikası və informasiya texnologiyalarının tətbiqi kimi müasir istiqamətləri də özündə birləşdirir. Paralel olaraq, riyazi metodların real sektorda, xüsusilə informasiya texnologiyaları və idarəetmə sistemlərində tətbiqi onun tədqiqatlarının əsas məqsədlərindən biridir. Leyla Məmmədova 40-dan artıq elmi məqalənin, 1 dərslik və 2 dərs vəsaitinin müəllifidir və onun tədqiqat işləri beynəlxalq elmi bazalara daxil olan nüfuzlu jurnallarda dərc olunmuşdur. Xüsusilə, məqalələri Scopus və Web of Science kimi beynəlxalq indeksləşdirmə sistemlərində yer alır. Tədqiqat fəaliyyəti ilə yanaşı, o, bir sıra elmi layihələrdə iştirak etmiş, universitet və sənaye tərəfdaşları ilə əməkdaşlıq qurmuşdur. Akademik fəaliyyət çərçivəsində diferensial tənliklər, riyazi analiz və data analitikası, ekonometrika üzrə mühazirələr aparır, magistr tələbələrinin elmi rəhbəri kimi onların tədqiqat bacarıqlarının inkişafına dəstək verir. Gələcək tədqiqat planları süni intellekt əsaslı modellərin inkişafı, böyük verilənlərin riyazi analizi, data analitika sahəsi üçün modelləşdirmə metodlarının işlənməsi və təhsil texnologiyalarında innovativ yanaşmaların tətbiqinə yönəlmişdir. Peşəkar fəaliyyəti: 2001–2002-ci illərdə Bakı Dövlət Universitetinin Tətbiqi riyaziyyat və kibernetika fakültəsinin İnformasiya texnologiyaları və proqramlaşdırma kafedrasında müəllim, 2002–2011-ci illərdə isə həmin fakültənin İqtisadi informatika kafedrasında baş müəllim, 2011–2025-ci illərdə Bakı Dövlət Universitetinin Beynəlxalq münasibətlər və iqtisadiyyat fakültəsinin Riyazi iqtisadiyyat kafedrasında dosent, 2017–2018-ci illərdə London School of Economics and Political Science (LSE) və UNEC ilə birgə həyata keçirilən ikili diplom proqramının rəhbəri, 2019–2023-cü illərdə isə Azərbaycan Respublikası Elm və Təhsil Nazirliyi tərəfindən tanınan xüsusi lisenziyalı Əlavə Təhsil Müəssisəsinin direktoru. 2025-ci ilin avqust ayından etibarən Azərbaycan Texniki Universitetinin İnformasiya texnologiyaları və telekommunikasiya fakültəsinin dekanı, hazırda fakültənin Mühəndis riyaziyyatı və süni intellekt kafedrasında dosent kimi fəaliyyət göstərir. Elmi fəaliyyəti: Tədqiqatları əsasən böyük verilənlərə analitik yanaşmaların tətbiqinə, proqnozlaşdırma alqoritmlərinin işlənməsinə, qeyri-müəyyənlik şəraitində adaptiv və intellektual sistemlərinin dizaynına yönəlmişdir. Mühəndis riyaziyyatı və süni intellektin fundamental komponentləri olan riyazi analiz, xətti cəbr, ehtimal nəzəriyyəsi və riyazi statistika onun tədqiqatlarının metodoloji əsasını təşkil edir. Bu fənlərin inteqrasiyası vasitəsilə yüksək dəqiqlikli və praktiki əhəmiyyətli nəticələrə nail olunur.',
'["Diferensial tənliklər", "Riyazi analiz", "Riyazi modelləşdirmə", "Optimallaşdırma üsulları", "Süni intellekt və maşın öyrənməsi", "Data analitikası və böyük verilənlər (Big Data)", "İnformasiya texnologiyaları və onların tətbiqləri", "Riyazi iqtisadiyyat və ekonometrika"]'::jsonb,
NOW() FROM director_insert
UNION ALL
SELECT id, 'en', 'PhD in Physics and Mathematics', 'Associate Professor',
'Leyla Mazdek Mammadova, PhD in Physics and Mathematics, Associate Professor, is engaged in scientific and pedagogical activities at the Faculty of Information Technologies and Telecommunications of Azerbaijan Technical University. Her research primarily focuses on differential equations, mathematical modeling, and optimization methods. In recent years, her research interests have expanded to include modern areas such as artificial intelligence, data analytic, and applications of information technologies. In parallel, one of the main objectives of her research is the application of mathematical methods in the real sector, particularly in information technologies and management systems. Leyla Mammadova is the author of more than 40 scientific articles, 1 textbook, and 2 instructional manuals. Her research has been published in reputable international journals indexed in major scientific databases. In particular, her publications are indexed in systems such as Scopus and Web of Science. Alongside her research activities, she has participated in a number of scientific projects and has established collaborations with universities and industry partners. Within her academic work, she delivers lectures on differential equations, mathematical analysis, data analytic, and econometrics. She also supervises graduate students, supporting the development of their research skills. Her future research plans are focused on the development of artificial intelligence-based models, mathematical analysis of big data, advancement of modeling methods for data analytic, and the application of innovative approaches in educational technologies. Professional Experience: In 2001–2002, she worked as a lecturer at the Department of Information Technologies and Programming of the Faculty of Applied Mathematics and Cybernetics at Baku State University. From 2002 to 2011, she served as a senior lecturer at the Department of Economic Informatics of the same faculty. Between 2011 and 2025, she worked as an associate professor at the Department of Mathematical Economics of the Faculty of International Relations and Economics at Baku State University. In 2017–2018, she was the head of the dual degree program jointly implemented by the London School of Economics and Political Science (LSE) and UNEC. From 2019 to 2023, she served as the director of a specialized licensed Continuing Education Institution recognized by the Ministry of Science and Education of the Republic of Azerbaijan. Since August 2025, she has been serving as the Dean of the Faculty of Information Technologies and Telecommunications at Azerbaijan Technical University. Currently, she also works as an associate professor at the Department of Engineering Mathematics and Artificial Intelligence of the Faculty. Research Activity: Her research primarily focuses on the application of analytical approaches to big data, the development of forecasting algorithms, and the design of adaptive and intelligent systems under conditions of uncertainty. Fundamental components of engineering mathematics and artificial intelligence such as mathematical analysis, linear algebra, probability theory, and mathematical statistics form the methodological basis of her research. Through the integration of these disciplines, highly accurate and practically significant results are achieved.',
'["Differential Equations", "Mathematical Analysis", "Mathematical Modeling", "Optimization Methods", "Artificial Intelligence and Machine Learning", "Data Analytics and Big Data", "Information Technologies and Their Applications", "Mathematical Economics and Econometrics"]'::jsonb,
NOW() FROM director_insert
ON CONFLICT (director_id, lang_code) DO UPDATE
SET scientific_degree = EXCLUDED.scientific_degree, scientific_title = EXCLUDED.scientific_title,
    bio = EXCLUDED.bio, scientific_research_fields = EXCLUDED.scientific_research_fields, updated_at = NOW();

-- 5. Insert Director Working Hours
WITH working_hour_insert AS (
    INSERT INTO faculty_director_working_hours (director_id, time_range, created_at)
    SELECT id, '09:00–17:00', NOW() FROM faculty_directors WHERE faculty_code = 'information_technologies_telecommunications'
    RETURNING id
)
INSERT INTO faculty_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Çərşənbə, Cümə', NOW() FROM working_hour_insert
UNION ALL
SELECT id, 'en', 'Wednesday, Friday', NOW() FROM working_hour_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- 6. Insert Deputy Deans (Clear old ones for clean state)
DELETE FROM faculty_deputy_deans WHERE faculty_code = 'information_technologies_telecommunications';

WITH deputy_inserts AS (
    INSERT INTO faculty_deputy_deans (faculty_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('information_technologies_telecommunications', 'Elmixan', 'Qurbanov', 'Mədəd', 'elmxan.qurbanov@aztu.edu.az', NULL, NOW()),
    ('information_technologies_telecommunications', 'Ülviyyə', 'Kərimova', 'Yasin', 'ulviyya.karimova@aztu.edu.az', NULL, NOW()),
    ('information_technologies_telecommunications', 'Aytən', 'Mövsümova', 'Hafiz', 'aytan.movsumova@aztu.edu.az', NULL, NOW())
    RETURNING id
)
INSERT INTO faculty_deputy_dean_tr (deputy_dean_id, lang_code, duty, created_at)
SELECT id, 'az', duty, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM deputy_inserts
) d JOIN (
    VALUES
    (1, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin tədris işləri üzrə dekan müavini, f.r.e.n., dosent'),
    (2, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin sosial məsələlər, ictimaiyyətlə əlaqələr və infrastruktur üzrə dekan müavini, r.ü.f.d., dosent'),
    (3, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin beynəlxalq əlaqələr və tədqiqatlar üzrə dekan müavini, r.ü.f.d., dosent')
) v(row_num, duty) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM deputy_inserts
) d JOIN (
    VALUES
    (1, 'Deputy Dean for Academic Affairs, Faculty of Information Technologies and Telecommunications; PhD in Physics and Mathematics, Associate Professor'),
    (2, 'Deputy Dean for Social Affairs, Public Relations, and Infrastructure, Faculty of Information Technologies and Telecommunications; PhD in Mathematics, Associate Professor'),
    (3, 'Deputy Dean for International Relations and Research, Faculty of Information Technologies and Telecommunications; PhD in Mathematics, Associate Professor')
) v(row_num, duty) ON d.row_num = v.row_num;

-- 7. Insert Faculty Workers (Academic Advisors and Academic Assistant) (Clear old ones for clean state)
DELETE FROM faculty_workers WHERE faculty_code = 'information_technologies_telecommunications';

WITH worker_inserts AS (
    INSERT INTO faculty_workers (faculty_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('information_technologies_telecommunications', 'Səfa', 'Əsədova', 'Raqif', 'sefa.asadova@aztu.edu.az', NULL, NOW()),
    ('information_technologies_telecommunications', 'Zəhra', 'Qarayusifli', 'Namiq', 'zehra.qarayusifli@aztu.edu.az', NULL, NOW()),
    ('information_technologies_telecommunications', 'Fidan', 'Zeynallı', 'Aydın', 'fidanzeynalli@aztu.edu.az', NULL, NOW()),
    ('information_technologies_telecommunications', 'Leyla', 'Qurbanova', 'Bəhman', 'leyla.gurbanova@aztu.edu.az', NULL, NOW()),
    ('information_technologies_telecommunications', 'Sevinc', 'Rzazadə', 'Mübariz', 'sevinj.rzazadeh@aztu.edu.az', NULL, NOW()),
    ('information_technologies_telecommunications', 'Nurlana', 'Qafarova', 'Altay', 'nurlana.orucova@aztu.edu.az', NULL, NOW())
    RETURNING id
)
INSERT INTO faculty_worker_tr (worker_id, lang_code, duty, created_at)
SELECT id, 'az', duty, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin akademik məsləhətçisi'),
    (2, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin akademik məsləhətçisi'),
    (3, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin akademik məsləhətçisi'),
    (4, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin akademik məsləhətçisi'),
    (5, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin akademik məsləhətçisi'),
    (6, 'İnformasiya texnologiyaları və telekommunikasiya fakültəsinin kargüzarı')
) v(row_num, duty) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () as row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1, 'Academic Advisor at the Faculty of Information Technologies and Telecommunications'),
    (2, 'Academic Advisor at the Faculty of Information Technologies and Telecommunications'),
    (3, 'Academic Advisor at the Faculty of Information Technologies and Telecommunications'),
    (4, 'Academic Advisor at the Faculty of Information Technologies and Telecommunications'),
    (5, 'Academic Advisor at the Faculty of Information Technologies and Telecommunications'),
    (6, 'Academic Assistant at the Faculty of Information Technologies and Telecommunications')
) v(row_num, duty) ON w.row_num = v.row_num;

COMMIT;
