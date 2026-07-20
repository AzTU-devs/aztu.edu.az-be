-- ============================================================
-- Cafedra scientific publications (Elmi nəşrlər) — seed
-- Migrated verbatim from the public site's curated static list:
--   aztu.edu.az/src/data/cafedraPublications.ts
--
-- `year` is derived from the free-text `date` string by taking the last
-- 4-digit run matching (19|20)\d{2} (AMENDMENT A1.5). No value is guessed.
--
-- Idempotent: each cafedra block is skipped when that cafedra already has
-- publications, so the file is safe to re-run.
--
-- Run AFTER migrations_fix_identity.sql, otherwise `returning id` yields a
-- null-PK violation.
-- ============================================================

BEGIN;

-- ── KIMYA_EKO ─────────────────────────────────────────
DO $$
DECLARE v_id integer;
BEGIN
    IF EXISTS (
        SELECT 1 FROM cafedra_scientific_publications
        WHERE cafedra_code = 'KIMYA_EKO'
    ) THEN
        RETURN;
    END IF;

    -- #1
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', '07.05.2026', 2026,
            'https://www.scopus.com/pages/publications/105038341146?origin=resultslist',
            0, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Filtirləmə və koliform bakteriyalarının təmizlənməsi üçün substrat kimi biokömürdən istifadə edərək davamlı su təmizləmə prosesinin hazırlanması',
         'F. Yusubov, T. Xəlil, M. İ. Əli, R. Abid, Ə. Müctəba, R. Əsğər, Ə. Cəmal, Y. Tutar, Ə. Həbib',
         'The Canadian Journal of Chemical Engineering',
         'Kanada', NOW(), NOW()),
        (v_id, 'en',
         'Filtirləmə və koliform bakteriyalarının təmizlənməsi üçün substrat kimi biokömürdən istifadə edərək davamlı su təmizləmə prosesinin hazırlanması',
         'F. Yusubov, T. Xəlil, M. İ. Əli, R. Abid, Ə. Müctəba, R. Əsğər, Ə. Cəmal, Y. Tutar, Ə. Həbib',
         'The Canadian Journal of Chemical Engineering',
         'Canada', NOW(), NOW());

    -- #2
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', '10.10.2025', 2025,
            'https://www.scopus.com/pages/publications/105030785708?origin=resultslist',
            1, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Study of the Complex Processing Technology of Alunite Using Sulfurous Acid: A Pilot Approach',
         'Fakhraddin Yusubov, Jamil I. Safarov, Ali A. Ibrahimov, Subhan N. Namazov, Ramil I. Hasanov',
         'Mathematical Modelling of Engineering Problems',
         NULL, NOW(), NOW()),
        (v_id, 'en',
         'Study of the Complex Processing Technology of Alunite Using Sulfurous Acid: A Pilot Approach',
         'Fakhraddin Yusubov, Jamil I. Safarov, Ali A. Ibrahimov, Subhan N. Namazov, Ramil I. Hasanov',
         'Mathematical Modelling of Engineering Problems',
         NULL, NOW(), NOW());

    -- #3
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Web of Science', 'Q4', '15.09.2025', 2025,
            'https://www.webofscience.com/wos/woscc/full-record/WOS:001592218500001',
            2, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Enantioselective Alkoxylation of β-Substituted Aromatic Nitroalkenes with Allyl Alcohol',
         'Talybov G. M.',
         'Hungarian Journal of Industry and Chemistry, 2025, V. 53(2), pp. 1–6',
         'Macarıstan', NOW(), NOW()),
        (v_id, 'en',
         'Enantioselective Alkoxylation of β-Substituted Aromatic Nitroalkenes with Allyl Alcohol',
         'Talybov G. M.',
         'Hungarian Journal of Industry and Chemistry, 2025, V. 53(2), pp. 1–6',
         'Hungary', NOW(), NOW());

    -- #4
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', 'İyun 2025', 2025,
            'https://www.scopus.com/pages/publications/105014719766?origin=resultslist',
            3, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Pressure and Density Distribution in Axisymmetric Compactions Pressed in a Rigid Matrix',
         'Jafarova A. A.',
         'Russian Engineering Research, Vol. 45, No. 6, pp. 780–784 (DOI: 10.3103/S1068798X25701278)',
         'Rusiya', NOW(), NOW()),
        (v_id, 'en',
         'Pressure and Density Distribution in Axisymmetric Compactions Pressed in a Rigid Matrix',
         'Jafarova A. A.',
         'Russian Engineering Research, Vol. 45, No. 6, pp. 780–784 (DOI: 10.3103/S1068798X25701278)',
         'Russia', NOW(), NOW());

    -- #5
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q4', '06.09.2025', 2025,
            'https://www.scopus.com/pages/publications/105021325155?origin=resultslist',
            4, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Разработка и освоение технологии термического упрочнения муфтовых заготовок бурильных и обсадных труб для нефтедобычи из стали 32Г2',
         'A. Mammadov, A. Jafarova, S. Rustamova',
         'Журнал «Черные металлы», Т. 1125, No 09, pp. 37–43 (DOI: 10.17580/chm.2025.09.06)',
         'Rusiya', NOW(), NOW()),
        (v_id, 'en',
         'Разработка и освоение технологии термического упрочнения муфтовых заготовок бурильных и обсадных труб для нефтедобычи из стали 32Г2',
         'A. Mammadov, A. Jafarova, S. Rustamova',
         'Журнал «Черные металлы», Т. 1125, No 09, pp. 37–43 (DOI: 10.17580/chm.2025.09.06)',
         'Russia', NOW(), NOW());

    -- #6
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', '30.12.2025', 2025,
            'https://www.scopus.com/pages/publications/105028625293?origin=resultslist',
            5, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Experience in Manufacturing Hot-Formed Casing Pipes from 32G2 Steel for Oil Production',
         'A. Mammadov, S. Rustamova, A. Jafarova, F. Jafarov',
         'International Journal on Technical and Physical Problems of Engineering, Issue 65, Volume 17, Number 4, pp. 162–167',
         'Rusiya', NOW(), NOW()),
        (v_id, 'en',
         'Experience in Manufacturing Hot-Formed Casing Pipes from 32G2 Steel for Oil Production',
         'A. Mammadov, S. Rustamova, A. Jafarova, F. Jafarov',
         'International Journal on Technical and Physical Problems of Engineering, Issue 65, Volume 17, Number 4, pp. 162–167',
         'Russia', NOW(), NOW());

    -- #7
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', 'Mart 2026', 2026,
            'https://journal.eu-jr.eu/engineering/article/view/4206',
            6, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Development of technology for producing a bimetallic roll for rolling construction rebars',
         'Arif Mammadov, Ramin Kerimov, Faiq Guliyev, Afet Jafarova',
         'EUREKA: Physics and Engineering, Number 3, pp. 66–74 (DOI: 10.21303/2461-4262.2026.004206)',
         'Estoniya', NOW(), NOW()),
        (v_id, 'en',
         'Development of technology for producing a bimetallic roll for rolling construction rebars',
         'Arif Mammadov, Ramin Kerimov, Faiq Guliyev, Afet Jafarova',
         'EUREKA: Physics and Engineering, Number 3, pp. 66–74 (DOI: 10.21303/2461-4262.2026.004206)',
         'Estonia', NOW(), NOW());

    -- #8
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q2', 'May 2026', 2026,
            'https://www.scopus.com/pages/publications/105034842160?origin=resultslist',
            7, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Influence of Metallurgical Defects on Cracking of Oil and Gas Pipelines',
         'A. T. Mammadov, N. Sh. Ismailov, A. I. Babayev, M. Ch. Hüseynov, A. A. Jafarova',
         'SOCAR Proceedings, No. 1 (2026) 099–105',
         'Azərbaycan', NOW(), NOW()),
        (v_id, 'en',
         'Influence of Metallurgical Defects on Cracking of Oil and Gas Pipelines',
         'A. T. Mammadov, N. Sh. Ismailov, A. I. Babayev, M. Ch. Hüseynov, A. A. Jafarova',
         'SOCAR Proceedings, No. 1 (2026) 099–105',
         'Azerbaijan', NOW(), NOW());

    -- #9
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', 'Dekabr 2025', 2025,
            'https://www.scopus.com/pages/publications/105027817306?origin=resultslist',
            8, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Performance Modeling and Field Validation of Decentralized Wastewater Treatment Systems in Semi-Arid Azerbaijan: A Pilot Case Study',
         'Pasha N., Mikayil O., Qasimov I., Aliyev E.',
         'Global NEST Journal, 27(10)',
         'Yunanıstan', NOW(), NOW()),
        (v_id, 'en',
         'Performance Modeling and Field Validation of Decentralized Wastewater Treatment Systems in Semi-Arid Azerbaijan: A Pilot Case Study',
         'Pasha N., Mikayil O., Qasimov I., Aliyev E.',
         'Global NEST Journal, 27(10)',
         'Greece', NOW(), NOW());

    -- #10
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', 'Yanvar 2026', 2026,
            'https://www.scopus.com/pages/publications/105030707240?origin=resultslist',
            9, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Adaptive Water Governance Model in Azerbaijan: Integrating International Experience under Climate and Institutional Risks',
         'Pasha N., Ismayilov R. & Mikayil O.',
         'Global NEST Journal, 28(1)',
         'Yunanıstan', NOW(), NOW()),
        (v_id, 'en',
         'Adaptive Water Governance Model in Azerbaijan: Integrating International Experience under Climate and Institutional Risks',
         'Pasha N., Ismayilov R. & Mikayil O.',
         'Global NEST Journal, 28(1)',
         'Greece', NOW(), NOW());

    -- #11
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus / Web of Science', 'Q1', '05.01.2026', 2026,
            'https://www.scopus.com/results/results.uri?st1=alkyl%2C+alkylphenil-substited+cyclohexsane%2C+benzimidazole%2C+benzoxazole%2C+phenylcarboxsylic+acid%2C+indole&st2=&s=TITLE%28The+study+of+the+laws+of+convective+heat+transfer+to+optimize+hydrogen+production+processes+from+carbohydrates%29&limit=10&origin=searchbasic&sort=plf-f&src=s&sot=b&sdt=b&sessionSearchId=2fac9269fce3f98f19a6e4a6cde11ede',
            10, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'The study of the laws of convective heat transfer to optimize hydrogen production processes from carbohydrates',
         'Sh. Mamedov, Sh. Nasirov, T. Jabarov, T. Axmedova, G. Alesgerov, S. Abdullayeva, Sh. Eyvazova, B. Mehdiyev, M. Javadova',
         'International Journal of Hydrogen Energy',
         'Rusiya', NOW(), NOW()),
        (v_id, 'en',
         'The study of the laws of convective heat transfer to optimize hydrogen production processes from carbohydrates',
         'Sh. Mamedov, Sh. Nasirov, T. Jabarov, T. Axmedova, G. Alesgerov, S. Abdullayeva, Sh. Eyvazova, B. Mehdiyev, M. Javadova',
         'International Journal of Hydrogen Energy',
         'Russia', NOW(), NOW());

    -- #12
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', '04.12.2025', 2025,
            'https://www.scopus.com/pages/publications/105025718463?origin=resultslist',
            11, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'The synthesis and study of tris-(2,4-bis(trichloromethyl))-1,3,5-triazapentadienato Co(III) complex through Hirshfeld surface analysis and evaluation of its antimicrobial activity',
         'Reyhana Ganiyeva, Gulnaz Mirzayeva, Nigar Ahmedova, Nazrin Zeynalli, Teymur Ilyasli, Arzu Niftaliyeva, Khudaverdi Ganbarov, Gaoussou Binate, Samir Aliyev',
         'New Materials, Compounds and Applications',
         NULL, NOW(), NOW()),
        (v_id, 'en',
         'The synthesis and study of tris-(2,4-bis(trichloromethyl))-1,3,5-triazapentadienato Co(III) complex through Hirshfeld surface analysis and evaluation of its antimicrobial activity',
         'Reyhana Ganiyeva, Gulnaz Mirzayeva, Nigar Ahmedova, Nazrin Zeynalli, Teymur Ilyasli, Arzu Niftaliyeva, Khudaverdi Ganbarov, Gaoussou Binate, Samir Aliyev',
         'New Materials, Compounds and Applications',
         NULL, NOW(), NOW());

    -- #13
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q4', 'Fevral 2026', 2026,
            'https://www.scopus.com/pages/publications/105029557770?origin=resultslist',
            12, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Syntheses, crystal structures and Hirshfeld surface analyses of (E)-1-[2,2-dichloro-1-(2,3-dimethoxyphenyl)ethen-1-yl]-2-phenyldiazene and (E)-1-(4-chlorophenyl)-2-[2,2-dichloro-1-(2,3-dimethoxyphenyl)ethen-1-yl]diazene',
         'Naila Mammadova, Gulnar T. Atakishiyeva, Peri A. Huseynova, Gulnara V. Babayeva, Gulnaz A. Mirzayeva, Mehmet Akkurt, Ajaya Bhattarai',
         'Acta Crystallographica Section E: Crystallographic Communications',
         NULL, NOW(), NOW()),
        (v_id, 'en',
         'Syntheses, crystal structures and Hirshfeld surface analyses of (E)-1-[2,2-dichloro-1-(2,3-dimethoxyphenyl)ethen-1-yl]-2-phenyldiazene and (E)-1-(4-chlorophenyl)-2-[2,2-dichloro-1-(2,3-dimethoxyphenyl)ethen-1-yl]diazene',
         'Naila Mammadova, Gulnar T. Atakishiyeva, Peri A. Huseynova, Gulnara V. Babayeva, Gulnaz A. Mirzayeva, Mehmet Akkurt, Ajaya Bhattarai',
         'Acta Crystallographica Section E: Crystallographic Communications',
         NULL, NOW(), NOW());

    -- #14
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', '18.02.2026', 2026,
            'https://www.scopus.com/pages/publications/105036645446?origin=resultslist',
            13, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Correction to: Numerical Modelling of Adsorption Wastewater Treatment to Remove Heavy Metals (Chemistry and Technology of Fuels and Oils, (2026), 61, 6, (1483–1490), 10.1007/s10553-026-01997-1)',
         'Yusubov F. V., Rzaeva A. A., Yariyeva A. M.',
         'Chemistry and Technology of Fuels and Oils',
         'Rusiya', NOW(), NOW()),
        (v_id, 'en',
         'Correction to: Numerical Modelling of Adsorption Wastewater Treatment to Remove Heavy Metals (Chemistry and Technology of Fuels and Oils, (2026), 61, 6, (1483–1490), 10.1007/s10553-026-01997-1)',
         'Yusubov F. V., Rzaeva A. A., Yariyeva A. M.',
         'Chemistry and Technology of Fuels and Oils',
         'Russia', NOW(), NOW());

    -- #15
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q3', '01.02.2026', 2026,
            'https://www.scopus.com/pages/publications/105030681214?origin=resultslist',
            14, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'A First-Principles Study of Structural Reorganization and Metallization in Fe-Substituted CrPSe3',
         'Phuc Nguyen, Tran T. A., Tran H. C., Yariyeva A. M., Aliyev M. E., +1 author',
         'Advanced Physical Research',
         'ABŞ', NOW(), NOW()),
        (v_id, 'en',
         'A First-Principles Study of Structural Reorganization and Metallization in Fe-Substituted CrPSe3',
         'Phuc Nguyen, Tran T. A., Tran H. C., Yariyeva A. M., Aliyev M. E., +1 author',
         'Advanced Physical Research',
         'USA', NOW(), NOW());

    -- #16
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q4', '07.07.2025', 2025,
            'https://www.scopus.com/pages/publications/105014201389?origin=resultslist',
            15, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Correlations of Analytical Properties of Mercury Complexes with 2-Hydroxythiophenol and Pyridine',
         'Zalov A. Z., Şahverdiyeva A. F., Mammadova Sh. A., Yariyeva A. M., Abdullayeva N. Z., +1 author',
         'Chemical Problems',
         'Azərbaycan', NOW(), NOW()),
        (v_id, 'en',
         'Correlations of Analytical Properties of Mercury Complexes with 2-Hydroxythiophenol and Pyridine',
         'Zalov A. Z., Şahverdiyeva A. F., Mammadova Sh. A., Yariyeva A. M., Abdullayeva N. Z., +1 author',
         'Chemical Problems',
         'Azerbaijan', NOW(), NOW());

    -- #17
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q4', 'Dekabr 2025', 2025,
            'https://www.scopus.com/pages/publications/105027370307?origin=resultslist',
            16, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Synthesis of bis-1,2,3-triazole derivatives based on terephthalic aldehyde and study of their biological activity',
         'Nigar E. Ahmadova, Afaq A. Abdullayeva, Gulnar T. Atakishiyeva, Irada J. Ahmadova, Shafiga A. Ibrahimova, Sevinc H. Mukhtarova, Khatira A. Garazade, Namiq Q. Shikhaliyev, Abel M. Maharramov',
         'New Materials, Compounds and Applications, Vol. 9, No. 3, 2025, pp. 455–467 (DOI: 10.62476/nmca.93455)',
         'Azərbaycan', NOW(), NOW()),
        (v_id, 'en',
         'Synthesis of bis-1,2,3-triazole derivatives based on terephthalic aldehyde and study of their biological activity',
         'Nigar E. Ahmadova, Afaq A. Abdullayeva, Gulnar T. Atakishiyeva, Irada J. Ahmadova, Shafiga A. Ibrahimova, Sevinc H. Mukhtarova, Khatira A. Garazade, Namiq Q. Shikhaliyev, Abel M. Maharramov',
         'New Materials, Compounds and Applications, Vol. 9, No. 3, 2025, pp. 455–467 (DOI: 10.62476/nmca.93455)',
         'Azerbaijan', NOW(), NOW());

    -- #18
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Scopus', 'Q4', '2026', 2026,
            'https://www.scopus.com/pages/publications/105035163609?origin=resultslist',
            17, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Computational assessment and molecular docking of arylhydrazone ester derivatives as SARS-CoV-2 main protease inhibitors',
         'Gulnar Atakishiyeva, Sevinc Mukhtarova, Sima Musayeva, Ulviyya Askerova, Khatira Garazade, Samira Miriyeva, Nurana Gurbanova, Namiq Shikhaliyev, Abel Maharramov',
         'New Materials, Compounds and Applications, Vol. 10, No. 1, 2026, pp. 65–85 (DOI: 10.62476/nmca.10165)',
         'Azərbaycan', NOW(), NOW()),
        (v_id, 'en',
         'Computational assessment and molecular docking of arylhydrazone ester derivatives as SARS-CoV-2 main protease inhibitors',
         'Gulnar Atakishiyeva, Sevinc Mukhtarova, Sima Musayeva, Ulviyya Askerova, Khatira Garazade, Samira Miriyeva, Nurana Gurbanova, Namiq Shikhaliyev, Abel Maharramov',
         'New Materials, Compounds and Applications, Vol. 10, No. 1, 2026, pp. 65–85 (DOI: 10.62476/nmca.10165)',
         'Azerbaijan', NOW(), NOW());

    -- #19
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Web of Science', 'Q1', '15.03.2026', 2026,
            'https://www.scopus.com/pages/publications/105027276187?origin=resultslist',
            18, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Adsorption and modeling of humic acid by Cu-doped metal-organic framework meta-ZIF-8',
         'Sima Musayeva, Mahmoud Shams, Elmina Gadirova, Sabiya Osmanova, Zohreh Niazi, Lee D. Wilson',
         'Materials Chemistry and Physics, Volume 352 (2026) 132038',
         NULL, NOW(), NOW()),
        (v_id, 'en',
         'Adsorption and modeling of humic acid by Cu-doped metal-organic framework meta-ZIF-8',
         'Sima Musayeva, Mahmoud Shams, Elmina Gadirova, Sabiya Osmanova, Zohreh Niazi, Lee D. Wilson',
         'Materials Chemistry and Physics, Volume 352 (2026) 132038',
         NULL, NOW(), NOW());

    -- #20
    INSERT INTO cafedra_scientific_publications
        (cafedra_code, publication_index, quartile, published_at, year, url,
         display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'Web of Science', 'Q4', 'Dekabr 2025', 2025,
            'https://www.scopus.com/pages/publications/105022938713?origin=resultslist',
            19, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_scientific_publication_tr
        (publication_id, lang_code, title, authors, journal, country, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Сернокислотное разложение каолиновых глин Човдарского месторождения (Азербайджан)',
         'Е. Гахраманова, С. Г. Эфендиева, П. А. Надиров, С. Т. Джафарова',
         'Химия в интересах устойчивого развития',
         'Rusiya', NOW(), NOW()),
        (v_id, 'en',
         'Сернокислотное разложение каолиновых глин Човдарского месторождения (Азербайджан)',
         'Е. Гахраманова, С. Г. Эфендиева, П. А. Надиров, С. Т. Джафарова',
         'Химия в интересах устойчивого развития',
         'Russia', NOW(), NOW());

END $$;

-- Publications intro for KIMYA_EKO (previously hardcoded in the public page)
UPDATE cafedras_tr
SET publications_intro = '<p>Kafedra əməkdaşlarının 2025–2026-cı illər üzrə beynəlxalq indeksli (Scopus, Web of Science) jurnallarda çap olunmuş elmi məqalələrinin siyahısı.</p>'
WHERE cafedra_code = 'KIMYA_EKO' AND lang_code = 'az'
  AND (publications_intro IS NULL OR publications_intro = '');

UPDATE cafedras_tr
SET publications_intro = '<p>List of scientific articles by the department''s staff published in internationally indexed (Scopus, Web of Science) journals during 2025–2026.</p>'
WHERE cafedra_code = 'KIMYA_EKO' AND lang_code = 'en'
  AND (publications_intro IS NULL OR publications_intro = '');

COMMIT;

-- ── Post-seed assertion (AMENDMENT A1.5) ─────────────────────
-- Every migrated publication must have a non-null year.
DO $$
DECLARE v_missing integer;
BEGIN
    SELECT count(*) INTO v_missing
    FROM cafedra_scientific_publications
    WHERE cafedra_code IN ('KIMYA_EKO')
      AND year IS NULL;

    IF v_missing > 0 THEN
        RAISE WARNING 'cafedra_scientific_publications: % row(s) have a NULL year', v_missing;
    END IF;
END $$;
