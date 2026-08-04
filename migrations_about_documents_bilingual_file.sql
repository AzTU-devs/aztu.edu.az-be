-- Make the About document file_url per-language.
--
-- The file lived on a single neutral column (about_documents.file_url), shared
-- by AZ and EN. It now lives on the per-language translation rows
-- (about_document_tr.file_url), mirroring the existing bilingual *_tr
-- convention (like name). The neutral column is KEPT (deprecated) for backfill
-- and as a backward-compat mirror.
--
-- Idempotent: safe to run more than once.

-- 1) Add the per-language column.
alter table about_document_tr
    add column if not exists file_url varchar(2048);

-- 2) Backfill — copy the neutral file into BOTH the az and en translation rows
--    wherever the tr file_url is still empty and the neutral file is present.
update about_document_tr as t
set file_url = d.file_url
from about_documents as d
where t.document_id = d.id
  and (t.file_url is null or t.file_url = '')
  and d.file_url is not null
  and d.file_url <> '';

-- 3) Verify — inspect the backfilled per-language files alongside the neutral one.
select
    d.id            as document_id,
    d.file_url      as neutral_file_url,
    t.lang_code,
    t.file_url      as tr_file_url
from about_documents as d
left join about_document_tr as t on t.document_id = d.id
order by d.id, t.lang_code;
