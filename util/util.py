import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import numpy as np
import keras
import threading
import os
import sys

sys.path.append('../')


def config_gpu(using_config=True, gpu='1'):
    '''
    Config GPU
    '''
    if using_config:
        print('Using config GPU!')
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu

        # Config minimize GPU with model
        config = tf.ConfigProto(allow_soft_placement=True,
                                log_device_placement=False)
        config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)
        keras.backend.set_session(sess)
    else:
        print('Not using config GPU!')


def create_folder(path_folder):
    '''
    Create folder if not exist
    '''
    if not os.path.exists(path_folder):
        os.makedirs((path_folder))
        print('Directory {} created successfully!'.format(path_folder))
    else:
        print('Directory {} already exists!'.format(path_folder))


def write_csv(data, path_file):
    '''
    Write data to csv file
    '''
    if not os.path.exists(path_file):
        with open(path_file, 'w') as f:
            data.to_csv(f, encoding='utf-8', header=True, index=False)


def create_insights(df, name, insights_df, parameter):
    '''
    Print insights of a certain dataframe and append it to insights_df.
    Insights_df is an aggregated insights dataframe, making it easier to plot the different insights from different datasets
    '''
    df.columns = map(str.upper, df.columns)
    print(name+" infos")
    icustays = df['ICUSTAY_ID'].nunique()
    print("Total icustays: ", icustays)
    non_aki = df.loc[df[parameter] == 0]['ICUSTAY_ID'].count()
    print('No AKI Observations : {}'.format(non_aki))
    aki_s1 = df.loc[df[parameter] == 1]['ICUSTAY_ID'].count()
    print('AKI STAGE 1 observations : {}'.format(aki_s1))
    aki_s2 = df.loc[df[parameter] == 2]['ICUSTAY_ID'].count()
    print('AKI STAGE 2 observations : {}'.format(aki_s2))
    aki_s3 = df.loc[df[parameter] == 3]['ICUSTAY_ID'].count()
    print('AKI STAGE 3 observations: {}'.format(aki_s3))
    aki_na = df[parameter].isna().sum()
    print('NaN AKI observations: {}'.format(aki_na))
    insights_df[name] = [icustays, non_aki, aki_s1, aki_s2, aki_s3, aki_na]
    df = df.dropna(subset=[parameter])
    return df, insights_df
