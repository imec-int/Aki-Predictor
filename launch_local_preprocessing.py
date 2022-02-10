import argparse
import os
import sys
from pathlib import Path
import threading
import logging
from functools import reduce

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
import seaborn as sns
import plotly.express as px

import aki_ml
import aki_postgres
import aki_preprocess
from config import EICU, MIMIC_III, config


class fakeArgsClass:
    '''
    fake class in order not to have to capture cmdline arguments for all hospitals.
    '''
    dbname = None
    dbmodel = 'eicu'


class local_flow():

    def __init__(self, args, mode, train_threshold=10, train_test_split=0.2):
        hospital_ids = [
            56,
            58,
            59,
            60,
            61,
            63,
            66,
            67,
            68,
            69,
            71,
            73,
            79,
            83,
            84,
            85,
            86,
            90,
            91,
            92,
            93,
            94,
            95,
            96,
            102,
            108,
            110,
            112,
            115,
            120,
            122,
            123,
            125,
            131,
            133,
            135,
            136,
            138,
            140,
            141,
            142,
            143,
            144,
            146,
            148,
            151,
            152,
            154,
            155,
            156,
            157,
            158,
            164,
            165,
            167,
            171,
            174,
            175,
            176,
            179,
            180,
            181,
            182,
            183,
            184,
            188,
            194,
            195,
            196,
            197,
            198,
            199,
            200,
            201,
            202,
            203,
            204,
            205,
            206,
            207,
            208,
            209,
            210,
            212,
            215,
            217,
            220,
            224,
            226,
            227,
            243,
            244,
            245,
            246,
            248,
            249,
            250,
            251,
            252,
            253,
            254,
            256,
            258,
            259,
            262,
            263,
            264,
            265,
            266,
            267,
            268,
            269,
            271,
            272,
            273,
            275,
            277,
            279,
            280,
            281,
            282,
            283,
            300,
            301,
            303,
            307,
            310,
            312,
            318,
            323,
            328,
            331,
            336,
            337,
            338,
            342,
            345,
            350,
            351,
            352,
            353,
            355,
            356,
            357,
            358,
            360,
            361,
            363,
            364,
            365,
            381,
            382,
            383,
            384,
            385,
            386,
            387,
            388,
            389,
            390,
            391,
            392,
            393,
            394,
            396,
            397,
            398,
            399,
            400,
            401,
            402,
            403,
            404,
            405,
            407,
            408,
            409,
            411,
            412,
            413,
            414,
            416,
            417,
            419,
            420,
            421,
            422,
            423,
            424,
            425,
            428,
            429,
            433,
            434,
            435,
            436,
            437,
            438,
            439,
            440,
            443,
            444,
            445,
            447,
            449,
            452,
            458,
            459,
        ]
        entire_set = ['eicu']
        self.args = args
        if(mode == 'local'):
            self.hospital_ids = hospital_ids
            self.db_prefix = "hospital_"
        else:
            self.hospital_ids = entire_set
            self.db_prefix = ""
        # threshold to decide whether we want to train a model on this dataset or not
        self.train_threshold = train_threshold
        self.train_test_split = train_test_split

    def query_flow(self):
        for i in self.hospital_ids:
            dbname = "{}{}".format(self.db_prefix, i)
            print("querying {}".format(dbname))
            self.args.dbname = dbname
            self.cfg = config(self.args)
            aki_psql = aki_postgres.aki_sql(self.cfg)
            aki_psql.create_database_connection()
            aki_psql.execute_sql()
            aki_psql.save_sql()

    def preprocess_thread(self, hospital_id, args, sema):
        sema.acquire()
        args.dbname = "{}{}".format(self.db_prefix, hospital_id)
        print("preprocessing {}".format(args.dbname))
        cfg = config(args)
        # create dir if not existing yet
        Path(cfg.preprocessed_path()).mkdir(parents=True, exist_ok=True)
        # log file to be saved with insights of each hospital
        aki_preprocess.main(cfg)
        log_file = open(Path(cfg.preprocessed_path() / 'insights.csv'), 'w')
        aki_ml.clean_data_creat_only(cfg, log_file)
        aki_ml.clean_data_creat_ur(cfg, log_file)
        log_file.close()
        sema.release()

    def preprocess_flow(self):
        threads = list()
        # we use a semaphore in order not to overload the CPU too much
        maxthreads = 20
        sema = threading.Semaphore(value=maxthreads)
        for i in self.hospital_ids:
            x = threading.Thread(
                target=self.preprocess_thread, args=(i, self.args, sema))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

    def insights(self):
        insights_cols = ['hospital', 'creat_only_normal',
                         'creat_only_AKI_1', 'creat_only_AKI_2', 'creat_only_AKI_3', 'creat+urine_normal', 'creat+urine_AKI_1', 'creat+urine_AKI_2', 'creat+urine_AKI_3']
        insights_list = list()
        for hospital_id in self.hospital_ids:
            self.args.dbname = "{}{}".format(self.db_prefix, hospital_id)
            cfg = config(self.args)
            # log file to be saved with insights of each hospital
            file = Path(cfg.preprocessed_path() / 'insights.csv')

            log_rows = pd.read_csv(
                file, delimiter=':', nrows=12, names=['origin', 'metric', 'value'], header=None)
            if(len(log_rows) < 10):
                print("too few results, skipping {}".format(self.args.dbname))
                continue
            print(hospital_id, log_rows)
            creat_ur_NOR = log_rows.loc[(log_rows.origin == ('creat+urine')) & (
                log_rows.metric.str.contains('NORMAL Patients in 7DAY'))].value.values[0]
            creat_ur_AKI_1 = log_rows.loc[(log_rows.origin == ('creat+urine')) & (
                log_rows.metric.str.contains('AKI patients STAGE 1 within 7DAY'))].value.values[0]
            creat_ur_AKI_2 = log_rows.loc[(log_rows.origin == ('creat+urine')) & (
                log_rows.metric.str.contains('AKI Patients STAGE 2 in 7DAY'))].value.values[0]
            creat_ur_AKI_3 = log_rows.loc[(log_rows.origin == ('creat+urine')) & (
                log_rows.metric.str.contains('AKI Patients STAGE 3 7DAY'))].value.values[0]
            creat_NOR = log_rows.loc[(log_rows.origin == ('creat')) & (
                log_rows.metric.str.contains('NORMAL Patients in 7DAY'))].value.values[0]
            creat_AKI_1 = log_rows.loc[(log_rows.origin == ('creat')) & (
                log_rows.metric.str.contains('AKI patients STAGE 1 within 7DAY'))].value.values[0]
            creat_AKI_2 = log_rows.loc[(log_rows.origin == ('creat')) & (
                log_rows.metric.str.contains('AKI Patients STAGE 2 in 7DAY'))].value.values[0]
            creat_AKI_3 = log_rows.loc[(log_rows.origin == ('creat')) & (
                log_rows.metric.str.contains('AKI Patients STAGE 3 7DAY'))].value.values[0]
            log_df = pd.DataFrame(
                [[hospital_id, creat_NOR, creat_AKI_1, creat_AKI_2, creat_AKI_3, creat_ur_NOR, creat_ur_AKI_1, creat_ur_AKI_2, creat_ur_AKI_3]], columns=insights_cols)
            insights_list.append(log_df)
        insights_df = pd.concat(insights_list, ignore_index=True)
        insights_df.to_csv(
            Path(Path.cwd() / 'data' / 'eicu' / 'insights_{}.csv'.format(mode)))

    def verify_further_processing(self, hospital_id) -> bool:
        insights = pd.read_csv(
            Path(Path.cwd() / 'data' / 'eicu' / 'insights_{}.csv'.format(mode)))
        res_row = insights.loc[insights['hospital'] == hospital_id]
        if(len(res_row) == 0):
            print('skipping {} due to empty dataframe'.format(hospital_id))
            return False
        if((res_row.creat_only_normal.values < self.train_threshold) or
           (round(res_row.creat_only_AKI_1.values[0]*self.train_test_split) < 1.0) or
            (round(res_row.creat_only_AKI_2.values[0]*self.train_test_split) < 1.0) or
                (round(res_row.creat_only_AKI_3.values[0]*self.train_test_split) < 1.0)):
            print("skipping due to 1. {}\r\n 2. {}\r\n 3. {}\r\n 4. {}\r\n".format(res_row.creat_only_normal.values < self.train_threshold, round(res_row.creat_only_AKI_1.values[0] *
                  self.train_test_split), round(res_row.creat_only_AKI_2.values[0]*self.train_test_split), round(res_row.creat_only_AKI_3.values[0]*self.train_test_split)))
            return False
        else:
            print("ok to start training on hospital_{}, {}, {}, {}, {}".format(
                hospital_id, res_row.creat_only_normal.values, (res_row.creat_only_AKI_1.values[0] *
                  self.train_test_split), (res_row.creat_only_AKI_2.values[0] *
                  self.train_test_split), (res_row.creat_only_AKI_3.values[0] *
                  self.train_test_split)))
            return True

    def ml_flow(self):
        """
        we first have to iterate over all hospitals
        """
        # now we train the model per hospital_id
        for i in self.hospital_ids:
            with open(Path(Path.cwd() / 'data' / 'eicu' / 'trained.csv'), 'a', newline='') as trained_res_file:
                if(not self.verify_further_processing(i)):
                    print("Too few datapoints in dataset")
                    print("{},{}".format(i, "False"), file=trained_res_file)
                    continue
                else:
                    print("{},{}".format(i, "True"), file=trained_res_file)

            self.args.dbname = "{}{}".format(self.db_prefix, i)
            # cfg is the config containing the link to the model
            model_cfg = config(
                self.args, runname="creatinine_model_" + self.args.dbname)
            try:
                data = pd.read_parquet(model_cfg.cleaned_data_path() /
                                       "INFO_DATASET_7days_creatinine2.parquet")
            except FileNotFoundError as err:
                print("file not found error: {0}".format(err))
                continue
            aki_ml.run_aki_model(model_cfg, data)
            if(os.path.exists(model_cfg.metrics_path() / "{}_auroc_comparison.csv".format(model_cfg.runname))):
                print('removing the previous csv auroc file')
                os.remove(model_cfg.metrics_path() /
                          "{}_auroc_comparison.csv".format(model_cfg.runname))

    def validate_local_models(self):
        val_args = fakeArgsClass()
        # we'll iterate over the hospitals of which we've trained a model
        train_file = pd.read_csv(Path(
            Path.cwd() / 'data' / 'eicu' / 'trained.csv'), names=['hospital_id', 'train_bool'])
        self.train_ids = train_file.loc[train_file['train_bool']
                                        == True]['hospital_id'].tolist()

        auroc_df = pd.DataFrame(index=self.train_ids)
        for i in self.train_ids:
            self.args.dbname = "{}{}".format(self.db_prefix, i)
            print("validating {}".format(self.args.dbname))
            # cfg is the config containing the link to the model
            model_cfg = config(
                self.args, runname="creatinine_model_" + self.args.dbname)
            # we'll validate it on the other hospital databases
            auroc_list = list()
            for j in self.train_ids:
                # val_cfg is the dataset on which we'll validate the model from cfg
                val_args.dbname = "hospital_{}".format(j)
                val_cfg = config(val_args)
                # compute the auroc and save it to list
                auroc_list.append(aki_ml.validate_model(model_cfg, val_cfg))
            auroc_df[self.args.dbname] = auroc_list
        auroc_df.to_csv(Path(Path.cwd() / 'data' /
                        'eicu' / 'auroc_local_matrix.csv'))
        fig = px.imshow(auroc_df)
        fig.show()
        fig.write_html(Path(Path.cwd() / 'data' /
                            'eicu' / 'auroc_local_matrix.html'))

    def validate_global_model(self, name):
        val_args = fakeArgsClass()
        # we'll iterate over the hospitals of which we've trained a model
        train_file = pd.read_csv(Path(
            Path.cwd() / 'data' / 'eicu' / 'trained.csv'), names=['hospital_id', 'train_bool'])
        self.train_ids = train_file.loc[train_file['train_bool']
                                        == True]['hospital_id'].tolist()
        auroc_df = pd.DataFrame(index=self.train_ids)
        # self.args.dbname = "eicu"
        print("validating {}".format(self.args.dbname))
        # cfg is the config containing the link to the model
        model_cfg = config(
            self.args, runname="creatinine_model_" + self.args.dbname)
        # we'll validate it on the other hospital databases
        auroc_list = list()
        for j in self.train_ids:
            # val_cfg is the dataset on which we'll validate the model from cfg
            val_args.dbname = "hospital_{}".format(j)
            val_cfg = config(val_args)
            # compute the auroc and save it to list
            auroc_list.append(aki_ml.validate_model(model_cfg, val_cfg))
        auroc_df[self.args.dbname] = auroc_list
        auroc_df.to_csv(Path(Path.cwd() / 'data' /
                        'eicu' / 'auroc_{}_matrix.csv'.format(name)))
        fig = px.imshow(auroc_df)
        fig.show()
        fig.write_html(Path(Path.cwd() / 'data' /
                            'eicu' / 'auroc_{}_matrix.html'.format(name)))

    def combine_datasets(self):
        '''
        this function combines the cleaned datasets, forming one big dataset which can be used for stratified training (stratified over classes, not hospitals)
        Next we'll train a model on it.
        '''
        train_file = pd.read_csv(Path(
            Path.cwd() / 'data' / 'eicu' / 'trained.csv'), names=['hospital_id', 'train_bool'])
        self.train_ids = train_file.loc[train_file['train_bool']
                                        == True]['hospital_id'].tolist()
        print(self.train_ids)
        combined_dataset_list = list()
        for i in self.train_ids:
            combined_dataset_list.append(pd.read_parquet(Path(Path.cwd() / 'data' / 'eicu' / "hospital_{}".format(i) / 'clean_data' / 'INFO_DATASET_7days_creatinine2.parquet')))
        combined_dataset = pd.concat(combined_dataset_list)
        self.args.dbname = "{}".format('combined')
        model_cfg = config(
                self.args, runname="creatinine_model_" + self.args.dbname)
        Path(model_cfg.cleaned_data_path()).mkdir(parents=True, exist_ok=True)
        combined_dataset.to_parquet(Path.cwd() / 'data' /'eicu' / 'combined'/ 'combined_cleaned_dataset.parquet')
        
        aki_ml.run_aki_model(model_cfg, combined_dataset)


