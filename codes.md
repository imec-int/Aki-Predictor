# codes

Converted codes
                                  
| sql file            | mimic III table | mimic III column | eICU table | eICU column | mimic III code(s)   | eICU code(s)     | source                                   |
| ------------------- | --------------- | ---------------- | ---------- | ----------- | ------------------- | ---------------- | ---------------------------------------- |
| 4_creatinine.sql    | labevents       | ITEMID           | lab        | labName     | 50912 (CREATININE)  | creatinine       |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50868 (ANION GAP)   | anion gap        |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50862 (ALBUMIN)     | albumin          |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51144 (BANDS)       | ?                |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50882 (BICARBONATE) | bicarbonate      |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50885 (BILIRUBIN)   | ?                |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50806 (CHLORIDE)    | chloride         |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50902 (CHLORIDE)    | chloride         |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50809 (GLUCOSE)     | glucose          |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50931 (GLUCOSE)     | glucose          |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50810 (HEMATOCRIT)  | Hct              | https://en.wikipedia.org/wiki/Hematocrit |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51221 (HEMATOCRIT)  | Hct              | https://en.wikipedia.org/wiki/Hematocrit |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50811 (HEMOGLOBIN)  | Hgb              | https://en.wikipedia.org/wiki/Hemoglobin |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51222 (HEMOGLOBIN)  | Hgb              | https://en.wikipedia.org/wiki/Hemoglobin |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50813 (LACTATE)     | lactate          |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51265 (PLATELET)    | platelets x 1000 |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50822 (POTASSIUM)   | potassium        |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50971 (POTASSIUM)   | potassium        |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51275 (PTT)         | PTT? PTT ratio?  |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51237 (INR)         | PT - INR?        |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51274 (PT)          | PT               |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50824 (SODIUM)      | sodium           |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 50983 (SODIUM)      | sodium           |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51006 (BUN)         | BUN              |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51300 (WBC)         | WBC x 1000?      |                                          |
| 9_get_labevents.sql | labevents       | ITEMID           | lab        | labName     | 51301 (WBC)         | WBC x 1000?      |                                          |





## eICU lab#labName values

`SELECT DISTINCT labName FROM eicu_crd.lab ORDER BY labName ASC`

=-bands
=-basos
=-eos
=-lymphs
=-monos
=-polys
24 h urine protein
24 h urine urea nitrogen
Acetaminophen
albumin
alkaline phos.
ALT (SGPT)
Amikacin - peak
Amikacin - random
Amikacin - trough
ammonia
amylase
ANF/ANA
anion gap
AST (SGOT)
Base Deficit
Base Excess
bedside glucose
bicarbonate
BNP
BUN
calcium
Carbamazepine
Carboxyhemoglobin
cd 4
chloride
Clostridium difficile toxin A+B
cortisol
CPK
CPK-MB
CPK-MB INDEX
creatinine
CRP
CRP-hs
Cyclosporin
Device
Digoxin
direct bilirubin
ESR
ethanol
Fe
Fe/TIBC Ratio
Ferritin
fibrinogen
FiO2
folate
free T4
Gentamicin - peak
Gentamicin - random
Gentamicin - trough
glucose
glucose - CSF
haptoglobin
HCO3
Hct
HDL
Hgb
HIV 1&2 AB
HSV 1&2 IgG AB
HSV 1&2 IgG AB titer
ionized calcium
lactate
LDH
LDL
Legionella pneumophila Ab
Lidocaine
lipase
Lithium
LPM O2
magnesium
MCH
MCHC
MCV
Methemoglobin
Mode
MPV
myoglobin
NAPA
O2 Content
O2 Sat (%)
Oxyhemoglobin
paCO2
paO2
Peak Airway/Pressure
PEEP
pH
Phenobarbital
Phenytoin
phosphate
platelets x 1000
potassium
prealbumin
Pressure Control
Pressure Support
Procainamide
prolactin
protein - CSF
protein C
protein S
PT
PT - INR
PTT
PTT ratio
RBC
RDW
Respiratory Rate
reticulocyte count
RPR titer
salicylate
serum ketones
serum osmolality
Site
sodium
Spontaneous Rate
T3
T3RU
T4
Tacrolimus-FK506
Temperature
Theophylline
TIBC
Tobramycin - peak
Tobramycin - random
Tobramycin - trough
total bilirubin
total cholesterol
Total CO2
total protein
transferrin
triglycerides
troponin - I
troponin - T
TSH
TV
uric acid
urinary creatinine
urinary osmolality
urinary sodium
urinary specific gravity
Vancomycin - peak
Vancomycin - random
Vancomycin - trough
Vent Other
Vent Rate
Vitamin B12
WBC x 1000
WBC's in body fluid
WBC's in cerebrospinal fluid
WBC's in pericardial fluid
WBC's in peritoneal fluid
WBC's in pleural fluid
WBC's in synovial fluid
WBC's in urine

