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
        results_list = []

        for (dirpath, dirnames, filenames) in os.walk(self.results_directory):
            results_list.extend(filenames)
            break
        filtered_results = [result for result in results_list if result.startswith(f'r_d_{date}')]

        assert len(filtered_results != 0), "There is no result file for this specific date"

        results_data = pd.read_csv(filtered_results[0])
        
if __name__ == "__main__":
    ver = Verification("0a1b3040-2c06-4cce-8acf-38d6fc99b9f7")
    ver.day_zscore_verification("2023-10-01")
        