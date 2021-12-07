-- weight duration
DROP MATERIALIZED VIEW IF EXISTS weightdurations CASCADE;
CREATE MATERIALIZED VIEW weightdurations as WITH htwt as (
    SELECT patientunitstayid,
        hospitaladmitoffset as starttime,
        -- entry in the ICU
        unitDischargeOffset as endtime,
        admissionheight as height,
        admissionweight as weight,
        CASE
            -- CHECK weight vs. height are swapped
            WHEN admissionweight >= 100
            AND admissionheight > 25
            AND admissionheight <= 100
            AND abs(admissionheight - admissionweight) >= 20 THEN 'swap'
        END AS method
    FROM eicu_crd.patient
),
htwt_fixed as (
    SELECT patientunitstayid,
        starttime,
        endtime,
        'admit' as weight_type,
        CASE
            WHEN method = 'swap' THEN weight
            WHEN height <= 0.30 THEN NULL
            WHEN height <= 2.5 THEN height * 100
            WHEN height <= 10 THEN NULL
            WHEN height <= 25 THEN height * 10 -- CHECK weight in both columns
            WHEN height <= 100
            AND abs(height - weight) < 20 THEN NULL
            WHEN height > 250 THEN NULL
            ELSE height
        END as height_fixed,
        CASE
            WHEN method = 'swap' THEN height
            WHEN weight <= 20 THEN NULL
            WHEN weight > 300 THEN NULL
            ELSE weight
        END as weight_fixed
    from htwt
) 
-- we removed wt1 as there's no valid data being returned
,
wt2 as (
--     -- there's no direct start- and endtime, yet only an offset. We could add this offset to the intake time of patient table?
select patientunitstayid,
    intakeoutputoffset as intake_starttime,
    intakeOutputEntryOffset,
    --    when intake values are noted in the ICU,    I expect this to be > patient.chartoffset 
    coalesce(
        LEAD(intakeoutputoffset) OVER (
        PARTITION BY patientunitstayid
        ORDER BY intakeoutputoffset
        ), intakeOutputEntryOffset --TODO not sure if this is a correct choice for endtime
     ) as intake_endtime,
    'daily' as weight_type,
    MAX(
        CASE
            WHEN cellpath = 'flowsheet|Flowsheet Cell Labels|I&O|Weight|Bodyweight (kg)' then cellvaluenumeric
            else NULL
        END
    ) AS weight_kg -- there are ~300 extra (lb) measurements compared to kg, so we include both
,
    MAX(
        CASE
            WHEN cellpath = 'flowsheet|Flowsheet Cell Labels|I&O|Weight|Bodyweight (lb)' then cellvaluenumeric * 0.453592
            else NULL
        END
    ) AS weight_kg2
FROM eicu_crd.intakeoutput
WHERE CELLPATH IN (
        'flowsheet|Flowsheet Cell Labels|I&O|Weight|Bodyweight (kg)',
        'flowsheet|Flowsheet Cell Labels|I&O|Weight|Bodyweight (lb)'
    )
    and INTAKEOUTPUTOFFSET < 60 * 24
GROUP BY patientunitstayid,
    intakeoutputoffset,
    intakeOutputEntryOffset
),

wt2fx as (
    -- we combine the intake start and endtimes with the patient starttime
    SELECT wt.patientunitstayid,
        -- wt.intakeOutputEntryOffset,
        hw.starttime + wt.intake_starttime as starttime,
        hw.starttime + wt.intake_endtime as endtime,
        wt.weight_type,
        wt.weight_kg,
        wt.weight_kg2
    FROM wt2 wt
        INNER JOIN htwt hw ON hw.patientunitstayid = wt.patientunitstayid
) 
-- we removed wt3 as there's no valid data being returned

-- combine together all weights  
SELECT patientunitstayid,
    -- NULL as intakeOutputEntryOffset,
    starttime,
    endtime,
    weight_type,
    weight_fixed as weight,
    'patient' as source_table
FROM htwt_fixed
WHERE weight_fixed IS NOT NULL
UNION ALL
-- SELECT patientunitstayid,
--     chartoffset,
--     'nursecharting' as source_table,
--     weight_type,
--     weight
-- FROM wt1
-- WHERE weight IS NOT NULL
-- UNION ALL
SELECT patientunitstayid,
    -- intakeOutputEntryOffset,
    starttime,
    endtime,
    weight_type,
    COALESCE(weight_kg, weight_kg2) as weight,
    'intakeoutput' as source_table
FROM wt2fx
WHERE weight_kg IS NOT NULL
    OR weight_kg2 IS NOT NULL -- UNION ALL
    -- SELECT patientunitstayid,
    --     chartoffset,
    --     'infusiondrug' as source_table,
    --     weight_type,
    --     weight
    -- FROM wt3
    -- WHERE weight IS NOT NULL
ORDER BY 1,
    2,
    3;