-- ============================================================
-- Maşınqayırma texnologiyası kafedrası — Full DB Import
-- cafedra_code: 'machine_engineering_technology'
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
    'machine_engineering_technology',
    2, 14, 3, 50, 5, 39, 19,
    '[4, 9, 12]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'machine_engineering_technology',
    'az',
    'Maşınqayırma texnologiyası kafedrası',
    'Maşınqayırma texnologiyası kafedrası 1932-ci ildə Metalların soyuq emalı adı ilə Azərbaycan Sənaye İnstitutunda yaradılıb. 1942-ci ildən kafedra Maşınqayırma texnologiyası adlandırılıb. 1950-ci ildə Azərbaycan Sənaye İnstitutunun Tikinti, Dəmir yolu nəqliyyatı və Mexanika fakültələrinin əsasında Azərbaycan Politexnik İnstitutu (indiki Azərbaycan Texniki Universiteti) yaradılıb və Mexanika fakültəsində Maşınqayırma texnologiyası kafedrası fəaliyyətini davam etdirib. 1951-ci ildə kafedranın 20 nəfərdən ibarət ilk buraxılışı olub. Kafedranın mühəndis kadrlarının hazırlanması imkanlarının artması və ixtisaslaşmaya tələblərin yüksəlməsi ilə əlaqədar olaraq, vaxtı ilə fəaliyyət göstərən Metalkəsən dəzgahlar və alətlər, Avtomatlaşdırılmış istehsalın texnologiyası, Maşınqayırmada avtomatlaşdırılmış layihələndirmə sistemləri, Maşınların etibarlığı və təmir texnologiyası, Texnoloji komplekslər və xüsusi texnika, Metrologiya və standartlaşdırma kafedraları və hazırda fəaliyyət göstərən Xüsusi texnologiyalar və avadanlıqlar kafedrası Maşınqayırma texnologiyası kafedrası əsasında yaradılıb. 1951-ci ildən 1996-cı ilə qədər Azərbaycan Texniki Universitetində (AzTU) maşınqayırma texnologiyası, metalkəsən dəzgahlar və alətlər ixtisası üzrə 15527 mühəndis hazırlanıb. 1992-ci ildən etibarən kafedra Maşınqayırma və material emalı istiqaməti üzrə bakalavr və 1998-ci ildən isə magistr hazırlığına başlayıb. Kafedranın ixtisas fənlərinin tədrisində kompüter texnologiyası geniş tətbiq olunur. Kafedrada tədrisin keyfiyyətini yüksəltmək üçün tədris prosesində hiper mətn texnologiyaları əsasında tərtib edilən elektron tədris vasitələrindən, mültimediya texnologiyalarından, animasiya vasitələrindən geniş istifadə edilir. Kafedranın laboratoriya və ixtisaslaşmış auditoriyaları interaktiv lövhə və elektron proyektorlarla təmin edilib, universitetin internet şəbəkəsinə qoşulub. Maşın mühəndisliyi və Cihaz mühəndisliyi ixtisasları üzrə mütəxəssis hazırlayır və bu sahələr üzrə elmi-tədqiqat işləri aparır.',
    NOW()
),
(
    'machine_engineering_technology',
    'en',
    'Department of Mechanical Engineering Technology',
    'The Department of Mechanical Engineering Technology was established in 1932 at the Azerbaijan Industrial Institute under the name "Cold Metal Processing." In 1942, it was renamed the Department of Mechanical Engineering Technology. In 1950, the Azerbaijan Polytechnic Institute (now the Azerbaijan Technical University) was founded based on the faculties of Construction, Railway Transport, and Mechanics from the Azerbaijan Industrial Institute, and the Department of Mechanical Engineering Technology continued its activities within the Faculty of Mechanics. In 1951, the department had its first graduation cohort consisting of 20 students. With the increasing demand for specialized engineering training and the department''s growing capacity for producing engineering professionals, several departments were formed based on the original Mechanical Engineering Technology Department. These include Metal-Cutting Machines and Tools, Technology of Automated Production, Automated Design Systems in Mechanical Engineering, Machine Reliability and Repair Technology, Technological Complexes and Special Machinery, and Metrology and Standardization. The currently active Department of Special Technologies and Equipment was also created on the foundation of the Department of Mechanical Engineering Technology. From 1951 to 1996, 15,527 engineers were trained at AzTU in the specializations of Mechanical Engineering Technology, Metal-Cutting Machines, and Tools. Since 1992, the department has offered bachelor''s degrees in Mechanical Engineering and Materials Processing, and since 1998 it has also provided master''s degree programs. Computer technology is widely used in teaching specialized subjects. To enhance education quality, electronic teaching aids based on hypertext technologies, multimedia, and animation tools are extensively employed. The department''s laboratories and specialized classrooms are equipped with interactive whiteboards and electronic projectors connected to the university''s internet network. The department trains specialists in Machine Engineering and Device Engineering and conducts scientific research in these areas.',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'machine_engineering_technology';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('machine_engineering_technology',  1, NOW()),
    ('machine_engineering_technology',  2, NOW()),
    ('machine_engineering_technology',  3, NOW()),
    ('machine_engineering_technology',  4, NOW()),
    ('machine_engineering_technology',  5, NOW()),
    ('machine_engineering_technology',  6, NOW()),
    ('machine_engineering_technology',  7, NOW()),
    ('machine_engineering_technology',  8, NOW()),
    ('machine_engineering_technology',  9, NOW()),
    ('machine_engineering_technology', 10, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1,  'Maşınqayırma sahəsində yüksəkixtisaslı kadr hazırlığı',
         'Kafedra maşınqayırma texnologiyası, istehsal prosesləri, metal emalı, avtomatlaşdırma və əlaqəli mühəndislik sahələri üzrə bakalavr, magistr və doktorant səviyyələrində mütəxəssis hazırlığını həyata keçirir.'),
    (2,  'Mexaniki emal texnologiyalarının işlənməsi və təkmilləşdirilməsi',
         'Kəsmə, torna, frezləmə və digər emal üsullarının optimallaşdırılması, məhsuldarlığın və keyfiyyətin artırılması üzrə yeni texnologiyalar hazırlanır və tətbiq edilir.'),
    (3,  'Müasir istehsal sistemlərinin təşkili və idarə olunması',
         'İstehsalat proseslərinin planlaşdırılması, çevik istehsal sistemləri, səmərəli istehsal və keyfiyyətin idarə olunması sahələrində fəaliyyət göstərilir.'),
    (4,  'Kompüter dəstəkli layihələndirmə və istehsal (CAD/CAM/CAE)',
         'Detalların və mexanizmlərin layihələndirilməsi, modelləşdirilməsi və istehsala hazırlanmasında müasir proqram təminatlarının tətbiqi təmin olunur.'),
    (5,  'Elmi-tədqiqat işlərinin aparılması',
         'Kafedrada maşınqayırma texnologiyaları, materialların emalı, alətlərin aşınması, istehsal proseslərinin modelləşdirilməsi və optimallaşdırılması istiqamətlərində elmi-tədqiqat işləri həyata keçirilir.'),
    (6,  'Yeni materiallar və onların emal texnologiyaları',
         'Kompozit materiallar, yüksək möhkəmlikli ərintilər və innovativ materialların emalı və tətbiqi üzrə tədqiqatlar aparılır.'),
    (7,  'Sənaye və istehsalatla inteqrasiya',
         'Kafedra sənaye müəssisələri ilə əməkdaşlıq edərək istehsalat təcrübələrinin təşkili, tətbiqi layihələrin icrası və real texnoloji problemlərin həlli istiqamətində fəaliyyət göstərir.'),
    (8,  'Avtomatlaşdırma və robot texnikasının tətbiqi',
         'İstehsalat proseslərində robotlaşdırılmış sistemlərin, CNC dəzgahların və avtomatlaşdırılmış idarəetmə texnologiyalarının tətbiqi və öyrənilməsi həyata keçirilir.'),
    (9,  'İnnovasiya və rəqəmsal texnologiyaların tətbiqi',
         'Sənaye 4.0 prinsipləri, rəqəmsal istehsal, ağıllı fabriklər və innovativ mühəndis həllərinin tədris və tədqiqat prosesinə inteqrasiyası təmin olunur.'),
    (10, 'Beynəlxalq və ölkədaxili elmi əməkdaşlıq',
         'Kafedra yerli və xarici universitetlər, elmi-tədqiqat institutları və sənaye tərəfdaşları ilə birgə layihələrdə iştirak edir, konfrans və seminarların təşkili və akademik mübadilə proqramlarını həyata keçirir.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1,  'Training of Highly Qualified Personnel in Mechanical Engineering',
         'The department carries out specialist training at the bachelor''s, master''s, and doctoral levels in mechanical engineering technology, manufacturing processes, metal processing, automation, and related engineering fields.'),
    (2,  'Development and Improvement of Mechanical Processing Technologies',
         'New technologies are developed and implemented for the optimization of cutting, turning, milling, and other machining methods, aimed at increasing productivity and quality.'),
    (3,  'Organization and Management of Modern Production Systems',
         'Activities are conducted in the fields of production process planning, flexible manufacturing systems (FMS), lean manufacturing, and quality management.'),
    (4,  'Computer-Aided Design and Manufacturing (CAD/CAM/CAE)',
         'The application of modern software is ensured in the design, modeling, and production preparation of parts and mechanisms.'),
    (5,  'Conduct of Scientific Research',
         'The department carries out scientific research in the areas of mechanical engineering technologies, materials processing, tool wear, and the modeling and optimization of production processes.'),
    (6,  'New Materials and Their Processing Technologies',
         'Research is conducted on the processing and application of composite materials, high-strength alloys, and innovative materials.'),
    (7,  'Integration with Industry and Production',
         'The department cooperates with industrial enterprises to organize internships, execute applied projects, and solve real-world technological challenges.'),
    (8,  'Application of Automation and Robotics',
         'The study and implementation of robotic systems, CNC machine tools, and automated control technologies in manufacturing processes are carried out.'),
    (9,  'Application of Innovation and Digital Technologies',
         'The integration of Industry 4.0 principles, digital manufacturing, smart factories, and innovative engineering solutions into the teaching and research process is ensured.'),
    (10, 'International and National Scientific Cooperation',
         'The department participates in joint projects with local and foreign universities, research institutes, and industrial partners, organizes conferences and seminars, and implements academic exchange programs.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ─
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'machine_engineering_technology',
        'Nizami', 'Yusubov', 'Dəmir oğlu',
        'nizami.yusubov@aztu.edu.az',
        '+994 50 324 50 12',
        'IV korpus, 213-cü otaq (daxili: 2520)',
        NOW()
    ) ON CONFLICT (cafedra_code) DO UPDATE
    SET first_name  = EXCLUDED.first_name,
        last_name   = EXCLUDED.last_name,
        father_name = EXCLUDED.father_name,
        email       = EXCLUDED.email,
        phone       = EXCLUDED.phone,
        room_number = EXCLUDED.room_number,
        updated_at  = NOW()
    RETURNING id
)
INSERT INTO cafedra_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, scientific_research_fields, created_at)
SELECT id, 'az',
    'Texnika elmləri doktoru',
    'Professor',
    'Nizami Dəmir oğlu Yusubov 2 fevral 1965-ci ildə Lənkəran şəhərində qulluqçu ailəsində anadan olub və 1972–1982-ci illərdə Lənkəran şəhərinin 2 saylı orta məktəbində orta təhsil alıb. Eyni zamanda 1981–1982-ci tədris ilində orta məktəbin 10-cu sinif şagirdi kimi M.V.Lomonosov adına Moskva Dövlət Universitetinin iki illik Qiyabi Fizika məktəbini bir ilə qurtarıb. Orta məktəbdə oxuduğu illərdə şəhərin ictimai həyatında fəal iştirak edib, müxtəlif fənn olimpiadalarının iştirakçısı və qalibi olub. 1982-ci ildə Azərbaycan Politexnik İnstitutuna maşınqayırma texnologiyası, metalkəsən dəzgahlar və alətlər ixtisası üzrə daxil olub, 1983–1985-ci illərdə Sovetlər Birliyində qəbul olunan qərara əsasən, institutun birinci kursunu bitirib ordu sıralarında xidmət edib. Ordu sıralarında 2 illik xidməti başa vurduqdan sonra 1985–1989-cu illərdə yenidən təhsilini Azərbaycan Politexnik İnstitutunda davam edib. Ali məktəbdə təhsil aldığı illərdə dərs əlaçısı və Lenin təqaüdçüsü olub. N.D.Yusubov 1989-cu ildə Azərbaycan Politexnik İnstitutunu maşınqayırma texnologiyası, metalkəsən dəzgahlar və alətlər ixtisası üzrə tam kursu fərqlənmə diplomu ilə bitirib və Maşınqayırma texnologiyası kafedrasının tövsiyəsi və Maşınqayırma fakültəsi Elmi şurasının qərarı ilə stajkeçən tədqiqatçı kimi kafedrada saxlanılıb. N.D.Yusubov 1990-cı ilin sentyabrından Çelyabinsk Politexnik İnstitutuna məqsədli aspiranturaya göndərilmiş və 1993-cü il yanvar ayının 25-də «Torna-revolver avtomatlarında səthlərin emal planlarının məhsuldarlıq kriteriyası üzrə optimallaşdırılması» mövzusunda namizədlik dissertasiyasını vaxtından əvvəl müdafiə edərək texnika elmləri namizədi elmi dərəcəsini alıb. N.D.Yusubov 1993-cü ilin oktyabr ayından Maşınqayırma texnologiyası kafedrasında assistent, 1994-cü ilin noyabrından baş müəllim, 1995-ci ilin noyabr ayından dosent, 2013-cü ilin noyabr ayından 09 sentyabr 2015-ci ilə qədər professor vəzifəsində çalışıb. Azərbaycan Respublikası Təhsil Naziri Mikayıl Cabbarovun 09 sentyabr 2015-ci il tarixli 11/944 saylı əmri ilə professor Nizami Dəmir oğlu Yusubov Lənkəran Dövlət Universitetinin (LDU) tədris işləri üzrə prorektoru təyin edilib. N.D.Yusubov 1998-ci ilin fevral ayının 2-də Ali Attestasiya Komissiyasının qərarı ilə Maşınqayırma texnologiyası kafedrası üzrə dosent elmi adını alıb. N.D.Yusubov 02 dekabr 2009-cu ildə AzTU-nun nəzdindəki D.02.171 Dissertasiya Şurasında «Torna avtomat-dəzgahlar qrupunda çoxalətli emalın səmərəliliyinin yüksəldilməsi» mövzusunda doktorluq dissertasiyasını müdafiə edib və 07 yanvar 2011-ci ildə texnika üzrə elmlər doktoru elmi dərəcəsini alıb. N.D.Yusubov 2015-ci ilin may ayının 22-də Ali Attestasiya Komissiyasının qərarı ilə Maşınqayırma texnologiyası kafedrası üzrə professor elmi adını alıb. 350-dən çox elmi və tədris-metodiki işin müəllifidir, o cümlədən 5 ixtira, 4 monoqrafiya (bunlardan 3-ü Almaniyanın Saarbryükken şəhərindəki LAP LAMBERT Academic Publishing nəşriyyatında çap olunub), 3 dərslik, 10 dərs vəsaiti, 10 metodiki göstəriş, 1 metodiki vəsait və 75 fənn proqramı. Elmi əsərlərindən 58-i ABŞ, Almaniya, İsveç, İsveçrə, Fransa, Malaysiya, Rusiya, Türkiyə, Belarusiya, Ukrayna və Kazaxstanın qabaqcıl texniki dərgi və məcmuələrində çap olunub. DAAD xətti ilə Almaniyanın Braunşveyq Texniki Universiteti (1996–1997), Drezden Texniki Universiteti (2001, 2015) və Aaxen Ali Texniki Məktəbinin (2012) institutlarında elmi tədqiqatlar aparıb; Rostok Universitetinin Fraunhofer İnstitutunda (2023) fəaliyyət göstərib. ABŞ Dövlət Departamentinin IVLP proqramı üzrə beynəlxalq sertifikat alıb (2015). N.D.Yusubova Azərbaycan Respublikası Prezidentinin 2020-ci il 30 dekabr tarixli 2394 nömrəli Sərəncamı ilə "Əməkdar mühəndis" fəxri adı verilib. Evlidir, 3 övladı var.',
    '["Çoxalətli torna emalı və çoxsupportlu RPİ dəzgahları", "Mexaniki emal proseslərinin riyazi və stoxastik modelləşdirilməsi", "Emal dəqiqliyinin matris modelləri və səpələnmə sahələrinin analizi", "Texnoloji sistemlərin elastikliyinin kompleks xarakteristikası", "Kəsmə qüvvələri və emal dinamikasının modelləşdirilməsi", "Adaptiv idarəetmə və optimallaşdırma metodları", "Rəqəmsal istehsal (Digital Twin) və enerji səmərəli emal texnologiyaları"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Technical Sciences',
    'Professor',
    'Nizami Yusubov Damir was born on February 2, 1965, in the city of Lankaran, in a family of civil servants. From 1972 to 1982, he received his secondary education at School No. 2 in Lankaran. During the 1981–1982 academic year, as a 10th-grade student, he completed a two-year Correspondence Physics School at Lomonosov Moscow State University in one year. He actively participated in the public life of the city and was a winner of various academic Olympiads. In 1982, he entered the Azerbaijan Polytechnic Institute to study Mechanical Engineering Technology, Metal-Cutting Machines, and Tools. After completing his first year he served in the army from 1983 to 1985, then resumed his studies from 1985 to 1989, graduating with distinction. He was an excellent student and a recipient of the Lenin scholarship. In 1989, based on the recommendation of the Department of Mechanical Engineering Technology and a decision by the Faculty''s Scientific Council, he was retained as a trainee researcher in the department. In September 1990, he was sent to a postgraduate program at Chelyabinsk Polytechnic Institute (later South Ural State University), and on January 25, 1993, he defended his candidate''s dissertation ahead of schedule on the topic "Optimization of Surface Processing Plans by Productivity Criteria on Turret Lathes" (specialty 05.02.08), earning the degree of Candidate of Technical Sciences. Since October 1993, he worked as an Assistant, became a Senior Lecturer in November 1994, an Associate Professor in November 1995, and a Professor from November 2013 to September 9, 2015. By order of the Minister of Education dated September 9, 2015 (No. 11/944), he was appointed Vice-Rector for Academic Affairs at Lankaran State University (LSU). On February 2, 1998, he received the academic title of Associate Professor. On December 2, 2009, he defended his doctoral dissertation on "Improving the Efficiency of Multi-spindle Machining on Turret Lathe Groups" at the D.02.171 Dissertation Council of AzTU and on January 7, 2011, was awarded the degree of Doctor of Technical Sciences. On May 22, 2015, he was awarded the academic title of Professor. He is the author of over 350 scientific and methodical works, including 5 inventions, 4 monographs (3 published by LAP LAMBERT Academic Publishing, Saarbrücken, Germany), 3 textbooks, 10 teaching aids, 10 methodological guidelines, and 75 subject programs. 58 of his scientific works have been published in leading journals in the USA, Germany, Sweden, Switzerland, France, Malaysia, Russia, Turkey, Belarus, Ukraine, and Kazakhstan. Through DAAD, he conducted research at Braunschweig''s Technical University (1996–1997), TU Dresden (2001, 2015), RWTH Aachen (2012), and the Fraunhofer Institute in Rostock (2023). He received an international certificate through the U.S. State Department IVLP program (2015). He was awarded the honorary title of "Honored Engineer" by Presidential Decree No. 2394 dated December 30, 2020. He is married and has three children.',
    '["Multi-tool lathe machining and multi-carriage CNC machines", "Mathematical and stochastic modeling of machining processes", "Matrix models of machining accuracy and analysis of dispersion zones", "Comprehensive characterization of the elasticity of technological systems", "Modeling of cutting forces and machining dynamics", "Adaptive control and optimization methods", "Digital production (Digital Twin) and energy-efficient machining technologies"]'::jsonb,
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
    FROM cafedra_directors WHERE cafedra_code = 'machine_engineering_technology'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Çərşənbə axşamı, Cümə axşamı', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Tuesday, Thursday',             NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
