from DataPrepare import DataPrepare
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

seasons = ['2017-2018']

dataPrepare = DataPrepare(seasons)
dataPrepare.get_csv_file()

