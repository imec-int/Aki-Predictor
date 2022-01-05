import flwr as fl
import argparse
import pandas as pd
import tensorflow as tf
import numpy as np

from pathlib import Path

from tensorflow.keras import callbacks

from aki_ml import create_model, cleanup_data, normalize_df, create_datasets, to_categorical, compute_metrics
from config import config

class FlwrClient(fl.client.NumPyClient):

    def __init__(self, config, input_filename, df_columns) -> None:
        self.config = config
        self.input_filename = input_filename
        self.df_columns = df_columns
        self.x_train, self.y_train, self.x_test, self.y_test = self.get_data()
        self.model = create_model(self.x_train.shape[1], self.y_train.shape[1])

    def get_data(self):
        input_pth = self.config.preprocessed_path() / self.input_filename
        df = pd.DataFrame()
        if input_pth.suffix == ".csv":
            df = pd.read_csv(input_pth)
        else: #input_pth.suffix == "parquet"
            df = pd.read_parquet(input_pth)
        
        df = cleanup_data(df)
        df = df[self.df_columns]
        df = normalize_df(df)
        train, train_label, test, test_label = create_datasets(df, split=0.2)

        self.test_label = test_label

        return train, to_categorical(train_label), test, to_categorical(test_label) # x_train, y_train, x_test, y_test

    def get_parameters(self):
        return self.model.get_weights()

    def fit(self, parameters, fit_config):
        self.model.set_weights(parameters)

        callbacks = [
            tf.keras.callbacks.EarlyStopping(monitor="loss", patience=10),
            tf.keras.callbacks.TensorBoard(log_dir=self.config.logs_path() / "round_{}".format(fit_config["round"])),
        ]

        #self.model.fit(self.x_train, self.y_train, epochs=1, batch_size=32, steps_per_epoch=3, callbacks=callbacks)
        self.model.fit(self.x_train, self.y_train, epochs=50, callbacks=callbacks, verbose="auto", use_multiprocessing=True)
        
        self.model.save_weights(cfg.weights_path())
        
        return self.model.get_weights(), len(self.x_train), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)

        metrics = dict()

        loss, accuracy = self.model.evaluate(self.x_test, self.y_test)
        metrics["accuracy"] = accuracy

        y_pred_test = np.argmax(self.model.predict(self.x_test), axis=-1)
        _, computed_metrics = compute_metrics(self.config, self.test_label, y_pred_test, multiclass=True)
        # flat_dict["classification_report"] = metrics["classification_report"] cannot be marshalled to protobuf
        # flat_dict["confusion_matrix"] = metrics["confusion_matrix"] cannot be marshalled to protobuf
        metrics["accuracy confusion matrix"] = computed_metrics["accuracy confusion matrix"]
        metrics["Area Under ROC"] = computed_metrics["Area Under ROC"]
        metrics["Accuracy score"] = computed_metrics["Accuracy score"]

        return loss, len(self.x_test), metrics


creat_df_columns = [
    "AKI",
    "AKI_STAGE_7DAY",
    "CREATININE_MAX",
    "CREATININE_MIN",
    "CREAT",
    "EGFR",
    "POTASSIUM_MAX",
    "GLUCOSE_MAX",
    "PLATELET_MIN",
    "BUN_MAX",
    "WBC_MIN",
    "PLATELET_MAX",
    "TEMPC_MEAN",
    "GLUCOSE_MEAN",
    "PTT_MAX",
    "TEMPC_MIN",
    "BUN_MIN",
    "HEMATOCRIT_MIN",
    "SPO2_MEAN",
    "MEANBP_MEAN",
    "AGE",
    "HEARTRATE_MEAN",
    "PT_MAX",
    "TEMPC_MAX",
    "RESPRATE_MEAN",
    "CHLORIDE_MAX",
    "GLUCOSE_MIN",
    "WBC_MAX",
    "DIASBP_MEAN",
    "SYSBP_MAX",
    "DIASBP_MIN",
    "CHLORIDE_MIN",
    "SPO2_MIN",
    "HEARTRATE_MAX",
    "HEMOGLOBIN_MAX",
    "SYSBP_MEAN",
    "HEMATOCRIT_MAX",
    "DIASBP_MAX",
    "HEARTRATE_MIN",
    "SYSBP_MIN",
    "SODIUM_MIN",
    "MEANBP_MAX",
    "BICARBONATE_MAX",
    "MEANBP_MIN",
    "SODIUM_MAX",
    "ANIONGAP_MAX",
    "ANIONGAP_MIN",
    "HEMOGLOBIN_MIN",
    "LACTATE_MIN",
    "BICARBONATE_MIN",
    "PTT_MIN",
    "PT_MIN",
    "BILIRUBIN_MAX",
    "RESPRATE_MIN",
    "LACTATE_MAX",
    "RESPRATE_MAX",
    "ALBUMIN_MIN",
    "POTASSIUM_MIN",
    "INR_MAX",
    "ALBUMIN_MAX",
    "BILIRUBIN_MIN",
    "INR_MIN",
    "BANDS_MIN",
    "ETHNICITY",
    "BANDS_MAX",
    "HYPERTENSION",
    "DIABETES_UNCOMPLICATED",
    "VALVULAR_DISEASE",
    "CONGESTIVE_HEART_FAILURE",
    "SPO2_MAX",
    "ALCOHOL_ABUSE",
    "GENDER",
    "CARDIAC_ARRHYTHMIAS",
    "PERIPHERAL_VASCULAR",
    "OBESITY",
    "HYPOTHYROIDISM",
    "DIABETES_COMPLICATED",
    "LIVER_DISEASE",
    "DRUG_ABUSE",
    "RENAL_FAILURE",
]

