-- =============================================================
-- MENU HEADER SEED DATA
-- Structure: Sections > Items (subheader/link) > Sub-items
-- Languages: 'en' (English), 'az' (Azerbaijani)
-- =============================================================

-- =============================================================
-- 0. TRUNCATE ALL MENU TABLES (order respects FK constraints)
-- =============================================================
TRUNCATE TABLE
    menu_social_links,
    menu_contact_addresses,
    menu_contact_phones,
    menu_contacts,
    menu_footer_quick_icon_translations,
    menu_footer_quick_icons,
    menu_footer_link_translations,
    menu_footer_links,
    menu_footer_column_translations,
    menu_footer_columns,
    menu_footer_partner_logos,
    menu_quick_section_item_translations,
    menu_quick_section_items,
    menu_quick_section_translations,
    menu_quick_sections,
    menu_quick_left_item_translations,
    menu_quick_left_items,
    menu_header_sub_item_translations,
    menu_header_sub_items,
    menu_header_item_translations,
    menu_header_items,
    menu_header_section_translations,
    menu_header_sections
RESTART IDENTITY CASCADE;

-- =============================================================
-- 1. SECTIONS (top-level nav items)
-- =============================================================
INSERT INTO menu_header_sections (id, section_key, image_url, direct_url, display_order, is_active) VALUES
(1,  'about',          '/images/menu/about.jpg',          NULL,             1,  true),
(2,  'academics',      '/images/menu/academics.jpg',      NULL,             2,  true),
(3,  'administration', '/images/menu/administration.jpg', NULL,             3,  true),
(4,  'students',       '/images/menu/students.jpg',       NULL,             4,  true),
(5,  'research',       '/images/menu/research.jpg',       NULL,             5,  true),
(6,  'community',      '/images/menu/community.jpg',      NULL,             6,  true),
(7,  'sustainability', '/images/menu/sustainability.jpg', '/sustainability', 7,  true),
(8,  'contact',        '/images/menu/contact.jpg',        '/contact',       8,  true);

-- Section Translations
INSERT INTO menu_header_section_translations (section_id, lang_code, label, base_path) VALUES
-- About
(1, 'en', 'About',          '/about'),
(1, 'az', 'Haqqında',       '/about'),
-- Academics
(2, 'en', 'Academics',      '/academics'),
(2, 'az', 'Akademik',       '/academics'),
-- Administration
(3, 'en', 'Administration', '/administration'),
(3, 'az', 'İdarəetmə',      '/administration'),
-- Students
(4, 'en', 'Students',       '/students'),
(4, 'az', 'Tələbələr',      '/students'),
-- Research
(5, 'en', 'Research',       '/research'),
(5, 'az', 'Tədqiqat',       '/research'),
-- Community
(6, 'en', 'Community',      '/community'),
(6, 'az', 'İcma',           '/community'),
-- Sustainability
(7, 'en', 'Sustainability',  '/sustainability'),
(7, 'az', 'Dayanıqlılıq',   '/sustainability'),
-- Contact
(8, 'en', 'Contact',        '/contact'),
(8, 'az', 'Əlaqə',          '/contact');


-- =============================================================
-- 2. ITEMS (second-level — subheader groups within sections)
-- =============================================================

-- --- ABOUT (section 1) ---
INSERT INTO menu_header_items (id, section_id, item_type, slug, display_order, is_active) VALUES
(1,  1, 'subheader', NULL, 1, true),  -- Vision & Mission
(2,  1, 'subheader', NULL, 2, true),  -- Leadership & Governance
(3,  1, 'subheader', NULL, 3, true),  -- Partner University & Affiliated Institutes
(4,  1, 'subheader', NULL, 4, true);  -- Legal Documents

-- --- ACADEMICS (section 2) ---
INSERT INTO menu_header_items (id, section_id, item_type, slug, display_order, is_active) VALUES
(5,  2, 'subheader', NULL, 1, true),  -- Faculties
(6,  2, 'subheader', NULL, 2, true);  -- Higher Education Institutes

