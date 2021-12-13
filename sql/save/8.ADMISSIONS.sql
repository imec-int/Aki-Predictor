SELECT a.*, p.*, s.*, --TODO which fields are actually used?
  EXTRACT(epoch FROM (a.dischtime - a.admittime))/3600 AS staytime,
  CASE
    WHEN EXTRACT(year FROM a.admittime) - EXTRACT(year FROM p.dob) NOT BETWEEN 0 AND 89 THEN 90
	ELSE EXTRACT(year FROM a.admittime) - EXTRACT(year FROM p.dob)
  END AS age,
  EXTRACT(epoch FROM (s.intime - a.admittime))/3600 AS timegoicu,
  EXTRACT(epoch FROM (s.outtime - s.intime))/3600 AS timeinicu,
  EXTRACT(epoch FROM (a.dischtime - s.outtime))/3600 AS timeaftergoicu,
  staysgroups.nbstays AS counttimesgoicu
FROM admissions a
  LEFT JOIN patients p USING (subject_id)
  RIGHT JOIN icustays s USING (hadm_id)
  LEFT JOIN (
  	SELECT hadm_id, COUNT(*) AS nbstays
	FROM icustays
	GROUP BY hadm_id, icustay_id
  ) staysgroups USING (hadm_id);