creat_urine_df_columns = [
    "AKI",
    "AKI_STAGE_7DAY",
    "UO_RT_24HR",
    "UO_RT_12HR",
    "UO_RT_6HR",
    "CREATININE_MAX",
    "CREATININE_MIN",
    "CREAT",
    "EGFR",
    "PLATELET_MAX",
    "WBC_MAX",
    "BUN_MAX",
    "PLATELET_MIN",
    "AGE",
    "GLUCOSE_MIN",
    "TEMPC_MIN",
    "WBC_MIN",
    "GLUCOSE_MAX",
    "DIASBP_MEAN",
    "BUN_MIN",
    "RESPRATE_MEAN",
    "SYSBP_MAX",
    "POTASSIUM_MAX",
    "CHLORIDE_MAX",
    "HEARTRATE_MAX",
    "HEARTRATE_MEAN",
    "SPO2_MEAN",
    "PTT_MAX",
    "MEANBP_MEAN",
    "CHLORIDE_MIN",
    "GLUCOSE_MEAN",
    "PTT_MIN",
    "TEMPC_MAX",
    "MEANBP_MIN",
    "ANIONGAP_MAX",
    "SODIUM_MIN",
    "HEMOGLOBIN_MAX",
    "HEMATOCRIT_MAX",
    "MEANBP_MAX",
    "DIASBP_MAX",
    "HEMATOCRIT_MIN",
    "SPO2_MIN",
    "SODIUM_MAX",
    "TEMPC_MEAN",
    "DIASBP_MIN",
    "HEARTRATE_MIN",
    "RESPRATE_MAX",
    "HEMOGLOBIN_MIN",
    "BICARBONATE_MAX",
    "SYSBP_MIN",
    "SYSBP_MEAN",
    "BICARBONATE_MIN",
    "POTASSIUM_MIN",
    "BILIRUBIN_MAX",
    "LACTATE_MAX",
    "ANIONGAP_MIN",
    "ALBUMIN_MAX",
    "PT_MIN",
    "BILIRUBIN_MIN",
    "INR_MIN",
    "ALBUMIN_MIN",
    "RESPRATE_MIN",
    "PT_MAX",
    "ETHNICITY",
    "LACTATE_MIN",
    "INR_MAX",
    "BANDS_MAX",
    "BANDS_MIN",
    "HYPERTENSION",
    "HYPOTHYROIDISM",
    "CONGESTIVE_HEART_FAILURE",
    "GENDER",
    "CARDIAC_ARRHYTHMIAS",
    "SPO2_MAX",
    "ALCOHOL_ABUSE",
    "DRUG_ABUSE",
    "VALVULAR_DISEASE",
    "OBESITY",
    "PERIPHERAL_VASCULAR",
    "DIABETES_COMPLICATED",
    "LIVER_DISEASE",
    "DIABETES_UNCOMPLICATED",
    "RENAL_FAILURE",
]

if __name__ == "__main__":
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
    cfg.runname = "flwr_creatinine_model_" + cfg.now.strftime("%Y%m%d-%H%M%S")

    fl.client.start_numpy_client(server_address="[::]:8080", client=FlwrClient(cfg, "INFO_DATASET_7days_creatinine2.parquet", creat_df_columns))