-- --- ADMINISTRATION (section 3) ---
INSERT INTO menu_header_items (id, section_id, item_type, slug, display_order, is_active) VALUES
(7,  3, 'subheader', NULL, 1, true),  -- Departments
(8,  3, 'subheader', NULL, 2, true);  -- Offices and Centers

-- --- STUDENTS (section 4) ---
INSERT INTO menu_header_items (id, section_id, item_type, slug, display_order, is_active) VALUES
(9,  4, 'subheader', NULL, 1, true),  -- Academic Calendar and Guidelines
(10, 4, 'subheader', NULL, 2, true),  -- Undergraduate
(11, 4, 'subheader', NULL, 3, true);  -- Postgraduates

-- --- RESEARCH (section 5) ---
INSERT INTO menu_header_items (id, section_id, item_type, slug, display_order, is_active) VALUES
(12, 5, 'subheader', NULL, 1, true),  -- Research Activities
(13, 5, 'subheader', NULL, 2, true),  -- Conferences & Events
(14, 5, 'subheader', NULL, 3, true),  -- Research Labs
(15, 5, 'subheader', NULL, 4, true),  -- Scientific Journals
(16, 5, 'subheader', NULL, 5, true),  -- Publications & Dissemination
(17, 5, 'subheader', NULL, 6, true);  -- Performance & Evaluation

-- --- COMMUNITY (section 6) ---
INSERT INTO menu_header_items (id, section_id, item_type, slug, display_order, is_active) VALUES
(18, 6, 'subheader', NULL, 1, true),  -- Campus Life
(19, 6, 'subheader', NULL, 2, true);  -- Union and Organizations


-- Item Translations
INSERT INTO menu_header_item_translations (item_id, lang_code, title) VALUES
-- About items
(1,  'en', 'Vision & Mission'),
(1,  'az', 'Vizyon və Missiya'),
(2,  'en', 'Leadership & Governance'),
(2,  'az', 'Rəhbərlik və İdarəetmə'),
(3,  'en', 'Partner University & Affiliated Institutes'),
(3,  'az', 'Tərəfdaş Universitet və Əlaqəli İnstitutlar'),
(4,  'en', 'Legal Documents'),
(4,  'az', 'Normativ Sənədlər'),
-- Academics items
(5,  'en', 'Faculties'),
(5,  'az', 'Fakültələr'),
(6,  'en', 'Higher Education Institutes'),
(6,  'az', 'Ali Təhsil İnstitutları'),
-- Administration items
(7,  'en', 'Departments'),
(7,  'az', 'Struktur Bölmələr'),
(8,  'en', 'Offices and Centers'),
(8,  'az', 'Ofis və Mərkəzlər'),
-- Students items
(9,  'en', 'Academic Calendar and Guidelines'),
(9,  'az', 'Tədris Təqvimi və Qaydalar'),
(10, 'en', 'Undergraduate'),
(10, 'az', 'Bakalavr'),
(11, 'en', 'Postgraduates'),
(11, 'az', 'Magistratura'),
-- Research items
(12, 'en', 'Research Activities'),
(12, 'az', 'Tədqiqat Fəaliyyəti'),
(13, 'en', 'Conferences & Events'),
(13, 'az', 'Konfranslar və Tədbirlər'),
(14, 'en', 'Research Labs'),
(14, 'az', 'Tədqiqat Laboratoriyaları'),
(15, 'en', 'Scientific Journals'),
(15, 'az', 'Elmi Jurnallar'),
(16, 'en', 'Publications & Dissemination'),
(16, 'az', 'Nəşrlər və Yayım'),
(17, 'en', 'Performance & Evaluation'),
(17, 'az', 'Performans və Qiymətləndirmə'),
-- Community items
(18, 'en', 'Campus Life'),
(18, 'az', 'Kampus Həyatı'),
(19, 'en', 'Union and Organizations'),
(19, 'az', 'İttifaq və Təşkilatlar');


-- =============================================================
-- 3. SUB-ITEMS (third-level links)
-- =============================================================

-- --- Vision & Mission (item 1) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(1,  1, '/about/vision',              1, true),
(2,  1, '/about/mission',             2, true),
(3,  1, '/about/history',             3, true),
(4,  1, '/about/anniversary-film',    4, true),
(5,  1, '/about/strategic-plan',      5, true);

