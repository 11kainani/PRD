import os
import numpy as np
import pandas as pd

from normalise import Normalise
from loader import Loader

class Calculation():
    def __init__(self, directory):
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
        
        "Creation of the results sub directory"
        self.results_directory = f'{self.directory}/results'
        os.makedirs(self.results_directory,exist_ok=True)
        

    def day_mean_simple_verification(self,date):
            """Using simple statistic indicators, calculates scores for each data entry

            Args:
                date (panda date): the date of the specific data
                normalized_data (dataframe): data that has been normalized with data_normalization()

            """
            normalized_data = Normalise(self.directory).data_substration_from_model(date)
            
            results_filename = f'{self.results_directory}/r_d_{date}_{self.site_id}.csv'
            columns = ['revenue', 'auctions', 'impressions']
            for column in columns: 
                #Mediane 
                mediane = np.nanpercentile(normalized_data[column], 50)
                #Mean of the field
                moyenne = np.mean(normalized_data[column])
                #Calculation of the Z_Score_Modified
                k = 1.4826

                
                distance_ecart_type = [abs(value - mediane) for value in normalized_data[column]]
                MAD = np.std(distance_ecart_type)
                normalized_data[f'z_score_{column}'] = [(value - moyenne) / (k * MAD) for value in normalized_data[column]]

            normalized_data.to_csv(results_filename)
             

    def simple_verification(self, data: pd.DataFrame):
        columns = ['revenue', 'auctions', 'impressions']
        for column in columns: 
           
            #Mediane 
            mediane = np.percentile(data[column], 50)
            #Mean of the field
            moyenne = np.mean(data[column])
            #Calculation of the Z_Score_Modified
            k = 1.4826
            distance_ecart_type = [abs(value - mediane) for value in data[column]]
            MAD = np.std(distance_ecart_type)
            data[f'z_score_{column}'] = [(value - moyenne) / (k * MAD) for value in data[column]]
        
        return data
        

        
    def rolling_average_calculation(self, date, window_size=4):
        ma_data = pd.DataFrame()
        columns = ['revenue', 'auctions', 'impressions']
        
        dataset = Loader(directory).data_for_day(date)
        dataset.set_index("datetime", inplace=True) 
        
        for column in columns:
            ma_data[f'ra_{column}'] = dataset[column].rolling(window=window_size).mean()
        
        return ma_data
    
    def moving_average_expo_calculation(self, date, smoothing_factor = 0.5 ,window_size=4):
        ma_data = pd.DataFrame()
        columns = ['revenue', 'auctions', 'impressions']
        
        dataset = Loader(directory).data_for_day(date)
        dataset.set_index("datetime", inplace=True) 
        
        
        for column in columns:
            ma_data[f'expma_{column}'] = round(dataset[column].ewm(alpha=smoothing_factor, adjust=False).mean(), 4)
        
        return ma_data

    
if __name__ == "__main__":
    directory = "3ee1bd1f-01d8-4277-929d-53b1cebe457b"
    cal = Calculation(directory) 
    cal.day_mean_simple_verification("2023-10-10")


    loader = Loader(directory)
    data = loader.data_for_week("2023-10-10")
    normal = Normalise(directory)
    weekly = normal.data_substraction_from_week_model()

    for index, data in weekly.items(): 
        values = cal.simple_verification(data)

        #values.to_csv(f'{index}_res.csv')
        
    #print(cal.moving_average_expo_calculation("2023-10-05"))
    #print(cal.rolling_average_calculation("2023-10-05"))