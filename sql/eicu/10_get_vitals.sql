-- This query pivots the vital signs during the first 7 days of a patient's stay
-- Vital signs include heart rate, blood pressure, respiration rate, and temperature
DROP MATERIALIZED VIEW IF EXISTS vitalsfirstday CASCADE;
  create materialized view vitalsfirstday as  
SELECT pvt.subject_id,
    pvt.hadm_id,
    pvt.icustay_id,
    min(HeartRate) as HeartRate_Min,
    max(HeartRate) as HeartRate_Max,
    avg(HeartRate) as HeartRate_Mean,
    min(SysBP) as SysBP_Min,
    max(SysBP) as SysBP_Max,
    avg(SysBP) as SysBP_Mean,
    min(DiasBP) as DiasBP_Min,  
    max(DiasBP) as DiasBP_Max,
    avg(DiasBP) as DiasBP_Mean,
    min(MeanBP) as MeanBP_Min,
    max(MeanBP) as MeanBP_Max,
    avg(MeanBP) as MeanBP_Mean,
    min(RespRate) as RespRate_Min,
    max(RespRate) as RespRate_Max,
    avg(RespRate) as RespRate_Mean,
    min(TempC) as TempC_Min,
    max(TempC) as TempC_Max,
    avg(TempC) as TempC_Mean,
    min(SpO2) as SpO2_Min,
    max(SpO2) as SpO2_Max,
    avg(SpO2) as SpO2_Mean,
    -- NULL as Glucose_Min, --TODO glucose
    -- NULL as Glucose_Max --TODO glucose
    -- NULL as Glucose_Mean --TODO glucose
FROM (
         
        SELECT ie.patientHealthSystemStayID AS subject_id, -- in eICU only hospital stays are identified, not patients
            ie.patientHealthSystemStayID AS hadm_id,
            ie.patientUnitStayID AS icustay_id,
            ce.heartRate AS HeartRate,
            CASE
                WHEN ce.systemicSystolic < 0 THEN NULL
                ELSE ce.systemicSystolic
            END AS SysBP,
            CASE
                WHEN ce.systemicDiastolic < 0 THEN NULL
                ELSE ce.systemicDiastolic
            END AS DiasBP,
            CASE
                WHEN ce.systemicMean < 0 THEN NULL
                ELSE ce.systemicMean
            END AS MeanBP,
            CASE
                WHEN ce.respiration > 1000 THEN NULL
                ELSE ce.respiration
            END AS RespRate,
            CASE
                WHEN ce.temperature > 45 THEN NULL
                WHEN ce.temperature < 15 THEN NULL
                ELSE ce.temperature
            END AS TempC,
            ce.saO2 AS SpO2 -- this is actually not correct, but close enough
            --TODO glucose from lab?
        FROM patient ie
            LEFT JOIN vitalperiodic ce ON ie.patientUnitStayID = ce.patientUnitStayID
                                          --AND ce.hadm_id = ie.hadm_id not needed, patientUnitStayID is enough
                                          --and anyStayOfPat.patientUnitStayID = ce.patientUnitStayID
                                          AND ce.observationOffset between -6*60
                                                                       and 7*24*60
                                          --and ce.error IS DISTINCT
                                          --             FROM 1
        --where ce.itemid in (...) in eICU columns are used to differentiate between signals instead of using multiple key-value rows
    ) pvt  
GROUP BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id  
ORDER BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id;