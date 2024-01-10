import os 
import pandas as pd
from datetime import datetime

class Loader(): 
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
    
    def data_for_day(self, date):
        """_summary_

        Args:
            date (pandas.Dataframe.date): The date for the data selected. The format for the date is YYYY-MM-DD

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
        print("For this file select a date")
        for unique_date, data in group_by_date: 
            unique_dates.append(unique_date)
            data['datetime'] = pd.to_datetime(data['datetime'])
            data['time'] = data['datetime'].dt.time
            data.set_index('time',inplace=True)
            data_to_date[unique_date] = data

        # Assuming the format is 'YYYY-MM-DD'
        date_in_datetime_format = datetime.strptime(date, '%Y-%m-%d').date()

        assert date_in_datetime_format in unique_dates, ("The date that you want doesn't have any data associated.")
    
        return data_to_date[date_in_datetime_format]

    def data_for_week():
        ""
if __name__ == "__main__": 
    obb = Loader("400a2fd4-d9cd-4b18-aa2f-06f245688ebf")
    #print(obb.data_model_from_file("friday"))
    #c,d = obb.data_for_day_with_selection()
    #print(c)
    print(obb.data_for_day("2023-10-01"))