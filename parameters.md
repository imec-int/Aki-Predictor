# AKI Parameters

as it is unclear to me right now what the correct AKI parameters are, which are being used in the ExaScience model, I'll first investigate what the used parameters are and what could be their corresponding value in the eICU database

It seems that Exascience is using the [Kdigo Classification](https://kdigo.org)

I'm not sure yet if we have all data for enough participants and or how ExaScience worked with missing data. #TODO check with ExaScience

Important, our database is a postgreSQL dB, the [eicu code files](https://github.com/MIT-LCP/eicu-code/tree/master/concepts) are written for Google BigQuery, so small adaptions have to be made.


| AKI parameter            | category                 | MIMIC III name                              | MIMIC III location                 | eICU name  | eICU location | unit preferred |
| ------------------------ | ------------------------ | ------------------------------------------- | ---------------------------------- | ---------- | ------------- | -------------- |
| AKI                      | --OUTPUT--               |                                             |                                    |            |               |                |
| AKI_STAGE_7DAY           | --OUTPUT--               |                                             |                                    |            |               |
| ETHNICITY                |                          |                                             | ADMISSIONS                         | ethnicity  | patient       | -              |
| AGE                      |                          | df['ADMITTIME'].dt.year - df['DOB'].dt.year | ADMITTIME: ADMISSIONS,DOB:PATIENTS | age        | patient       | -              |
| GENDER                   |                          | PATIENTS                                    |                                    | gender     | patient       | -              |
| HYPERTENSION             |                          |                                             |                                    |            |               |
| HYPOTHYROIDISM           |                          |                                             |                                    |            |               |
| CONGESTIVE_HEART_FAILURE |                          |                                             |                                    |            |               |
| CARDIAC_ARRHYTHMIAS      |                          |                                             |                                    |            |               |
| ALCOHOL_ABUSE            |                          |                                             |                                    |            |               |
| DRUG_ABUSE               |                          |                                             |                                    |            |               |
| VALVULAR_DISEASE         |                          |                                             |                                    |            |               |
| OBESITY                  |                          |                                             |                                    |            |               |
| PERIPHERAL_VASCULAR      |                          |                                             |                                    |            |               |
| DIABETES_COMPLICATED     |                          |                                             |                                    |            |               |
| LIVER_DISEASE            |                          |                                             |                                    |            |               |
| DIABETES_UNCOMPLICATED   |                          |                                             |                                    |            |               |
| RENAL_FAILURE            |                          |                                             |                                    |            |               |
| UO_RT_24HR               | urine output             |                                             |                                    |            |               |
| UO_RT_12HR               | urine output             |                                             |                                    |            |               |
| UO_RT_6HR                | urine output             |                                             |                                    |            |               |
| CREAT                    | kidigo 7 days creatinine | creat                                       |                                    | creatinine | apacheApsVar  |
| EGFR                     |                          | Estimated Glomerular Filtration Rate        |                                    |            |               |
| TEMPC_MIN                | vitals                   |                                             |                                    |            |               |
| TEMPC_MAX                | vitals                   |                                             |                                    |            |               |
| TEMPC_MEAN               | vitals                   |                                             |                                    |            |               |
| HEARTRATE_MIN            | vitals                   |                                             |                                    |            |               |
| HEARTRATE_MAX            | vitals                   |                                             |                                    |            |               |
| HEARTRATE_MEAN           | vitals                   |                                             |                                    |            |               |
| SPO2_MIN                 | vitals                   |                                             |                                    |            |               |
| SPO2_MAX                 | vitals                   |                                             |                                    |            |               |
| SPO2_MEAN                | vitals                   |                                             |                                    |            |               |
| MEANBP_MIN               | vitals                   |                                             |                                    |            |               |
| MEANBP_MAX               | vitals                   |                                             |                                    |            |               |
| MEANBP_MEAN              | vitals                   |                                             |                                    |            |               |
| DIASBP_MIN               | vitals                   |                                             |                                    |            |               |
| DIASBP_MAX               | vitals                   |                                             |                                    |            |               |
| DIASBP_MEAN              | vitals                   |                                             |                                    |            |               |
| RESPRATE_MIN             | vitals                   |                                             |                                    |            |               |
| RESPRATE_MAX             | vitals                   |                                             |                                    |            |               |
| RESPRATE_MEAN            | vitals                   |                                             |                                    |            |               |
| SYSBP_MIN                | vitals                   |                                             |                                    |            |               |
| SYSBP_MAX                | vitals                   |                                             |                                    |            |               |
| SYSBP_MEAN               | vitals                   |                                             |                                    |            |               |
| ALBUMIN_MIN              |                          | LABEVENTS                                   |                                    |            |               |
| ALBUMIN_MAX              |                          | LABEVENTS                                   |                                    |            |               |
| ANIONGAP_MIN             |                          | LABEVENTS                                   |                                    |            |               |
| ANIONGAP_MAX             |                          | LABEVENTS                                   |                                    |            |               |
| BANDS_MIN                |                          | LABEVENTS                                   |                                    |            |               |
| BANDS_MAX                |                          | LABEVENTS                                   |                                    |            |               |
| BICARBONATE_MIN          |                          | LABEVENTS                                   |                                    |            |               |
| BICARBONATE_MAX          |                          | LABEVENTS                                   |                                    |            |               |
| BILIRUBIN_MIN            |                          | LABEVENTS                                   |                                    |            |               |
| BILIRUBIN_MAX            |                          | LABEVENTS                                   |                                    |            |               |
| BUN_MIN                  |                          | LABEVENTS (blood urea nitrogen)              |                                    |            |               |                |
| BUN_MAX                  |                          | LABEVENTS                                   |                                    |            |               |                |
| CHLORIDE_MIN             |                          | LABEVENTS                                   |                                    |            |               |
| CHLORIDE_MAX             |                          | LABEVENTS                                   |                                    |            |               |
| CREATININE_MIN           |                          | LABEVENTS                                   |                                    |            |               |
| CREATININE_MAX           |                          | LABEVENTS                                   |                                    |            |               |
| GLUCOSE_MIN              | vitals?                  | LABEVENTS                                   |                                    |            |               |
| GLUCOSE_MAX              | vitals?                  | LABEVENTS                                   |                                    |            |               |
| GLUCOSE_MEAN             | vitals?                  | LABEVENTS                                   |                                    |            |               |
| HEMATOCRIT_MIN           |                          | LABEVENTS                                   |                                    |            |               |
| HEMATOCRIT_MAX           |                          | LABEVENTS                                   |                                    |            |               |
| HEMOGLOBIN_MIN           |                          | LABEVENTS                                   |                                    |            |               |
| HEMOGLOBIN_MAX           |                          | LABEVENTS                                   |                                    |            |               |
| INR_MIN                  |                          | LABEVENTS(international normalized ratio)   |                                    |            |               |
| INR_MAX                  |                          | LABEVENTS                                   |                                    |            |               |
| LACTATE_MIN              |                          | LABEVENTS                                   |                                    |            |               |
| LACTATE_MAX              |                          | LABEVENTS                                   |                                    |            |               |
| PLATELET_MIN             |                          | LABEVENTS                                   |                                    |            |               |
| PLATELET_MAX             |                          | LABEVENTS                                   |                                    |            |               |
| POTASSIUM_MIN            |                          | LABEVENTS                                   |                                    |            |               |
| POTASSIUM_MAX            |                          | LABEVENTS                                   |                                    |            |               |
| PT_MIN                   | prothrombin time         | LABEVENTS                                   |                                    |            |               |
| PT_MAX                   |                          | LABEVENTS                                   |                                    |            |               |
| PTT_MIN                  |                          | LABEVENTS(partial throm- boplastin time)    |                                    |            |               |
| PTT_MAX                  |                          | LABEVENTS(partial throm- boplastin time)    |                                    |            |               |
| SODIUM_MIN               |                          | LABEVENTS                                   |                                    |            |               |
| SODIUM_MAX               |                          | LABEVENTS                                   |                                    |            |               |
| WBC_MIN                  | (white blood count)      | LABEVENTS                                   |                                    |            |               |
| WBC_MAX                  |                          | LABEVENTS                                   |                                    |            |               |

## adaptions

* I needed to alter each FROM statement to "my" correct db table: e.g. eicu.patient
* REG\_EXP\_CONTAINS is not available, this is changed by: `and nursingchartvalue ~ '^([0-9]+\.?[0-9]*|\.[0-9]+)$'`
* 

## sql approach

The query is fairly large and there's serial processing of the different queries. Thus one cannot parallelize them all. Here I'll quickly indicate the dependencies:

|order| sql-file                                                                      | depends on other sql?                                   | output |
|-----|-------------------------------------------------------------------------------|---------------------------------------------------------|--------|
|  1. | [1\_urineoutput.sql](./sql/eicu/1_urineoutput.sql)                            | independent                                             |        |
|  2. | [2\_pivot_weigths.sql](./sql/eicu/2_pivot_weights.sql)                        | independent                                             |        |
|  3. | [3\_urine_kidigo.sql](./sql/eicu/3_urine_kidigo.sql)                          | `1_urineoutput.sql`, `2_pivot_weigths.sql`              |        |
|  4. | [4\_creatinine.sql](./sql/eicu/4_creatinine.sql)                              | independent                                             |        |
|  5. | [5\_kidigo_stages.sql](./sql/eicu/5_kidigo_stages.sql)                        | `3_urine_kidigo.sql`, `4_creatinine.sql`                |        |
|  6. | [6\_kidigo\_7_days.sql](./sql/eicu/6_kidigo_7_days.sql)                       | `5_kidigo_stages.sql`                                   |        |
|  7. | [7\_kidigo\_stages_creatinine.sql](./sql/eicu/7_kidigo_stages_creatinine.sql) | `4_creatinine.sql`, `5_kidigo_stages.sql`               |        |
|  8. | [8\_kidigo\_7\_days_creatinine.sql](./sql/eicu/8_kidigo_7_days_creatinine.sql)| `5_kidigo_stages.sql`, `7_kidigo_stages_creatinine.sql` |        |
|  9. | [9\_get_labevents.sql](./sql/eicu/9_getl_labevents.sql)                       | independent                                             |        |
| 10. | [10\_labstay.sql](./sql/eicu/10_labstay.sql)                                  | `9_get_labevents.sql`                                   |        |
| 11. | [11\_get_vitals.sql](./sql/eicu/11_get_vitals.sql)                            | independent                                             |        |
| 12. | [12\_vitalsfirstday.sql](./sql/eicu/12_vitalsfirstday.sql)                    | `11_get_vitals.sql`                                     |        |
| 13. | [13\_get_comorbidities.sql](./sql/eicu/13_get_comorbidities.sql)              | independent                                             |        |
| 14. | [14\_set_comorbidities.sql](./sql/eicu/14_set_comorbidities.sql)              | `13_get_comorbidities.sql`                              |        |
| 15. | [15\_count_icustays.sql](./sql/eicu/15_count_icustays.sql)                    | independent                                             |        |
	



## output

I'd propose to save the output in .parquet files or .csv files. The latter have the advantage of being able to be read in a text-oriented software suite, the first one is faster, binary and uses less memory. 

ExaScience is creating multiple csv files for the MIMIC-III approach.

