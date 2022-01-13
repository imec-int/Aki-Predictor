from pathlib import Path
from datetime import datetime
from copy import deepcopy

MIMIC_III = 'mimiciii'
EICU = 'eicu'

class config:
    def __init__(self,args,runname="") -> None:
        self.dbmodel = args.dbmodel
        if not args.dbmodel:
            self.dbmodel = EICU

        self.dbname = args.dbname
        if not args.dbname and self.dbmodel == EICU:
                self.dbname = "eicu"

        self.now = datetime.now()

        self.runname = runname

    def sql_path(self) -> Path:
        sql_pth = Path.cwd() / "sql"
        if self.dbmodel == MIMIC_III:
            return sql_pth / "mimicIII" # notice different casing from dbmodel
        elif self.dbmodel == EICU:
            return sql_pth / "eicu"
        else:
            return sql_pth / self.dbmodel

    def save_sql_path(self) -> Path:
        return Path.cwd() / 'sql' / 'save'

    def _data_path(self) -> Path:
        if self.dbname:
            return Path.cwd() / 'data' / self.dbmodel / self.dbname
        else:
            return Path.cwd() / 'data' / self.dbmodel

    def queried_path(self) -> Path:
        return self._data_path() / 'queried'

    def preprocessed_path(self) -> Path:
        return self._data_path() / 'preprocessed'

    def logs_path(self) -> Path:
        return self._data_path() / 'model' / self.runname / 'logs'

    def weights_path(self) -> Path:
        return self._data_path() / 'model' / self.runname / 'weights' / 'model.weights'

    def metrics_path(self) -> Path:
        return self._data_path() / 'model' / self.runname / 'metrics'

    def copy(self):
        return deepcopy(self)
