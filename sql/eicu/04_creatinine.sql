DROP MATERIALIZED VIEW IF EXISTS kdigo_creat CASCADE;
CREATE MATERIALIZED VIEW kdigo_creat  AS
WITH cr as (
    select ie.patientUnitStayID AS icustay_id,
        --ie.intime,  actually not used
        --ie.outtime, actually not used
        le.labResult AS creat,
        le.labResultOffset - anyStayOfPat.hospitalAdmitOffset AS charttime -- charttime is relative to hospital admin (in minutes), which is okay as long as compared only with charttimes of the same patient/hospital stay
    from patient ie
         left join patient anyStayOfPat on ie.patientHealthSystemStayID = anyStayOfPat.patientHealthSystemStayID -- in mimic we can group data on a patient level, here we can only group on a hospital stay level
         left join lab le on anyStayOfPat.patientUnitStayID = le.patientUnitStayID -- mimic doesn't associate lab events to unit stays, so we also select lab data from all stays of the patient
                             and le.labName = 'creatinine'
                             and le.labResult is not null
                             and le.labResultOffset - anyStayOfPat.hospitalAdmitOffset between -7*24*60-ie.hospitalAdmitOffset AND 7*24*60-ie.hospitalAdmitOffset -- correct for the time difference (base for the labResultOffset) between the 'ie' stay and anyStayOfPat
)
SELECT cr.icustay_id,
    cr.charttime,
    cr.creat,
    MIN(cr48.creat) AS creat_low_past_48hr,
    MIN(cr7.creat) AS creat_low_past_7day
FROM cr
    LEFT JOIN cr cr48 ON cr.icustay_id = cr48.icustay_id
                         AND cr48.charttime < cr.charttime --TODO this results in null values in the column creat_low_past_48hr for the rows where cr.creat is the lowest value for the unit stay, is this correct behaviour?
                         AND cr48.charttime >= (cr.charttime - 48*60)
    LEFT JOIN cr cr7 ON cr.icustay_id = cr7.icustay_id
                        AND cr7.charttime < cr.charttime --TODO this results in null values in the column creat_low_past_7day for the rows where cr.creat is the lowest value for the unit stay, is this correct behaviour?
                        AND cr7.charttime >= (cr.charttime - 7*24*60)
GROUP BY cr.icustay_id, cr.charttime, cr.creat
ORDER BY cr.icustay_id, cr.charttime, cr.creat;