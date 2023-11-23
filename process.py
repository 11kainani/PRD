import pandas as pd
import os
import numpy as np
import time
import matplotlib.pyplot  as plt

class DataProcessor: 
    def __init__(self):
        self.data_directory = 'data'
        self.datafile_location = 'data/data.csv'
        self.selected_directory = None
        """ The currrent directory to be studied -> A directory corresponds to a site 
        """
        self.base_csv_file = None 
        """The current file to be studied -> This file corresponds to the day of the week we want to study
        """
        self.proccessus()
    
    def _tag_division(self):
         
        csv_path = f'{self.data_directory}/data.csv'
        separators = [';', ',']  
        group_field = 'tagid'


        for sep in separators:
            try:
                data = pd.read_csv(csv_path, sep=sep, encoding='utf-8')
                if data.columns.size > 1 :
                    break          
            except pd.errors.ParserError:
                continue  

        if 'data' in locals():  
            print("Données correctemment récuperé")
        else:
            print("Les données n'ont pas été correctement lus, vérifiez le séparateur [',' ou ';'] et le formatage des données")

        
        #[(value - moyenne) / (k * MAD) for value in data[column]]
        grouped = data.groupby(group_field)

        for group_key, group_data in grouped:
            directory = f'data/{group_key}'
            os.makedirs(directory, exist_ok=True)
            # Trier les données du groupe par date, heures et minutes
            sorted_grouped_data = group_data.sort_values(by=['date', 'hours', 'minutes'], ascending=[False, False, False])
            sorted_grouped_data['datetime'] = pd.to_datetime(sorted_grouped_data['date'] + ' ' + sorted_grouped_data['hours'].astype(str) + ':' + sorted_grouped_data['minutes'].astype(str))
            sorted_grouped_data['weekday'] = sorted_grouped_data['datetime'].dt.day_name()
            # Créer le nom du fichier en utilisant la date du groupe
            filename = f'{directory}/{group_key}.csv'
            # Sauvegarder les données du groupe dans le fichier
            selected_columns =  sorted_grouped_data[['datetime','currency','revenue','auctions','impressions','weekday']]
            selected_columns.to_csv(filename, index=False)

        '''
         Divide the data into seperate directories according to the site id. The files are once again seperated into different csv files according to the date of the mesure
        '''
        def _day_division(self):
            csv_path = self.datafile_location
            
            separators = [';', ',']  
            group_field = 'tagid'


            for sep in separators:
                try:
                    data = pd.read_csv(csv_path, sep=sep, encoding='utf-8')
                    if data.columns.size > 1 :
                        break          
                except pd.errors.ParserError:
                    continue  

            if 'data' in locals():  
                print("Données correctemment récuperé")
            else:
                print("Les données n'ont pas été correctement lus, vérifiez le séparateur [',' ou ';'] et le formatage des données")


            grouped = data.groupby(group_field)

            for group_key, group_data in grouped:
                # Trier les données du groupe par date, heures et minutes
                sorted_grouped_data = group_data.sort_values(by=['date', 'hours', 'minutes'], ascending=[False, False, False])

                # Créer le répertoire pour le groupe s'il n'existe pas
                directory = f'data/{group_key}/days'
                os.makedirs(directory, exist_ok=True)

                # Parcourir les données triées par date
                for date, row in sorted_grouped_data.groupby('date'):
                    row['datetime'] = pd.to_datetime(row['date'] + ' ' + row['hours'].astype(str) + ':' + row['minutes'].astype(str))
                    row['time'] = row['datetime'].dt.time
                    # Créer le nom du fichier en utilisant la date du groupe
                    filename = f'{directory}/{date}_{group_key}.csv'
                    # Sauvegarder les données du groupe dans le fichier
                    selected_columns =  row[['time','currency','revenue','auctions','impressions']]
                    selected_columns.to_csv(filename, index=False)
        
    def _day_regroupement(self,data):
        """ Get the unique dates in a dataframe and regroup 

        Args:
            data (Dataframe): the dataframe that has been retreive from the csv

        Returns:
            dataFrame: Dataframe regrouped by their date
        """
        data['datetime'] = pd.to_datetime(data['datetime'])
        unique_dates = data['datetime'].dt.date.unique()  # Replace 'date_column_name' with the actual column name
        date_groups = {day: [] for day in range(7)}
        for date in unique_dates:
                day_of_week = date.weekday()  # 0 for Monday, 6 for Sunday
                date_groups[day_of_week].append(date)
        return date_groups
    
    def _getDayOfWeek(self,week_number): 
        """
        Map associating an int to the correct day of the week

        Args:
            week_number (_type_): An integer between [0;6]

        Returns:
            string: the name of the day of the week
        """
        week_index = {
            0: 'monday', #Monday
            1: 'tuesday', 
            2:'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday', #Sunday
        }
        return week_index[week_number]
        
    def _directoryFromFile(self):
        """Get the directory of the current file

        Returns:
            string: the name of the directory of the selected file
        """
        csv_name = str(self.base_csv_file)
        directory = os.path.dirname(csv_name)
        return directory

        
    def _filter_and_save_data(self,data, date_groups):
        """
        Filters the data of a site accordining to the unique dates in date_groups and creates seperate files that containes the informations for all the data in that specific day
        Creates weekdays directory
        Args:
            pandas dataframe with theses columns [datetime,currency,revenue,auctions,impressions]: datatime as a pandas datetime yyyy-mm-dd hh:mm:ss
            date_groups (Dict): A dictionnaires with each date associated with it day of week 
        """
        directory = f'{self._directoryFromFile()}/weekdays'
        os.makedirs(directory, exist_ok=True)
        for day_of_week, dates in date_groups.items():
            # Filter the data for the current day_of_week
            filtered_data = data[data['datetime'].dt.weekday == day_of_week]
            
            # Save the filtered data to a CSV file
            csv_name = f'{directory}/data_{self._getDayOfWeek(day_of_week)}.csv'
            filtered_data.to_csv(csv_name, index=False)
            
        
    def _file_selection(self):
        """Select the base file to be used to construct the model files
        """
        # Select a directory
        directories = self._directory_selection()
        for (dirpath, dirnames, filenames) in os.walk(self.data_directory):
            directories.extend(dirnames)
            break
        
        
        files = os.listdir(self.selected_directory)
        filtered_files = [f for f in files if not (os.path.isdir(os.path.join(self.selected_directory, f)) or f.endswith("_model.csv"))]
        print(f"\nAvailable Files in {self.selected_directory}:")
        for i, file in enumerate(filtered_files, 1):
            print(f"{i}. {file}")

        file_index = -1
        while(file_index < 0 or file_index >= filtered_files.__len__()):
            file_index = int(input("Select a file (enter the number): ")) - 1
            if(file_index < 0 or file_index >= filtered_files.__len__()):
                print("Selection outside of the available files - TRY AGAIN")
        
        self.base_csv_file = os.path.join(self.selected_directory, filtered_files[file_index])

        print(f"\nSelected Directory: {self.selected_directory}")
        print(f"Selected File: {self.base_csv_file}")


    def _directory_selection(self): 
        """Select the directory that corresponds to the site that is to be used since each main directroy is seperated by the tagid
        """
         # Select a directory
        directories = []
        for (dirpath, dirnames, filenames) in os.walk(self.data_directory):
            directories.extend(dirnames)
            break

        print("Available Directories:")
        for i, directory in enumerate(directories, 1):
            print(f"{i}. {directory}")

        directory_index = -1
        while(directory_index < 0 or directory_index >= directories.__len__()):
            directory_index = int(input("Select a directory (enter the number): ")) - 1
            if(directory_index < 0 or directory_index >= directories.__len__()):
                print("Selection outside of the available files - TRY AGAIN")
        self.selected_directory = os.path.join(self.data_directory, directories[directory_index])
        return directories
    
    def _saving_preprocess(self):
        """Process to create the skeleton of all the data files witch corresponds to weekdays
        """
        if(self.base_csv_file == None):
            self._file_selection()
        df = pd.read_csv(self.base_csv_file)
        date_groups = self._day_regroupement(df)
        self._filter_and_save_data(data=df, date_groups=date_groups)
    

    def _day_model_file_selection(self):
        if(self.selected_directory == None):
            self._directory_selection()
        if (os.path.exists(f'{self.selected_directory}/weekdays') == False):
            
            self._saving_preprocess()
        day_directory = f'{self.selected_directory}/weekdays'
         # Select a file within the selected directory
        files = os.listdir(day_directory)
        filtered_files = []
        while(filtered_files.__len__()== 0):
            filtered_files = [f for f in files if  (os.path.isdir(os.path.join(day_directory, f)) or f.endswith("_model.csv"))]
            if(filtered_files.__len__() == 0 ):
                print("There is no model file ! \n Create one then select it")
                self._mean_weekday()
                       
                time.sleep(1)  

             # Refresh the directory listing
                files = os.listdir(day_directory)

                filtered_files = [f for f in files if  (os.path.isdir(os.path.join(day_directory, f)) or f.endswith("_model.csv"))]
        print(f"\nAvailable Files in {day_directory}:")
        
        
        for i, file in enumerate(filtered_files, 1):
            print(f"{i}. {file}")
        file_index = -1
        while(file_index < 0 or file_index >= filtered_files.__len__()):
            file_index = int(input("Select a file (enter the number): ")) - 1
            if(file_index < 0 or file_index >= filtered_files.__len__()):
                print("Selection outside of the available files - TRY AGAIN")
        
        selected_csv = os.path.join(day_directory, filtered_files[file_index])

        print(f"Selected File: {selected_csv}")
        return selected_csv
    
    def _day_file_selection(self):
        if (os.path.isdir(f'{self.selected_directory}/weekdays') ==False):
            self._saving_preprocess()
        if(self.base_csv_file == None):
            self._directory_selection()
        
            
        day_directory = f'{self.selected_directory}/weekdays'
        
        # Select a file within the selected directory
        files = os.listdir(day_directory)
       
        filtered_files = [f for f in files if not (os.path.isdir(os.path.join(day_directory, f)) or f.endswith("_model.csv"))]
        
        
        print(f"\nAvailable Files in {day_directory}:")
        for i, file in enumerate(filtered_files, 1):
            print(f"{i}. {file}")

        file_index = -1
        while(file_index < 0 or file_index >= filtered_files.__len__()):
            file_index = int(input("Select a file (enter the number): ")) - 1
            if(file_index < 0 or file_index >= filtered_files.__len__()):
                print("Selection outside of the available files - TRY AGAIN")
        
        selected_csv = os.path.join(day_directory, filtered_files[file_index])

        print(f"Selected File: {selected_csv}")
        return selected_csv
        
    def _mean_weekday(self, csv_file = None): 
        if csv_file == None :
            csv_file = self._day_file_selection()
        data_means = pd.DataFrame()
        data = pd.read_csv(csv_file)
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['time'] = data['datetime'].dt.time  # Remove the parentheses here
        time_group = data.groupby([data['datetime'].dt.hour, data['datetime'].dt.minute])
        for times, group_data in time_group:
            mean_values = group_data[['revenue', 'auctions', 'impressions']].mean()
            mean_df = pd.DataFrame(mean_values).transpose()
            mean_df['time'] = pd.to_datetime(f"{times[0]:02d}:{times[1]:02d}").time()  # Convert the hour and minute to time
            data_means = pd.concat([data_means, mean_df], ignore_index=True)

        data_means = data_means[['time', 'revenue', 'auctions', 'impressions']]  # Reorder columns if needed

        
       
        os.makedirs(f'{self.selected_directory}/models', exist_ok=True)
        file_base = os.path.splitext(os.path.basename(csv_file))[0]
        data_means.to_csv(f'{self.selected_directory}/models/model_{file_base}.csv', index=False)
        return data_means
          
    def proccessus(self):
        self._tag_division
        #self.calculate_weekday_mean()

    def calculate_weekday_mean(self):
        self._file_selection()
        self._saving_preprocess()
        self._mean_weekday()      
   
    def statistic_model_data(self):
        csv_file = self._day_model_file_selection()
        data = pd.read_csv(csv_file)
        columns = ['revenue', 'auctions', 'impressions']
        for column in columns: 
                #Quartile 1 (25% of the results)
            Q1 = np.percentile(data[column], 25)
            #Quartile 3 (75% of the results)
            Q3 = np.percentile(data[column], 75)
            #Mediane 
            mediane = np.percentile(data[column], 50)

            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            #Standard deviation of the data field
            ecart_type = np.std(data[column])
            #Mean of the field
            moyenne = np.mean(data[column])

            #data[f'z_score_{column}'] = [(value - moyenne) / ecart_type for value in data[column]]

            #Calculation of the Z_Score_Modified
            k = 1.4826
            distance_ecart_type = [abs(value - mediane) for value in data[column]]
            MAD = np.std(distance_ecart_type)
            data[f'z_score_{column}_modified'] = [(value - moyenne) / (k * MAD) for value in data[column]]
            

       
        print(lower_bound)
        return lower_bound
    
    def generate_model_weekday(self, weekday):
        if(self.selected_directory == None):
            self._directory_selection()
        
        model_file = f'{self.selected_directory}/models/model_data_{str.lower(weekday)}.csv'
        
        if os.path.exists(model_file):
            print('Model already exists')
        else:
            day_data = f'{self.selected_directory}/weekdays/data_{str.lower(weekday)}.csv'
            self._mean_weekday(day_data)
            print("Model has been correctly generated")
            
    def data_model_from_file(self, weekday):
        if(self.base_csv_file == None):
            self._file_selection()
        
        model_files = []
        
        for (dirpath, dirnames, filenames) in os.walk(f'{self.selected_directory}/models'):
            model_files.extend(filenames)
            break
        selected_model_list =  [f for f in model_files if f.endswith(f"{str.lower(weekday)}.csv")]
        
        data =  pd.read_csv(f'{self.selected_directory}/models/{selected_model_list[0]}')
        return data
   
   
    
    def data_for_day(self):
        if(self.base_csv_file == None):
            self._file_selection()
        data = pd.read_csv(self.base_csv_file)
        data['datetime'] =  pd.to_datetime(data['datetime'])
        data['date'] = data['datetime'].dt.date
        group_by_date = data.groupby('date')
        
        unique_dates = []
        print("For this file select a date")
        for date, data in group_by_date: 
            unique_dates.append(date)
            
        for i, unique_date in enumerate(unique_dates, 1):
            print(f"{i}. {unique_date}")
            
        date_index = -1
        while(date_index < 0 or date_index >= len(unique_dates)):
            date_index = int(input("Select a file (enter the number): ")) - 1
            if(date_index < 0 or date_index >= len(unique_dates)):
                print("Selection outside of the available files - TRY AGAIN")
        
        selected_date = unique_dates[date_index]
    
        # Filter the DataFrame based on the selected date
        data_selected_date = data[data['date'] == selected_date]
        
        return selected_date,data_selected_date
        
    def data_normalization(self, date ,data):
        
        
        ##Transformation of the date to the name of it in the day of the week
        day_date = pd.to_datetime( pd.to_datetime(date))
        weekday = day_date.day_name()

        
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['time'] = data['datetime'].dt.time
        dp.generate_model_weekday(weekday)
        day_data = dp.data_model_from_file(weekday)
    

        columns_to_subtract = ['revenue', 'auctions', 'impressions']
        result = day_data[columns_to_subtract].sub(data[columns_to_subtract], fill_value=0)
        result['time'] = day_data['time']
        result.set_index('time',inplace=True)
       
        return result
        

    def simple_verification(self,date,normalized_data):
        
        os.makedirs(f'{self.selected_directory}/results',exist_ok=True)
        
        directory_name = os.path.basename(self.selected_directory)
        results_filename = f'{self.selected_directory}/results/r_{date}_{directory_name}.csv'
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
            #Standard deviation of the data field
            ecart_type = np.std(normalized_data[column])
            #Mean of the field
            moyenne = np.mean(normalized_data[column])
            #Calculation of the Z_Score_Modified
            k = 1.4826
            distance_ecart_type = [abs(value - mediane) for value in normalized_data[column]]
            MAD = np.std(distance_ecart_type)
            normalized_data[f'z_score_{column}_modified'] = [(value - moyenne) / (k * MAD) for value in normalized_data[column]]
            lower_bounds[column] = lower_bound
        
        
        result.to_csv(results_filename)
        
        return lower_bounds
        

dp = DataProcessor()


selected_date,df = dp.data_for_day()

result = dp.data_normalization(selected_date,df)
print (result)
result.plot(kind='line', marker='o')

plt.xlabel('time')
plt.ylabel('Difference')
plt.title('Subtraction of DataFrames')

plt.show()

dp.simple_verification(selected_date,result)

#dp.calculate_distance_from_model()