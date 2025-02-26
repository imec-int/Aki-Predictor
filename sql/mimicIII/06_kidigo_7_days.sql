-- This query checks if the patient had AKI during the first 7 days of their ICU
-- stay according to the KDIGO guideline.
-- https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf
DROP MATERIALIZED VIEW IF EXISTS kdigo_stages_7day;
CREATE MATERIALIZED VIEW kdigo_stages_7day AS WITH cr_aki AS (
    SELECT k.icustay_id,
        k.charttime,
        k.creat,
        k.aki_stage_creat,
        ROW_NUMBER() OVER (
            PARTITION BY k.icustay_id
            ORDER BY k.aki_stage_creat DESC,
                k.creat DESC
        ) AS rn
    FROM icustays ie
        INNER JOIN kdigo_stages k ON ie.icustay_id = k.icustay_id
    WHERE k.charttime > (ie.intime - interval '6' hour)
        AND k.charttime <= (ie.intime + interval '7' day)
        AND k.aki_stage_creat IS NOT NULL
),
uo_aki AS (
    SELECT k.icustay_id,
        k.charttime,
        k.uo_rt_6hr,
        k.uo_rt_12hr,
        k.uo_rt_24hr,
        k.aki_stage_uo,
        ROW_NUMBER() OVER (
            PARTITION BY k.icustay_id
            ORDER BY k.aki_stage_uo DESC,
                k.uo_rt_24hr DESC,
                k.uo_rt_12hr DESC,
                k.uo_rt_6hr DESC
        ) AS rn
    FROM icustays ie
        INNER JOIN kdigo_stages k ON ie.icustay_id = k.icustay_id
    WHERE k.charttime > (ie.intime - interval '6' hour)
        AND k.charttime <= (ie.intime + interval '7' day)
        AND k.aki_stage_uo IS NOT NULL
)
select ie.icustay_id,
    cr.charttime as charttime_creat,
    cr.creat,
    cr.aki_stage_creat,
    uo.charttime as charttime_uo,
    uo.uo_rt_6hr,
    uo.uo_rt_12hr,
    uo.uo_rt_24hr,
    uo.aki_stage_uo,
    GREATEST(cr.aki_stage_creat, uo.aki_stage_uo) AS aki_stage_7day,
    CASE
        WHEN GREATEST(cr.aki_stage_creat, uo.aki_stage_uo) > 0 THEN 1
        ELSE 0
    END AS aki_7day
FROM icustays ie
    LEFT JOIN cr_aki cr ON ie.icustay_id = cr.icustay_id
    AND cr.rn = 1
    LEFT JOIN uo_aki uo ON ie.icustay_id = uo.icustay_id
    AND uo.rn = 1
order by ie.icustay_id;