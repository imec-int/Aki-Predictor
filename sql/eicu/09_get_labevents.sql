-- This query pivots lab values taken during the 7 first days of  a patient's stay
-- Have already confirmed that the unit of measurement is always the same: null or the correct unit
-- Extract all bicarbonate, blood urea nitrogen (BUN), calcium, chloride, creatinine, 
-- hemoglobin, international normalized ratio (INR), platelet, potassium, prothrombin time (PT), 
-- partial throm- boplastin time (PTT), and white blood count (WBC) values from labevents around patient's ICU stay
DROP MATERIALIZED VIEW IF EXISTS labstay CASCADE;
CREATE materialized VIEW labstay AS
SELECT pvt.subject_id,
    pvt.hadm_id,
    pvt.icustay_id,
    min(
        CASE
            WHEN label = 'ANION GAP' THEN valuenum
            ELSE null
        END
    ) as ANIONGAP_min,
    max(
        CASE
            WHEN label = 'ANION GAP' THEN valuenum
            ELSE null
        END
    ) as ANIONGAP_max,
    min(
        CASE
            WHEN label = 'ALBUMIN' THEN valuenum
            ELSE null
        END
    ) as ALBUMIN_min,
    max(
        CASE
            WHEN label = 'ALBUMIN' THEN valuenum
            ELSE null
        END
    ) as ALBUMIN_max,
    min(
        CASE
            WHEN label = 'BANDS' THEN valuenum
            ELSE null
        END
    ) as BANDS_min,
    max(
        CASE
            WHEN label = 'BANDS' THEN valuenum
            ELSE null
        END
    ) as BANDS_max,
    min(
        CASE
            WHEN label = 'BICARBONATE' THEN valuenum
            ELSE null
        END
    ) as BICARBONATE_min,
    max(
        CASE
            WHEN label = 'BICARBONATE' THEN valuenum
            ELSE null
        END
    ) as BICARBONATE_max,
    min(
        CASE
            WHEN label = 'BILIRUBIN' THEN valuenum
            ELSE null
        END
    ) as BILIRUBIN_min,
    max(
        CASE
            WHEN label = 'BILIRUBIN' THEN valuenum
            ELSE null
        END
    ) as BILIRUBIN_max,
    min(
        CASE
            WHEN label = 'CREATININE' THEN valuenum
            ELSE null
        END
    ) as CREATININE_min,
    max(
        CASE
            WHEN label = 'CREATININE' THEN valuenum
            ELSE null
        END
    ) as CREATININE_max,
    min(
        CASE
            WHEN label = 'CHLORIDE' THEN valuenum
            ELSE null
        END
    ) as CHLORIDE_min,
    max(
        CASE
            WHEN label = 'CHLORIDE' THEN valuenum
            ELSE null
        END
    ) as CHLORIDE_max,
    min(
        CASE
            WHEN label = 'GLUCOSE' THEN valuenum
            ELSE null
        END
    ) as GLUCOSE_min,
    max(
        CASE
            WHEN label = 'GLUCOSE' THEN valuenum
            ELSE null
        END
    ) as GLUCOSE_max,
    avg(
        CASE
            WHEN label = 'GLUCOSE' THEN valuenum
            ELSE NULL
        END
    ) as GLUCOSE_mean,
    min(
        CASE
            WHEN label = 'HEMATOCRIT' THEN valuenum
            ELSE null
        END
    ) as HEMATOCRIT_min,
    max(
        CASE
            WHEN label = 'HEMATOCRIT' THEN valuenum
            ELSE null
        END
    ) as HEMATOCRIT_max,
    min(
        CASE
            WHEN label = 'HEMOGLOBIN' THEN valuenum
            ELSE null
        END
    ) as HEMOGLOBIN_min,
    max(
        CASE
            WHEN label = 'HEMOGLOBIN' THEN valuenum
            ELSE null
        END
    ) as HEMOGLOBIN_max,
    min(
        CASE
            WHEN label = 'LACTATE' THEN valuenum
            ELSE null
        END
    ) as LACTATE_min,
    max(
        CASE
            WHEN label = 'LACTATE' THEN valuenum
            ELSE null
        END
    ) as LACTATE_max,
    min(
        CASE
            WHEN label = 'PLATELET' THEN valuenum
            ELSE null
        END
    ) as PLATELET_min,
    max(
        CASE
            WHEN label = 'PLATELET' THEN valuenum
            ELSE null
        END
    ) as PLATELET_max,
    min(
        CASE
            WHEN label = 'POTASSIUM' THEN valuenum
            ELSE null
        END
    ) as POTASSIUM_min,
    max(
        CASE
            WHEN label = 'POTASSIUM' THEN valuenum
            ELSE null
        END
    ) as POTASSIUM_max,
    min(
        CASE
            WHEN label = 'PTT' THEN valuenum
            ELSE null
        END
    ) as PTT_min,
    max(
        CASE
            WHEN label = 'PTT' THEN valuenum
            ELSE null
        END
    ) as PTT_max,
    min(
        CASE
            WHEN label = 'INR' THEN valuenum
            ELSE null
        END
    ) as INR_min,
    max(
        CASE
            WHEN label = 'INR' THEN valuenum
            ELSE null
        END
    ) as INR_max,
    min(
        CASE
            WHEN label = 'PT' THEN valuenum
            ELSE null
        END
    ) as PT_min,
    max(
        CASE
            WHEN label = 'PT' THEN valuenum
            ELSE null
        END
    ) as PT_max,
    min(
        CASE
            WHEN label = 'SODIUM' THEN valuenum
            ELSE null
        END
    ) as SODIUM_min,
    max(
        CASE
            WHEN label = 'SODIUM' THEN valuenum
            ELSE null
        end
    ) as SODIUM_max,
    min(
        CASE
            WHEN label = 'BUN' THEN valuenum
            ELSE null
        end
    ) as BUN_min,
    max(
        CASE
            WHEN label = 'BUN' THEN valuenum
            ELSE null
        end
    ) as BUN_max,
    min(
        CASE
            WHEN label = 'WBC' THEN valuenum
            ELSE null
        end
    ) as WBC_min,
    max(
        CASE
            WHEN label = 'WBC' THEN valuenum
            ELSE null
        end
    ) as WBC_max
