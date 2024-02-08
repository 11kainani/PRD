import pandas as pd
import os

file_csv = 'data/data.csv'


def tag_division(csv_path): 
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
        directory = f'data/{group_key}'
        os.makedirs(directory, exist_ok=True)
        # Trier les données du groupe par date, heures et minutes
        sorted_grouped_data = group_data.sort_values(by=['date', 'hours', 'minutes'], ascending=[False, False, False])
        sorted_grouped_data['datetime'] = pd.to_datetime(sorted_grouped_data['date'] + ' ' + sorted_grouped_data['hours'].astype(str) + ':' + sorted_grouped_data['minutes'].astype(str))
        # Créer le nom du fichier en utilisant la date du groupe
        filename = f'{directory}/{group_key}.csv'
        # Sauvegarder les données du groupe dans le fichier
        selected_columns =  sorted_grouped_data[['datetime','currency','revenue','auctions','impressions']]
        selected_columns.to_csv(filename, index=False)

    
def day_division(csv_path):
    """_summary_
    Divide the data into seperate directories according to the site id. The files are once again seperated into different csv files according to the date of the mesure
    Args:
        csv_path (_type_):The path to the main data csv
    """
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
        
       
        
def tag_date_division(csv_path):
    # Charger le fichier CSV principal
    df = pd.read_csv(csv_path)

    # Convertir la colonne 'date' en objet de date
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Parcourir chaque tagid unique
    for tagid in df['tagid'].unique():
        # Filtrer le DataFrame par tagid
        df_tagid = df[df['tagid'] == tagid]

        # Parcourir chaque jour unique
        for date in df_tagid['date'].dt.date.unique():
            # Filtrer le DataFrame par jour
            df_tagid_date = df_tagid[df_tagid['date'].dt.date == date]

            # Créer une nouvelle colonne "time" en combinant les colonnes "hours" et "minutes"
            df_tagid_date['time'] = df_tagid_date['hours'].astype(str).str.zfill(2) + ':' + df_tagid_date['minutes'].astype(str).str.zfill(2)

            # Sélectionner les colonnes requises dans l'ordre souhaité
            df_result = df_tagid_date[['date', 'time', 'tagid', 'currency', 'auctions', 'impressions', 'revenue']]

            # Enregistrer le DataFrame résultant dans un nouveau fichier CSV
            directory = 'data/division'
            os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
            filename = f'{directory}/{tagid}_{date}.csv'
            df_result.to_csv(filename, index=False)


def main():
    tag_division(file_csv)
    
    
if __name__ == "__main__":
    main()
