import os
from DataPrepare import DataPrepare
import numpy as np


class Utils:

    @staticmethod
    def delete_file(path_to_file):
        if os.path.exists(path_to_file):
            os.remove(path_to_file)
            return True
        else:
            return False

    @staticmethod
    def get_snooker_data(seasons=['2017-2018']):
        data_prepare = DataPrepare(seasons)
        data_prepare.get_csv_file()
        return True

    @staticmethod
    def convert_seasons(since, to):
        result = []
        for i in range(int(since), int(to)):
            s = str(i) + "-" + str(i+1)
            result.append(s)
        return result
