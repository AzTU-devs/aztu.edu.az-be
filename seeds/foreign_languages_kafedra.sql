-- ============================================================
-- "Xarici dillər" kafedrası — Full DB Import
-- cafedra_code: 'foreign_languages'
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
    'foreign_languages',
    7, 0, 0, 0, 0, 0, 0,
    '[4, 5, 10, 16, 17]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'foreign_languages',
    'az',
    'Xarici dillər kafedrası',
    '<p>"Xarici dillər" kafedrası 1950-ci ildə Azərbaycan Politexnik İnstitutu (indiki Azərbaycan Texniki Universiteti) yarandığı ilk gündən fəaliyyətə başlamışdır. Kafedrada 3 dil — ingilis, alman, fransız dilləri tədris olunmuşdur.</p><p>Xarici dillər kafedrasında tədris bakalavr üçün dörd dildə (ingilis, rus, alman, fransız) aparılır. Hər semestr üçün məşğələ dərsləri həftədə 5–6–7 saat olmaqla 18 həftə nəzərdə tutulur. İllik dərs yükü bütün fənlər üzrə (ingilis, rus, alman, fransız) 245 saatdır.</p><p>Tədris işçi proqramları (sillabuslar) hər bir fənnin (ingilis, alman, rus, fransız) proqramına uyğun hazırlanıb və onların elektron versiyası da kafedranın kitabxana bölməsində yerləşdirilib.</p><p><strong>Kafedranın fəaliyyət istiqaməti.</strong> Xarici dillər kafedrasında müasir dilin tədrisi sahəsində innovativ metodlar aşağıda qeyd olunan qaydada həyata keçirilir.</p><p><strong>Dinləmə və danışıq:</strong> Dinləmə çalışmaları məzmunun proqnozlaşdırılması, əsas mənanı və detalları anlama, köməkçi detalların və müəllif fərziyyələrinin müəyyənləşdirilməsinə əsaslanır. Tapşırıqlar tənqidi düşüncəni inkişaf etdirməyə, tələbələrin ixtisasları üçün vacib olan bacarıqlarını gücləndirməyə istiqamətlənir. Dərslər yaradıcı şifahi təcrübəni inkişaf etdirən strukturlaşdırılmış bir yanaşmaya malikdir. Tələbələr təqdimatlar, debatlar, simulyasiyalar, rol oyunları keçirərək danışıq qabiliyyətlərini inkişaf etdirmək üçün fürsət əldə edirlər. Dərslikdən əlavə müəllimlər hər bölməyə aid tematik olaraq uyğun olan "TED Talks", "YouTube"-un orijinal dinləmə materiallarından və əlavə mətnlərdən istifadə edirlər. Qiymətləndirmə tələbələrin cavablarının səs yazısına, tənqidi təhlilə və əsas arqumentlərin ümumiləşdirilməsinə əsaslanır.</p><p><strong>Oxu və yazı:</strong> Yazı tapşırıqları akademik yazı, həmyaşıdlar və müəllimlərlə qarşılıqlı münasibət yaratmaq və sənədləri redaktə etmək kimi vacib strategiyaları əhatə edir. Tələbələr auditoriyanı müəyyənləşdirməyi, güclü arqument inkişaf etdirməyi, tezis və mövzuya uyğun cümlələr qurmağı, düzgün paraqraflar yazmağı, paralel strukturlardan istifadə etməyi, konspekt və yaxşı strukturlaşdırılmış esse yazmağı, səbəb və nəticələri ümumiləşdirməyi öyrənirlər. Oxu tapşırıqları mənanı proqnozlaşdırmağa, oxuda əsas mənanı və detalları müəyyən etməyə, müəllif fərziyyələrini və xüsusi vurğulanmış mesajı aşkar etməyə əsaslanır.</p><p><strong>Lüğət və qrammatika:</strong> Lüğət və qrammatika ayrı-ayrılıqda tədris olunmaqdan çox kontekstlə inteqrasiya edilmişdir. Hər bölmənin sonunda tələbələr qrammatik cəhətdən düzgün, yüksək səviyyəli dil biliklərinin köməyi ilə mürəkkəb düşüncələrini ifadə edə bilirlər. Bütün qrammatika tematik olaraq əhatə olunur.</p>',
    NOW()
),
(
    'foreign_languages',
    'en',
    'Department of Foreign Languages',
    '<p>The Department of "Foreign Languages" began its activities in 1950 from the very first day of the establishment of the Azerbaijan Polytechnic Institute (now Azerbaijan Technical University). Three languages — English, German, and French — were taught in the department.</p><p>The Department of Foreign Languages provides education in four languages (English, Russian, German, French) for bachelors. Each semester includes 18 weeks of classes, 5–6–7 hours per week. The annual teaching load for all subjects (English, Russian, German, French) is 245 hours.</p><p>The teaching work programs (syllabuses) are prepared in accordance with the program of each subject (English, German, Russian, French) and their electronic version is also placed in the library section of the department.</p><p><strong>Direction of the department''s activities.</strong> Innovative methods in the field of modern language teaching are implemented in the Department of Foreign Languages as follows.</p><p><strong>Listening and Speaking:</strong> Listening exercises are based on predicting content, understanding the main meaning and details, and identifying supporting details and authorial assumptions. Tasks aim to develop critical thinking and strengthen skills important for students'' majors. Lessons follow a structured approach that develops creative oral practice through presentations, debates, simulations, and role-playing. In addition to the textbook, teachers use thematically relevant "TED Talks", "YouTube" original listening materials, and supplementary texts. Assessment is based on audio recordings of answers, critical analysis, and summarization of main arguments.</p><p><strong>Reading and Writing:</strong> Writing tasks cover important strategies such as academic writing, interaction with peers and teachers, and document editing. Students learn to identify their audience, develop strong arguments, construct thesis-relevant sentences, write proper paragraphs, use parallel structures, produce outlines and well-structured essays, and summarize causes and effects. Reading assignments focus on predicting meaning, identifying main ideas and details, and detecting authorial assumptions and emphasized messages.</p><p><strong>Vocabulary and Grammar:</strong> Vocabulary and grammar are integrated into context rather than taught in isolation. By the end of each unit, students can express complex ideas in grammatically correct, high-level language. All grammar is covered thematically.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'foreign_languages';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('foreign_languages', 1, NOW()),
    ('foreign_languages', 2, NOW()),
    ('foreign_languages', 3, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Dinləmə və danışıq',   'Dinləmə çalışmaları məzmunun proqnozlaşdırılması, əsas mənanın və detalların anlanılması, müəllif fərziyyələrinin müəyyənləşdirilməsinə əsaslanır. Təqdimatlar, debatlar, simulyasiyalar və rol oyunları vasitəsilə tələbələrin şifahi nitq bacarıqları inkişaf etdirilir; "TED Talks", "YouTube" kimi orijinal materiallar tətbiq olunur.'),
    (2, 'Oxu və yazı',           'Akademik yazı, həmyaşıdlar və müəllimlərlə qarşılıqlı münasibət qurma, sənədlərin redaktəsi kimi strategiyalar tədris olunur. Tələbələr güclü arqument qurmağı, tezisyönümlü cümlə və paraqraflar yazmağı, strukturlaşdırılmış esse və konspekt hazırlamağı, oxuda əsas məna və müəllif fərziyyələrini müəyyənləşdirməyi öyrənirlər.'),
    (3, 'Lüğət və qrammatika',   'Lüğət və qrammatika ayrı-ayrılıqda deyil, kontekstə inteqrasiya olunmuş şəkildə tədris olunur. Hər bölmənin sonunda tələbələr qrammatik düzgün, yüksək səviyyəli dil biliyi ilə mürəkkəb fikirləri ifadə edə bilirlər; bütün qrammatika tematik olaraq əhatə olunur.')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Listening and Speaking', 'Listening exercises focus on predicting content, understanding main meaning and details, and identifying authorial assumptions. Students develop oral skills through presentations, debates, simulations, and role-playing, supported by original materials such as "TED Talks" and "YouTube".'),
    (2, 'Reading and Writing',    'Students are taught academic writing, peer and instructor interaction, and document editing. They learn to develop strong arguments, write thesis-relevant sentences and well-structured paragraphs, produce outlines and essays, and identify main ideas and authorial assumptions while reading.'),
    (3, 'Vocabulary and Grammar', 'Vocabulary and grammar are integrated into context rather than taught in isolation. By the end of each unit, students can express complex ideas in grammatically correct, high-level language; all grammar is covered thematically.')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'foreign_languages',
        'Səbinə', 'Alməmmədova', 'Məmməd qızı',
        'sabina.almemmedova@aztu.edu.az',
        '+994 50 346 43 12',
        NULL,
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
    'Filologiya elmləri doktoru',
    'Professor',
    '<p>Alməmmədova Səbinə Məmməd qızı — filologiya elmləri doktoru, professor; müqayisəli dilçilik, terminologiya və müasir Azərbaycan dili üzrə ixtisaslaşdırılmış alimdir. O, filologiya (dilçilik) istiqamətində elmi və pedaqoji fəaliyyət göstərir.</p><p>Onun elmi tədqiqatlarının əsas istiqamətlərinə Azərbaycan dilinin zənginləşməsində alınmalar və onların unifikasiyası problemləri, terminoloji leksikada alınmalarda baş verən semantik proseslər, Azərbaycan dilinin lüğət tərkibində alınma paralelizmlər və onu yaradan amillər, alınma terminlərin mənimsənilməsi və unifikasiya formaları, terminoloji lüğətlərdə alınma terminlərin verilmə üsulları və unifikasiyası, müasir Azərbaycan dilində alınma terminlərin standartlaşdırma formaları, standartlaşdırma prosesində unifikasiya ilə nizamasalmanın qarşılıqlı əlaqəsi, beynəlxalq terminlərin unifikasiya problemi, alınmaların tərcüməsində unifikasiya, sahə terminologiyasında alınma terminlərin təsbiti və terminoloji bazanın yaradılması, terminoloji lüğətlərdə terminlərin standartlaşdırma yolları daxildir.</p><p>Hazırda o, Azərbaycan Texniki Universitetinin Xarici dillər kafedrasının müdiri vəzifəsində çalışır.</p><p>O, 150-dən çox elmi məqalə, 8 monoqrafiya, 3 dərs vəsaiti, 25 tərcümə əsəri, 1 metodik vəsait və 3 lüğətin müəllifidir.</p>',
    '["Müasir Azərbaycan dili", "Müqayisəli dilçilik", "Terminologiya"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Philological Sciences',
    'Professor',
    '<p>Almammedova Sabina Mammad gizi — Doctor of Philological Sciences, Professor; a scientist specializing in comparative linguistics, terminology, and the modern Azerbaijani language. She carries out scientific and pedagogical activities in the field of philology (linguistics).</p><p>The main directions of her scientific research include the problems of borrowings and their unification in the enrichment of the Azerbaijani language, semantic processes occurring in borrowings in the terminological lexicon, borrowing parallelisms in the vocabulary of the Azerbaijani language and the factors that create them, the assimilation and unification forms of borrowed terms, the methods of presenting and unifying borrowed terms in terminological dictionaries, forms of standardization of borrowed terms in the modern Azerbaijani language, the interaction of unification and regularization in the standardization process, the problem of unification of international terms, unification in the translation of borrowings, identification of borrowed terms in field terminology and the creation of a terminological base, and ways of standardizing terms in terminological dictionaries.</p><p>She currently serves as the Head of the Department of Foreign Languages at Azerbaijan Technical University.</p><p>She is the author of more than 150 scientific articles, 8 monographs, 3 textbooks, 25 translated works, 1 methodological manual, and 3 dictionaries.</p>',
    '["Modern Azerbaijani language", "Comparative linguistics", "Terminology"]'::jsonb,
    NOW()
FROM director_insert
ON CONFLICT (director_id, lang_code) DO UPDATE
SET scientific_degree          = EXCLUDED.scientific_degree,
    scientific_title           = EXCLUDED.scientific_title,
    bio                        = EXCLUDED.bio,
    scientific_research_fields = EXCLUDED.scientific_research_fields,
    updated_at                 = NOW();

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1989', '1994', NOW() FROM cafedra_directors WHERE cafedra_code = 'foreign_languages'
UNION ALL
SELECT id, '2003', '2008', NOW() FROM cafedra_directors WHERE cafedra_code = 'foreign_languages'
UNION ALL
SELECT id, '2012', '2018', NOW() FROM cafedra_directors WHERE cafedra_code = 'foreign_languages'
UNION ALL
SELECT id, '2024', '2024', NOW() FROM cafedra_directors WHERE cafedra_code = 'foreign_languages'
UNION ALL
SELECT id, '2025', '2025', NOW() FROM cafedra_directors WHERE cafedra_code = 'foreign_languages'
UNION ALL
SELECT id, '2026', '2026', NOW() FROM cafedra_directors WHERE cafedra_code = 'foreign_languages';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'foreign_languages')
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bakalavr + Magistr',                                   'Azərbaycan Dillər Universiteti'),
    (2, 'Elmlər namizədi (PhD)',                                'AMEA İ.Nəsimi adına Dilçilik İnstitutu'),
    (3, 'Elmlər doktoru (DSc)',                                 'AMEA İ.Nəsimi adına Dilçilik İnstitutu'),
    (4, 'İxtisasartırma kursu',                                 'Böyük Britaniya, Oxford və London'),
    (5, 'İxtisasartırma kursu',                                 'İspaniya, Barselona'),
    (6, 'İxtisasartırma kursu (Dil İnstitutu)',                 'Avstriya, Vyana')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Bachelor''s + Master''s',                               'Azerbaijan University of Languages'),
    (2, 'Candidate of Sciences (PhD)',                          'Institute of Linguistics named after I. Nasimi, ANAS'),
    (3, 'Doctor of Sciences (DSc)',                             'Institute of Linguistics named after I. Nasimi, ANAS'),
    (4, 'Advanced training course',                             'Oxford and London, United Kingdom'),
    (5, 'Advanced training course',                             'Barcelona, Spain'),
    (6, 'Advanced training course (Institute of Languages)',    'Vienna, Austria')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'foreign_languages';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('foreign_languages', 'Xatirə',    'Məmmədova-Rəhimova', 'İsrafil qızı',    'xatire.memmedova@aztu.edu.az',    '+994 50 324 70 39', NOW()),  -- 1
    ('foreign_languages', 'Nuriyyə',   'Rzayeva',            'Əsgər qızı',      'nuriyye.rzayeva@aztu.edu.az',     '+994 50 324 70 39', NOW()),  -- 2
    ('foreign_languages', 'Pərvanə',   'Məmmədova',          'Həbib qızı',      'parvana.memmedova@aztu.edu.az',   '+994 50 540 35 82', NOW()),  -- 3
    ('foreign_languages', 'Kəmalə',    'Mehdixanlı',         'Əhliyyət qızı',   'kemale.mehdixanli@aztu.edu.az',   '+994 50 585 05 03', NOW()),  -- 4
    ('foreign_languages', 'Aytən',     'Sadıqova',           'Pilağa qızı',     'ayten.sadiqova@aztu.edu.az',      '+994 51 984 32 32', NOW()),  -- 5
    ('foreign_languages', 'Sevil',     'Məmmədova',          'Ələsgər qızı',    'sevil.mammadova@aztu.edu.az',     '+994 50 732 68 28', NOW()),  -- 6
    ('foreign_languages', 'Təbərrük',  'Cahangirli',         'Fərrux qızı',     'tabarruk.cahangirli@aztu.edu.az', '+994 50 586 44 84', NOW()),  -- 7
    ('foreign_languages', 'Elmira',    'Hüseynova',          'Abdulla qızı',    'elmira.huseynova@aztu.edu.az',    '+994 70 948 58 90', NOW()),  -- 8
    ('foreign_languages', 'Ləman',     'Axundova',           'Pərviz qızı',     'leman.axundova@aztu.edu.az',      '+994 70 793 00 70', NOW()),  -- 9
    ('foreign_languages', 'İradə',     'Bədəlova',           'Elman qızı',      'irada.badalova@aztu.edu.az',      '+994 50 396 32 15', NOW()),  -- 10
    ('foreign_languages', 'Aytən',     'Hacıyeva',           'Fikrət qızı',     'ayten.haciyeva@aztu.edu.az',      '+994 55 577 15 77', NOW()),  -- 11
    ('foreign_languages', 'Ellada',    'Hacıyeva',           'Fərman qızı',     'ellada.gadjiyeva@aztu.edu.az',    '+994 50 519 75 82', NOW()),  -- 12
    ('foreign_languages', 'Sevinc',    'Hacıyeva',           'Əli qızı',        'sevinc.haciyeva@aztu.edu.az',     '+994 50 424 50 07', NOW()),  -- 13
    ('foreign_languages', 'Şəfiqə',    'Heydərova',          'Qurban qızı',     'shafiga.heyderova@aztu.edu.az',   '+994 50 544 77 74', NOW()),  -- 14
    ('foreign_languages', 'Dilarə',    'Həmidova',           'Ağamirzə qızı',   'dilare.hemidova@aztu.edu.az',     '+994 50 245 37 31', NOW()),  -- 15
    ('foreign_languages', 'Aybəniz',   'Həsənova',           'Mahmud qızı',     'aybeniz.hesenova@aztu.edu.az',    '+994 50 452 91 65', NOW()),  -- 16
    ('foreign_languages', 'Nigar',     'Həsənova',           'Xalid qızı',      'nigar.hesenova@aztu.edu.az',      '+994 50 515 11 40', NOW()),  -- 17
    ('foreign_languages', 'Kəmalə',    'Hüseynova',          'Sabir qızı',      'kamala.huseynova@aztu.edu.az',    '+994 50 394 72 21', NOW()),  -- 18
    ('foreign_languages', 'Gülnarə',   'İsmayılova',         'Ədhəm qızı',      'gulnare.ismayilova@aztu.edu.az',  '+994 55 793 51 91', NOW()),  -- 19
    ('foreign_languages', 'Yeganə',    'Qurbanova',          'Təlhəd qızı',     'yegane.qurbanova@aztu.edu.az',    '+994 50 425 62 52', NOW()),  -- 20
    ('foreign_languages', 'Mehriban',  'Muradova',           'Kirman qızı',     'mehriban.muradova@aztu.edu.az',   '+994 50 640 95 29', NOW()),  -- 21
    ('foreign_languages', 'Zibahət',   'Nəsirova',           'Əli qızı',        'zibahet.nesirova@aztu.edu.az',    '+994 55 664 62 37', NOW()),  -- 22
    ('foreign_languages', 'Vəfa',      'Rəşidli',            'Əhməd qızı',      'vefa.reshidli@aztu.edu.az',       '+994 50 742 77 68', NOW()),  -- 23
    ('foreign_languages', 'İradə',     'Vəliyeva',           'Zahir qızı',      'irade.veliyeva@aztu.edu.az',      '+994 50 353 97 33', NOW()),  -- 24
    ('foreign_languages', 'Xalidə',    'Zamanova',           'Yaşar qızı',      'xalide.zamanova@aztu.edu.az',     '+994 50 688 98 15', NOW()),  -- 25
    ('foreign_languages', 'Klaudio',   'Kasperl',            'Felix oğlu',      'klaudio.kasperl@aztu.edu.az',     '+994 51 730 37 91', NOW()),  -- 26
    ('foreign_languages', 'Nilüfər',   'Hüseynova',          'Maarif qızı',     'nilufar.huseynova@aztu.edu.az',   '+994 55 903 47 30', NOW()),  -- 27
    ('foreign_languages', 'Fəxriyyə',  'Abdullayeva',        'Qanboy qızı',     'fakhriya.abdullayeva@aztu.edu.az','+994 50 334 31 21', NOW()),  -- 28
    ('foreign_languages', 'Sürəyya',   'Quliyeva',           'Xanlar qızı',     'sureyya.memmedli@aztu.edu.az',    '+994 50 327 33 36', NOW()),  -- 29
    ('foreign_languages', 'Aysel',     'Yusubova',           'Dadaş qızı',      'aysel.yusubova@aztu.edu.az',      '+994 55 237 92 97', NOW()),  -- 30
    ('foreign_languages', 'Aytac',     'Hacıyeva',           'Fərman qızı',     'aytac.hajiyeva@aztu.edu.az',      '+994 77 641 26 05', NOW()),  -- 31
    ('foreign_languages', 'Aygül',     'Xəlilova',           'Mətləb qızı',     'aygul.khalilova@aztu.edu.az',     '+994 51 916 74 66', NOW()),  -- 32
    ('foreign_languages', 'Nəsrin',    'Hacıyeva',           'Ənvər qızı',      'nasrin.hajiyeva@aztu.edu.az',     '+994 51 315 05 09', NOW()),  -- 33
    ('foreign_languages', 'Solmaz',    'Cəfərquliyeva',      'Yaşar qızı',      'solmaz.jafarguliyeva@aztu.edu.az','+994 55 560 86 46', NOW()),  -- 34
    ('foreign_languages', 'Bəyim',     'Əkbərova',           'İsmayıl qızı',    'bayim.akberova@aztu.edu.az',      '+994 55 692 58 89', NOW()),  -- 35
    ('foreign_languages', 'Rəşid',     'Sultanov',           'Əli oğlu',        'rashid.sultanov@aztu.edu.az',     '+994 50 662 17 13', NOW()),  -- 36
    ('foreign_languages', 'Günay',     'Hüseynova',          'Xanəli qızı',     'gunay.huseynova@aztu.edu.az',     '+994 55 519 66 67', NOW()),  -- 37
    ('foreign_languages', 'Sənubər',   'Həmidli',            'Zabil qızı',      'sanuber.hamidli@aztu.edu.az',     '+994 77 397 98 88', NOW()),  -- 38
    ('foreign_languages', 'Şəbnəm',    'Surxayzadə',         'İlham qızı',      'shabnam.surxayzade@aztu.edu.az',  '+994 51 621 80 29', NOW()),  -- 39
    ('foreign_languages', 'Pərvanə',   'Mövsümova',          'Firdovsi qızı',   'parvana.movsumova@aztu.edu.az',   '+994 50 306 74 76', NOW()),  -- 40
    ('foreign_languages', 'Famil',     'Məmmədov',           'Zakir oğlu',      'famil.mammadov@aztu.edu.az',      '+994 55 242 52 78', NOW()),  -- 41
    ('foreign_languages', 'Afaq',      'İsmayılzadə',        'Rafiq qızı',      'afag.ismayilzade@aztu.edu.az',    '+994 50 654 96 64', NOW()),  -- 42
    ('foreign_languages', 'Pakizə',    'Həziyeva',           'Miri qızı',       'pakize.haziyeva@aztu.edu.az',     '+994 99 875 17 75', NOW()),  -- 43
    ('foreign_languages', 'Günel',     'Vənətizadə',         'Vüqar qızı',      'gunel.vanetizadeh@aztu.edu.az',   '+994 51 314 19 10', NOW()),  -- 44
    ('foreign_languages', 'Miranə',    'Əfəndiyeva',         'Ramiz qızı',      'mirane.efendiyeva@aztu.edu.az',   '+994 55 257 57 01', NOW())   -- 45
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Xarici dillər kafedrasının baş müəllimi',                                         'Dosent'::varchar, 'fil.ü.f.d.'::varchar),
    (2,  'Xarici dillər kafedrasının baş müəllimi',                                         'Dosent',          'fil.ü.f.d.'),
    (3,  'Xarici dillər kafedrasının baş müəllimi',                                         'Dosent',          'fil.ü.f.d.'),
    (4,  'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              'fil.ü.f.d.'),
    (5,  'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              'fil.ü.f.d.'),
    (6,  'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              'fil.ü.f.d.'),
    (7,  'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              'fil.ü.f.d.'),
    (8,  'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              'fil.ü.f.d.'),
    (9,  'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (10, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (11, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (12, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (13, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (14, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (15, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (16, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (17, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (18, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (19, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (20, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (21, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (22, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (23, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (24, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (25, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (26, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (27, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (28, 'Xarici dillər kafedrasının baş müəllimi',                                         NULL,              NULL),
    (29, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (30, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (31, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (32, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (33, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (34, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (35, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (36, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (37, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (38, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (39, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (40, 'Xarici dillər kafedrasının müəllimi (Keyfiyyətin təminatı şöbəsinin müdiri)',     NULL,              NULL),
    (41, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (42, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (43, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (44, 'Xarici dillər kafedrasının müəllimi',                                             NULL,              NULL),
    (45, 'Xarici dillər kafedrasının kargüzarı',                                            NULL,              NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    (1,  'Senior Lecturer of the Department of Foreign Languages',                                   'Associate Professor'::varchar, 'PhD in Philology'::varchar),
    (2,  'Senior Lecturer of the Department of Foreign Languages',                                   'Associate Professor',          'PhD in Philology'),
    (3,  'Senior Lecturer of the Department of Foreign Languages',                                   'Associate Professor',          'PhD in Philology'),
    (4,  'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           'PhD in Philology'),
    (5,  'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           'PhD in Philology'),
    (6,  'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           'PhD in Philology'),
    (7,  'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           'PhD in Philology'),
    (8,  'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           'PhD in Philology'),
    (9,  'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (10, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (11, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (12, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (13, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (14, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (15, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (16, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (17, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (18, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (19, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (20, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (21, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (22, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (23, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (24, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (25, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (26, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (27, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (28, 'Senior Lecturer of the Department of Foreign Languages',                                   NULL,                           NULL),
    (29, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (30, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (31, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (32, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (33, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (34, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (35, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (36, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (37, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (38, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (39, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (40, 'Lecturer of the Department of Foreign Languages (Head of the Quality Assurance Department)', NULL,                         NULL),
    (41, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (42, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (43, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (44, 'Lecturer of the Department of Foreign Languages',                                          NULL,                           NULL),
    (45, 'Clerk of the Department of Foreign Languages',                                             NULL,                           NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