-- --- Leadership & Governance (item 2) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(6,  2, '/about/rector',              1, true),
(7,  2, '/about/vice-rector',         2, true),
(8,  2, '/about/scientific-board',    3, true);

-- --- Partner University & Affiliated Institutes (item 3) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(9,  3, '/about/tau',                 1, true),
(10, 3, '/about/iti',                 2, true),
(11, 3, '/about/ics',                 3, true),
(12, 3, '/about/btc',                 4, true),
(13, 3, '/about/bscct',               5, true);

-- --- Legal Documents (item 4) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(14, 4, '/about/policies/general',        1, true),
(15, 4, '/about/policies/academic',       2, true),
(16, 4, '/about/policies/sustainability', 3, true),
(17, 4, '/about/policies/procedures',     4, true);

-- --- Faculties (item 5) - placeholder faculty slugs ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(18, 5, '/academics/faculties/1',     1, true),
(19, 5, '/academics/faculties/2',     2, true),
(20, 5, '/academics/faculties/3',     3, true),
(21, 5, '/academics/faculties/4',     4, true),
(22, 5, '/academics/faculties/5',     5, true),
(23, 5, '/academics/faculties/6',     6, true);

-- --- Higher Education Institutes (item 6) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(24, 6, '/academics/mba',             1, true),
(25, 6, '/academics/cdio',            2, true);

-- --- Departments (item 7) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(26, 7, '/administration/departments/education-affairs',          1,  true),
(27, 7, '/administration/departments/research-development',       2,  true),
(28, 7, '/administration/departments/international-affairs',      3,  true),
(29, 7, '/administration/departments/quality-assurance',          4,  true),
(30, 7, '/administration/departments/documents-applications',     5,  true),
(31, 7, '/administration/departments/human-resources',            6,  true),
(32, 7, '/administration/departments/finance-accountant',         7,  true),
(33, 7, '/administration/departments/information-technologies',   8,  true),
(34, 7, '/administration/departments/communication',              9,  true),
(35, 7, '/administration/departments/mass-media',                 10, true),
(36, 7, '/administration/departments/analytical-analysis',        11, true),
(37, 7, '/administration/departments/procurement',                12, true);

-- --- Offices and Centers (item 8) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(38, 8, '/administration/offices/career-employability',   1, true),
(39, 8, '/administration/offices/lifelong-learning',      2, true),
(40, 8, '/administration/offices/tto',                    3, true),
(41, 8, '/administration/offices/nabran-resort',          4, true),
(42, 8, '/administration/offices/sabah-centre',           5, true),
(43, 8, '/administration/offices/library',                6, true);

-- --- Academic Calendar and Guidelines (item 9) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(44, 9, '/students/calendar/2026-2027',       1, true),
(45, 9, '/students/calendar/2025-2026',       2, true),
(46, 9, '/students/guidelines/examinations',  3, true),
(47, 9, '/students/guidelines/credit-system', 4, true),
(48, 9, '/students/guidelines/lms',           5, true);

-- --- Undergraduate (item 10) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(49, 10, '/students/undergraduate/specialties',       1, true),
(50, 10, '/students/undergraduate/curriculum',        2, true),
(51, 10, '/students/undergraduate/learning-outcomes', 3, true),
(52, 10, '/students/undergraduate/exchange-programs', 4, true),
(53, 10, '/students/undergraduate/tuition-fees',      5, true);

-- --- Postgraduates (item 11) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(54, 11, '/students/postgraduate/specialties',              1, true),
(55, 11, '/students/postgraduate/curriculum',               2, true),
(56, 11, '/students/postgraduate/cdio',                     3, true),
(57, 11, '/students/postgraduate/international-students',   4, true),
(58, 11, '/students/postgraduate/exchange-programs',        5, true);

-- --- Research Activities (item 12) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(59, 12, '/research/activities/priorities',             1, true),
(60, 12, '/research/activities/institutes',             2, true),
(61, 12, '/research/activities/interdisciplinary',      3, true),
(62, 12, '/research/activities/intellectual-property',  4, true),
(63, 12, '/research/activities/projects',               5, true);