FROM (
        SELECT ie.patientHealthSystemStayID AS subject_id, -- in eICU only hospital stays are identified, not patients
            ie.patientHealthSystemStayID AS hadm_id,
            ie.patientUnitStayID AS icustay_id,
            CASE
                WHEN labName = 'anion gap' THEN 'ANION GAP'
                WHEN labName = 'albumin' THEN 'ALBUMIN'
                WHEN labName = '-bands' THEN 'BANDS'
                WHEN labName = 'bicarbonate' THEN 'BICARBONATE'
                WHEN labName = 'total bilirubin' THEN 'BILIRUBIN'
                WHEN labName = 'creatinine' THEN 'CREATININE'
                WHEN labName = 'chloride' THEN 'CHLORIDE'
                --WHEN labName = 'chloride' THEN 'CHLORIDE'
                WHEN labName = 'glucose' THEN 'GLUCOSE'
                --WHEN labName = 'glucose' THEN 'GLUCOSE'
                WHEN labName = 'Hct' THEN 'HEMATOCRIT'
                --WHEN labName = 'Hct' THEN 'HEMATOCRIT'
                WHEN labName = 'Hgb' THEN 'HEMOGLOBIN'
                --WHEN labName = 'Hgb' THEN 'HEMOGLOBIN'
                WHEN labName = 'lactate' THEN 'LACTATE'
                WHEN labName = 'platelets x 1000' THEN 'PLATELET'
                WHEN labName = 'potassium' THEN 'POTASSIUM'
                --WHEN labName = 'potassium' THEN 'POTASSIUM'
                WHEN labName = 'PTT' THEN 'PTT'
                WHEN labName = 'PT - INR' THEN 'INR'
                WHEN labName = 'PT' THEN 'PT'
                WHEN labName = 'sodium' THEN 'SODIUM'
                -- WHEN labName = 'sodium' THEN 'SODIUM'
                WHEN labName = 'BUN' THEN 'BUN'
                WHEN labName = 'WBC x 1000' THEN 'WBC'
                --WHEN labName = 'WBC x 1000' THEN 'WBC'
                ELSE null
            END AS label,
            CASE
                WHEN labName = 'albumin' --50862
                 and labResult > 10 THEN null
                WHEN labName = 'anion gap' --50868
                 and labResult > 10000 THEN null
                WHEN labName = '-bands' --51144
                 and labResult < 0 THEN null
                WHEN labName = '-bands' --51144
                 and labResult > 100 THEN null
                WHEN labName = 'bicarbonate' --50882
                 and labResult > 10000 THEN null
                WHEN labName = 'total bilirubin' --50885
                 and labResult > 150 THEN null
                WHEN labName = 'chloride' --50806
                 and labResult > 10000 THEN null
                -- also chloride WHEN labName = 50902
                -- also chloride  and labResult > 10000 THEN null
                WHEN labName = 'creatinine' --50912
                 and labResult > 150 THEN null
                WHEN labName = 'glucose' --50809
                 and labResult > 10000 THEN null
                -- also glucose WHEN labName = 50931
                -- also glucose  and labResult > 10000 THEN null
                WHEN labName = 'Hct' --50810
                 and labResult > 100 THEN null
                -- also Hct WHEN labName = 51221
                -- also Hct  and labResult > 100 THEN null
                WHEN labName = 'Hgb' --50811
                 and labResult > 50 THEN null
                -- also Hgb WHEN labName = 51222
                -- also Hgb  and labResult > 50 THEN null
                WHEN labName = 'lactate' --50813
                 and labResult > 50 THEN null
                WHEN labName = 'platelets x 1000' --51265
                 and labResult > 10000 THEN null
                WHEN labName = 'potassium' --50822
                 and labResult > 30 THEN null
                -- also potassium WHEN labName = 50971
                -- also potassium  and labResult > 30 THEN null
                WHEN labName = 'PTT' --51275
                 and labResult > 150 THEN null
                WHEN labName = 'PT - INR' --51237
                 and labResult > 50 THEN null
                WHEN labName = 'PT' --51274
                 and labResult > 150 THEN null
                WHEN labName = 'sodium' --50824
                 and labResult > 200 THEN null
                -- also sodium WHEN labName = 50983
                -- also sodium  and labResult > 200 THEN null
                WHEN labName = 'BUN' --51006
                 and labResult > 300 THEN null
                WHEN labName = 'WBC x 1000' --51300
                 and labResult > 1000 THEN null
                -- also WCB x 1000 WHEN labName = 51301
                -- also WCB x 1000  and labResult > 1000 THEN null
                ELSE le.labResult
            END AS valuenum
        FROM patient ie
            LEFT JOIN patient anyStayOfPat ON ie.patientHealthSystemStayID = anyStayOfPat.patientHealthSystemStayID -- in mimic we can group data on a patient level, here we can only group on a hospital stay level
            LEFT JOIN lab le ON anyStayOfPat.patientUnitStayID = le.patientUnitStayID -- mimic doesn't associate lab events to unit stays, so we also select lab data from all unit stays of the patient
                                --AND le.hadm_id = ie.hadm_id not needed, patientUnitStayID is enough
                                AND le.labResultOffset - anyStayOfPat.hospitalAdmitOffset between -6*60-ie.hospitalAdmitOffset
                                                                                              and 7*24*60-ie.hospitalAdmitOffset -- correct for the time difference (base for the labResultOffset) between the 'ie' stay and anyStayOfPat
                                AND le.labName in (
                                    'anion gap',        --50868,
                                    'albumin',          --50862,
                                    '-bands',           --51144,
                                    'bicarbonate',      --50882,
                                    'total bilirubin',  --50885,
                                    'creatinine',       --50912,
                                    'chloride',         --50902,
                                    -- also 'chloride'    50806,
                                    'glucose',          --50931,
                                    -- also 'glucose'     50809,
                                    'Hct',              --51221,
                                    -- also 'Hct'         50810,
                                    'Hgb',              --51222,
                                    -- also 'Hgb'         50811,
                                    'lactate',          --50813,
                                    'platelets x 1000', --51265,
                                    'potassium',        --50971,
                                    -- also 'potassium'   50822,
                                    'PTT',              --51275,
                                    'PT - INR',         --51237,
                                    'PT',               --51274,
                                    'sodium',           --50983,
                                    -- also 'sodium'      50824,
                                    'BUN',              --51006,
                                    'WBC x 1000'        --51301,
                                    -- also 'WBC x 1000'  51300
                                )
                                AND le.labResult IS NOT null
                                AND le.labResult > 0
    ) pvt
GROUP BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id
ORDER BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id;