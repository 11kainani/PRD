from file_manager import FileManager
from calculation import Calculation
from model_generator import Model_generator
from verification import Verification


if __name__ == "__main__":
    directory = "3ee1bd1f-01d8-4277-929d-53b1cebe457b"
    FileManager("data/519a0d18-032d-4027-bd7f-21a1c39e8d89.csv")
    cal = Calculation(directory)
    ver = Verification(directory)
    model = Model_generator(directory)
    

    
    for seuil in range(2,6):
        print('*'*50)
        print("Seuil Test : ", seuil)
        time = "2024-10-10"
        ver.day_mean_analyze_and_print_results(time,seuil)

        '''
        cal.day_mean_simple_verification(time)
        
        abnormal =ver.day_mean_zscore_verification(time, seuil)
        following = ver.day_following_timestamps(abnormal)

        headers = ['z_score_revenue','z_score_revenue','z_score_impressions']

        

        for itera, data in following.items(): 

            print("{:<10} {:<10}".format("Time", itera))
            print("-" * 25)
            for time_index, z_score in data.items():
                print("{:<10} {:<10}".format(time_index.strftime("%H:%M"), z_score))
            


        print('\n','-'*50)
        previous_data = (ver.day_mean_anomalie_slope(time,seuil))
        
        for index, data in previous_data.items():
            print("{:<10} {:<10}".format("Time", f'{index}_drop'))
            print("-" * 25)
            for time_index, z_score in data.items():
                print("{:<10} {:<10}".format(time_index, z_score))
        
        '''
           

    