-- --- Conferences & Events (item 13) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(64, 13, '/research/conferences/local',         1, true),
(65, 13, '/research/conferences/international', 2, true),
(66, 13, '/research/conferences/seminars',      3, true);

-- --- Research Labs (item 14) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(67, 14, '/research/labs/1',  1, true);

-- --- Scientific Journals (item 15) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(68, 15, '/research/journals/machine-science',              1, true),
(69, 15, '/research/journals/energy-sustainability',        2, true),
(70, 15, '/research/journals/elmi-eserler',                 3, true),
(71, 15, '/research/journals/advance-material-processing',  4, true);

-- --- Publications & Dissemination (item 16) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(72, 16, '/research/publications/open-access',      1, true),
(73, 16, '/research/publications/plagiarism-ethics', 2, true),
(74, 16, '/research/publications/ethics-compliance', 3, true),
(75, 16, '/research/publications/annual-reports',   4, true);

-- --- Performance & Evaluation (item 17) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(76, 17, '/research/performance/incentive-mechanism',  1, true),
(77, 17, '/research/performance/researcher-platforms', 2, true),
(78, 17, '/research/performance/internal-grants',      3, true);

-- --- Campus Life (item 18) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(79, 18, '/community/campus/student-life',      1, true),
(80, 18, '/community/campus/clubs',             2, true),
(81, 18, '/community/campus/sport',             3, true),
(82, 18, '/community/campus/cultural-events',   4, true),
(83, 18, '/community/campus/polyclinic',        5, true);

-- --- Union and Organizations (item 19) ---
INSERT INTO menu_header_sub_items (id, item_id, slug, display_order, is_active) VALUES
(84, 19, '/community/organizations/trade-union',         1, true),
(85, 19, '/community/organizations/student-trade-union', 2, true),
(86, 19, '/community/organizations/student-youth',       3, true);


-- =============================================================
-- 4. SUB-ITEM TRANSLATIONS
-- =============================================================

INSERT INTO menu_header_sub_item_translations (sub_item_id, lang_code, title) VALUES
-- Vision & Mission sub-items
(1,  'en', 'Vision'),
(1,  'az', 'Vizyon'),
(2,  'en', 'Mission'),
(2,  'az', 'Missiya'),
(3,  'en', 'History of AzTU'),
(3,  'az', 'AzTU-nun Tarixi'),
(4,  'en', '75th Anniversary Film'),
(4,  'az', '75 illik Yubiley Filmi'),
(5,  'en', 'Strategic Plan'),
(5,  'az', 'Strateji Plan'),

-- Leadership & Governance sub-items
(6,  'en', 'Rector'),
(6,  'az', 'Rektor'),
(7,  'en', 'Vice-Rector'),
(7,  'az', 'Prorektor'),
(8,  'en', 'Scientific Board'),
(8,  'az', 'Elmi Şura'),

-- Partner University & Affiliated Institutes sub-items
(9,  'en', 'Turkish-Azerbaijan University (TAU)'),
(9,  'az', 'Türk-Azərbaycan Universiteti (TAU)'),
(10, 'en', 'Institute of Information Technology'),
(10, 'az', 'İnformasiya Texnologiyaları İnstitutu'),
(11, 'en', 'Institute of Control Systems'),
(11, 'az', 'İdarəetmə Sistemləri İnstitutu'),
(12, 'en', 'Baku Technical Colleges'),
(12, 'az', 'Bakı Texniki Kollecləri'),
(13, 'en', 'Baku State Colleges of Communication and Transport'),
(13, 'az', 'Bakı Rabitə və Nəqliyyat Dövlət Kollecləri'),

-- Legal Documents sub-items
(14, 'en', 'General Policies'),
(14, 'az', 'Ümumi Siyasətlər'),
(15, 'en', 'Academic Policies'),
(15, 'az', 'Akademik Siyasətlər'),
(16, 'en', 'Sustainability Policies'),
(16, 'az', 'Davamlılıq Siyasətləri'),
(17, 'en', 'Procedure and Guidelines'),
(17, 'az', 'Prosedur və Təlimatlar'),

