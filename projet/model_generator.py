import os 
import pandas as pd
from datetime import datetime, timedelta
from loader import Loader

class Model_generator(): 
    def __init__(self, directory):
        self.directory = None 
        self.base_file = None
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
        main_file = f'{directory}/{self.site_id}.csv'
        print(main_file)
        if not os.path.isfile(main_file): 
            raise ValueError("The main datafile doesn't exist")
        else:
            self.base_file = main_file
        
    def mean_per_day(self): 
        """Generate the model file for each day of the week
        """
        csv_file = self.base_file
        data = pd.read_csv(csv_file)
        data['datetime'] = pd.to_datetime(data['datetime'])
        day_data = data.groupby(data['datetime'].dt.day_name())

        for day_of_week, day in day_data: 
            data_means = pd.DataFrame()
            day['datetime'] = pd.to_datetime(day['datetime'])
            day['time'] = day['datetime'].dt.time  # Remove the parentheses here
            time_group = day.groupby([day['datetime'].dt.hour, day['datetime'].dt.minute])
            for times, group_data in time_group:
                mean_values = group_data[['revenue', 'auctions', 'impressions']].mean()
                mean_df = pd.DataFrame(mean_values).transpose()
                mean_df['time'] = pd.to_datetime(f"{times[0]:02d}:{times[1]:02d}").time()  # Convert the hour and minute to time
                data_means = pd.concat([data_means, mean_df], ignore_index=True)
            data_means = data_means[['time', 'revenue', 'auctions', 'impressions']]  # Reorder columns if needed
            os.makedirs(f'{self.directory}/models', exist_ok=True)
            file_base = os.path.splitext(os.path.basename(csv_file))[0]
            data_means.to_csv(f'{self.directory}/models/model_{str.lower(day_of_week)}.csv', index=False)

    def mean_per_weekend(self): 
        csv_file = self.base_file
        data = pd.read_csv(csv_file, parse_dates=["datetime"])
        data["date"] = data["datetime"].dt.date

        pd.to_datetime(data['date'])
        data.set_index("date", inplace=True)

        weekend_dic = {}
        for date, value in data.iterrows():
            date = pd.to_datetime(date)
            day_name = date.day_name()
            
            if day_name == 'Saturday':
                if date.date() not in weekend_dic:
                    weekend_dic[date.date()] = []
                weekend_dic[date.date()].append(value)
            elif day_name == 'Sunday':
                start_weekend_date = date - timedelta(days=1)
                start_weekend_date = start_weekend_date.date()
                if start_weekend_date not in weekend_dic:
                    weekend_dic[start_weekend_date] = []
                weekend_dic[start_weekend_date].append(value)

        os.makedirs(f'{self.directory}/models', exist_ok=True)
        file_base = os.path.splitext(os.path.basename(csv_file))[0]
        weekend_dic.to_csv(f'{self.directory}/models/model_weekend.csv', index=False)
                
        return weekend_dic
    
    def mean_week(self):
        data_means = pd.DataFrame()
        dataset = Loader(self.directory).main_data()
        dataset['datetime'] = pd.to_datetime(dataset['datetime'])
        dataset['dayname'] = dataset['datetime'].dt.day_name()
        dataset['time'] = dataset['datetime'].dt.time

        # Group by week and day of the week
        #data_weekly = dataset.groupby([pd.Grouper(key='datetime', freq='W')])

        mean_weekly = dataset.groupby(['dayname', 'time']).agg({'revenue': 'mean', 'impressions': 'mean', 'auctions' : 'mean'})

        os.makedirs(f'{self.directory}/models', exist_ok=True)
        mean_weekly.to_csv(f'{self.directory}/models/model_week.csv')
        return mean_weekly
          

    
if __name__ == "__main__":        
    directory = " f6b6b7f3-abad-46ed-8d39-1d36e6eed9ea"
    msl = Model_generator(directory)
    msl.mean_week()
    