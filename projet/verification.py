import pandas as pd
import numpy as np 
import os

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
        results_list = []

        for (dirpath, dirnames, filenames) in os.walk(self.results_directory):
            results_list.extend(filenames)
            break
        filtered_results = [result for result in results_list if result.startswith(f'r_d_{date}')]

        assert len(filtered_results) != 0, "There is no result file for this specific date"

        results_data = pd.read_csv(f'{self.results_directory}/{filtered_results[0]}', index_col=0)
        
        print(results_data.columns)
        zscore_columns = ['z_score_revenue',
       'z_score_auctions', 'z_score_impressions']

        minus2_anomalies = {}
        minus3_anomalies = {}

        
        for column in zscore_columns:
            indices_minus2 = results_data.index[results_data[column] < -2].tolist()
            #Remove duplicates
            minus2_anomalies[column] =  list(set(indices_minus2))

            indices_minus3 = results_data.index[results_data[column] < -3].tolist()
            minus3_anomalies[column] = list(set(indices_minus3))


        return minus2_anomalies,minus3_anomalies
            
        
if __name__ == "__main__":
    ver = Verification("0a1b3040-2c06-4cce-8acf-38d6fc99b9f7")
    ver.day_zscore_verification("2023-10-01")
        