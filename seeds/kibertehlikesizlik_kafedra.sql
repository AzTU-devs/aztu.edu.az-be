-- ============================================================
-- Kibertəhlükəsizlik kafedrası — Full DB Import
-- faculty_code: 'KIBER'  ← change if your convention differs
-- NOTE: faculty_workers has no phone column; worker phones
--       from the source data are not importable here.
-- ============================================================

-- ── 1. Faculty base record ──────────────────────────────────
INSERT INTO faculties (faculty_code, created_at, updated_at)
VALUES ('KIBER', NOW(), NOW());


-- ── 2. Faculty translations ─────────────────────────────────
INSERT INTO faculties_tr (faculty_code, lang_code, faculty_name, about_text, created_at, updated_at)
VALUES
(
  'KIBER', 'az',
  'Kibertəhlükəsizlik kafedrası',
  '<p>Kibertəhlükəsizlik kafedrası Azərbaycan Texniki Universiteti (AzTU) Elmi Şurasının 12 iyul 2022-ci il tarixli qərarı ilə yaradılmışdır. Kafedra regionda kibertəhlükəsizlik və informasiya təhlükəsizliyi sahəsində təhsil və elmi-tədqiqat üzrə qabaqcıl mərkəzə çevrilməyi qarşısına məqsəd qoymuşdur.</p><p>Kafedranın missiyası innovativ və kreativ düşüncəyə malik, analitik bacarıqları inkişaf etmiş, müasir texnologiyalar əsasında effektiv həllər təqdim edə bilən yüksək ixtisaslı mütəxəssislər hazırlamaqdır. Bu mütəxəssislər informasiya təhlükəsizliyi sahəsində yeni yanaşmaların formalaşdırılması və cəmiyyətin rəqəmsal təhlükəsizliyinin təmin edirlər.</p><p>Kafedra təhsil, elmi-tədqiqat və sənaye əməkdaşlığının vəhdət təşkil etdiyi müasir və inklüziv akademik mühitin formalaşdırılmasına çalışır. Böyük verilənlərin analizi, süni intellekt tətbiqləri, kibertəhlükəsizlik, IoT və smart sistemlərin təhlükəsizliyi, eləcə də texnoloji sahibkarlıq istiqamətində həyata keçirilən təşəbbüslər vasitəsilə nəzəri biliklərin praktik tətbiqlərə çevrilməsi təmin olunur.</p>',
  NOW(), NOW()
),
(
  'KIBER', 'en',
  'Department of Cybersecurity',
  '<p>The Department of Cybersecurity was established by the decision of the Academic Council of Azerbaijan Technical University (AzTU) on July 12, 2022. The department aims to become a leading center in the region for education and scientific research in the field of cybersecurity and information security.</p><p>The mission of the department is to train highly qualified specialists with innovative and creative thinking, well-developed analytical skills, who can provide effective solutions based on modern technologies. These specialists contribute to forming new approaches in the field of information security and ensuring the digital security of society.</p><p>The department strives to create a modern and inclusive academic environment that integrates education, scientific research, and industry collaboration. Through initiatives in big data analytics, artificial intelligence applications, cybersecurity, IoT and smart systems security, and technological entrepreneurship, theoretical knowledge is transformed into practical applications.</p>',
  NOW(), NOW()
);


