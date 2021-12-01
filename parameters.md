# AKI Parameters

as it is unclear to me right now what the correct AKI parameters are, which are being used in the ExaScience model, I'll first investigate what the used parameters are and what could be their corresponding value in the eICU database

It seems that Exascience is using the [Kdigo Classification](https://kdigo.org)

I'm not sure yet if we have all data for enough participants and or how ExaScience worked with missing data. #TODO check with ExaScience

Important, our database is a postgreSQL dB, the [eicu code files](https://github.com/MIT-LCP/eicu-code/tree/master/concepts) are written for Google BigQuery, so small adaptions have to be made.


| AKI parameter            | description                    | category   | MIMIC III name                              | MIMIC III table(s)                 | eICU name                                  | eICU location | unit preferred |
| ------------------------ | ------------------------------ | ---------- | ------------------------------------------- | ---------------------------------- | ------------------------------------------ | ------------- | -------------- |
| AKI                      |                                | OUTPUT     |                                             |                                    |                                            |               |                |
| AKI_STAGE_7DAY           |                                | OUTPUT     |                                             |                                    |                                            |               |                |
| ETHNICITY                |                                |            |                                             | ADMISSIONS                         | ethnicity                                  | patient       | -              |
| AGE                      |                                |            | df['ADMITTIME'].dt.year - df['DOB'].dt.year | ADMITTIME: ADMISSIONS,DOB:PATIENTS | age                                        | patient       | -              |
| GENDER                   |                                |            | PATIENTS                                    |                                    | gender                                     | patient       | -              |
| HYPERTENSION             |                                |            |                                             |                                    |                                            |               |                |
| HYPOTHYROIDISM           |                                |            |                                             |                                    |                                            |               |                |
| CONGESTIVE_HEART_FAILURE |                                |            |                                             |                                    |                                            |               |                |
| CARDIAC_ARRHYTHMIAS      |                                |            |                                             |                                    |                                            |               |                |
| ALCOHOL_ABUSE            |                                |            |                                             |                                    |                                            |               |                |
| DRUG_ABUSE               |                                |            |                                             |                                    |                                            |               |                |
| VALVULAR_DISEASE         |                                |            |                                             |                                    |                                            |               |                |
| OBESITY                  |                                |            |                                             |                                    |                                            |               |                |
| PERIPHERAL_VASCULAR      |                                |            |                                             |                                    |                                            |               |                |
| DIABETES_COMPLICATED     |                                |            |                                             |                                    |                                            |               |                |
| LIVER_DISEASE            |                                |            |                                             |                                    |                                            |               |                |
| DIABETES_UNCOMPLICATED   |                                |            |                                             |                                    |                                            |               |                |
| RENAL_FAILURE            |                                |            |                                             |                                    |                                            |               |                |
| UO_RT_24HR               | urine output                   |            |                                             |                                    |                                            |               |                |
| UO_RT_12HR               | urine output                   |            |                                             |                                    |                                            |               |                |
| UO_RT_6HR                | urine output                   |            |                                             |                                    |                                            |               |                |
| CREAT                    | kidigo 7 days creatinine       | lab        | creat                                       |                                    |                                            | lab           |                |
| EGFR                     |                                |            | Estimated Glomerular Filtration Rate        |                                    |                                            |               |                |
| TEMPC_MIN                |                                | vitals     |                                             |                                    |                                            |               |                |
| TEMPC_MAX                |                                | vitals     |                                             |                                    |                                            |               |                |
| TEMPC_MEAN               |                                | vitals     |                                             |                                    |                                            |               |                |
| HEARTRATE_MIN            |                                | vitals     |                                             |                                    |                                            |               |                |
| HEARTRATE_MAX            |                                | vitals     |                                             |                                    |                                            |               |                |
| HEARTRATE_MEAN           |                                | vitals     |                                             |                                    |                                            |               |                |
| SPO2_MIN                 |                                | vitals     |                                             |                                    |                                            |               |                |
| SPO2_MAX                 |                                | vitals     |                                             |                                    |                                            |               |                |
| SPO2_MEAN                |                                | vitals     |                                             |                                    |                                            |               |                |
| MEANBP_MIN               |                                | vitals     |                                             |                                    |                                            |               |                |
| MEANBP_MAX               |                                | vitals     |                                             |                                    |                                            |               |                |
| MEANBP_MEAN              |                                | vitals     |                                             |                                    |                                            |               |                |
| DIASBP_MIN               |                                | vitals     |                                             |                                    |                                            |               |                |
| DIASBP_MAX               |                                | vitals     |                                             |                                    |                                            |               |                |
| DIASBP_MEAN              |                                | vitals     |                                             |                                    |                                            |               |                |
| RESPRATE_MIN             |                                | vitals     |                                             |                                    |                                            |               |                |
| RESPRATE_MAX             |                                | vitals     |                                             |                                    |                                            |               |                |
| RESPRATE_MEAN            |                                | vitals     |                                             |                                    |                                            |               |                |
| SYSBP_MIN                |                                | vitals     |                                             |                                    |                                            |               |                |
| SYSBP_MAX                |                                | vitals     |                                             |                                    |                                            |               |                |
| SYSBP_MEAN               |                                | vitals     |                                             |                                    |                                            |               |                |
| ALBUMIN_MIN              |                                | lab        |  valuenum, ITEMID IN (50862)                | LABEVENTS                          | labResult, labName IN ('albumin')          | lab           |                |
| ALBUMIN_MAX              |                                | lab        |  valuenum, ITEMID IN (50862)                | LABEVENTS                          | labResult, labName IN ('albumin')          | lab           |                |
| ANIONGAP_MIN             |                                | lab        |  valuenum, ITEMID IN (50868)                | LABEVENTS                          | labResult, labName IN ('anion gap')        | lab           |                |
| ANIONGAP_MAX             |                                | lab        |  valuenum, ITEMID IN (50868)                | LABEVENTS                          | labResult, labName IN ('anion gap')        | lab           |                |
| BANDS_MIN                |                                | lab        |  valuenum, ITEMID IN (51144)                | LABEVENTS                          | labResult, labName IN ('')                 | lab           |                |
| BANDS_MAX                |                                | lab        |  valuenum, ITEMID IN (51144)                | LABEVENTS                          | labResult, labName IN ('')                 | lab           |                |
| BICARBONATE_MIN          |                                | lab        |  valuenum, ITEMID IN (50882)                | LABEVENTS                          | labResult, labName IN ('bicarbonate')      | lab           |                |
| BICARBONATE_MAX          |                                | lab        |  valuenum, ITEMID IN (50882)                | LABEVENTS                          | labResult, labName IN ('bicarbonate')      | lab           |                |
| BILIRUBIN_MIN            |                                | lab        |  valuenum, ITEMID IN (50885)                | LABEVENTS                          | labResult, labName IN ('total bilirubin')  | lab           |                |
| BILIRUBIN_MAX            |                                | lab        |  valuenum, ITEMID IN (50885)                | LABEVENTS                          | labResult, labName IN ('total bilirubin')  | lab           |                |
| BUN_MIN                  | blood urea nitrogen            | lab        |  valuenum, ITEMID IN (51006)                | LABEVENTS                          | labResult, labName IN ('BUN')              | lab           |                |
| BUN_MAX                  |                                | lab        |  valuenum, ITEMID IN (51006)                | LABEVENTS                          | labResult, labName IN ('BUN')              | lab           |                |
| CHLORIDE_MIN             |                                | lab        |  valuenum, ITEMID IN (50806, 50902)         | LABEVENTS                          | labResult, labName IN ('chloride')         | lab           |                |
| CHLORIDE_MAX             |                                | lab        |  valuenum, ITEMID IN (50806, 50902)         | LABEVENTS                          | labResult, labName IN ('chloride')         | lab           |                |
| CREATININE_MIN           |                                | lab        |  valuenum, ITEMID IN (50912)                | LABEVENTS                          | labResult, labName IN ('creatinine')       | lab           |                |
| CREATININE_MAX           |                                | lab        |  valuenum, ITEMID IN (50912)                | LABEVENTS                          | labResult, labName IN ('creatinine')       | lab           |                |
| GLUCOSE_MIN              |                                | lab        |  valuenum, ITEMID IN (50809, 50931)         | LABEVENTS                          | labResult, labName IN ('glucose')          | lab           |                |
| GLUCOSE_MAX              |                                | lab        |  valuenum, ITEMID IN (50809, 50931)         | LABEVENTS                          | labResult, labName IN ('glucose')          | lab           |                |
| GLUCOSE_MEAN             |                                | lab        |  valuenum, ITEMID IN (50809, 50931)         | LABEVENTS                          | labResult, labName IN ('glucose')          | lab           |                |
| HEMATOCRIT_MIN           |                                | lab        |  valuenum, ITEMID IN (50810, 51221)         | LABEVENTS                          | labResult, labName IN ('Hct')              | lab           |                |
| HEMATOCRIT_MAX           |                                | lab        |  valuenum, ITEMID IN (50810, 51221)         | LABEVENTS                          | labResult, labName IN ('Hct')              | lab           |                |
| HEMOGLOBIN_MIN           |                                | lab        |  valuenum, ITEMID IN (50811, 51222)         | LABEVENTS                          | labResult, labName IN ('Hgb')              | lab           |                |
| HEMOGLOBIN_MAX           |                                | lab        |  valuenum, ITEMID IN (50811, 51222)         | LABEVENTS                          | labResult, labName IN ('Hgb')              | lab           |                |
| INR_MIN                  | international normalized ratio | lab        |  valuenum, ITEMID IN (51237)                | LABEVENTS                          | labResult, labName IN ('')                 | lab           |                |
| INR_MAX                  | international normalized ratio | lab        |  valuenum, ITEMID IN (51237)                | LABEVENTS                          | labResult, labName IN ('')                 | lab           |                |
| LACTATE_MIN              |                                | lab        |  valuenum, ITEMID IN (50813)                | LABEVENTS                          | labResult, labName IN ('lactate')          | lab           |                |
| LACTATE_MAX              |                                | lab        |  valuenum, ITEMID IN (50813)                | LABEVENTS                          | labResult, labName IN ('lactate')          | lab           |                |
| PLATELET_MIN             |                                | lab        |  valuenum, ITEMID IN (51265)                | LABEVENTS                          | labResult, labName IN ('platelets x 1000') | lab           |                |
| PLATELET_MAX             |                                | lab        |  valuenum, ITEMID IN (51265)                | LABEVENTS                          | labResult, labName IN ('platelets x 1000') | lab           |                |
| POTASSIUM_MIN            |                                | lab        |  valuenum, ITEMID IN (50822, 50971)         | LABEVENTS                          | labResult, labName IN ('potassium')        | lab           |                |
| POTASSIUM_MAX            |                                | lab        |  valuenum, ITEMID IN (50822, 50971)         | LABEVENTS                          | labResult, labName IN ('potassium')        | lab           |                |
| PT_MIN                   | prothrombin time               | lab        |  valuenum, ITEMID IN (51274)                | LABEVENTS                          | labResult, labName IN ('PT')               | lab           |                |
| PT_MAX                   |                                | lab        |  valuenum, ITEMID IN (51274)                | LABEVENTS                          | labResult, labName IN ('PT')               | lab           |                |
| PTT_MIN                  | partial thromboplastin time    | lab        |  valuenum, ITEMID IN (51275)                | LABEVENTS                          | labResult, labName IN ('PTT')              | lab           |                |
| PTT_MAX                  | partial thromboplastin time    | lab        |  valuenum, ITEMID IN (51275)                | LABEVENTS                          | labResult, labName IN ('PTT')              | lab           |                |
| SODIUM_MIN               |                                | lab        |  valuenum, ITEMID IN (50824, 50983)         | LABEVENTS                          | labResult, labName IN ('sodium')           | lab           |                |
| SODIUM_MAX               |                                | lab        |  valuenum, ITEMID IN (50824, 50983)         | LABEVENTS                          | labResult, labName IN ('sodium')           | lab           |                |
| WBC_MIN                  | white blood count              | lab        |  valuenum, ITEMID IN (51300, 51301)         | LABEVENTS                          | labResult, labName IN ('WBC x 1000')       | lab           |                |
| WBC_MAX                  |                                | lab        |  valuenum, ITEMID IN (51300, 51301)         | LABEVENTS                          | labResult, labName IN ('WBC x 1000')       | lab           |                |

## adaptions

* I needed to alter each FROM statement to "my" correct db table: e.g. eicu.patient
* REG\_EXP\_CONTAINS is not available, this is changed by: `and nursingchartvalue ~ '^([0-9]+\.?[0-9]*|\.[0-9]+)$'`

## sql approach

The query is fairly large and there's serial processing of the different queries. Thus one cannot parallelize them all. Here I'll quickly indicate the dependencies:

|order| sql-file                                                                      | depends on other sql?                                   | output                      |
|-----|-------------------------------------------------------------------------------|---------------------------------------------------------|-----------------------------|
|  1. | [1\_urineoutput.sql](./sql/eicu/1_urineoutput.sql)                            | independent                                             |  urineoutput                |
|  2. | [2\_pivot_weigths.sql](./sql/eicu/2_pivot_weights.sql)                        | independent                                             |  weightdurations            |
|  3. | [3\_urine_kidigo.sql](./sql/eicu/3_urine_kidigo.sql)                          | `1_urineoutput.sql`, `2_pivot_weigths.sql`              |  kdigo\_uo                  |
|  4. | [4\_creatinine.sql](./sql/eicu/4_creatinine.sql)                              | independent                                             |  kdigo\_creat               |
|  5. | [5\_kidigo_stages.sql](./sql/eicu/5_kidigo_stages.sql)                        | `3_urine_kidigo.sql`, `4_creatinine.sql`                |  kdigo\_stages              |
|  6. | [6\_kidigo\_7_days.sql](./sql/eicu/6_kidigo_7_days.sql)                       | `5_kidigo_stages.sql`                                   |  kdigo\_stages\_7day        |
|  7. | [7\_kidigo\_stages_creatinine.sql](./sql/eicu/7_kidigo_stages_creatinine.sql) | `4_creatinine.sql`, `5_kidigo_stages.sql`               |  kdigo\_stages\_creatinine  |
|  8. | [8\_kidigo\_7\_days_creatinine.sql](./sql/eicu/8_kidigo_7_days_creatinine.sql)| `5_kidigo_stages.sql`, `7_kidigo_stages_creatinine.sql` |  kdigo\_7\_days\_creatinine |
|  9. | [9\_get_labevents.sql](./sql/eicu/9_getl_labevents.sql)                       | independent                                             |  labstay                    |
| 10. | [10\_labstay.sql](./sql/eicu/10_labstay.sql)                                  | `9_get_labevents.sql`                                   |                             |
| 11. | [11\_get_vitals.sql](./sql/eicu/11_get_vitals.sql)                            | independent                                             |   vitalsfirstday            |
| 12. | [12\_vitalsfirstday.sql](./sql/eicu/12_vitalsfirstday.sql)                    | `11_get_vitals.sql`                                     |                             |
| 13. | [13\_get_comorbidities.sql](./sql/eicu/13_get_comorbidities.sql)              | independent                                             |   COMORBIDITIES             |
| 14. | [14\_set_comorbidities.sql](./sql/eicu/14_set_comorbidities.sql)              | `13_get_comorbidities.sql`                              |                             |
| 15. | [15\_count_icustays.sql](./sql/eicu/15_count_icustays.sql)                    | independent                                             |                             |

## output

I'd propose to save the output in .parquet files or .csv files. The latter have the advantage of being able to be read in a text-oriented software suite, the first one is faster, binary and uses less memory. 

ExaScience is creating multiple csv files for the MIMIC-III approach.
