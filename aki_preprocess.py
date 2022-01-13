from logging import debug
import os

import pandas as pd
import argparse
from pathlib import Path

from util.util import create_insights

from config import config


def read_queried(cfg:config, filename:str):
    df = pd.read_parquet(cfg.queried_path() / filename)
    df.columns = map(str.upper, df.columns)
    return df

def contains_with_hadm(hadm_id, diagnoses):
    """Returns whether diagnoses contains at least one diagnosis with diagnosis['HADM_ID'] == hadm_id ."""
    return not diagnoses.loc[diagnoses['HADM_ID'].isin(hadm_id)].empty


def caculate_eGFR_MDRD_equation(cr, gender, eth, age):
    # TODO error RuntimeWarning: divide by zero encountered in power
    if(cr is None or cr == 0 or age == 0):
        #print("skipping sample: ", cr, age)
        return 0
    temp = 186 * (cr ** (-1.154)) * (age ** (-0.203))
    if (gender == 'F'):
        temp = temp * 0.742
    if eth == 'BLACK/AFRICAN AMERICAN':
        temp = temp * 1.21
    return temp

def get_aki_patients_7days(cfg:config,aki_sql_results, aki_out_dataset, debugprint: bool):
    '''
    get_aki_patients_7days: this function preprocceses the <aki_sql_results> dataset in order to create a more expanded view on the data.
    <aki_out_dataset> is the file in which we'll write the output
    '''
    df = read_queried(cfg, 'ADMISSIONS.parquet')
    df = df.sort_values(by=['SUBJECT_ID', 'HADM_ID', 'ICUSTAY_ID'])
    

    info_save = df.drop_duplicates(subset=['ICUSTAY_ID'])
    info_save.loc[:,'AKI'] = -1 #info_save['AKI'] = -1
    info_save.loc[:,'EGFR']= -1 #info_save['EGFR'] = -1
    if(debugprint):
        print("admissions info", df.shape)
        print("number of unique subjects in admission: ",
            df['SUBJECT_ID'].nunique())
        print("number of icustays info in admissions: ",
            df['ICUSTAY_ID'].nunique())
        print("the biggest number of ICU stays for a patient: ",
          info_save['COUNTTIMESGOICU'].max())

    c_aki_7d = read_queried(cfg, aki_sql_results)
    if(debugprint):
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
    if(debugprint):
        print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())

    df_save = pd.merge(info_save, c_aki_7d, how='inner', on='ICUSTAY_ID')
    df_save.columns = map(str.upper, df_save.columns)
    icustays_data = [frame for season,
                     frame in df_save.groupby(['ICUSTAY_ID'])]
    if(debugprint):
        count_ckd_normal = 0
        count_ckd_aki = 0
        count_akibefore_normal = 0
        count_akibefore_aki = 0
        count_normal = 0
        count_aki = 0
        count_renalfailure_normal = 0
        count_renalfailure_aki = 0

    diagnoses = read_queried(cfg, 'comorbidities.parquet')
    renal_diagnoses = diagnoses.loc[diagnoses['RENAL_FAILURE'] == 1]

    diagnoses_check = read_queried(cfg, 'DIAGNOSES_ICD.parquet')

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
        #df_corresponds_check is an often returning comparison, extracted for readability
        df_corresponds_check = df_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0])
        df_save.loc[df_corresponds_check, 'EGFR'] = eGFR
        df_save.loc[df_corresponds_check, 'AKI'] = c_aki_7d.loc[c_aki_7d['ICUSTAY_ID'] == int(
            temp['ICUSTAY_ID'].values[0])]['AKI_7DAY'].values[0]
        if(debugprint):
            if (df_save.loc[df_corresponds_check, 'AKI'].values[0] == 1):
                count_aki = count_aki + 1
            else:
                count_normal = count_normal + 1

            if (contains_with_hadm(temp['HADM_ID'], check_CKD_diagnoses) == True):
                df_save.loc[df_corresponds_check, 'AKI'] = 2
                if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                    count_ckd_aki = count_ckd_aki + 1
                else:
                    count_ckd_normal = count_ckd_normal + 1

            if (contains_with_hadm(temp['HADM_ID'], check_aki_before_diagnoses) == True):
                df_save.loc[df_corresponds_check, 'AKI'] = 3
                if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                    count_akibefore_aki = count_akibefore_aki + 1
                else:
                    count_akibefore_normal = count_akibefore_normal + 1

            if (contains_with_hadm(temp['HADM_ID'], renal_diagnoses) == True):
                df_save.loc[df_corresponds_check, 'AKI'] = 4
                if (info_save.loc[info_save['ICUSTAY_ID'] == int(temp['ICUSTAY_ID'].values[0]), 'AKI'].values[0] == 1):
                    count_renalfailure_aki = count_renalfailure_aki + 1
                else:
                    count_renalfailure_normal = count_renalfailure_normal + 1

    lab = read_queried(cfg, 'labstay.parquet')
    info_save = pd.merge(df_save, lab, how='left', on='ICUSTAY_ID')

    chart = read_queried(cfg, 'chart_vitals_stay.parquet')
    df_save = pd.merge(info_save, chart, how='left', on='ICUSTAY_ID')

    comorbidities = read_queried(cfg, 'comorbidities.parquet')

    info_save = pd.merge(df_save, comorbidities, how='left', on='HADM_ID')
    #info_save = info_save.drop(columns=['UNNAMED: 0'])
    if(debugprint):
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

    
    folderpath = cfg.preprocessed_path()
    folderpath.mkdir(parents=True, exist_ok=True)
    info_save.to_parquet(folderpath / aki_out_dataset)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbmodel",
                        type=str,
                        help="choose database model: eicu (default) or mimiciii",
                        choices=['eicu', 'mimiciii']
                        )
    parser.add_argument("--dbname",
                        type=str,
                        help="choose database",
                        )

    cfg = config(parser.parse_args())
    

    cols_insights = ["total ICUstays", "No AKI Observations", "AKI STAGE 1 observations",
                     "AKI STAGE 2 observations", "AKI STAGE 3 observations", "NaN AKI observations"]
    insights_df = pd.DataFrame(index=cols_insights)

    c_aki = read_queried(cfg, 'AKI_KIDIGO_STAGES_SQL.parquet')
    c_aki, insights_df = create_insights(
        c_aki, "c_aki_full", insights_df, 'AKI_STAGE')

    c_aki_7d = read_queried(cfg, 'AKI_KIDIGO_7D_SQL.parquet')
    c_aki_7d, insights_df = create_insights(
        c_aki_7d, "c_aki_7d_full", insights_df, 'AKI_STAGE_7DAY')
    c_aki_7d = c_aki_7d.dropna(subset=['AKI_STAGE_7DAY'])
    print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())

    print("USING ONLY CREATININE")
    c_aki_7d = read_queried(cfg, 'AKI_KIDIGO_7D_SQL_CREATININE.parquet')
    c_aki_7d, insights_df = create_insights(
        c_aki_7d, "c_aki_7d creat_only", insights_df, 'AKI_STAGE_7DAY')

    #c_aki_7d = c_aki_7d.loc[c_aki_7d['AKI_STAGE_7DAY'].isin(['0', '1'])]
    print("Total icustays: ", c_aki_7d['ICUSTAY_ID'].nunique())

    c_aki = read_queried(cfg, 'AKI_KIDIGO_STAGES_SQL_CREATININE.parquet')
    c_aki, insights_df = create_insights(
        c_aki, "c_aki_full creatinine infos", insights_df, 'AKI_STAGE')
    #get aki patients 7 days with creatinine and urine
    get_aki_patients_7days(cfg, 'AKI_KIDIGO_7D_SQL.parquet', 'INFO_DATASET_7days_creatinine+urine2.parquet', debugprint=False)
    # get aki patients 7 days merged with only creatinine
    get_aki_patients_7days(cfg, 'AKI_KIDIGO_7D_SQL_CREATININE.parquet','INFO_DATASET_7days_creatinine2.parquet', debugprint=False)

    # statistical_itemid_missing()
