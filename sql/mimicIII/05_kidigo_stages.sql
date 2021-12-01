-- This query checks if the patient had AKI according to KDIGO.
-- AKI is calculated every time a creatinine or urine output measurement occurs.
-- Baseline creatinine is defined as the lowest creatinine in the past 7 days.
DROP MATERIALIZED VIEW IF EXISTS kdigo_stages CASCADE;
CREATE MATERIALIZED VIEW kdigo_stages AS with cr_stg AS (
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
uo_stg as (
    select uo.icustay_id,
        uo.charttime,
        uo.weight,
        uo.uo_rt_6hr,
        uo.uo_rt_12hr,
        uo.uo_rt_24hr,
        CASE
            WHEN uo.uo_rt_6hr IS NULL THEN NULL
            WHEN uo.charttime <= ie.intime + interval '6' hour THEN 0
            WHEN uo.uo_tm_24hr >= 11
            AND uo.uo_rt_24hr < 0.3 THEN 3
            WHEN uo.uo_tm_12hr >= 5
            AND uo.uo_rt_12hr = 0 THEN 3
            WHEN uo.uo_tm_12hr >= 5
            AND uo.uo_rt_12hr < 0.5 THEN 2
            WHEN uo.uo_tm_6hr >= 2
            AND uo.uo_rt_6hr < 0.5 THEN 1
            ELSE 0
        END AS aki_stage_uo
    from kdigo_uo uo
        INNER JOIN icustays ie ON uo.icustay_id = ie.icustay_id
),
tm_stg AS (
    SELECT icustay_id,
        charttime
    FROM cr_stg
    UNION
    SELECT icustay_id,
        charttime
    FROM uo_stg
)
select ie.icustay_id,
    tm.charttime,
    cr.creat,
    cr.aki_stage_creat,
    uo.uo_rt_6hr,
    uo.uo_rt_12hr,
    uo.uo_rt_24hr,
    uo.aki_stage_uo,
    GREATEST(cr.aki_stage_creat, uo.aki_stage_uo) AS aki_stage
FROM icustays ie
    LEFT JOIN tm_stg tm ON ie.icustay_id = tm.icustay_id
    LEFT JOIN cr_stg cr ON ie.icustay_id = cr.icustay_id
    AND tm.charttime = cr.charttime
    LEFT JOIN uo_stg uo ON ie.icustay_id = uo.icustay_id
    AND tm.charttime = uo.charttime
order by ie.icustay_id,
    tm.charttime;