if __name__ == "__main__":
    load_dotenv()

    fakeArgs = fakeArgsClass()

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--query', action="store_true",
                        help="send out query requests to all dbs")
    parser.add_argument('-pp', '--preprocess', action="store_true",
                        help="send out preprocess requests to all queried parquet files")
    parser.add_argument('-i', '--insights', action="store_true",
                        help='print insights results form all dbs')
    parser.add_argument('-ml', '--machine_learning', action="store_true",
                        help="train ML model on all dbs and verify results")
    parser.add_argument('-v', '--validate', action="store_true",
                        help="validate ML model(s) on all dbs and verify results")
    parser.add_argument('-m', '--mode', help='define if we want to train on "local" or "global" datasets/hospitals', type=str,
                        choices=['local', 'global'], default='local')
    parser.add_argument('-c', '--combine', help='combine the cleaned datasets', action="store_true")
    args = parser.parse_args()
    mode = args.mode
    print("starting in {} mode".format(mode))
    lf = local_flow(fakeArgs, mode,
                    train_threshold=10, train_test_split=0.2)
    if args.query:
        lf.query_flow()
    elif args.preprocess:
        lf.preprocess_flow()
    elif args.insights:
        lf.insights()
    elif args.machine_learning:
        lf.ml_flow()
    elif args.validate:
        if(mode == 'local'):
            lf.validate_local_models()
        else:
            lf.args.dbname = "eicu"
            lf.validate_global_model(name="global")
    elif args.combine:
        # lf.combine_datasets()
        lf.args.dbname = "combined"
        lf.validate_global_model(name="combined")
    else:
        logger.error("Unknown command: {}".format(args.command))
