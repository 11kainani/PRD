import pandas as pd
import numpy as np 
import os
from datetime import datetime, timedelta
from collections import defaultdict

from loader import Loader

def remove_zscore_key_word(item :str):
            keyword = 'z_score_'
            return item.replace(keyword,'')

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
        all_first_anomalie_dict = {}
        for key, value in timestamp_dict.items():
            following_times = defaultdict(int)
            first_anomalie_dict = {}
            skip_list = set()
            first_main = []

            value = [datetime.strptime(item, '%H:%M:%S') for item in value]

            for timestamp in value:
                delay = 0
                while (timestamp + timedelta(minutes=delay)) in value:
                    if delay != 0:
                        following_times[timestamp.time()] += 1
                    delay += 1

            results_dict = sorted(following_times.items())
            for index, row in results_dict:
                if index not in first_main:
                    index_datetime = datetime.combine(datetime.min, index)
                    if index_datetime not in skip_list:
                        first_main.append(index)
                        first_anomalie_dict[index] = row
                    skip_list.update(datetime.combine(datetime.min, index) + timedelta(minutes=i) for i in range(1, row + 1))

            all_first_anomalie_dict[key] = first_anomalie_dict

        return all_first_anomalie_dict

    
        
    def day_anomalie_slope(self, date, only_critical = False):
        z_columns_slopes = {}
        results_data = Loader(self.directory).day_result(date)
        index_list = results_data.index.tolist()
        abnormal, worse =ver.day_zscore_verification(date)
        if only_critical:
            critical_level = worse
        else:
            critical_level = abnormal
        anomalies = self.day_following_timestamps(critical_level)

        print(anomalies)
        anomalie_slope = {}

        for key, data_anomalie in anomalies.items():
            print(key)
            anomalie_dates = data_anomalie.keys()
            anomalie_dates = [time_index.strftime('%H:%M:%S') for time_index in anomalie_dates]

            for anomalie_date in anomalie_dates:
                
                error_dict = {}
                target_value = results_data.loc[anomalie_date]
                current_index_position = index_list.index(anomalie_date)

                
                down_value = True
                index_delay = 0
                while down_value:
                    
                    index_delay +=1
                    previous_index = index_list[current_index_position - index_delay] if current_index_position > 0 else None
                    if(previous_index == None):
                        down_value = False
                        break
                    else:  
                        
                        current_index = index_list[current_index_position - (index_delay-1)]
                      

                        if results_data.loc[previous_index, key] > results_data.loc[current_index, key]:
                            error_dict[current_index] = results_data.loc[current_index, remove_zscore_key_word(key)] - results_data.loc[previous_index, remove_zscore_key_word(key)]
                            
                        else:
                            down_value= False
                            anomalie_slope[index_list[current_index_position]] = error_dict
                          

            
        return anomalie_slope
            
            

        

        
            

        

                
                  
if __name__ == "__main__":
    ver = Verification("data/0a1b3040-2c06-4cce-8acf-38d6fc99b9f7")
    abnormal, worse =ver.day_zscore_verification("2023-10-01")
    #print(worse)
    #print (ver.day_following_timestamps(worse))
    ver.day_anomalie_slope("2023-10-01",True)
        