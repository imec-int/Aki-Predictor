DROP MATERIALIZED VIEW IF EXISTS ADMISSIONS_VIEW CASCADE;
CREATE MATERIALIZED VIEW ADMISSIONS_VIEW AS
SELECT a.patientHealthSystemStayID AS subject_id, a.patientHealthSystemStayID AS hadm_id, -- no patientId/subjectId in eICU
  --a.admittime, a.dischtime, not actually used
  CASE
    WHEN a.ethnicity = 'African American' THEN 'BLACK/AFRICAN AMERICAN'
    WHEN a.ethnicity = 'Asian'            THEN 'ASIAN'
    WHEN a.ethnicity = 'Caucasian'        THEN 'WHITE'
    WHEN a.ethnicity = 'Hispanic'         THEN 'HISPANIC OR LATINO'
    WHEN a.ethnicity = 'Native American'  THEN 'AMERICAN INDIAN/ALASKA NATIVE'
    ELSE 'OTHER'
  END AS ethnicity,
  -- s.intime, s.outtime, s.los, not actually used
  CASE
    WHEN a.gender = 'Male' THEN 'M'
    WHEN a.gender = 'Female' THEN 'F'
    ELSE 'X'
  END AS gender,
  -- p.dob, not actually used
  -- EXTRACT(epoch FROM (a.dischtime - a.admittime))/3600 AS staytime, not actually used
  CASE
    WHEN age = '> 89' THEN 90
    WHEN age = '' OR age IS NULL THEN -1
	  ELSE age::INTEGER
  END AS age,
  -- EXTRACT(epoch FROM (s.intime - a.admittime))/3600 AS timegoicu, not actually used
  -- EXTRACT(epoch FROM (s.outtime - s.intime))/3600 AS timeinicu, not actually used
  -- EXTRACT(epoch FROM (a.dischtime - s.outtime))/3600 AS timeaftergoicu, not actually used
  staysgroups.nbstays AS counttimesgoicu
FROM patient a
  LEFT JOIN (
  	SELECT patientHealthSystemStayID, COUNT(*) AS nbstays
	FROM patient
	GROUP BY patientHealthSystemStayID, patientUnitStayID
  ) staysgroups USING (patientHealthSystemStayID)
WHERE a.gender IN ('Male', 'Female');