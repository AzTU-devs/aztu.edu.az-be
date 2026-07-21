-- ============================================================
-- Cafedra patents (Patentlər) — seed for KIMYA_EKO
--
-- Source: the 2024 / 2026 patent list supplied by the department.
--
-- Author names and patent titles are transliterated for the EN rows where a
-- meaningful English rendering exists; the patent NUMBER is a registry code and
-- is never translated. Where no official English title was supplied, the AZ text
-- is repeated rather than machine-translated — a wrong translation on a legal
-- document is worse than an untranslated one, and the admin can correct it.
--
-- The URL column is left NULL: the source listed a "Link" label with no address.
-- Fill it in from the admin panel.
--
-- Idempotent: skipped entirely when KIMYA_EKO already has patents.
-- Run AFTER migrations_cafedra_patents.sql, and follow with
-- migrations_resync_sequences.sql (explicit-id seeds do not advance sequences).
-- ============================================================

BEGIN;

DO $$
DECLARE v_id integer;
BEGIN
    IF EXISTS (SELECT 1 FROM cafedra_patents WHERE cafedra_code = 'KIMYA_EKO') THEN
        RETURN;
    END IF;

    -- ── 2024 ────────────────────────────────────────────────
    INSERT INTO cafedra_patents
        (cafedra_code, patent_number, year, url, display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', 'İ 2024 0058', 2024, NULL, 0, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_patent_tr (patent_id, lang_code, title, authors, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Alüminium oksidin alınması üsulu',
         'İbrahimov Əli, Namazov Sübhan, Vəkilova Rəna, Həsənli Ramiz, Yusubov Fəxrəddin',
         NOW(), NOW()),
        (v_id, 'en',
         'Method for producing aluminium oxide',
         'Ibrahimov Ali, Namazov Subhan, Vakilova Rana, Hasanli Ramiz, Yusubov Fakhraddin',
         NOW(), NOW());

    -- ── 2026 ────────────────────────────────────────────────
    INSERT INTO cafedra_patents
        (cafedra_code, patent_number, year, url, display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', '№053029', 2026, NULL, 1, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_patent_tr (patent_id, lang_code, title, authors, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Alunitin sulfit turşusu ilə emalında effektiv qarışmanı təmin edən qurğu',
         'İbrahimov Əli, Səfərov Cəmil, Namazov Sübhan, Yusubov Fəxrəddin',
         NOW(), NOW()),
        (v_id, 'en',
         'Device providing effective mixing in the treatment of alunite with sulfurous acid',
         'Ibrahimov Ali, Safarov Jamil, Namazov Subhan, Yusubov Fakhraddin',
         NOW(), NOW());

    INSERT INTO cafedra_patents
        (cafedra_code, patent_number, year, url, display_order, created_at, updated_at)
    VALUES ('KIMYA_EKO', '№053039', 2026, NULL, 2, NOW(), NOW())
    RETURNING id INTO v_id;

    INSERT INTO cafedra_patent_tr (patent_id, lang_code, title, authors, created_at, updated_at)
    VALUES
        (v_id, 'az',
         'Suyun ağır metal ionlarından təmizlənməsi zamanı adsorbentlərin istifadə olunmamış tutumunun azaldılması üsulu',
         'Yusubov Fəxrəddin, İbrahimov Əli, Təhməzova Kəmalə',
         NOW(), NOW()),
        (v_id, 'en',
         'Method for reducing the unused capacity of adsorbents during the removal of heavy metal ions from water',
         'Yusubov Fakhraddin, Ibrahimov Ali, Tahmazova Kamala',
         NOW(), NOW());
END $$;

COMMIT;

-- Verify: expect 3 patents (1 in 2024, 2 in 2026) and 6 translation rows.
SELECT p.year, p.patent_number, t.lang_code, left(t.title, 45) AS title
FROM cafedra_patents p
JOIN cafedra_patent_tr t ON t.patent_id = p.id
WHERE p.cafedra_code = 'KIMYA_EKO'
ORDER BY p.year DESC, p.display_order, t.lang_code;
