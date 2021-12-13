import os

import pandas as pd
import argparse
from pathlib import Path

from util.util import create_insights


dbname = 'mimiciii'


def read_queried(dbname:str, filename:str):
    df = pd.read_parquet(os.path.join('.', 'data', dbname, 'queried', filename))
    df.columns = map(str.upper, df.columns)
    return df


def open_preprocessed_to_write(dbname:str, filename:str):
    folderpath = Path.cwd() / 'data' / dbname / 'preprocessed'
    folderpath.mkdir(parents=True, exist_ok=True)
    return open(os.path.join(folderpath, filename), 'w')


def contains_with_hadm(hadm_id, diagnoses):
    """Returns whether diagnoses contains at least one diagnosis with diagnosis['HADM_ID'] == hadm_id ."""
    return not diagnoses.loc[diagnoses['HADM_ID'].isin(hadm_id)].empty


def caculate_eGFR_MDRD_equation(cr, gender, eth, age):
    # TODO error RuntimeWarning: divide by zero encountered in power
    if(cr == 0 or age == 0):
        #print("skipping sample: ", cr, age)
        return 0
    temp = 186 * (cr ** (-1.154)) * (age ** (-0.203))
    if (gender == 'F'):
        temp = temp * 0.742
    if eth == 'BLACK/AFRICAN AMERICAN':
        temp = temp * 1.21
    return temp


