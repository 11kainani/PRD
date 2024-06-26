import os
import numpy as np
import pandas as pd

from normalise import Normalise
from loader import Loader

class Calculation():
    def __init__(self, directory):
        """Initialize the Calculation object.

    Args:
        directory (str): The directory path containing the data files.
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
            raise ValueError (f"The directory entered ({directory}) isn't a directory. Use FileManager to create the directory seperation then select a correct directory by coping the relative path in the data directory. Beware to replace the the antislash by /") 
        self.site_id = os.path.basename(directory)
        
        "Creation of the results sub directory"
        self.results_directory = f'{self.directory}/results'
        os.makedirs(self.results_directory,exist_ok=True)
        

    def day_mean_simple_verification(self,date:str):
            """Calculate 

            Args:
                date (str)[YYYY-MM-DD]: the date of the specific data
                normalized_data (dataframe): data that has been normalized with data_normalization()

            """
            normalized_data = Normalise(self.directory).data_substration_from_model(date)
            
            results_filename = f'{self.results_directory}/r_d_{date}_{self.site_id}.csv'
            columns = ['revenue', 'auctions', 'impressions']
            for column in columns: 
                mediane = np.nanpercentile(normalized_data[column], 50)
                moyenne = np.mean(normalized_data[column])
                k = 1.4826
                distance_ecart_type = [abs(value - mediane) for value in normalized_data[column]]
                MAD = np.std(distance_ecart_type)
                normalized_data[f'z_score_{column}'] = [(value - moyenne) / (k * MAD) for value in normalized_data[column]]

            normalized_data.to_csv(results_filename)
             

    def zscore_verification(self, data: pd.DataFrame):
        """Calculate the z-score for the given data.

    Args:
        data (pd.DataFrame): The data for which to calculate the z-score.

    Returns:
        pd.DataFrame: The input data DataFrame with z-score columns added.
    """
        columns = ['revenue', 'auctions', 'impressions']
        for column in columns: 
            mediane = np.percentile(data[column], 50)
            moyenne = np.mean(data[column])
            k = 1.4826
            distance_ecart_type = [abs(value - mediane) for value in data[column]]
            MAD = np.std(distance_ecart_type)
            data[f'z_score_{column}'] = [(value - moyenne) / (k * MAD) for value in data[column]]
        
        return data
        

        
    def day_rolling_average_calculation(self, date:str, window_size=4):
        """Calculate the rolling average for the given date.

    Args:
        date (str)['YYYY-MM-DD']: The dataset for which to calculate the rolling average.
        window_size (int, optional): The size of the rolling window. Defaults to 4.

    Returns:
        pd.DataFrame: The dataset with rolling average columns added.
    """
        ma_data = pd.DataFrame()
        columns = ['revenue', 'auctions', 'impressions']
        
        dataset = Loader(directory).data_for_day(date)
        assert dataset is not None, "The data for the selected day, make sure that the date contains data or change the date"
        dataset.set_index("datetime", inplace=True) 
        
        for column in columns:
            ma_data[f'ra_{column}'] = dataset[column].rolling(window=window_size).mean()
        
        return ma_data

    def rolling_average_calculation(self, dataset : pd.DataFrame, window_size=4):
        """Calculate the rolling average for the given dataset.

    Args:
        dataset (pd.DataFrame): The dataset for which to calculate the rolling average.
        window_size (int, optional): The size of the rolling window. Defaults to 4.

    Returns:
        pd.DataFrame: The dataset with rolling average columns added.
    """
        ma_data = pd.DataFrame()
        columns = ['revenue', 'auctions', 'impressions']
        dataset.set_index("datetime", inplace=True) 
        
        for column in columns:
            ma_data[f'ra_{column}'] = dataset[column].rolling(window=window_size).mean()
        
        return ma_data
    
    def day_moving_average_expo_calculation(self, date:str, smoothing_factor = 0.5 ,window_size=4):
        """Calculate the exponential moving average for a given date.

        Args:
            dataset (pd.DataFrame): The dataset for which to calculate the exponential moving average
            smoothing_factor (float, optional): The smoothing factor Defaults to 0.5.
            window_size (int, optional): The size of the window. Defaults to 4.

        Returns:
             pd.DataFrame: The dataset with exponential moving average columns added.
        """
        ma_data = pd.DataFrame()
        columns = ['revenue', 'auctions', 'impressions']
        
        dataset = Loader(directory).data_for_day(date)
        assert dataset.size > window_size , "There isn't enough data in your set"
        dataset.set_index("datetime", inplace=True) 
        
        
        for column in columns:
            ma_data[f'expma_{column}'] = round(dataset[column].ewm(alpha=smoothing_factor, adjust=False).mean(), window_size)
        
        return ma_data

    def moving_average_expo_calculation(self, dataset : pd.DataFrame, smoothing_factor = 0.5 ,window_size=4):
        """Calculate the exponential moving average for the given dataset.

        Args:
            dataset (pd.DataFrame): The dataset for which to calculate the exponential moving average
            smoothing_factor (float, optional): The smoothing factor Defaults to 0.5.
            window_size (int, optional): The size of the window. Defaults to 4.

        Returns:
             pd.DataFrame: The dataset with exponential moving average columns added.
        """

        assert dataset.size > window_size , "The dataset doesn't have enough values"

        ma_data = pd.DataFrame()
        columns = ['revenue', 'auctions', 'impressions']
        
        dataset.set_index("datetime", inplace=True) 
        
        
        for column in columns:
            ma_data[f'expma_{column}'] = round(dataset[column].ewm(alpha=smoothing_factor, adjust=False).mean(), window_size)
        
        return ma_data 

    
if __name__ == "__main__":
    directory = 'data/3ee1bd1f-01d8-4277-929d-53b1cebe457b'
    time = "2023-09-29"
    cal = Calculation(directory) 
    cal.day_mean_simple_verification(time)


    loader = Loader(directory)
    data = loader.week_data(time)
    normal = Normalise(directory)
    weekly = normal.data_substraction_from_week_model()

    results = cal.zscore_verification(data) 
    results.to_csv('test.csv')
        #values.to_csv(f'{index}_res.csv')
        
    #print(cal.moving_average_expo_calculation("2023-10-05"))
    #print(cal.rolling_average_calculation("2023-10-05"))