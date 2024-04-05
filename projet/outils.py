import pandas as pd
from statsmodels.tsa.stattools import adfuller
from loader import Loader
from model_generator import Model_generator
from calculation import Calculation
 
# import python numpy package
import numpy as np
class Outils: 
    def __init__(self):
        ''''''
    def isStationnary(self,data : pd.DataFrame):
        columns = ['auctions','revenue','impressions']

        for column in columns:
            res = adfuller(data[column])
            print(f'Augmneted Dickey_fuller Statistic ({column}): %f' % res[0])
            print('p-value: %f' % res[1])
            
            # printing the critical values at different alpha levels.
            print('critical values at different levels:')
            for k, v in res[4].items():
                print('\t%s: %.3f' % (k, v))

if __name__ == '__main__':
    directory = 'data/3ee1bd1f-01d8-4277-929d-53b1cebe457b'
    load = Loader(directory)
    Model_generator(directory)
    Calculation(directory).day_mean_simple_verification("2023-10-10")
    data = load.day_mean_result("2023-10-10")
    outils = Outils()
    outils.isStationnary(data)