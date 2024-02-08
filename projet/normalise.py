import os
import loader
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


from model_generator import Model_generator
from loader import Loader

class Normalise():
    def __init__(self, site_directory):
        self.site_id = None
        self.directory = None
        self.main_data_file = None
        self.laoder = None

        if site_directory is None:
             raise ValueError("Site directory cannot be None. Please provide a valid directory.")
        else:  
            if os.path.dirname(site_directory) != "data":
                site_directory = os.path.join("data", site_directory)      
            self.directory = site_directory.strip() 
            self.site_id = os.path.basename(self.directory)
            main = f'{self.directory}/{self.site_id}.csv' 
            if os.path.isfile(main):
                self.main_data_file = main
            else: 
                raise ValueError("The directory doesn't have the main data file(csv)")

        self.laoder = Loader(site_directory)
        self.generator = Model_generator(site_directory)
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
        data_load = self.laoder

        
        data_model = data_load.data_model_from_file(day_of_week)
        day_data = data_load.data_for_day(date)

        day_data = day_data[['revenue', 'auctions', 'impressions']]

    


        day_data = day_data.sort_index()
        data_model = data_model.sort_index()

        data_model.index = pd.to_datetime(data_model.index).time
     
        
        result = day_data.sub(data_model) 
        
        return result   

    def data_substraction_from_week_model(self):
        weekly = self.laoder.data_grouped_by_week()
        week_model = self.generator.mean_week()
        normalised_week = {}
        columns_to_substract = ['revenue', 'auctions', 'impressions']
        for index, data in weekly:
            data.set_index(['dayname','time'],  inplace=True)
            formated_data =  data[columns_to_substract].sub(week_model[columns_to_substract]).dropna()
            normalised_week[index[0].date()] = formated_data

        return normalised_week
        

    def local_outlier_factor_model(self, dataset):

        dataset["time"] = dataset.index
        #dataset["time_str"] = str(dataset["time"])
        #dataset["time_minutes"] = pd.to_datetime(dataset["time_str"], format="%H:%M:%S").dt.hour * 60 + pd.to_datetime(dataset["time_str"], format="%H:%M:%S").dt.minute

        dataset["time_str"] = dataset["time"].apply(lambda x: str(x).split()[-1])

        # Now 'time_str' should contain only the time part of the mixed-format strings
        dataset["time_minutes"] = pd.to_datetime(dataset["time_str"], format="%H:%M:%S", errors='coerce').dt.hour * 60 + pd.to_datetime(dataset["time_str"], format="%H:%M:%S", errors='coerce').dt.minute

        column_params = ["revenue", "auctions", "impressions"]

        data_subset = dataset[column_params]

        lof_model = LocalOutlierFactor(n_neighbors=2000, contamination=0.01)
        y_pred = lof_model.fit_predict(data_subset)

        
        # Visualize the results (scatter plot)
        for column in column_params:
            plt.scatter(dataset["time_minutes"], dataset[column], c=y_pred, cmap='viridis', label=f"{column} Outliers")

        plt.xlabel('Time (minutes since midnight)')
        plt.ylabel('Value')
        plt.legend()
        plt.show()

if __name__ == "__main__": 
    directory = "0a1b3040-2c06-4cce-8acf-38d6fc99b9f7"
    ii = Normalise(directory)
    #res =ii.data_substration_from_model("2023-10-01")
    #ii.local_outlier_factor_model(res)

    ii.data_substraction_from_week_model()