-- ── 3. Director + working hours + educations ────────────────
WITH dir AS (
  INSERT INTO faculty_directors (
    faculty_code, first_name, last_name, father_name,
    scientific_degree, scientific_title,
    email, phone, room_number, bio,
    profile_image, created_at, updated_at
  )
  VALUES (
    'KIBER',
    'Yadigar', 'İmamverdiyev', 'Nəsib oğlu',
    'Texnika elmləri doktoru', 'Dosent',
    'yadigar.imamverdiyev@aztu.edu.az',
    '+994125390824',
    'V korpus, K406-cı otaq',
    '<p>İmamverdiyev Yadigar Nəsib oğlu — texnika elmləri doktoru, dosent, informasiya təhlükəsizliyi və kriptoqrafiya sahəsi üzrə ixtisaslaşmış alimdir. O, informasiya təhlükəsizliyi və kibertəhlükəsizlik istiqamətində elmi və pedaqoji fəaliyyət göstərir.</p><p>Onun elmi tədqiqatlarının əsas istiqamətlərinə informasiya təhlükəsizliyi, tətbiqi kriptoqrafiya və kriptoanaliz, süni intellekt metodları və biometrik texnologiyalar daxildir. Bu sahələr üzrə apardığı tədqiqatların nəticələri nüfuzlu elmi jurnallarda dərc olunmuş və informasiya təhlükəsizliyi sahəsinin inkişafına mühüm töhfə vermişdir.</p><p>İmamverdiyev Y.N. pedaqoji fəaliyyətində müasir kibertəhlükəsizlik yanaşmalarını tətbiq edərək tələbələrin analitik və tənqidi düşünmə bacarıqlarının inkişafına, eləcə də gənc mütəxəssislərin hazırlanması və elmi-tədqiqat fəaliyyətinə cəlb olunmasına xüsusi önəm verir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin Kibertəhlükəsizlik kafedrasının müdiri vəzifəsində çalışır. O, 200-dən çox elmi məqalənin və 8 kitabın müəllifidir, həmçinin ölkədə ilk CERT komandasının yaradılmasında və biometrik identifikasiya sistemlərinin tətbiqi üzrə dövlət layihələrində aktiv iştirak etmişdir.</p>',
    NULL,
    NOW(), NOW()
  )
  RETURNING id
),
wh AS (
  INSERT INTO faculty_director_working_hours (director_id, day, time_range, created_at, updated_at)
  SELECT id, 'Bazar ertəsi', '14:00-17:00', NOW(), NOW() FROM dir
  UNION ALL
  SELECT id, 'Çərşənbə',    '14:00-17:00', NOW(), NOW() FROM dir
  RETURNING id
),
ed AS (
  INSERT INTO faculty_director_educations (director_id, degree, university, start_year, end_year, created_at, updated_at)
  SELECT id, 'Bakalavr + Magistr',    'Azərbaycan Dövlət Neft və Sənaye Universiteti', '1982', '1989', NOW(), NOW() FROM dir
  UNION ALL
  SELECT id, 'Elmlər namizədi (PhD)', 'AMEA İnformasiya Texnologiyaları İnstitutu',    '2003', '2006', NOW(), NOW() FROM dir
  UNION ALL
  SELECT id, 'Elmlər doktoru (DSc)',  'AMEA İnformasiya Texnologiyaları İnstitutu',    '2008', '2012', NOW(), NOW() FROM dir
  RETURNING id
)
SELECT 1;