-- Faculties sub-items (placeholder — replace with real faculty names)
(18, 'en', 'Faculty 1'),
(18, 'az', 'Fakültə 1'),
(19, 'en', 'Faculty 2'),
(19, 'az', 'Fakültə 2'),
(20, 'en', 'Faculty 3'),
(20, 'az', 'Fakültə 3'),
(21, 'en', 'Faculty 4'),
(21, 'az', 'Fakültə 4'),
(22, 'en', 'Faculty 5'),
(22, 'az', 'Fakültə 5'),
(23, 'en', 'Faculty 6'),
(23, 'az', 'Fakültə 6'),

-- Higher Education Institutes sub-items
(24, 'en', 'MBA'),
(24, 'az', 'MBA'),
(25, 'en', 'CDIO'),
(25, 'az', 'CDIO'),

-- Departments sub-items
(26, 'en', 'Education Affairs'),
(26, 'az', 'Tədris İşləri'),
(27, 'en', 'Research, Development and Reputation'),
(27, 'az', 'Tədqiqat, İnkişaf və Reputasiya'),
(28, 'en', 'International Affairs'),
(28, 'az', 'Beynəlxalq Əlaqələr'),
(29, 'en', 'Quality Assurance'),
(29, 'az', 'Keyfiyyətin Təminatı'),
(30, 'en', 'Documents and Applications'),
(30, 'az', 'Sənədlər və Müraciətlərlə İş'),
(31, 'en', 'Human Resources'),
(31, 'az', 'İnsan Resursları'),
(32, 'en', 'Finance and Accountant'),
(32, 'az', 'Maliyyə və Mühasibat'),
(33, 'en', 'Information Technologies'),
(33, 'az', 'İnformasiya Texnologiyaları'),
(34, 'en', 'Communication'),
(34, 'az', 'Kommunikasiya'),
(35, 'en', 'Mass Media'),
(35, 'az', 'Mətbuat Xidməti'),
(36, 'en', 'Analytical Analysis'),
(36, 'az', 'Analitik Təhlil'),
(37, 'en', 'Procurement'),
(37, 'az', 'Satınalma Təchizat'),

-- Offices and Centers sub-items
(38, 'en', 'Career and Employability Centre'),
(38, 'az', 'Karyera və Məşğulluq Mərkəzi'),
(39, 'en', 'LifeLong Learning'),
(39, 'az', 'Ömürboyu Təhsil'),
(40, 'en', 'Technology Transfer Office (TTO)'),
(40, 'az', 'Texnoloji Transfer Ofisi (TTO)'),
(41, 'en', 'Nabran Resort Centre'),
(41, 'az', 'Nabran İstirahət Mərkəzi'),
(42, 'en', 'Sabah Centre'),
(42, 'az', 'Sabah Mərkəzi'),
(43, 'en', 'Library Information Centre'),
(43, 'az', 'Kitabxana İnformasiya Mərkəzi'),

-- Academic Calendar and Guidelines sub-items
(44, 'en', '2026-2027 Academic Calendar'),
(44, 'az', '2026-2027 Tədris İli Təqvimi'),
(45, 'en', '2025-2026 Academic Calendar'),
(45, 'az', '2025-2026 Tədris İli Təqvimi'),
(46, 'en', 'Organization of Examinations at Azerbaijan Technical University'),
(46, 'az', 'Qiymətləndirmə və İmtahanın Təşkili Qaydaları'),
(47, 'en', 'Credit System at Bachelor''s and Master''s Levels'),
(47, 'az', 'Bakalavr və Magistratura Səviyyələrində Kredit Sistemi'),
(48, 'en', 'LMS Guidelines'),
(48, 'az', 'LMS Təlimatları'),

-- Undergraduate sub-items
(49, 'en', 'Specialties'),
(49, 'az', 'İxtisaslar'),
(50, 'en', 'Curriculum'),
(50, 'az', 'Tədris Proqramı'),
(51, 'en', 'Learning Outcomes'),
(51, 'az', 'Öyrənmə Nəticələri'),
(52, 'en', 'Exchange Programs'),
(52, 'az', 'Mübadilə Proqramları'),
(53, 'en', 'Tuition Fees'),
(53, 'az', 'Təhsil Haqqı'),

