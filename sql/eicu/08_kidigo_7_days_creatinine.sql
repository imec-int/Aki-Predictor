-- This query checks if the patient had AKI during the first 7 days of their ICU
-- stay according to the KDIGO guideline.
-- https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf
DROP MATERIALIZED VIEW IF EXISTS kdigo_7_days_creatinine;
CREATE MATERIALIZED VIEW kdigo_7_days_creatinine AS WITH cr_aki AS (
    SELECT k.icustay_id,
            k.charttime,
            k.creat,
        k.aki_stage_creat,
        ROW_NUMBER() OVER (
            PARTITION BY k.icustay_id
            ORDER BY k.aki_stage_creat DESC,
                k.creat DESC
        ) AS rn
    FROM patient ie
        INNER JOIN kdigo_stages_creatinine k ON ie.patientUnitStayID = k.icustay_id
    WHERE k.charttime > - 6*60 - ie.hospitalAdmitOffset -- assuming kdigo_stage_creatinine.charttime is also relative to hospital admission and in minutes
        AND k.charttime <= 7*24*60 - ie.hospitalAdmitOffset
        AND k.aki_stage_creat IS NOT NULL
)
select ie.patientUnitStayID AS icustay_id,
    cr.charttime as charttime_creat,
    cr.creat,
    cr.aki_stage_creat,
    cr.aki_stage_creat AS aki_stage_7day,
    CASE
        WHEN (cr.aki_stage_creat > 0) THEN 1
        ELSE 0
    END AS aki_7day
FROM patient ie
    LEFT JOIN cr_aki cr ON ie.patientUnitStayID = cr.icustay_id
    AND cr.rn = 1
order by ie.patientUnitStayID;