-- This query checks if the patient had AKI according to KDIGO.
-- AKI is calculated every time a creatinine or urine output measurement occurs.
-- Baseline creatinine is defined as the lowest creatinine in the past 7 days.
DROP MATERIALIZED VIEW IF EXISTS kdigo_stages_creatinine CASCADE;
CREATE MATERIALIZED VIEW kdigo_stages_creatinine AS with cr_stg AS (
    SELECT cr.icustay_id,
        cr.charttime,
        cr.creat,
        case
            when cr.creat >= (cr.creat_low_past_7day * 3.0) then 3
            when cr.creat >= 4
            and (
                cr.creat_low_past_48hr <= 3.7
                OR cr.creat >= (1.5 * cr.creat_low_past_7day)
            ) then 3
            when cr.creat >= (cr.creat_low_past_7day * 2.0) then 2
            when cr.creat >= (cr.creat_low_past_48hr + 0.3) then 1
            when cr.creat >= (cr.creat_low_past_7day * 1.5) then 1
            else 0
        end as aki_stage_creat
    FROM kdigo_creat cr
),
tm_stg AS (
    SELECT icustay_id,
        charttime
    FROM cr_stg
)
select ie.icustay_id,
    tm.charttime,
    cr.creat,
    cr.aki_stage_creat,
    cr.aki_stage_creat AS aki_stage
FROM icustays ie
    LEFT JOIN tm_stg tm ON ie.icustay_id = tm.icustay_id
    LEFT JOIN cr_stg cr ON ie.icustay_id = cr.icustay_id
    AND tm.charttime = cr.charttime
order by ie.icustay_id,
    tm.charttime;