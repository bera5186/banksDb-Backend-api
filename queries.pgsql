-- select * from branches where city = 'DELHI' LIMIT 100;

-- CREATE INDEX BRANCHES_BRANCH_VECTOR_IDX ON branches USING gin(branch_vector);
-- 
-- SELECT
--     tablename,
--     indexname,
--     indexdef
-- FROM
--     pg_indexes
-- WHERE
--     schemaname = 'public'
-- ORDER BY
--     tablename,
--     indexname;

-- EXPLAIN ANALYSE SELECT "branches"."ifsc",
--        "branches"."bank_id",
--        "branches"."branch",
--        "branches"."address",
--        "branches"."city",
--        "branches"."district",
--        "branches"."state",
--        "branches"."branch_vector",
--        ts_rank((((to_tsvector(COALESCE("branches"."city", '')) || to_tsvector(COALESCE("branches"."state", ''))) || to_tsvector(COALESCE("branches"."address", ''))) || to_tsvector(COALESCE("branches"."branch", ''))), plainto_tsquery('NEW')) AS "rank"
--   FROM "branches"
--  WHERE "branches"."city" = 'DELHI'
--  ORDER BY "rank" DESC
--  LIMIT 40;
-- 
-- CREATE INDEX BANK_ID_IDX ON banks USING gin(id);
-- 
-- explain ANALYSE SELECT * FROM banks;

select * from banks;