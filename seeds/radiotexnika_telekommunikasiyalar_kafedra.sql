-- ============================================================
-- Radiotexnika və Telekommunikasiyalar kafedrası — Full DB Import
-- cafedra_code: 'radio_engineering_telecommunications'
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
    'radio_engineering_telecommunications',
    1, 6, 0, 7, 0, 0, 0,
    '[4, 9, 17, 11, 12, 13]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'radio_engineering_telecommunications',
    'az',
    'Radiotexnika və Telekommunikasiyalar kafedrası',
    '<p>"Radiotexnika və Telekommunikasiyalar" kafedrası 2021-ci ildə "Çoxkanallı Telekommunikasiyalar" kafedrasının və "Radiotexnika" kafedrasının birləşdirilməsi nəticəsində yaradılmışdır. Kafedraya texnika elmləri doktoru, professor Həsənov Mehman Hüseyn rəhbərlik edir.</p><p>"Radiotexnika və Telekommunikasiyalar" kafedrası əvvəlcə Elektrik Rabitəsi adı altında fəaliyyət göstərmişdir. Kafedra 1964-cü ildə Çingiz İldırım adına Azərbaycan Politexnik İnstitutunda, hazırda Azərbaycan Texniki Universitetində yaradılmışdır. Kafedranın yaradılmasında xidmətləri olan Rəhimov Qurbanhuseyn Abdulrəhim onun ilk müdiri olmuşdur. Sonrakı illərdə professorlar Həsənov Əlşən Nəriman, İmamverdiyev Qəzənfər Məmməd, Mansurov Tofiq Məhəmməd və İbrahimov Bayram Qənimət bu kafedraya rəhbərlik etmişlər.</p><p>Kafedranın hazırkı bazası aşağıdakı kafedralardan formalaşmışdır: "Radiotexnika" (1961-ci ildə yaradılmışdır, kafedra müdiri t.e.d. prof. U.S. Kəngərlinski), "Ümumi Nəzəri Radiotexnika" (1964-cü ildə yaradılmışdır, kafedra müdiri t.e.d. prof. U.S. Kəngərlinski), "Elektrik Rabitəsi" (1965-ci ildə yaradılmışdır, kafedra müdiri t.e.n., dos. Q.A. Rəhimov), "Televiziya və Radio Sistemləri" (1974-cü ildə yaradılmışdır, kafedra müdiri t.e.d., prof. Ç.A. Əfəndiyev), "Texniki Elektrodinamika və Ultra Yüksək Tezlikli Cihazlar" (1990-cı ildə yaradılmışdır, kafedra müdiri t.e.d. prof. E.Q. İsmiyev), "Avtomatik Elektrik Rabitəsi" (1991-ci ildə yaradılmışdır, kafedra müdiri t.e.d. prof. A.N. Həsənov) və "İnformasiya Şəbəkələri və Sistemləri" (1992-ci ildə yaradılmışdır, kafedra müdiri t.e.n., dos. F.M. Məmmədov).</p><p>Kafedranın əsas məqsədi televiziya, radio, internet, mobil rabitə, aerokosmik sahə və sənayenin müxtəlif sektorları üçün yüksək ixtisaslı mütəxəssislər hazırlamaqdır. Kafedra tələbələrə radioelektron avadanlıqların layihələndirilməsi, istehsalı, idarə edilməsi və texniki istismarı sahəsində müasir bilik və bacarıqlar verməyi hədəfləyir.</p><p>Eyni zamanda, kafedra sürətlə inkişaf edən informasiya və telekommunikasiya texnologiyaları sahəsində ölkənin artan tələblərini qarşılaya biləcək peşəkar mühəndislərin hazırlanmasına xüsusi diqqət yetirir. Tədris prosesi tələbələrin nəzəri biliklərini praktik bacarıqlarla birləşdirməyə, innovativ texnologiyaları öyrənməyə və müasir radioelektron sistemləri tətbiq etməyə yönəlmişdir.</p>',
    NOW()
),
(
    'radio_engineering_telecommunications',
    'en',
    'Department of Radio Engineering and Telecommunications',
    '<p>The "Radio Engineering and Telecommunications" department was established in 2021 through the merger of the "Multichannel Telecommunications" Department and the "Radio Engineering" Department. The department is headed by doctor of technical sciences, professor Hasanov Mehman Huseyn.</p><p>The "Radio Engineering and Telecommunications" department initially operated under the name Electrical Communications. The department was established in 1964 at the Azerbaijan Polytechnic Institute named after Chingiz Ildirim, currently Azerbaijan Technical University. Rahimov Gurbanhuseyn Abdulrahim, who contributed to the establishment of the department, was its first head. In the following years, professors Hasanov Alshan Nariman, Imamverdiyev Gazanfar Mammad, Mansurov Tofiq Mahammad, and Ibrahimov Bayram Qanimat headed this department.</p><p>The current base of the department was formed from the following departments: "Radio Engineering" (established in 1961, Head of Department t.e.d. Prof. U.S. Kangerlinski), "General Theoretical Radio Engineering" (established in 1964, Head of Department t.e.d. Prof. U.S. Kangerlinski), "Electrical Communications" (established in 1965, Head of Department t.e.n., Assoc. Prof. Q.A. Rahimov), "Television and Radio Systems" (established in 1974, Head of Department t.e.d., Prof. Ch.A. Afandiyev), "Technical Electrodynamics and Ultra High Frequency Devices" (established in 1990, Head of Department t.e.d. Prof. E.Q. Ismiyev), "Automatic Electrical Communications" (established in 1991, Head of Department t.e.d. Prof. A.N. Hasanov), and "Information Networks and Systems" (established in 1992, Head of Department t.e.n., Assoc. Prof. F.M. Mammadov).</p><p>The main purpose of the Department is to train highly qualified specialists for television, radio, internet, mobile communications, the aerospace field, and various sectors of industry. The department aims to provide students with modern knowledge and skills in the design, production, management, and technical operation of radio-electronic equipment.</p><p>At the same time, the department pays special attention to preparing professional engineers who can meet the growing demands of the country in the rapidly developing field of information and telecommunication technologies. The educational process is aimed at combining students'' theoretical knowledge with practical skills, learning innovative technologies, and applying modern radio-electronic systems.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'radio_engineering_telecommunications';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('radio_engineering_telecommunications', 1, NOW()),
    ('radio_engineering_telecommunications', 2, NOW()),
    ('radio_engineering_telecommunications', 3, NOW()),
    ('radio_engineering_telecommunications', 4, NOW()),
    ('radio_engineering_telecommunications', 5, NOW()),
    ('radio_engineering_telecommunications', 6, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Tədris fəaliyyəti',                    'Radiotexnika, telekommunikasiya və informasiya təhlükəsizliyi sahələrində elm və texnikanın ən son nailiyyətlərindən istifadə edilir'),
    (2, 'Elmi-tədqiqat fəaliyyəti',             'Elmi tədqiqatların aparılmasında müasir infotelekommunikasiya texnologiyalarından istifadə olunur'),
    (3, 'Kadr hazırlığı',                       'Bakalavr (600640 – Radiotexnika və Telekommunikasiya Mühəndisliyi) və Magistratura səviyyəsində 6 ixtisaslaşma üzrə mütəxəssis hazırlığı'),
    (4, 'Beynəlxalq əlaqələr',                  'Mübadilə proqramları, ikili diplom proqramları və AQAS akkreditasiyası vasitəsilə beynəlxalq əməkdaşlıq'),
    (5, 'Praktiki və laboratoriya işləri',       'Müasir texnologiya tələblərinə cavab verən tədris laboratoriyaları və Wi-Fi şəbəkəsi ilə təchiz olunmuş kompüter şəbəkəsi'),
    (6, 'Tələbələrin elmi tədqiqata cəlb edilməsi','Tələbələrin elmi-tədqiqat fəaliyyətinə cəlb edilməsi, yeni texnologiyaların öyrənilməsinin təşviqi')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Teaching activities',                    'The latest achievements in science and technology in the fields of Radio Engineering, telecommunications, and information security are used in the teaching process'),
    (2, 'Scientific research activities',         'Modern infotelecommunication technology is used in conducting scientific research'),
    (3, 'Human resource development',             'Training of specialists at Bachelor''s level (600640 – Radio Engineering and Telecommunication Engineering) and Master''s level with 6 specializations'),
    (4, 'International relations',                'International cooperation through exchange programs, double degree programs, and AQAS accreditation'),
    (5, 'Practical and laboratory work',          'Teaching laboratories meeting modern technology requirements and a local computer network equipped with Wi-Fi'),
    (6, 'Student involvement in research',        'Involving students in scientific research activities and encouraging the study of new technologies')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'radio_engineering_telecommunications',
        'Mehman', 'Həsənov', 'Hüseyn oğlu',
        'mehman.hasanov@aztu.edu.az',
        '+994 12 538-87-66',
        'VII korpus, 419-cu otaq',
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
    '<p>Həsənov Mehman Hüseyn oğlu 1959-cu ildə Ermənistan Respublikasının Krasnoselo rayonunun Cil kəndində anadan olmuşdur.</p><p>1982-ci ildə Azərbaycan Politexnik İnstitutunu (hazırda Azərbaycan Texniki Universiteti) bitirdikdən sonra 1982-1985-ci illərdə Moskvada Kosmik Mərkəzdə çalışmışdır. 1985-1986-cı illərdə Azərbaycan Texniki Universitetində (AzTU) işləmiş, 1986-1990-cı illərdə aspiranturada təhsil almışdır.</p><p>1990-cı ildə texnika elmləri namizədi dərəcəsi almış və 1990-1997-ci illərdə Elektrik Rabitəsi kafedrasında dosent vəzifəsində çalışmışdır. 1997-2004-cü illərdə Bakı Telefon Rabitəsi İstehsalat Birliyində baş texniki mütəxəssis, 2004-2016-cı illərdə Aztelecom İstehsalat Birliyində informasiya texnologiyaları üzrə baş direktorun müavini vəzifəsində çalışmışdır.</p><p>2022-ci ildə 3325.01 – "Telekommunikasiya texnologiyası" ixtisası üzrə doktorluq dissertasiyasını uğurla müdafiə edərək Azərbaycan Respublikasının Prezidenti yanında Ali Attestasiya Komissiyasının qərarı ilə texnika elmləri doktoru dərəcəsi almışdır.</p><p>300-dən çox elmi məqalənin, 22 ixtira-patentin, 5 monoqrafiya və dərsliyin müəllifidir. Çoxsaylı milli və beynəlxalq qrant layihələrinin rəhbəridir. 2015-ci ildə "Tərəqqi" medalı ilə təltif olunmuşdur. Fərqlənmiş telekommunikasiya mütəxəssisi kimi tanınır və İTU-T sertifikatlarına malikdir. Azərbaycan Mühəndislik Akademiyasının həqiqi üzvü və Beynəlxalq Mühəndislik Akademiyasının müxbir üzvüdür.</p><p>2016-cı ildən Azərbaycan Texniki Universitetinin Radiotexnika və Telekommunikasiyalar kafedrasının müdiri vəzifəsində çalışır. 2023-cü ildə professor elmi adı almışdır.</p>',
    '["Sərbəst fəzada optik rabitə texnologiyaları", "Aşağı Yer Orbitində (LEO) nanopeyk şəbəkələrinin idarə edilməsi", "LiFi texnologiyaları", "Yeni nəsil mobil rabitə texnologiyaları"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Technical Sciences',
    'Professor',
    '<p>Mehman Huseyn Hasanov was born in 1959 in the village of Cil, Krasnoselo district, Republic of Armenia.</p><p>After graduating from the Azerbaijan Polytechnic Institute (now Azerbaijan Technical University) in 1982, he worked at the Space Center in Moscow from 1982 to 1985. From 1985 to 1986, he worked at Azerbaijan Technical University (AzTU), and between 1986 and 1990, he pursued postgraduate studies.</p><p>In 1990, he was awarded the degree of Candidate of Technical Sciences and worked as an Associate Professor at the Department of Electrical Communications from 1990 to 1997. Between 1997 and 2004, he served as a Chief Technical Specialist at the Baku Telephone Communications Production Association. From 2004 to 2016, he held the position of Deputy General Director for Information Technologies at Aztelekom Production Association.</p><p>In 2022, he successfully defended his doctoral dissertation in the specialty 3325.01 – "Telecommunication Technology" and was awarded the degree of Doctor of Technical Sciences by the decision of the Higher Attestation Commission under the President of the Republic of Azerbaijan.</p><p>He is the author of more than 300 scientific articles, 22 inventions-patent, and 5 monographs and textbooks. He is the head of numerous national and international grant projects. In 2015, he was awarded the "Progress" medal. He is recognized as a distinguished telecommunications specialist and has received ITU-T certifications. He is a full member of the Azerbaijan Engineering Academy and a corresponding member of the International Engineering Academy.</p><p>Since 2016, Mehman Hasanov has been serving as the Head of the Department of Radio Engineering and Telecommunications at Azerbaijan Technical University. In 2023, he was awarded the academic title of Professor.</p>',
    '["Free-space optical communication technologies", "Management of nanosatellite networks in Low Earth Orbit (LEO)", "LiFi technologies", "Next-generation mobile communication technologies"]'::jsonb,
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
    SELECT id, '11:00–13:00', NOW()
    FROM cafedra_directors WHERE cafedra_code = 'radio_engineering_telecommunications'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi, Çərşənbə, Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday, Wednesday, Friday',       NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1977', '1982', NOW() FROM cafedra_directors WHERE cafedra_code = 'radio_engineering_telecommunications'
UNION ALL
SELECT id, '1986', '1990', NOW() FROM cafedra_directors WHERE cafedra_code = 'radio_engineering_telecommunications'
UNION ALL
SELECT id, '2008', '2022', NOW() FROM cafedra_directors WHERE cafedra_code = 'radio_engineering_telecommunications';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'radio_engineering_telecommunications')
    ORDER BY id DESC
    LIMIT 3
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bakalavr və Magistr (Avtomatik Elektrik Rabitəsi Mühəndisliyi)', 'Azərbaycan Texniki Universiteti'),
    (2, 'Texnika elmləri namizədi (Hesablama texnikasının elementləri və cihazları)', 'Azərbaycan Texniki Universiteti'),
    (3, 'Texnika elmləri doktoru (Telekommunikasiya texnologiyaları)', 'Azərbaycan Texniki Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Bachelor''s and Master''s (Automatic Electrical Communications Engineering)', 'Azerbaijan Technical University'),
    (2, 'Candidate of Technical Sciences (Elements and Devices of Computing Technology)', 'Azerbaijan Technical University'),
    (3, 'Doctor of Technical Sciences (Telecommunications Technologies)', 'Azerbaijan Technical University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers (professors, associate professors, senior lecturers, lecturers, assistants, clerk) ──
DELETE FROM cafedra_workers WHERE cafedra_code = 'radio_engineering_telecommunications';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Professors (t.e.d.)
    ('radio_engineering_telecommunications', 'İsa',       'Məmmədov',      'Rəhman oğlu',        'isa.memmedov@aztu.edu.az',          '+994 70-353-45-87',  NOW()),  -- 1
    ('radio_engineering_telecommunications', 'Tofiq',     'Mansurov',      'Məhəmməd oğlu',      'tofiq.mansurov@aztu.edu.az',        '+994 50-470-22-77',  NOW()),  -- 2
    -- Associate Professors (dosentlər)
    ('radio_engineering_telecommunications', 'Əli',       'Tağıyev',       'Daşdəmir oğlu',      'ali.tagiyev@aztu.edu.az',           '+994 55-202-41-56',  NOW()),  -- 3
    ('radio_engineering_telecommunications', 'Əlixan',    'Məmmədov',      'Heydər oğlu',         'elixan.memmedov@aztu.edu.az',       '+994 50-212-27-60',  NOW()),  -- 4
    ('radio_engineering_telecommunications', 'İradə',     'Dəvrişova',     'Naməz qızı',          'irade.devrishova@aztu.edu.az',      '+994 50-304-91-63',  NOW()),  -- 5
    ('radio_engineering_telecommunications', 'Namiq',     'Şükürov',       'Malik oğlu',          'namik.shukurov@aztu.edu.az',        '+994 50-342-03-61',  NOW()),  -- 6
    ('radio_engineering_telecommunications', 'Simnarə',   'Əhmədova',      'Rəffaq qızı',         'simnare.ehmedova@aztu.edu.az',      '+994 50-380-39-30',  NOW()),  -- 7
    ('radio_engineering_telecommunications', 'Elmar',     'Hünbətaliyev',  'Zülfüqar oğlu',       'elmar.hunbeteliyev@aztu.edu.az',    '+994 50-553-66-01',  NOW()),  -- 8
    ('radio_engineering_telecommunications', 'İltimas',   'Məmmədov',      'Əhməd oğlu',          'iltimas.memmedov@aztu.edu.az',      '+994 50',            NOW()),  -- 9
    ('radio_engineering_telecommunications', 'Aqil',      'Mövsümov',      'Adil oğlu',           'agil.movsumov@aztu.edu.az',         '+994 50-221-02-96',  NOW()),  -- 10
    ('radio_engineering_telecommunications', 'Murad',     'Cahangrov',     'Muxtar oğlu',         'murad.cahangirov@aztu.edu.az',      '+994 50-689-07-86',  NOW()),  -- 11
    -- Senior Lecturers (Baş müəllimlər)
    ('radio_engineering_telecommunications', 'Rəşid',     'Abdullayev',    'Şaban oğlu',          'reshid.abdullayev@aztu.edu.az',     '+994 50-386-16-35',  NOW()),  -- 12
    ('radio_engineering_telecommunications', 'Şadiyə',    'Sultanova',     'Aqşin qızı',          'shadiye.sultanova@aztu.edu.az',     '+994 70-214-74-34',  NOW()),  -- 13
    ('radio_engineering_telecommunications', 'Elnarə',    'Cəfərova',      'Mirtağı qızı',        'elnare.ceferova@aztu.edu.az',       '+994 55-342-27-10',  NOW()),  -- 14
    ('radio_engineering_telecommunications', 'Baloğlan',  'Nəcəfov',       'Kamil oğlu',          'baloglan.necefov@aztu.edu.az',      '+994 55-286-77-73',  NOW()),  -- 15
    -- Lecturers (Müəllimlər)
    ('radio_engineering_telecommunications', 'Qızılgül',  'İsrafilova',    'Azir qızı',           'qizilgul.israfilova@aztu.edu.az',   '+994 55-819-21-24',  NOW()),  -- 16
    ('radio_engineering_telecommunications', 'Babək',     'Süleymanov',    'Fərhad oğlu',         'babek.suleymanov@aztu.edu.az',      '+994 50-210-00-92',  NOW()),  -- 17
    -- Clerk (Katibə)
    ('radio_engineering_telecommunications', 'İradə',     'Rzayeva',       'Yusif qızı',          'irade.rzayeva@aztu.edu.az',         '+994 50-649-17-40',  NOW()),  -- 18
    -- Assistants to Lecturer (Müəllim assistentləri)
    ('radio_engineering_telecommunications', 'Surə',      'Ağayeva',       'Panah qızı',          'sure.agayeva@aztu.edu.az',          '+994 55-978-89-24',  NOW()),  -- 19
    ('radio_engineering_telecommunications', 'Samirə',    'Əmirova',       'Vaqif qızı',          'samira.amirova@aztu.edu.az',        '+994 55-841-48-49',  NOW())   -- 20
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Radiotexnika və Telekommunikasiyalar kafedrası, professor',         'Professor', 't.e.d.'),
    (2,  'Radiotexnika və Telekommunikasiyalar kafedrası, professor',         'Professor', 't.e.d.'),
    (3,  'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    't.e.n.'),
    (4,  'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    't.e.n.'),
    (5,  'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    't.e.n.'),
    (6,  'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    't.e.n.'),
    (7,  'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    't.e.n.'),
    (8,  'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    't.e.n.'),
    (9,  'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    'təhsil elmləri doktoru'),
    (10, 'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    't.e.n.'),
    (11, 'Radiotexnika və Telekommunikasiyalar kafedrası, dosent',            'Dosent',    't.e.n.'),
    (12, 'Radiotexnika və Telekommunikasiyalar kafedrası, baş müəllim',       NULL,        NULL),
    (13, 'Radiotexnika və Telekommunikasiyalar kafedrası, baş müəllim',       NULL,        NULL),
    (14, 'Radiotexnika və Telekommunikasiyalar kafedrası, baş müəllim',       NULL,        NULL),
    (15, 'Radiotexnika və Telekommunikasiyalar kafedrası, baş müəllim',       NULL,        NULL),
    (16, 'Radiotexnika və Telekommunikasiyalar kafedrası, müəllim',           NULL,        NULL),
    (17, 'Radiotexnika və Telekommunikasiyalar kafedrası, müəllim',           NULL,        NULL),
    (18, 'Radiotexnika və Telekommunikasiyalar kafedrası, katibə',            NULL,        NULL),
    (19, 'Radiotexnika və Telekommunikasiyalar kafedrası, müəllim assistenti', NULL,        NULL),
    (20, 'Radiotexnika və Telekommunikasiyalar kafedrası, müəllim assistenti', NULL,        NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Department of Radio Engineering and Telecommunications, Professor',            'Professor',           'D.Tech.Sci.'),
    (2,  'Department of Radio Engineering and Telecommunications, Professor',            'Professor',           'D.Tech.Sci.'),
    (3,  'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'PhD'),
    (4,  'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'PhD'),
    (5,  'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'PhD'),
    (6,  'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'PhD'),
    (7,  'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'PhD'),
    (8,  'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'PhD'),
    (9,  'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'Doctor of Educational Sciences'),
    (10, 'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'PhD'),
    (11, 'Department of Radio Engineering and Telecommunications, Associate Professor',  'Associate Professor', 'PhD'),
    (12, 'Department of Radio Engineering and Telecommunications, Senior Lecturer',       NULL,                  NULL),
    (13, 'Department of Radio Engineering and Telecommunications, Senior Lecturer',       NULL,                  NULL),
    (14, 'Department of Radio Engineering and Telecommunications, Senior Lecturer',       NULL,                  NULL),
    (15, 'Department of Radio Engineering and Telecommunications, Senior Lecturer',       NULL,                  NULL),
    (16, 'Department of Radio Engineering and Telecommunications, Lecturer',              NULL,                  NULL),
    (17, 'Department of Radio Engineering and Telecommunications, Lecturer',              NULL,                  NULL),
    (18, 'Department of Radio Engineering and Telecommunications, Clerk',                 NULL,                  NULL),
    (19, 'Department of Radio Engineering and Telecommunications, Assistant to Lecturer', NULL,                  NULL),
    (20, 'Department of Radio Engineering and Telecommunications, Assistant to Lecturer', NULL,                  NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
