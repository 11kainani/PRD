import os
import loader
import pandas as pd

import model_generator

class Normalise():
    def __init__(self, site_directory):
        self.site_id = None
        self.directory = None
        self.main_data_file = None

        if site_directory is None:
             raise ValueError("Site directory cannot be None. Please provide a valid directory.")
        else:   
            if os.path.dirname(site_directory) != "data":
                site_directory = os.path.join("data", site_directory)      
            self.directory = site_directory
            self.site_id = os.path.basename(self.directory)
            main = f'{self.directory}/{self.site_id}.csv' 
            if os.path.isfile(main):
                self.main_data_file = main
            else: 
                raise ValueError("The directory doesn't have the main data file(csv)")

    def data_substration_from_model(self, date):
        """Normalises the data so i can be used to calculate 

        Args:
            date (string): he date of the data to be used 
            data : The data of a site

        Returns:
            results: Dataframe of the normalized data
        """
        day_of_week = pd.to_datetime(date).day_name()
        ##Transformation of the date to the name of it in the day of the week
        data_load = loader.Loader(self.directory)
        
        data_model = data_load.data_model_from_file(day_of_week)
        day_data = data_load.data_for_day(date)


        print(day_data)
        print(data_model)
        columns_to_subtract = ['revenue', 'auctions', 'impressions']
        result = day_data[columns_to_subtract].sub(data_model[columns_to_subtract], fill_value=0)
       
        return result   

if __name__ == "__main__": 

    
    
    
    ii = Normalise("0a1b3040-2c06-4cce-8acf-38d6fc99b9f7")
    print(ii.data_substration_from_model("2023-10-07"))