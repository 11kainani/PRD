import os 
import pandas as pd


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


directory = " 0a1b3040-2c06-4cce-8acf-38d6fc99b9f7"
msl = Model_generator(directory)
msl.mean_per_day()