-- Postgraduates sub-items
(54, 'en', 'Specialties'),
(54, 'az', 'İxtisaslar'),
(55, 'en', 'Curriculum'),
(55, 'az', 'Tədris Proqramı'),
(56, 'en', 'CDIO'),
(56, 'az', 'CDIO'),
(57, 'en', 'International Students Unit'),
(57, 'az', 'Beynəlxalq Tələbələr Bölməsi'),
(58, 'en', 'Exchange Programs'),
(58, 'az', 'Mübadilə Proqramları'),

-- Research Activities sub-items
(59, 'en', 'Research Priorities'),
(59, 'az', 'Tədqiqat Prioritetləri'),
(60, 'en', 'Research Institutes'),
(60, 'az', 'Tədqiqat İnstitutları'),
(61, 'en', 'Interdisciplinary Research'),
(61, 'az', 'Çoxsahəli Tədqiqat'),
(62, 'en', 'Intellectual Property & Patents'),
(62, 'az', 'Əqli Mülkiyyət və Patentlər'),
(63, 'en', 'Research Projects'),
(63, 'az', 'Tədqiqat Layihələri'),

-- Conferences & Events sub-items
(64, 'en', 'Local Conferences'),
(64, 'az', 'Yerli Konfranslar'),
(65, 'en', 'International Conferences'),
(65, 'az', 'Beynəlxalq Konfranslar'),
(66, 'en', 'Seminars and Trainings'),
(66, 'az', 'Seminarlar və Təlimlər'),

-- Research Labs sub-items
(67, 'en', 'Research Lab 1'),
(67, 'az', 'Tədqiqat Laboratoriyası 1'),

-- Scientific Journals sub-items
(68, 'en', 'Machine Science'),
(68, 'az', 'Maşın Elmi'),
(69, 'en', 'Energy Sustainability: Risks and Decision Making'),
(69, 'az', 'Enerji Davamlılığı: Risklər və Qərarların Qəbul Edilməsi'),
(70, 'en', 'Scientific Works'),
(70, 'az', 'Elmi Əsərlər'),
(71, 'en', 'Journal of Advance Material Processing and Applications'),
(71, 'az', 'Qabaqcıl Material Emalı və Tətbiqləri Jurnalı'),

-- Publications & Dissemination sub-items
(72, 'en', 'Open Access Policy'),
(72, 'az', 'Açıq Giriş Siyasəti'),
(73, 'en', 'Plagiarism & Ethics'),
(73, 'az', 'Plagiat və Etika'),
(74, 'en', 'Ethics & Compliance Guidance'),
(74, 'az', 'Etika və Uyğunluq Təlimatları'),
(75, 'en', 'Annual Research Reports'),
(75, 'az', 'İllik Tədqiqat Hesabatları'),

-- Performance & Evaluation sub-items
(76, 'en', 'Incentive Mechanism'),
(76, 'az', 'Həvəsləndirmə Mexanizmi'),
(77, 'en', 'Researcher Platforms'),
(77, 'az', 'Tədqiqatçı Platformaları'),
(78, 'en', 'Internal Grant Programs'),
(78, 'az', 'Daxili Qrant Proqramları'),

-- Campus Life sub-items
(79, 'en', 'Student Life'),
(79, 'az', 'Tələbə Həyatı'),
(80, 'en', 'Clubs'),
(80, 'az', 'Klublar'),
(81, 'en', 'Sport'),
(81, 'az', 'İdman'),
(82, 'en', 'Cultural Events'),
(82, 'az', 'Mədəni Tədbirlər'),
(83, 'en', 'AzTU Polyclinic'),
(83, 'az', 'AzTU Poliklinikası'),

-- Union and Organizations sub-items
(84, 'en', 'Trade Union'),
(84, 'az', 'Həmkarlar İttifaqı'),
(85, 'en', 'Student Trade Union'),
(85, 'az', 'Tələbə Həmkarlar İttifaqı'),
(86, 'en', 'Student Youth Organization'),
(86, 'az', 'Tələbə Gənclər Təşkilatı');