-- ── 4. Directions of action ─────────────────────────────────
WITH
d1 AS (
  INSERT INTO faculty_directions_of_action (faculty_code, display_order, created_at, updated_at)
  VALUES ('KIBER', 1, NOW(), NOW()) RETURNING id
),
d2 AS (
  INSERT INTO faculty_directions_of_action (faculty_code, display_order, created_at, updated_at)
  VALUES ('KIBER', 2, NOW(), NOW()) RETURNING id
),
d3 AS (
  INSERT INTO faculty_directions_of_action (faculty_code, display_order, created_at, updated_at)
  VALUES ('KIBER', 3, NOW(), NOW()) RETURNING id
),
d4 AS (
  INSERT INTO faculty_directions_of_action (faculty_code, display_order, created_at, updated_at)
  VALUES ('KIBER', 4, NOW(), NOW()) RETURNING id
),
t1az AS (
  INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at, updated_at)
  SELECT id, 'az', 'İnformasiya təhlükəsizliyi üzrə müasir və beynəlxalq standartlara uyğun tədris proqramlarının hazırlanması və tətbiqi', NULL, NOW(), NOW() FROM d1
  RETURNING id
),
t1en AS (
  INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at, updated_at)
  SELECT id, 'en', 'Development and implementation of modern curricula aligned with international information security standards', NULL, NOW(), NOW() FROM d1
  RETURNING id
),
t2az AS (
  INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at, updated_at)
  SELECT id, 'az', 'Sənaye və dövlət qurumları ilə əməkdaşlıq çərçivəsində praktiki bacarıqlara malik mütəxəssislərin hazırlanması', NULL, NOW(), NOW() FROM d2
  RETURNING id
),
t2en AS (
  INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at, updated_at)
  SELECT id, 'en', 'Training of specialists with practical skills through collaboration with industry and government institutions', NULL, NOW(), NOW() FROM d2
  RETURNING id
),
t3az AS (
  INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at, updated_at)
  SELECT id, 'az', 'Kritik informasiya infrastrukturunun qorunması üçün metod və texnologiyaların inkişaf etdirilməsi', NULL, NOW(), NOW() FROM d3
  RETURNING id
),
t3en AS (
  INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at, updated_at)
  SELECT id, 'en', 'Development of methods and technologies for the protection of critical information infrastructure', NULL, NOW(), NOW() FROM d3
  RETURNING id
),
t4az AS (
  INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at, updated_at)
  SELECT id, 'az', 'Müxtəlif sektorlar üzrə informasiya təhlükəsizliyinin təmin edilməsi istiqamətində elmi tədqiqatların aparılması və innovativ həllərin işlənməsi', NULL, NOW(), NOW() FROM d4
  RETURNING id
),
t4en AS (
  INSERT INTO faculty_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at, updated_at)
  SELECT id, 'en', 'Conducting scientific research and developing innovative solutions for information security across various sectors', NULL, NOW(), NOW() FROM d4
  RETURNING id
)
SELECT 1;


-- ── 5. Workers ───────────────────────────────────────────────
-- Note: faculty_workers has no phone column.
-- scientific_name = title (Dosent), scientific_degree = abbreviation (t.f.d., etc.)
-- "Yoxdur" → both columns NULL

INSERT INTO faculty_workers
  (faculty_code, first_name, last_name, father_name, duty, scientific_name, scientific_degree, email, created_at, updated_at)
