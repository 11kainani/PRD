import os 
import pandas as pd
from datetime import datetime, timedelta

class Loader(): 
    def __init__(self, site_directory):
        self.site_id = None
        self.directory = None
        self.main_data_file = None
        self.results_directory = None

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
            
            results_path = f'{self.directory}/results'
            if not os.path.isdir(results_path):
                os.makedirs(results_path)
            self.results_directory = results_path

    def main_data(self): 
        data = pd.read_csv(self.main_data_file)
        return data
    
    def data_model_from_file(self, day_of_week):
        """read the data of a csv file that corresponds to the model file of the day of the week

        Args:
            day_of_week (string): the name in english of a day of the week

        Returns:
            data: dataframe that corresponds to the model of that data
        """
        model_files = []
        
        for (dirpath, dirnames, filenames) in os.walk(f'{self.directory}/models'):
            model_files.extend(filenames)
            break
        assert len(model_files) > 0, "The model directory hasn't been created yet. Use Model_Generation to generate the model file for this site first"
        
        
        selected_model_list =  [f for f in model_files if f.endswith(f"{str.lower(day_of_week)}.csv")]

 
            

        selected_file = f'{self.directory}/models/{selected_model_list[0]}'
        assert os.path.isfile(selected_file), "The file doesn't exist for that date. Use Model_Generation to compute the file for that date" 
            
        data =  pd.read_csv(selected_file)

        data.set_index("time", inplace=True)
        
        return data
    
    def data_for_day_with_selection(self):
        """Read the data of a specific date

        Returns:
            selected_date : The date selected from the list of available dates
            data_selected_date: the data for that specific date
        """
        selected_file = self.main_data_file 
        assert os.path.isfile(selected_file), "The main file for this file doesn't exist. Create it using FileManager tagdivison"
        data = pd.read_csv(selected_file)
     
        data['datetime'] =  pd.to_datetime(data['datetime'])
        data['date'] = data['datetime'].dt.date
        group_by_date = data.groupby('date')
        
        unique_dates = []
        data_to_date = {}
        print("For this file select a date")
        for date, data in group_by_date: 
            unique_dates.append(date)
            data_to_date[date] = data

        for i, unique_date in enumerate(unique_dates, 1):
            print(f"{i}. {unique_date}")
            
        date_index = -1
        while(date_index < 0 or date_index >= len(unique_dates)):
            date_index = int(input("Select a file (enter the number): ")) - 1
            if(date_index < 0 or date_index >= len(unique_dates)):
                print("Selection outside of the available files - TRY AGAIN")
        
        selected_date = unique_dates[date_index]
    
        return selected_date,data_to_date[selected_date]
    
    def data_for_day(self, date:str):
        """_summary_

        Args:
            date (str): The date for the data selected. The format for the date is YYYY-MM-DD

        Returns:
            _type_: _description_
        """
              
        selected_file = self.main_data_file 
        assert os.path.isfile(selected_file), "The main file for this file doesn't exist. Create it using FileManager tagdivison"
        data = pd.read_csv(selected_file)
     
        data['datetime'] =  pd.to_datetime(data['datetime'])
        data['date'] = data['datetime'].dt.date
        group_by_date = data.groupby('date')
        
        unique_dates = []
        data_to_date = {}
        for unique_date, data in group_by_date: 
            unique_dates.append(unique_date)
            data['time'] = data['datetime'].dt.time
            data_to_date[unique_date] = data

        # Assuming the format is 'YYYY-MM-DD'
        date_in_datetime_format = datetime.strptime(date, '%Y-%m-%d').date()

        assert date_in_datetime_format in unique_dates, ("The date that you want doesn't have any data associated.")

        selected_data = pd.DataFrame(data_to_date[date_in_datetime_format])
        selected_data.set_index("time",inplace=True)
        
        
        return selected_data

    def data_for_week(self, start_date_str: str):
        """
        Generates a dictionary of data for the next seven days starting from the given start date.
        
        Args:
            start_date_str (str): The start date in the format 'YYYY-MM-DD'.
            
        Returns:
            tuple: A tuple containing a dictionary of data for the next seven days and a list of dates with missing data.
        """
        empty_set = []
        #get the date for the seven next days 
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = start_date + timedelta(days=7)
        data_dic = self.generate_date_dict(start_date,end_date)
        for key, value in data_dic.items(): 
            if value is None: 
                empty_set.append(key)

        return data_dic, empty_set    

        #Check if the date has the according data 

    def generate_date_dict(self, start_date:str, end_date:str):
        """
        Generates a dictionary with data for each date within the specified range.
        
        Args:
            start_date (str): The start date in the format 'YYYY-MM-DD'.
            end_date (str): The end date in the format 'YYYY-MM-DD'.
            
        Returns:
            dict: A dictionary with data for each date within the specified range.
        """
   
        date_dict = {}
        current_date = start_date

        while current_date <= end_date:
            selected_file_data = pd.read_csv(self.main_data_file, parse_dates=["datetime"])
            current_date_data = selected_file_data[selected_file_data["datetime"].dt.date == current_date]
            date_dict[current_date] = current_date_data
            current_date += timedelta(days=1)
        return date_dict

    def day_mean_result(self, date: str):
        """ Retrieves the mean results for a specific date.

        Args:
            date (str): The date for which the mean results are required in the format 'YYYY-MM-DD'.

        DataFrame: A DataFrame containing the mean results for the specified date.
        
        Raises:
            AssertionError: If there is no result file for the specified date.
        """
        results_list = []

        for (dirpath, dirnames, filenames) in os.walk(self.results_directory):
            results_list.extend(filenames)
            break
        filtered_results = [result for result in results_list if result.startswith(f'r_d_{date}')]
        
        assert len(filtered_results) != 0, "There is no result file for this specific date. Use the calculation class (méthode: day_mean_simple_verification) to create the appropriate file"

        results_data = pd.read_csv(f'{self.results_directory}/{filtered_results[0]}', index_col=0)

        return results_data

    def data_grouped_by_week(self):
        """
        Groups the main data by week.
        
        Returns:
            DataFrameGroupBy: A DataFrameGroupBy object containing the main data grouped by week.
        """
        dataset = self.main_data()
        dataset['datetime'] = pd.to_datetime(dataset['datetime'])
        dataset['dayname'] = dataset['datetime'].dt.day_name()
        dataset['time'] = dataset['datetime'].dt.time

        dataset.set_index('datetime')
        data_weekly = dataset.groupby([pd.Grouper(key='datetime', freq='W')])
        
        return data_weekly

    def get_available_dates(self):
        """
        Retrieves available dates from the main data.
        
        Returns:
            list: A list of available dates.
        """
        dates = list()
        for unique_date, data in self.main_data().iterrows(): 
            dates.append(data["datetime"])
        return dates

    def  get_available_dates_dataframe(self, data: pd.DataFrame):
        """
        Retrieves available dates from the provided DataFrame.
        
        Args:
            data (pd.DataFrame): The DataFrame containing the data.
            
        Returns:
            list: A list of available dates.
        """
        dates = list()
        for unique_date, data in data.iterrows(): 
            dates.append(data["datetime"])
        return dates

    def week_data(self,start_date : str):
        """Unfinished"""
        
        data = self.main_data()
        data['datetime'] = pd.to_datetime(data['datetime'])
        start_date = pd.to_datetime(str) 

        end_date = start_date + pd.DateOffset(days=6)

        week_data = data[(data['datetime'] >= start_date) & (data['datetime'] <= end_date)]

        week_data['date'] = week_data['datetime'].dt.date  
        return week_data          
if __name__ == "__main__": 
    obb = Loader("data/0a1b3040-2c06-4cce-8acf-38d6fc99b9f7")
    #print(obb.get_available_dates_dataframe(obb.data_for_day("2023-10-10")))
    #print(obb.data_model_from_file("friday"))
    #c,d = obb.data_for_day_with_selection()
    #print(c)
    #obb.data_for_week("2023-10-01")
    #print(obb.day_result("2023-10-01"))
    #week = obb.data_grouped_by_week()
    print(obb.week_data('2023-10-01'))

 