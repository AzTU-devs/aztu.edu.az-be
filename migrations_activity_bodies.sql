-- =====================================================================
-- MIGRATION — Activity log: request/response bodies
--
-- Adds:
--   admin_activity_log.request_body   → the sanitised request payload
--   admin_activity_log.response_body  → the sanitised response payload
--
-- Both are JSONB and both are *sanitised and size-capped before they are
-- written* (see app/core/audit_payload.py):
--
--   * every value under a secret-looking key — password, token, api_key,
--     secret, authorization … — is replaced with "[redacted]", at any
--     depth, before the row is built;
--   * file uploads are never buffered: a multipart request records only
--     the field names and each file's name/size;
--   * anything larger than the cap is truncated with a marker rather
--     than stored whole;
--   * only JSON payloads are captured — binary and HTML are skipped.
--
-- `request_id` already existed on this table but nothing ever wrote to
-- it. It is now populated with a per-request UUID that is also returned
-- in the `X-Request-ID` response header, so a log row can be tied back
-- to a specific call.
--
-- Idempotent and additive. Existing rows keep NULL for both columns.
-- =====================================================================


-- =====================================================================
-- STEP 1 — SCHEMA
-- =====================================================================
alter table admin_activity_log
    add column if not exists request_body  jsonb;
alter table admin_activity_log
    add column if not exists response_body jsonb;


-- =====================================================================
-- STEP 2 — VERIFY. Expect both rows.
-- =====================================================================
select column_name, data_type
from information_schema.columns
where table_name = 'admin_activity_log'
  and column_name in ('request_body', 'response_body', 'request_id')
order by column_name;
