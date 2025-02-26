-- This query extracts weights for ICU patients with start/stop times 
-- if only an admission weight is given, then this is assigned from intime to outtime 
DROP MATERIALIZED VIEW IF EXISTS weightdurations CASCADE;
CREATE MATERIALIZED VIEW weightdurations as WITH 
wt_neonate AS (
    SELECT c.icustay_id,
        c.charttime,
        MAX(
            CASE
                WHEN c.itemid = 3580 THEN c.valuenum
            END
        ) as wt_kg,
        MAX(
            CASE
                WHEN c.itemid = 3581 THEN c.valuenum
            END
        ) as wt_lb,
        MAX(
            CASE
                WHEN c.itemid = 3582 THEN c.valuenum
            END
        ) as wt_oz
    FROM chartevents c
    WHERE c.itemid in (3580, 3581, 3582)
        AND c.icustay_id IS NOT NULL
        AND c.error IS DISTINCT
    FROM 1
        AND c.valuenum > 0
    GROUP BY c.icustay_id,
        c.charttime
),
birth_wt AS (
    SELECT c.icustay_id,
        c.charttime,
        MAX(
            CASE
                WHEN c.itemid = 4183 THEN CASE
                    WHEN c.value ~ '[^0-9 .]' THEN NULL
                    WHEN CAST(c.value AS NUMERIC) > 100 THEN CAST(c.value AS NUMERIC) / 1000
                    WHEN CAST(c.value AS NUMERIC) < 10 THEN CAST(c.value AS NUMERIC)
                    ELSE NULL
                END
                WHEN c.itemid = 3723
                AND c.valuenum < 10 THEN c.valuenum
                ELSE NULL
            END
        ) as wt_kg
    FROM chartevents c
    WHERE c.itemid in (3723, 4183)
        AND c.icustay_id IS NOT NULL
        AND c.error IS DISTINCT
    FROM 1
    GROUP BY c.icustay_id,
        c.charttime
),
wt_stg as (
    SELECT c.icustay_id,
        c.charttime,
        case
            when c.itemid in (762, 226512) then 'admit'
            else 'daily'
        end as weight_type,
        c.valuenum as weight
    FROM chartevents c
    WHERE c.valuenum IS NOT NULL
        AND c.itemid in (
            762,
            226512,
            763,
            224639
        )
        AND c.icustay_id IS NOT NULL
        AND c.valuenum > 0
        AND c.error IS DISTINCT
    FROM 1
    UNION ALL
    SELECT n.icustay_id,
        n.charttime,
        'daily' AS weight_type,
        CASE
            WHEN wt_kg IS NOT NULL THEN wt_kg
            WHEN wt_lb IS NOT NULL THEN wt_lb * 0.45359237 + wt_oz * 0.0283495231
            ELSE NULL
        END AS weight
    FROM wt_neonate n
    UNION ALL
    SELECT b.icustay_id,
        b.charttime,
        'admit' AS weight_type,
        wt_kg as weight
    FROM birth_wt b
),
wt_stg1 as (
    select icustay_id,
        charttime,
        weight_type,
        weight,
        ROW_NUMBER() OVER (
            partition by icustay_id,
            weight_type
            order by charttime
        ) as rn
    from wt_stg
    WHERE weight IS NOT NULL
),
wt_stg2 AS (
    SELECT wt_stg1.icustay_id,
        ie.intime,
        ie.outtime,
        case
            when wt_stg1.weight_type = 'admit'
            and wt_stg1.rn = 1 then ie.intime - interval '2' hour
            else wt_stg1.charttime
        end as starttime,
        wt_stg1.weight
    from wt_stg1
        INNER JOIN icustays ie on ie.icustay_id = wt_stg1.icustay_id
),
wt_stg3 as (
    select icustay_id,
        intime,
        outtime,
        starttime,
        coalesce(
            LEAD(starttime) OVER (
                PARTITION BY icustay_id
                ORDER BY starttime
            ),
            outtime + interval '2' hour
        ) as endtime,
        weight
    from wt_stg2
),
wt1 as (
    select icustay_id,
        starttime,
        coalesce(
            endtime,
            LEAD(starttime) OVER (
                partition by icustay_id
                order by starttime
            ),
            outtime + interval '2' hour
        ) as endtime,
        weight
    from wt_stg3
),
wt_fix as (
    select ie.icustay_id,
        ie.intime - interval '2' hour as starttime,
        wt.starttime as endtime,
        wt.weight
    from icustays ie
        inner join (
            SELECT wt1.icustay_id,
                wt1.starttime,
                wt1.weight,
                ROW_NUMBER() OVER (
                    PARTITION BY wt1.icustay_id
                    ORDER BY wt1.starttime
                ) as rn
            FROM wt1
        ) wt ON ie.icustay_id = wt.icustay_id
        AND wt.rn = 1
        and ie.intime < wt.starttime
),
wt2 as (
    select wt1.icustay_id,
        wt1.starttime,
        wt1.endtime,
        wt1.weight
    from wt1
    UNION
    SELECT wt_fix.icustay_id,
        wt_fix.starttime,
        wt_fix.endtime,
        wt_fix.weight
    from wt_fix
),
echo_lag as (
    select ie.icustay_id,
        ie.intime,
        ie.outtime,
        0.453592 * ec.weight as weight_echo,
        ROW_NUMBER() OVER (
            PARTITION BY ie.icustay_id
            ORDER BY ec.charttime
        ) as rn,
        ec.charttime as starttime,
        LEAD(ec.charttime) OVER (
            PARTITION BY ie.icustay_id
            ORDER BY ec.charttime
        ) as endtime
    from icustays ie
        inner join echo_data ec on ie.hadm_id = ec.hadm_id
    where ec.weight is not null
),
echo_final as (
    select el.icustay_id,
        el.starttime,
        coalesce(el.endtime, el.outtime + interval '2' hour) as endtime,
        weight_echo
    from echo_lag el
    UNION
    select el.icustay_id,
        el.intime - interval '2' hour as starttime,
        el.starttime as endtime,
        el.weight_echo
    from echo_lag el
    where el.rn = 1
        and el.starttime > el.intime - interval '2' hour
)
select wt2.icustay_id,
    wt2.starttime,
    wt2.endtime,
    wt2.weight
from wt2
UNION
select ef.icustay_id,
    ef.starttime,
    ef.endtime,
    ef.weight_echo as weight
from echo_final ef
where ef.icustay_id not in (
        select distinct icustay_id
        from wt2
    )
order by icustay_id,
    starttime,
    endtime;