DROP MATERIALIZED VIEW IF EXISTS kdigo_creat CASCADE;
CREATE MATERIALIZED VIEW kdigo_creat as with cr as (
    select ie.icustay_id,
        ie.intime,
        ie.outtime,
        le.valuenum as creat,
        le.charttime
    from icustays ie
        left join labevents le on ie.subject_id = le.subject_id
        and le.ITEMID = 50912 -- Creatinine,Creatinine,,verify,,50912,CREATININE,,labevents,797476,CHEMISTRY,,BLOOD,2160-0,,,,
        and le.VALUENUM is not null
        and le.CHARTTIME between (ie.intime - interval '7' day)
        and (ie.intime + interval '7' day)
)
SELECT cr.icustay_id,
    cr.charttime,
    cr.creat,
    MIN(cr48.creat) AS creat_low_past_48hr,
    MIN(cr7.creat) AS creat_low_past_7day
FROM cr
    LEFT JOIN cr cr48 ON cr.icustay_id = cr48.icustay_id
    AND cr48.charttime < cr.charttime
    AND cr48.charttime >= (cr.charttime - INTERVAL '48' HOUR)
    LEFT JOIN cr cr7 ON cr.icustay_id = cr7.icustay_id
    AND cr7.charttime < cr.charttime
    AND cr7.charttime >= (cr.charttime - INTERVAL '7' DAY)
GROUP BY cr.icustay_id,
    cr.charttime,
    cr.creat
ORDER BY cr.icustay_id,
    cr.charttime,
    cr.creat;