VALUES
  ('KIBER', 'Fərid',   'Qasımlı',       'Fikrət oğlu',  'Kibertəhlükəsizlik kafedrasının baş müəllimi', NULL,     NULL,       'farid.gasimli@aztu.edu.az',       NOW(), NOW()),
  ('KIBER', 'Aynur',   'Məhərrəmova',   'Natiq',        'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'aynur.meherremova@aztu.edu.az',   NOW(), NOW()),
  ('KIBER', 'Nərmin',  'Məmmədova',     'Ləyaqət',      'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'narmin.mammadova@aztu.edu.az',    NOW(), NOW()),
  ('KIBER', 'Samirə',  'Qəhrəmanova',   'Həsən',        'Kibertəhlükəsizlik kafedrasının dosenti',      'Dosent', 't.f.d.',   'samira.qahramanova@aztu.edu.az',  NOW(), NOW()),
  ('KIBER', 'Arzu',    'Babayeva',      'Ələm',         'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'arzu.babayeva@aztu.edu.az',       NOW(), NOW()),
  ('KIBER', 'Əzimə',   'Hüseynova',     'Şahin',        'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'ezime.huseynova@aztu.edu.az',     NOW(), NOW()),
  ('KIBER', 'İlahə',   'Qəhrəmanova',   'Həsən',        'Kibertəhlükəsizlik kafedrasının baş müəllimi', NULL,     NULL,       'ilaha.qahramanova@aztu.edu.az',   NOW(), NOW()),
  ('KIBER', 'Aytəkin', 'İbrahimova',    'Bəybala',      'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'aytekin.ibrahimova@aztu.edu.az',  NOW(), NOW()),
  ('KIBER', 'Qahirə',  'Əliyeva',       'Tehran',       'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'qahire.vahidli@aztu.edu.az',      NOW(), NOW()),
  ('KIBER', 'Pərişan', 'Quluzadə',      'Ceyhun',       'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'perishan.guluzade@aztu.edu.az',   NOW(), NOW()),
  ('KIBER', 'Cavad',   'Nəcəfli',       'Vaqif',        'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'cavad.necefli@aztu.edu.az',       NOW(), NOW()),
  ('KIBER', 'Aydan',   'Arifli',        'Rauf',         'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'aydan.arifli@aztu.edu.az',        NOW(), NOW()),
  ('KIBER', 'Leyla',   'Orucova',       'Sənan',        'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'leyla.orucova@aztu.edu.az',       NOW(), NOW()),
  ('KIBER', 'Xumar',   'Şirəliyeva',    'Rəşad',        'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'khumar.shiraliyeva@aztu.edu.az',  NOW(), NOW()),
  ('KIBER', 'İnci',    'Abdullayeva',   'Tağı',         'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'inci.abdullayeva@aztu.edu.az',    NOW(), NOW()),
  ('KIBER', 'Azad',    'Fərzəliyev',    'Novruz',       'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'azad.farzaliyev@aztu.edu.az',     NOW(), NOW()),
  ('KIBER', 'Ramidə',  'Səfərli',       'Elşən',        'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'ramida.safarli@aztu.edu.az',      NOW(), NOW()),
  ('KIBER', 'Adilə',   'Kərimova',      'Yadigar',      'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'adila.karimova@aztu.edu.az',      NOW(), NOW()),
  ('KIBER', 'Rahib',   'Ağababayev',    'Rəsul',        'Kibertəhlükəsizlik kafedrasının baş müəllimi', NULL,     NULL,       'rahib.agababayev@aztu.edu.az',    NOW(), NOW()),
  ('KIBER', 'Natiq',   'Quliyev',       'Əliabbas',     'Kibertəhlükəsizlik kafedrasının dosenti',      'Dosent', 'f.r.e.n.', 'natiq.quliyev@aztu.edu.az',       NOW(), NOW()),
  ('KIBER', 'Rəhilə',  'Sadıqova',      'Hidayət',      'Kibertəhlükəsizlik kafedrasının dosenti',      'Dosent', 'r.ü.f.d.', 'rahila.sadygova@aztu.edu.az',     NOW(), NOW()),
  ('KIBER', 'Aydın',   'Hüseynov',      'Fridun',       'Kibertəhlükəsizlik kafedrasının dosenti',      'Dosent', 't.e.n.',   'aydin.huseynov@aztu.edu.az',      NOW(), NOW()),
  ('KIBER', 'Əli',     'Əliyev',        'Əbülfəz',      'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'ali.aliyev@aztu.edu.az',          NOW(), NOW()),
  ('KIBER', 'Nigar',   'Məmmədzadə',    'Ərəstun',      'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'nigar.mammadzade@aztu.edu.az',    NOW(), NOW()),
  ('KIBER', 'Elşən',   'İbayev',        'Akif',         'Kibertəhlükəsizlik kafedrasının dosenti',      'Dosent', 'r.ü.f.d.', 'elshen.ibayev@aztu.edu.az',       NOW(), NOW()),
  ('KIBER', 'Əminə',   'Abbasova',      'Elşad',        'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'amina.abbasova@aztu.edu.az',      NOW(), NOW()),
  ('KIBER', 'Samirə',  'Həsənova',      'Əfrasiyab',    'Kibertəhlükəsizlik kafedrasının assistenti',   NULL,     NULL,       'samirahasanova75@gmail.com',      NOW(), NOW()),
  ('KIBER', 'Təbriz',  'Cəfərov',       'Ramal',        'Kibertəhlükəsizlik kafedrasının dosenti',      'Dosent', 'h.ü.f.d.', 'tabriz.cafarov@aztu.edu.az',      NOW(), NOW());