def get_aki_patients_7days():

    df = read_queried(dbname, 'ADMISSIONS.parquet')
    df = df.sort_values(by=['SUBJECT_ID', 'HADM_ID', 'ICUSTAY_ID'])

    print("admissions info", df.shape)
    print("number of unique subjects in admission: ",
          df['SUBJECT_ID'].nunique())
    print("number of icustays info in admissions: ",
          df['ICUSTAY_ID'].nunique())

    info_save = df.drop_duplicates(subset=['ICUSTAY_ID'])
    info_save['AKI'] = -1
    info_save['EGFR'] = -1

    print("the biggest number of ICU stays for a patient: ",
          info_save['COUNTTIMESGOICU'].max())

    c_aki_7d = read_queried(dbname, 'AKI_KIDIGO_7D_SQL.parquet')
    
    print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())
    print('NORMAL Patients in 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 0]['ICUSTAY_ID'].count()))
    print('AKI patients STAGE 1 within 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 1]['ICUSTAY_ID'].count()))
    print('AKI Patients STAGE 2 in 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 2]['ICUSTAY_ID'].count()))
    print('AKI Patients STAGE 3 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 3]['ICUSTAY_ID'].count()))
    print('NAN patients within 7DAY: {}'.format(
        c_aki_7d['AKI_STAGE_7DAY'].isna().sum()))
    c_aki_7d = c_aki_7d.dropna(subset=['AKI_STAGE_7DAY'])
    print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())

    df_save = pd.merge(info_save, c_aki_7d, how='inner', on='ICUSTAY_ID')
    df_save.columns = map(str.upper, df_save.columns)
    icustays_data = [frame for season,
                     frame in df_save.groupby(['ICUSTAY_ID'])]

    count_ckd_normal = 0
    count_ckd_aki = 0
    count_akibefore_normal = 0
    count_akibefore_aki = 0
    count_normal = 0
    count_aki = 0
    count_renalfailure_normal = 0
    count_renalfailure_aki = 0
    print("entering temp")
    diagnoses = read_queried(dbname, 'comorbidities.parquet')
    renal_diagnoses = diagnoses.loc[diagnoses['RENAL_FAILURE'] == 1]

    diagnoses_check = read_queried(dbname, 'DIAGNOSES_ICD.parquet')
    
    check_aki_before_diagnoses = diagnoses_check.loc[diagnoses_check['ICD9_CODE'].isin(
        ['5845', '5846', '5847', '5848'])]
    check_CKD_diagnoses = diagnoses_check.loc[diagnoses_check['ICD9_CODE'].isin(
        ['5851', '5852', '5853', '5854', '5855'])]
    for temp in icustays_data:

        temp = temp.sort_values(by=['ICUSTAY_ID'])

        gender = temp['GENDER'].values[0]
        age = temp['AGE'].values[0]
        eth = temp['ETHNICITY'].values[0]
        cr = temp['CREAT'].values[0]

        eGFR = caculate_eGFR_MDRD_equation(
            cr=cr, gender=gender, age=age, eth=eth)

        df_save.loc[df_save['ICUSTAY_ID'] == int(
            temp['ICUSTAY_ID'].values[0]), 'EGFR'] = eGFR
        df_save.loc[df_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'] = c_aki_7d.loc[c_aki_7d['ICUSTAY_ID'] == int(
            temp['ICUSTAY_ID'].values[0])]['AKI_7DAY'].values[0]

        if (df_save.loc[df_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
            count_aki = count_aki + 1
        else:
            count_normal = count_normal + 1

        if (contains_with_hadm(temp['HADM_ID'], check_CKD_diagnoses) == True):
            df_save.loc[df_save['ICUSTAY_ID'] == int(
                temp['ICUSTAY_ID'].values[0]), 'AKI'] = 2
            if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                count_ckd_aki = count_ckd_aki + 1
            else:
                count_ckd_normal = count_ckd_normal + 1

        if (contains_with_hadm(temp['HADM_ID'], check_aki_before_diagnoses) == True):
            df_save.loc[df_save['ICUSTAY_ID'] == int(
                temp['ICUSTAY_ID'].values[0]), 'AKI'] = 3
            if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                count_akibefore_aki = count_akibefore_aki + 1
            else:
                count_akibefore_normal = count_akibefore_normal + 1

        if (contains_with_hadm(temp['HADM_ID'], renal_diagnoses) == True):
            df_save.loc[df_save['ICUSTAY_ID'] == int(
                temp['ICUSTAY_ID'].values[0]), 'AKI'] = 4
            if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                count_renalfailure_aki = count_renalfailure_aki + 1
            else:
                count_renalfailure_normal = count_renalfailure_normal + 1
    print("merging with labstay")
    lab = read_queried(dbname, 'labstay.parquet')
    info_save = pd.merge(df_save, lab, how='left', on='ICUSTAY_ID')
    print("merging with vitalstay")
    chart = read_queried(dbname, 'chart_vitals_stay.parquet')
    df_save = pd.merge(info_save, chart, how='left', on='ICUSTAY_ID')

    print("merging with comorbidities")
    comorbidities = read_queried(dbname, 'comorbidities.parquet')
    
    info_save = pd.merge(df_save, comorbidities, how='left', on='HADM_ID')
    #info_save = info_save.drop(columns=['UNNAMED: 0'])

    print('NORMAL Patients in 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 0]['ICUSTAY_ID'].count()))
    print('AKI patients STAGE 1 within 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 1]['ICUSTAY_ID'].count()))
    print('CKD counted as normal: {}'.format(count_ckd_normal))
    print('CKD counted as aki: {}'.format(count_ckd_aki))
    print('AKI on admission counted as normal: {}'.format(count_akibefore_normal))
    print('AKI on admission counted as aki: {}'.format(count_akibefore_aki))
    print('RENAL FAILURE counted as normal: {}'.format(count_renalfailure_normal))
    print('RENAL FAILURE counted as aki: {}'.format(count_renalfailure_aki))
    print('normal: {}'.format(count_normal))
    print('aki: {}'.format(count_aki))

    with open_preprocessed_to_write(dbname, 'INFO_DATASET_7days_creatinine+urine2.csv') as f:
        info_save.to_csv(f, encoding='utf-8', header=True)


def get_aki_patients_7days_creatinine():

    df = read_queried(dbname, 'ADMISSIONS.parquet')
    df = df.sort_values(by=['SUBJECT_ID', 'HADM_ID', 'ICUSTAY_ID'])

    print("admissions info", df.shape)
    print("number of unique subjects in admission: ",
          df['SUBJECT_ID'].nunique())
    print("number of icustays info in admissions: ",
          df['ICUSTAY_ID'].nunique())

    info_save = df.drop_duplicates(subset=['ICUSTAY_ID'])
    info_save['AKI'] = -1
    info_save['EGFR'] = -1

    print("the biggest number of ICU stays for a patient: ",
          info_save['COUNTTIMESGOICU'].max())

    c_aki_7d = read_queried(dbname, 'AKI_KIDIGO_7D_SQL_CREATININE.parquet')
    print("c_aki_7d infos")
    print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())
    print('NORMAL Patients in 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 0]['ICUSTAY_ID'].count()))
    print('AKI patients STAGE 1 within 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 1]['ICUSTAY_ID'].count()))
    print('AKI Patients STAGE 2 in 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 2]['ICUSTAY_ID'].count()))
    print('AKI Patients STAGE 3 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 3]['ICUSTAY_ID'].count()))
    print('NAN patients within 7DAY: {}'.format(
        c_aki_7d['AKI_STAGE_7DAY'].isna().sum()))
    c_aki_7d = c_aki_7d.dropna(subset=['AKI_STAGE_7DAY'])
    #c_aki_7d = c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'].isin(['0', '1'])]
    print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())

    df_save = pd.merge(info_save, c_aki_7d, how='inner', on='ICUSTAY_ID')
    df_save.columns = map(str.upper, df_save.columns)
    icustays_data = [frame for season,
                     frame in df_save.groupby(['ICUSTAY_ID'])]

    count_ckd_normal = 0
    count_ckd_aki = 0
    count_akibefore_normal = 0
    count_akibefore_aki = 0
    count_normal = 0
    count_aki = 0
    count_renalfailure_normal = 0
    count_renalfailure_aki = 0

    diagnoses = read_queried(dbname, 'comorbidities.parquet')
    renal_diagnoses = diagnoses.loc[diagnoses['RENAL_FAILURE'] == 1]

    diagnoses_check = read_queried(dbname, 'DIAGNOSES_ICD.parquet')
    
    check_aki_before_diagnoses = diagnoses_check.loc[diagnoses_check['ICD9_CODE'].isin(
        ['5845', '5846', '5847', '5848'])]
    check_CKD_diagnoses = diagnoses_check.loc[diagnoses_check['ICD9_CODE'].isin(
        ['5851', '5852', '5853', '5854', '5855'])]
    for temp in icustays_data:

        temp = temp.sort_values(by=['ICUSTAY_ID'])

        gender = temp['GENDER'].values[0]
        age = temp['AGE'].values[0]
        eth = temp['ETHNICITY'].values[0]
        cr = temp['CREAT'].values[0]

        eGFR = caculate_eGFR_MDRD_equation(
            cr=cr, gender=gender, age=age, eth=eth)  # TODO this one returned zero

        df_save.loc[df_save['ICUSTAY_ID'] == int(
            temp['ICUSTAY_ID'].values[0]), 'EGFR'] = eGFR
        df_save.loc[df_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'] = c_aki_7d.loc[c_aki_7d['ICUSTAY_ID'] == int(
            temp['ICUSTAY_ID'].values[0])]['AKI_7DAY'].values[0]

        if (df_save.loc[df_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
            count_aki = count_aki + 1
        else:
            count_normal = count_normal + 1

        if (contains_with_hadm(temp['HADM_ID'],check_CKD_diagnoses) == True):
            df_save.loc[df_save['ICUSTAY_ID'] == int(
                temp['ICUSTAY_ID'].values[0]), 'AKI'] = 2
            if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                count_ckd_aki = count_ckd_aki + 1
            else:
                count_ckd_normal = count_ckd_normal + 1

        if (contains_with_hadm(temp['HADM_ID'],check_aki_before_diagnoses) == True):
            df_save.loc[df_save['ICUSTAY_ID'] == int(
                temp['ICUSTAY_ID'].values[0]), 'AKI'] = 3
            if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                count_akibefore_aki = count_akibefore_aki + 1
            else:
                count_akibefore_normal = count_akibefore_normal + 1

        if (contains_with_hadm(temp['HADM_ID'],renal_diagnoses) == True):
            df_save.loc[df_save['ICUSTAY_ID'] == int(
                temp['ICUSTAY_ID'].values[0]), 'AKI'] = 4
            if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                count_renalfailure_aki = count_renalfailure_aki + 1
            else:
                count_renalfailure_normal = count_renalfailure_normal + 1

    lab = read_queried(dbname, 'labstay.parquet')
    info_save = pd.merge(df_save, lab, how='left', on='ICUSTAY_ID')

    chart = read_queried(dbname, 'chart_vitals_stay.parquet')
    df_save = pd.merge(info_save, chart, how='left', on='ICUSTAY_ID')

    comorbidities = read_queried(dbname, 'comorbidities.parquet')
    info_save = pd.merge(df_save, comorbidities, how='left', on='HADM_ID')
    #info_save = info_save.drop(columns=['UNNAMED: 0'])

    print('NORMAL Patients in 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 0]['ICUSTAY_ID'].count()))
    print('AKI patients STAGE 1 within 7DAY: {}'.format(
        c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'] == 1]['ICUSTAY_ID'].count()))
    print('CKD counted as normal: {}'.format(count_ckd_normal))
    print('CKD counted as aki: {}'.format(count_ckd_aki))
    print('AKI on admission counted as normal: {}'.format(count_akibefore_normal))
    print('AKI on admission counted as aki: {}'.format(count_akibefore_aki))
    print('RENAL FAILURE counted as normal: {}'.format(count_renalfailure_normal))
    print('RENAL FAILURE counted as aki: {}'.format(count_renalfailure_aki))
    print('normal: {}'.format(count_normal))
    print('aki: {}'.format(count_aki))

    with open_preprocessed_to_write(dbname, 'INFO_DATASET_7days_creatinine2.csv') as f:
        info_save.to_csv(f, encoding='utf-8', header=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbname", type=str, help="choose database name: eicu or mimiciii", choices=[
                        'eicu', 'mimiciii'])
    args = parser.parse_args()
    dbname = 'eicu' # default
    if args.dbname:
        dbname = args.dbname

    cols_insights = ["total ICUstays", "No AKI Observations", "AKI STAGE 1 observations",
                     "AKI STAGE 2 observations", "AKI STAGE 3 observations", "NaN AKI observations"]
    insights_df = pd.DataFrame(index=cols_insights)

    c_aki = read_queried(dbname, 'AKI_KIDIGO_STAGES_SQL.parquet')
    c_aki, insights_df = create_insights(
        c_aki, "c_aki_full", insights_df, 'AKI_STAGE')

    c_aki_7d = read_queried(dbname, 'AKI_KIDIGO_7D_SQL.parquet')
    c_aki_7d, insights_df = create_insights(
        c_aki_7d, "c_aki_7d_full", insights_df, 'AKI_STAGE_7DAY')
    c_aki_7d = c_aki_7d.dropna(subset=['AKI_STAGE_7DAY'])
    print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())

    print("USING ONLY CREATININE")
    c_aki_7d = read_queried(dbname, 'AKI_KIDIGO_7D_SQL_CREATININE.parquet')
    c_aki_7d, insights_df = create_insights(
        c_aki_7d, "c_aki_7d creat_only", insights_df, 'AKI_STAGE_7DAY')

    #c_aki_7d = c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'].isin(['0', '1'])]
    print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())

    c_aki = read_queried(dbname, 'AKI_KIDIGO_STAGES_SQL_CREATININE.parquet')
    c_aki, insights_df = create_insights(
        c_aki, "c_aki_full creatinine infos", insights_df, 'AKI_STAGE')

    get_aki_patients_7days()

    get_aki_patients_7days_creatinine()

    # statistical_itemid_missing()