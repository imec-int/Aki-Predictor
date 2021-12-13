# Deep Learning model for AKI Prediction on MIMIC-III

Aki-Predictor is a set of python script running deep learning model to predict Acute Kiden Injuries during the first 7 days of stay in ICU. The proposed model was tested on MIMIC-III database.

We developed our model based on 83 features referring to routinely collected clinical parameters.  
The features includes demographics data, vital signs measured at the bedsidesuch as heart rate, arterial blood pressure, respiration rate, etc. laboratory test results such 
as blood urea nitrogen, hemoglobin, white blood count, etc. average of urine output, theminimum  value  of  estimated  glomerular  filtration  rate  (eGFR)  and  creatinine.
We also included co-morbidities such as congestive heart failure,  hypertension,  diabetes,  etc.

## How to run

1. First create a conda environment based on the [environment.yml](environment.yml) file:
   ```
   conda env create -f environment.yml
   conda activate aki-predictor 
   ```
2. Make a copy of .env.template named .env: `cp .env.template .env`
   
   (If the .env file is missing, a database connection to localhost will be used)
3. Fill in the values.
4. Set the environment variables using: `. .env`
5. Execute one of the following commands to extract AKI patient data from the MIMIC III or eICU databases:
   - `python aki-postgres.py --dbname mimiciii`
   - `python aki-postgres.py --dbname eicu`
   
   This will generate parquet files of all responses in [data/queried](./data/queried)

(In order to explore if this data fetching of eicu data was succesful in comparison with the (proven by ExaScience) mimic-iii fetch, we've added a jupyter notebook to explore the data and create images for all parameters in which mimic data is compared with eicu data:
[jupyter notebook](data_exploration.ipynb).)

6. Execute one of the following commands to clean and preprocess the csv files generated from the data extraction step:
   - `python aki-preprocess.py --dbname mimiciii`
   - `python aki-preprocess.py --dbname eicu`
7. To run the machine learning model run: `python aki-ml.py`

The scripts contains the following functions:

* run_aki_model: predicts wether a patient will develop AKI withnin the first 7 days of its stay and which stage of AKI it is according to the KIDIGO guidelines.
* cluster_ethnicity: subsets the data  by  ethnicity:  train  on  ”Caucasian”  (all variants),  predict  for  all  other  ethnicities.   
* change_data_size: does random subsampling of available training data
