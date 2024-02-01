import pandas as pd
import numpy as np 
import os
from datetime import datetime, timedelta

from loader import Loader

class Verification: 
    def __init__(self, directory) -> None:
        self.directory = None 
        self.results_directory = None
        self.site_id = None
        assert directory is not None, "Directory is none so we cannot affect the directory to the class"
        directory = directory.strip()
        if os.path.dirname(directory) != "data":
            directory = os.path.join("data", directory)
        if os.path.isdir(directory): 
            self.directory = directory
        else:
            raise ValueError (f"The directory entered ({directory}) isn't a directory") 
        self.site_id = os.path.basename(directory)
        assert os.path.isdir(f'{self.directory}/results'), "The selected directory doesn't have any results"
        self.results_directory = f'{self.directory}/results'

    def day_zscore_verification(self,date):
        """For a selected date, verifies the result file associated and return all the dates with a zscore lesser than -2 and -3 on any of the columns. This method should be used after simple verification  

        Args:
            date (dataframe.date): return 2 elemets : The first element is the list of all the data that has a zscore lower than 2 which corresponds to a medium level of anoamlie. The second element concerns all the data that has a zscore worst than -3 which corresponds to an anormal  data entry 
        """
        
        results_data = Loader(self.directory).day_result(date)
        zscore_columns = ['z_score_revenue',
       'z_score_auctions', 'z_score_impressions']

        minus2_anomalies = {}
        minus3_anomalies = {}

        
        for column in zscore_columns:
            indices_minus2 = results_data.index[results_data[column] < -2].tolist()
            minus2_anomalies[column] =  list(set(indices_minus2))
            indices_minus3 = results_data.index[results_data[column] < -3].tolist()
            minus3_anomalies[column] = list(set(indices_minus3))


        return minus2_anomalies,minus3_anomalies
            

    def day_following_timestamps(self,timestamp_dict: dict):
        following_times = {}

        for key, value in timestamp_dict.items():
            # Convert strings to datetime objects
            value = [datetime.strptime(item, '%H:%M:%S') for item in value]

            for timestamp in value:
                delay = 0
                following_times[timestamp.time()] = 0
                while (timestamp + timedelta(minutes=delay)) in value:
                    following_times[timestamp.time()] += 1
                    delay += 1
        
        return following_times

    def day_anomalie_slope(self, date, error_level = False):
        mild, worse = self.day_zscore_verification(date)

        

                
                  
if __name__ == "__main__":
    ver = Verification("0a1b3040-2c06-4cce-8acf-38d6fc99b9f7")
    abnormal, worse =ver.day_zscore_verification("2023-10-01")
    print (ver.day_following_timestamps(worse))
    print(worse)
        