import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

#Read the data that has been firstly treated by the script : data_processing.py
def read_data(file_path, rows=None):
    data = pd.read_csv(file_path)
    
    return data

def calculate_statistics(data, column):
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

    return lower_bound

def moving_average(data): 
    
    df = data[['time', 'revenue']].copy()

    
    df['ma_60'] = df['revenue'].rolling(window=3600).mean()


    print(df)
    return df

def identify_outliers(data,  lower_bound,column , threshold = -2):
    outliers = data[(data[column] < lower_bound)]
    outliers_zscore_modified = data[(data[f'z_score_{column}_modified'] < threshold)]
    print(outliers_zscore_modified)
    outliers_data = pd.concat([outliers, outliers_zscore_modified])
    return outliers_data

#Display the element according to the date
def plot_data(data, outliers):
    
    if 'time' not in data.columns:
        data['time'] = pd.to_datetime(data['datetime'])
        
    fig, data_graphs = plt.subplots(2, 3, figsize=(12, 6))

    # Define the data and labels for each subplot
    data_to_plot = [
        (data['time'], data['revenue'], 'Revenue'),
        (data['time'], data['auctions'], 'Auctions'),
        (data['time'], data['impressions'], 'Impressions')
    ]
    
    score_to_plot = [
        (data['time'], data['z_score_revenue_modified'], 'Z-Revenue'),
        (data['time'], data['z_score_auctions_modified'], 'Z-Auctions'),
        (data['time'], data['z_score_impressions_modified'], 'Z-Impressions')
    ]
    
    colors = []
    
    for value in data:
        if value in outliers:
            colors.append('b')
        else:
            colors.append('r')
            
    print(colors)
    for i in range(3):
        data_graphs[0, i].plot(data_to_plot[i][0], data_to_plot[i][1],)
        data_graphs[0, i].set_xlabel('Time')
        data_graphs[0, i].set_ylabel('Value')
        data_graphs[0, i].set_title(data_to_plot[i][2])
        data_graphs[0, i].grid(True)
        
        data_graphs[1, i].plot(score_to_plot[i][0], score_to_plot[i][1])
        data_graphs[1, i].set_xlabel('Time')
        data_graphs[1, i].set_ylabel('Value')
        data_graphs[1, i].set_title(score_to_plot[i][2])
        data_graphs[1, i].grid(True)

    # If you want to create additional plots, you can add them here as well.

    fig.tight_layout()
    plt.show()

def scatter_plot(data, outliers):
    outlier_indices = outliers['datetime'] 
    outlier_mask = np.full(len(data['datetime']), False)
    outlier_mask[outlier_indices] = True 
      
    plt.scatter(data['datetime'], data[~outlier_mask], color ='blue')
    plt.scatter(data['datetime'], data['revenue'])
    plt.xlabel('datetime')
    plt.ylabel('Value')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

def data_processing(directory, filename):
    filepath = f'{directory}/{filename}.csv'
    data = read_data(filepath)
    columns = ['revenue','impressions','auctions']
    
    for element in columns: 
        print(element)
        lower_bound = calculate_statistics(data, element)
        outliers_data = identify_outliers(data, lower_bound, element)
    return outliers_data

def result_csv(directory,filename,data): 
    os.makedirs(f'{directory}/results', exist_ok=True)
    destination = f'{directory}/results/results_{filename}.csv'
    data.to_csv(destination, index=False)
    
    
def main():
    directory =  'data/2e6a7662-889d-4c27-9027-f3609860ff67/days'
    for i in range(1,8):
        filename = f'data_day{i}'
        data = read_data(f'{directory}/{filename}.csv')
        outliers = data_processing(directory,filename)
        #plot_data(data , data)
        scatter_plot(data, outliers)
        result_csv(directory,filename, data)
    
if __name__ == "__main__":
    main()
