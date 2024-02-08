import os
import pandas as pd

def day_regroupement(data):
   data['datetime'] = pd.to_datetime(data['datetime'])
   unique_dates = data['datetime'].dt.date.unique()  # Replace 'date_column_name' with the actual column name
   date_groups = {day: [] for day in range(7)}
   for date in unique_dates:
        day_of_week = date.weekday()  # 0 for Monday, 6 for Sunday
        date_groups[day_of_week].append(date)
   return date_groups
    
def getDayOfWeek(week_number): 
    week_index = {
        0: 'day1', #Monday
        1: 'day2', 
        2:'day3',
        3: 'day4',
        4: 'day5',
        5: 'day6',
        6: 'day7', #Sunday
    }
    return week_index[week_number]
      
def directoryFromFile(csv_name):
    csv_name = str(csv_name)
    directory = csv_name.rsplit(sep='/',maxsplit=1,)
    return directory[0]
      
def filter_and_save_data(data, date_groups, main_filename):
    directory = f'{directoryFromFile(main_filename)}/weekdays'
    os.makedirs(directory, exist_ok=True)
    for day_of_week, dates in date_groups.items():
        # Filter the data for the current day_of_week
        filtered_data = data[data['datetime'].dt.weekday == day_of_week]
        
        # Save the filtered data to a CSV file
        csv_name = f'{directory}/data_{getDayOfWeek(day_of_week)}.csv'
        filtered_data.to_csv(csv_name, index=False)
        
def mean_by_time(data):
    data['datetime'] = pd.to_datetime(data['datetime'], unit='s')  # adjust 'unit' as needed
    # Group by hour and minute
    time_group = data.groupby([data['datetime'].dt.hour, data['datetime'].dt.minute])
    print(time_group)
    

def saving_preprocess(csv_name):
    df = pd.read_csv(csv_name)
    directoryFromFile(csv_name)
    date_groups = day_regroupement(df)
    filter_and_save_data(df, date_groups,csv_name)

def mean_weekday(filename): 
    data_means = pd.DataFrame()
    data = pd.read_csv(filename)
    data['datetime'] = pd.to_datetime(data['datetime'])
    time_group = data.groupby([data['datetime'].dt.hour, data['datetime'].dt.minute])
    for times, group_data in time_group:
        mean_values = group_data[['revenue', 'auctions', 'impressions']].mean()
        mean_df = pd.DataFrame(mean_values).transpose()
        mean_df['hours'], mean_df['minutes'] = times 
        data_means = pd.concat([data_means, mean_df], ignore_index=True)
    data_means= data_means[['hours','minutes','revenue', 'auctions', 'impressions']]
    
    directory = filename.rsplit('.',1)[0]
    data_means.to_csv(f'{directory}_model.csv', index=False)
    print(directory)
    return data_means

    
if __name__ == "__main__":
    #saving_process('data/2e6a7662-889d-4c27-9027-f3609860ff67/2e6a7662-889d-4c27-9027-f3609860ff67.csv')
    df = mean_weekday('data/2e6a7662-889d-4c27-9027-f3609860ff67/weekdays/data_day1.csv')
