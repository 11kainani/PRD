import os
import numpy as np
import pandas as pd

from normalise import Normalise

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
        

    def day_simple_verification(self,date):
            """Using simple statistic indicators, calculates scores for each data entry

            Args:
                date (panda date): the date of the specific data
                normalized_data (dataframe): data that has been normalized with data_normalization()

            Returns:
                lower_bound : The most lower bound using the interquartile method 
            """
            normalized_data = Normalise(self.directory).data_substration_from_model(date)
            print(normalized_data)
            results_filename = f'{self.results_directory}/r_d_{date}_{self.site_id}.csv'
            columns = ['revenue', 'auctions', 'impressions']
            lower_bounds = pd.DataFrame()
            for column in columns: 
                    #Quartile 1 (25% of the results)
                Q1 = np.percentile(normalized_data[column], 25)
                #Quartile 3 (75% of the results)
                Q3 = np.percentile(normalized_data[column], 75)
                #Mediane 
                mediane = np.percentile(normalized_data[column], 50)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                #Mean of the field
                moyenne = np.mean(normalized_data[column])
                #Calculation of the Z_Score_Modified
                k = 1.4826
                distance_ecart_type = [abs(value - mediane) for value in normalized_data[column]]
                MAD = np.std(distance_ecart_type)
                normalized_data[f'z_score_{column}'] = [(value - moyenne) / (k * MAD) for value in normalized_data[column]]
                lower_bounds[column] = lower_bound
            
            
            normalized_data.to_csv(results_filename)
            
            return lower_bounds    


if __name__ == "__main__":
    directory = " 0a1b3040-2c06-4cce-8acf-38d6fc99b9f7"
    cal = Calculation(directory) 
    cal.day_simple_verification("2023-10-01")