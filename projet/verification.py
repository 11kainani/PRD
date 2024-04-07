import pandas as pd
import numpy as np 
import os
from normalise import Normalise
from datetime import datetime, timedelta
from collections import defaultdict
from tabulate import tabulate
import csv 
from loader import Loader
from calculation import Calculation
from statsmodels.tsa.stattools import adfuller

def remove_zscore_key_word(item :str):
            keyword = 'z_score_'
            return item.replace(keyword,'')

class Verification: 
    def __init__(self, directory) -> None:
        """Initialize the Verification class with the directory containing data files.

        Args:
            directory (str): The directory path containing the data files.

        Raises:
            ValueError: If the directory is None or invalid.
        """
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
        self.normalise = Normalise(directory)
        self.loader = Loader(directory)
        self.calcul = Calculation(directory)

    def day_mean_zscore_verification(self,date,seuil = 3):
        """Verify the z-scores for a given date and return anomalies.

        Args:
            date (str): The date to be verified.
            seuil (int, optional): The threshold value for z-score anomalies. Defaults to 3.

        Returns:
            dict: A dictionary containing anomalies based on z-scores for each column.
        """
        
        results_data = Loader(self.directory).day_mean_result(date)
        zscore_columns = ['z_score_revenue',
       'z_score_auctions', 'z_score_impressions']

        anomalies = {}
        

        for column in zscore_columns:
            indices = results_data.index[results_data[column] < -seuil].tolist()
            anomalies[column] =  list(set(indices))
            

        
        return anomalies

    def z_score_verification(self, data: pd.DataFrame, seuil : float):
        """Verify z-scores for a given DataFrame and return anomalies.

        Args:
            data (pd.DataFrame): The DataFrame to be verified.
            seuil (int): The threshold value for z-score anomalies.

        Returns:
            dict: A dictionary containing anomalies based on z-scores for each column.
        """
        zscore_columns = ['z_score_revenue',
       'z_score_auctions', 'z_score_impressions']

        anomalies = {}
     
        for column in zscore_columns:
            indices = data.index[data[column] < -seuil].tolist()
            indices = [item.strftime('%H:%M:%S') for item in indices]
            anomalies[column] =  list(set(indices))

    
        return anomalies
        
            

    def day_following_timestamps(self,timestamp_dict: dict):
        """Find the following timestamps for anomalies.

        Args:
            timestamp_dict (dict): A dictionary containing timestamps of anomalies.

        Returns:
            dict: A dictionary containing the following timestamps for anomalies.
        """

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
                    delay +=  1

                
                following_times[timestamp.time()] = delay-1 #Subtract 1 beacause delay start at 0 so if an anomalie is detected but the the next value isn't an anomalie, delay == 1 but following_times should be 0
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

            
        
    def day_anomalie_slope(self, date : str, seuil : float):
        """Calculate the slope of anomalies for a given date.

        Args:
            date (str): The date to be analyzed.
            seuil (int): The threshold value for z-score anomalies.

        Returns:
            dict: A dictionary containing the slope of anomalies for each column.
        """
        z_columns_slopes = {}
        day_data = Loader(self.directory).data_for_day(date)
        zscore_calculation_data = Calculation(self.directory).zscore_verification(day_data)
        index_list = zscore_calculation_data.index.tolist()
        index_list.sort()
        errors = self.z_score_verification(zscore_calculation_data,seuil)
        anomalies = self.day_following_timestamps(errors)
        anomalie_slope = {}
        error_dict = {}
        for key, data_anomalie in anomalies.items():
            anomalie_dates = data_anomalie.keys()
            anomalie_dates = [time_index.strftime('%H:%M:%S') for time_index in anomalie_dates]
            for anomalie_date in anomalie_dates:  
                if isinstance(anomalie_date, str):
                    anomalie_date = datetime.strptime(anomalie_date, '%H:%M:%S').time() 
                current_index_position = index_list.index(anomalie_date)
                current_index = index_list[current_index_position]
                previous_index = index_list[current_index_position - 1] if current_index_position > 0 else None
                assert previous_index != None, f'There is no previous index for this data {index_list[current_index_position - 1]}'
                drop = (day_data.loc[previous_index,remove_zscore_key_word(key)] - day_data.loc[current_index,remove_zscore_key_word(key)])  / day_data.loc[previous_index,remove_zscore_key_word(key)] * 100
              
                anomalie_slope[index_list[current_index_position]] = drop
            z_columns_slopes[key]= anomalie_slope
            anomalie_slope= {}
        return z_columns_slopes
        

        
    def day_mean_anomalie_slope(self, date : str, seuil : float):
        """Calculate the mean slope of anomalies for a given date.

        Args:
            date (str): The date to be analyzed.
            seuil (int): The threshold value for z-score anomalies.

        Returns:
            dict: A dictionary containing the mean slope of anomalies for each column.
        """
        z_columns_slopes = {}
        results_data = Loader(self.directory).day_mean_result(date)
        index_list = results_data.index.tolist()
        index_list.sort()
        errors =self.day_mean_zscore_verification(date, seuil)
        anomalies = self.day_following_timestamps(errors)
        anomalie_slope = {}
        error_dict = {}
        for key, data_anomalie in anomalies.items():
            anomalie_dates = data_anomalie.keys()
            anomalie_dates = [time_index.strftime('%H:%M:%S') for time_index in anomalie_dates]
            
            for anomalie_date in anomalie_dates:
                current_index_position = index_list.index(anomalie_date)
                current_index = index_list[current_index_position]
                previous_index = index_list[current_index_position - 1] if current_index_position > 0 else None

                if current_index_position == 0: 
                    drop = 0
                else:
                #assert previous_index != None, 'There is no previous index for this data'
                    drop = (-results_data.loc[previous_index,remove_zscore_key_word(key)] + results_data.loc[current_index,remove_zscore_key_word(key)])  / results_data.loc[previous_index,remove_zscore_key_word(key)] * 100
                anomalie_slope[index_list[current_index_position]] = drop
           
            z_columns_slopes[key]= anomalie_slope
            anomalie_slope= {}
        return z_columns_slopes
        
            
    def convert_time_to_str(self,time_obj : datetime.time):
        """Convert a datetime object to a string in '%H:%M:%S' format.

        Args:
            time_obj (datetime): The datetime object to be converted.

        Returns:
            str: The string representation of the time object.
        """
        return time_obj.strftime('%H:%M:%S')


        
    def following_error_drop_dict(self,following : dict,previous_data: dict ):
        """Combine following anomalies with their corresponding drop values.

        Args:
            following (dict): A dictionary containing following anomalies.
            previous_data (dict): A dictionary containing previous data.

        Returns:
            dict: A dictionary containing following anomalies with drop values.
        """
        
        result_dict = {}
        for key in following.keys():
            result_dict[key] = {}
            for time_key, value in following[key].items():
                str_time_key = self.convert_time_to_str(time_key)
                result_dict[key][str_time_key] = {'serie': value}

            for time_key, value in previous_data[key].items():
                if isinstance(time_key, str) == False: 
                    time_key = self.convert_time_to_str(time_key)
                str_time_key = time_key
                if str_time_key not in result_dict[key]:
                    result_dict[key][str_time_key] = {}
                result_dict[key][str_time_key]['drop'] = value
        return result_dict
        
    def _save_following_drop_csv(result_dict: dict):
        """Save following anomalies with drop values to a CSV file.

        Args:
            result_dict (dict): A dictionary containing following anomalies with drop values.
        """
        for key, data in result_dict.items():
            csv_filename = f"{key}_data.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                fieldnames = ['time', 'previous', 'drop']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for time_key, values in data.items():
                    writer.writerow({
                        'time': time_key,
                        'previous': values.get('previous', ''),
                        'drop': values.get('drop', '')
                    })

            print(f"CSV file '{csv_filename}' created successfully.")

       
    def _add_minutes_to_time(self,input_time_str:str, delta_minutes : int):
        """Add minutes to a time string.

        Args:
            input_time_str (str): The input time string in '%H:%M:%S' format.
            delta_minutes (int): The number of minutes to add.

        Returns:
            str: The resulting time string after adding minutes.
        """
        input_time = datetime.strptime(input_time_str, '%H:%M:%S')
        result_time = input_time + timedelta(minutes=delta_minutes)
        result_time_str = result_time.strftime('%H:%M:%S')

        return result_time_str 

    def filter_drop_series(self, drop_series_dict : dict, drop = 0, serie = 2):
        filtered_dict = {}
        for category, values in drop_series_dict.items():
            condition_respected_dict = {}
            for key, results in values.items():
                if results.get('drop') >= drop and results.get('serie') >= serie:
                    condition_respected_dict[key]=results
            filtered_dict[category] = condition_respected_dict
        return (filtered_dict)
                    
            
    def day_analyze_and_print_results(self, directory:str, time:str, seuil = 2.0,  min_serie = 0, min_drop = 0):
        """Analyze anomalies for a given day and print the results.

        Args:
            directory (str): The directory containing data files.
            time (str): The date to be analyzed.
            seuil (int): The threshold value for z-score anomalies.

        Returns:
            None
        """
        assert seuil >= 0.0 , "Le seuil doit être un nombre positif"
        assert min_serie >= 0, "Le min_serie doit être positif"
        assert min_drop >= 0 , "Le min_drop doit être positif"
        day_data = Loader(directory).data_for_day(time)
        results_data = Calculation(directory).zscore_verification(day_data)
        
        abnormal = self.z_score_verification(results_data, seuil)
        following = self.day_following_timestamps(abnormal)
        previous_data = self.day_anomalie_slope(time, seuil)

        # Concatenate dictionaries with the desired format
        drop_series_dict = self.following_error_drop_dict(following, previous_data)
        filtered_drop_series_dict = self.filter_drop_series(drop_series_dict,min_drop,min_serie)
        self.prettier_following_drop(filtered_drop_series_dict)
        

    def day_mean_analyze_and_print_results(self, time : str, seuil = 2.0, min_serie = 0, min_drop = 0):
        """Analyze mean anomalies for a given day and print the results.

        Args:
            time (str): The date to be analyzed.
            seuil (int): The threshold value for z-score anomalies.

        Returns:
            None
        """
        assert seuil >= 0.0 , "Le seuil doit être un nombre positif"
        assert min_serie >= 0, "Le min_serie doit être positif"
        assert min_drop >= 0 , "Le min_drop doit être positif"
        abnormal =self.day_mean_zscore_verification(time, seuil)
        following = self.day_following_timestamps(abnormal)
        previous_data = self.day_mean_anomalie_slope(time,seuil)
        
        
        drop_series_dict = self.following_error_drop_dict(following, previous_data)
        filtered_drop_series_dict = self.filter_drop_series(drop_series_dict,min_drop,min_serie)
        self.prettier_following_drop(filtered_drop_series_dict)

   
        
    def prettier_following_drop(self,result_dict):
        """Print following anomalies with drop values in a prettier format.

        Args:
            result_dict (dict): A dictionary containing following anomalies with drop values.

        Returns:
            None
        """
        for key, data in result_dict.items():
            print(f"\n{key} data:")
            print("{:<12} {:<10} {:<10} {:<10}".format('Time', 'End_time' ,'Serie', 'Drop'))
            for time_key, values in data.items():
                print("{:<12} {:<10} {:<10} {:<10}".format(
                    time_key, self._add_minutes_to_time(time_key, values.get('serie', '') ) , values.get('serie', ''), values.get('drop', '')
                ))

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
               
if __name__ == "__main__":
    directory = 'data/3ee1bd1f-01d8-4277-929d-53b1cebe457b'
    time = "2023-09-29"
    ver = Verification(directory)
    Calculation(directory).day_mean_simple_verification(time)
    seuil = 2
    min_serie =2
    min_drop = 16
    
    mean =True 
    if mean: 
        ver.day_mean_analyze_and_print_results(time,seuil,min_serie,min_drop)
    else:    
        ver.day_analyze_and_print_results(directory,time,seuil,min_serie,min_drop)
    
   
    
    ver.week_analyze_and_print_results(time,seuil,min_serie,min_drop)