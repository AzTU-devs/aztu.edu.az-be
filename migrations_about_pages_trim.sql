-- =====================================================================
-- TRIM — remove About blocks that are no longer part of the page spec
--
-- ⚠️  DESTRUCTIVE. Unlike the seed, this DELETES rows. Each block listed
--     below was seeded by an earlier version of the blueprint and is not
--     in the agreed page structure any more. Deleting a block also
--     deletes its items and translations (ON DELETE CASCADE), so any copy
--     already typed into these blocks is lost.
--
--     Run the PREVIEW first and check the counts before the DELETE.
--
-- Removed, per page:
--   history         → stats
--   strategic-plan  → vision, mission, values, targets
--   rector          → responsibilities, priorities, message_closing
--
-- Everything else — and every other page — is untouched.
-- =====================================================================


-- =====================================================================
-- STEP 1 — PREVIEW. Run this alone first.
-- =====================================================================
select p.page_key,
       s.section_key,
       s.section_type,
       (select count(*) from about_items i where i.section_id = s.id)  as items,
       (select count(*) from about_people h where h.section_id = s.id) as people
from about_sections s
join about_pages p on p.id = s.page_id
where (p.page_key = 'history'        and s.section_key in ('stats'))
   or (p.page_key = 'strategic-plan' and s.section_key in ('vision', 'mission', 'values', 'targets'))
   or (p.page_key = 'rector'         and s.section_key in ('responsibilities', 'priorities', 'message_closing'))
order by p.page_key, s.display_order;


-- =====================================================================
-- STEP 2 — DELETE. Only run once the preview looks right.
-- =====================================================================
delete from about_sections s
using about_pages p
where p.id = s.page_id
  and ( (p.page_key = 'history'        and s.section_key in ('stats'))
     or (p.page_key = 'strategic-plan' and s.section_key in ('vision', 'mission', 'values', 'targets'))
     or (p.page_key = 'rector'         and s.section_key in ('responsibilities', 'priorities', 'message_closing')) );


-- =====================================================================
-- STEP 3 — VERIFY the five pages now match the spec exactly.
-- =====================================================================
select p.page_key,
       string_agg(s.section_key || '(' || s.section_type || ')', ' → ' order by s.display_order) as blocks
from about_pages p
join about_sections s on s.page_id = p.id
where p.page_key in
      ('vision-mission-goal', 'history', 'anniversary-film', 'strategic-plan', 'rector')
group by p.page_key
order by p.page_key;
