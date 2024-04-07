import pandas as pd
import os


class FileManager(): 
    """Class to set up the project correctly. With a base csv file, 
    """
    def __init__(self,main_csv_file):
        self.data_directory = "data"
        os.makedirs(self.data_directory,exist_ok=True)
        "The name of the the data file in the project. The main data csv should be placed in a directory named data"
        
        self.datafile_location = f'{main_csv_file}'
        
        self.selected_directory = None
        """ The currrent directory to be studied -> A directory corresponds to a site 
        """
        self.base_csv_file = None 
        """The current file to be studied -> This file corresponds to the csv file containing all the information about the specific site"""
        self.tag_division()
        #self.saving_preprocess()

    def tag_division(self):
        """Divide the main data file into seperate csv file grouped by thier tagid which is the site identification.
        """
        csv_path = self.datafile_location
        separators = [';', ',']  
        group_field = 'tagid'

        assert os.path.isdir(self.data_directory), "A directory named data doesn't exist. Please create it and put your main csv file into the newly created data directory in your working project"
        assert os.path.isfile(self.datafile_location), "The main csv file isn't located in the correct directory. Make sure that it is placed inside the directory named data"
            
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
            # Créer le nom du fichier en utilisant la date du groupe
            filename = f'{directory}/{group_key}.csv'

            selected_columns =  sorted_grouped_data[['datetime','currency','revenue','auctions','impressions']]
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
            week_number (int): An integer between [0;6]

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

    def filter_and_save_data(self,data : pd.DataFrame, date_groups):
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

    def file_selection(self):
        """Select the base file to be used to construct the model files
        """
        # Select a directory
        directories = self.directory_selection()
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

    def _directoryFromFile(self):
        """Get the directory of the current file

        Returns:
            string: the name of the directory of the selected file
        """
        csv_name = str(self.base_csv_file)
        directory = os.path.dirname(csv_name)
        return directory


    def directory_selection(self): 
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

    def saving_preprocess(self):
        """Process to create the skeleton of all the data files witch corresponds to weekdays
        """
        print("Weekday folder création....")
        if(self.base_csv_file == None):
            self.file_selection()
        df = pd.read_csv(self.base_csv_file)
        date_groups = self._day_regroupement(df)
        self.filter_and_save_data(data=df, date_groups=date_groups)    


    def get_site_directory_and_file(self):
        """Return the selected site directory and the main file with all the information about the set site
        Returns:
            tuple: there are two elements in this tuple, the first being the selected directory and the seconde being the main file for that directory
        """
        return self.data_directory ,self.base_csv_file

    def concat_files(self, main_file, secondairy_file):
        main = pd.read_csv(main_file)
        secondary = pd.read_csv(secondairy_file)

        main.add(secondary)
        main.to_csv("data/data.csv", index=False) 
        


if __name__ == "__main__": 
    dp = FileManager("data/519a0d18-032d-4027-bd7f-21a1c39e8d89.csv")
    #dp.tag_division()

    #dp.saving_preprocess()