WITH
ed1 AS (
    INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
    SELECT id, '1982', '1989', NOW() FROM cafedra_directors WHERE cafedra_code = 'machine_engineering_technology'
    RETURNING id
),
ed2 AS (
    INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
    SELECT id, '1990', '1993', NOW() FROM cafedra_directors WHERE cafedra_code = 'machine_engineering_technology'
    RETURNING id
),
ed3 AS (
    INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
    SELECT id, '2009', '2011', NOW() FROM cafedra_directors WHERE cafedra_code = 'machine_engineering_technology'
    RETURNING id
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', 'Bakalavr + Magistr (1983–1985: hərbi xidmət)', 'Azərbaycan Politexnik İnstitutu', NOW() FROM ed1
UNION ALL
SELECT id, 'en', 'Bachelor''s + Master''s Degrees (1983–1985: Military Service)', 'Azerbaijan Polytechnic Institute', NOW() FROM ed1
UNION ALL
SELECT id, 'az', 'Texnika elmləri namizədi (PhD)', 'Çelyabinsk Politexnik İnstitutu', NOW() FROM ed2
UNION ALL
SELECT id, 'en', 'Candidate of Sciences (PhD)', 'Chelyabinsk Polytechnic Institute', NOW() FROM ed2
UNION ALL
SELECT id, 'az', 'Texnika elmləri doktoru (DSc)', 'Azərbaycan Texniki Universiteti (AzTU)', NOW() FROM ed3
UNION ALL
SELECT id, 'en', 'Doctor of Sciences (DSc)', 'Azerbaijan Technical University (AzTU)', NOW() FROM ed3;


-- ── 5. Workers ───────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'machine_engineering_technology';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Məsləhətçi professorlar (t.e.d.)
    ('machine_engineering_technology', 'Vaqif',    'Mövlazadə',   'Zahid oğlu',    'movlazade.vaqif@aztu.edu.az',      NULL, NOW()),  -- 1
    ('machine_engineering_technology', 'Nəriman',  'Rəsulov',     'Moğbil oğlu',   'nariman.rasulov@aztu.edu.az',      NULL, NOW()),  -- 2
    ('machine_engineering_technology', 'Həsən',    'Hüseynov',    'Əhməd oğlu',    'tk_xt2001@aztu.edu.az',            NULL, NOW()),  -- 3
    -- Professorlar (t.e.d.)
    ('machine_engineering_technology', 'Yusif',    'Həsənov',     'Nadir oğlu',    'yusif.huseynov@aztu.edu.az',       NULL, NOW()),  -- 4
    ('machine_engineering_technology', 'Yaşar',    'Musayev',     'Balabəy oğlu',  'yasar.musayev@aztu.edu.az',        NULL, NOW()),  -- 5
    -- Dosentlər
    ('machine_engineering_technology', 'Ərəstun',  'Məmmədov',    'Salman oğlu',   'arastun.mammadov@aztu.edu.az',     NULL, NOW()),  -- 6
    ('machine_engineering_technology', 'Malik',    'Qarayev',     'Fikrət oğlu',   'malik.qarayev@aztu.edu.az',        NULL, NOW()),  -- 7
    ('machine_engineering_technology', 'Müxəddin', 'Səmədov',     'Kamal oğlu',    'm.semedov@aztu.edu.az',            NULL, NOW()),  -- 8
    ('machine_engineering_technology', 'Ağa',      'Şıxseyidov',  'Şıxzadə oğlu', 'agashixseyidov@aztu.edu.az',       NULL, NOW()),  -- 9
    ('machine_engineering_technology', 'Gövhər',   'Abbasova',    'Nadir qızı',    'govher.abbasova@aztu.edu.az',      NULL, NOW()),  -- 10
    ('machine_engineering_technology', 'Ceyhun',   'Rəhimov',     'Rasif oğlu',    'jeyhun.rahimov@aztu.edu.az',       NULL, NOW()),  -- 11
    ('machine_engineering_technology', 'Asim',     'Mirzəyev',    'Mirzəxan oğlu', 'asimmi@aztu.edu.az',               NULL, NOW()),  -- 12
    ('machine_engineering_technology', 'Sarvan',   'Əziz',        'Şirvan oğlu',   'sarvan.aziz@aztu.edu.az',          NULL, NOW()),  -- 13
    ('machine_engineering_technology', 'Elgün',    'Şəbiyev',     'Tağı oğlu',     'elgun@aztu.edu.az',                NULL, NOW()),  -- 14
    ('machine_engineering_technology', 'Heyran',   'Abbasova',    'Mürşüd qızı',   'abbasova.heyran@aztu.edu.az',      NULL, NOW()),  -- 15
    -- Baş müəllimlər
    ('machine_engineering_technology', 'İradə',    'Abbasova',    'Əziz qızı',     'irada.abasova.a@aztu.edu.az',      NULL, NOW()),  -- 16
    ('machine_engineering_technology', 'Ağasi',    'Ağayev',      'Ramiz oğlu',    'agasig@aztu.edu.az',               NULL, NOW()),  -- 17
    ('machine_engineering_technology', 'Ramil',    'Dadaşov',     'Yengibar oğlu', 'dadashov@aztu.edu.az',             NULL, NOW()),  -- 18
    -- Assistent
    ('machine_engineering_technology', 'Yusif',    'Hüseynov',    'Eldar oğlu',    'yusif.huseynov@aztu.edu.az',       NULL, NOW()),  -- 19
    -- Digər vəzifələr
    ('machine_engineering_technology', 'Zərifə',   'Əzizli',      'Mahmud qızı',   'zerife.ezizli@aztu.edu.az',        NULL, NOW()),  -- 20
    ('machine_engineering_technology', 'Könül',    'Şəmmədova',   'Akif qızı',     'konul.shammadova@aztu.edu.az',     NULL, NOW()),  -- 21
    ('machine_engineering_technology', 'Alı',      'Göşşüyev',    'Asəf oğlu',     'ali.goshshuyev@aztu.edu.az',       NULL, NOW()),  -- 22
    ('machine_engineering_technology', 'Sahib',    'Rzaquliyev',  'Zahir oğlu',    'sahib.rzaquliyev@aztu.edu.az',     NULL, NOW()),  -- 23
    ('machine_engineering_technology', 'Fəridə',   'Məmmədova',   'Elşən qızı',    'farida.mammadova@aztu.edu.az',     NULL, NOW())   -- 24
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Maşınqayırma texnologiyası kafedrası, məsləhətçi professor', 'Professor', 't.e.d.'),
    (2,  'Maşınqayırma texnologiyası kafedrası, məsləhətçi professor', 'Professor', 't.e.d.'),
    (3,  'Maşınqayırma texnologiyası kafedrası, məsləhətçi professor', 'Professor', 't.e.d.'),
    (4,  'Maşınqayırma texnologiyası kafedrası, professor',            'Professor', 't.e.d.'),
    (5,  'Maşınqayırma texnologiyası kafedrası, professor',            'Professor', 't.e.d.'),
    (6,  'Maşınqayırma texnologiyası kafedrası, dosent, Tədris şöbəsinin müdiri', 'Dosent', 'f.d.'),
    (7,  'Maşınqayırma texnologiyası kafedrası, dosent, Maşınqayırma və metallurgiya fakültəsinin dekanı', 'Dosent', 'f.d.'),
    (8,  'Maşınqayırma texnologiyası kafedrası, dosent',               'Dosent',    'f.d.'),
    (9,  'Maşınqayırma texnologiyası kafedrası, dosent',               'Dosent',    't.e.n.'),
    (10, 'Maşınqayırma texnologiyası kafedrası, dosent',               'Dosent',    'f.d.'),
    (11, 'Maşınqayırma texnologiyası kafedrası, dosent',               'Dosent',    'f.d.'),
    (12, 'Maşınqayırma texnologiyası kafedrası, dosent',               'Dosent',    't.e.d.'),
    (13, 'Maşınqayırma texnologiyası kafedrası, dosent',               'Dosent',    'f.d.'),
    (14, 'Maşınqayırma texnologiyası kafedrası, dosent, tədris işləri üzrə dekan müavini', 'Dosent', 't.ü.f.d.'),
    (15, 'Maşınqayırma texnologiyası kafedrası, dosent',               'Dosent',    't.ü.f.d.'),
    (16, 'Maşınqayırma texnologiyası kafedrası, baş müəllim',          NULL,         NULL),
    (17, 'Maşınqayırma texnologiyası kafedrası, baş müəllim',          NULL,         NULL),
    (18, 'Maşınqayırma texnologiyası kafedrası, baş müəllim',          NULL,         NULL),
    (19, 'Maşınqayırma texnologiyası kafedrası, assistent',            NULL,         NULL),
    (20, 'Maşınqayırma texnologiyası kafedrası, laboratoriya müdiri',  NULL,         NULL),
    (21, 'Maşınqayırma texnologiyası kafedrası, kargüzar',             NULL,         NULL),
    (22, 'Maşınqayırma texnologiyası kafedrası, müəllim köməkçisi',    NULL,         NULL),
    (23, 'Maşınqayırma texnologiyası kafedrası, müəllim köməkçisi',    NULL,         NULL),
    (24, 'Maşınqayırma texnologiyası kafedrası, kargüzar',             NULL,         NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Department of Mechanical Engineering Technology, Advisor Professor', 'Professor',           't.e.d.'),
    (2,  'Department of Mechanical Engineering Technology, Advisor Professor', 'Professor',           't.e.d.'),
    (3,  'Department of Mechanical Engineering Technology, Advisor Professor', 'Professor',           't.e.d.'),
    (4,  'Department of Mechanical Engineering Technology, Professor',         'Professor',           't.e.d.'),
    (5,  'Department of Mechanical Engineering Technology, Professor',         'Professor',           't.e.d.'),
    (6,  'Department of Mechanical Engineering Technology, Associate Professor, Head of Educational Department', 'Associate Professor', 'Ph.D.'),
    (7,  'Department of Mechanical Engineering Technology, Associate Professor, Dean of the Faculty of Mechanical Engineering and Metallurgy', 'Associate Professor', 'Ph.D.'),
    (8,  'Department of Mechanical Engineering Technology, Associate Professor','Associate Professor', 'Ph.D.'),
    (9,  'Department of Mechanical Engineering Technology, Associate Professor','Associate Professor', 't.e.n.'),
    (10, 'Department of Mechanical Engineering Technology, Associate Professor','Associate Professor', 'Ph.D.'),
    (11, 'Department of Mechanical Engineering Technology, Associate Professor','Associate Professor', 'Ph.D.'),
    (12, 'Department of Mechanical Engineering Technology, Associate Professor','Associate Professor', 't.e.d.'),
    (13, 'Department of Mechanical Engineering Technology, Associate Professor','Associate Professor', 'Ph.D.'),
    (14, 'Department of Mechanical Engineering Technology, Associate Professor, Deputy Dean for Academic Affairs', 'Associate Professor', 'Ph.D.'),
    (15, 'Department of Mechanical Engineering Technology, Associate Professor','Associate Professor', 'Ph.D.'),
    (16, 'Department of Mechanical Engineering Technology, Senior Lecturer',   NULL,                  NULL),
    (17, 'Department of Mechanical Engineering Technology, Senior Lecturer',   NULL,                  NULL),
    (18, 'Department of Mechanical Engineering Technology, Senior Lecturer',   NULL,                  NULL),
    (19, 'Department of Mechanical Engineering Technology, Assistant',         NULL,                  NULL),
    (20, 'Department of Mechanical Engineering Technology, Laboratory Director',NULL,                 NULL),
    (21, 'Department of Mechanical Engineering Technology, Administrative Assistant', NULL,           NULL),
    (22, 'Department of Mechanical Engineering Technology, Teacher Assistant', NULL,                  NULL),
    (23, 'Department of Mechanical Engineering Technology, Teacher Assistant', NULL,                  NULL),
    (24, 'Department of Mechanical Engineering Technology, Administrative Assistant', NULL,           NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
