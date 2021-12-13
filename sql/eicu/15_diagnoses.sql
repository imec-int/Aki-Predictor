DROP MATERIALIZED VIEW IF EXISTS DIAGNOSES_VIEW CASCADE;
CREATE MATERIALIZED VIEW DIAGNOSES_VIEW AS
SELECT d.patientUnitStayId AS subject_id,
  p.patientHealthSystemStayID AS hadm_id,
  REPLACE(SUBSTRING(d.icd9code, '[(0-9\.]*'), '.', '') AS icd9_code
  --seq_num not used
FROM diagnosis d
  LEFT JOIN patient p USING (patientUnitStayId)
WHERE icd9code IS NOT NULL
  AND icd9code != '';