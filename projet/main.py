
from calculation import Calculation
from verification import Verification

if __name__ == "__main__":
    directory = "data/0a1b3040-2c06-4cce-8acf-38d6fc99b9f7"
    ver = Verification(directory)
    cal = Calculation(directory)

    
    seuil = 2
    time = "2023-10-01"

    cal.day_simple_verification(time)
    
    abnormal =ver.day_zscore_verification(time, seuil)
    
    #print(abnormal)
    following = ver.day_following_timestamps(abnormal)

    for itera, data in following.items(): 
        print(itera, data)


    print('-'*10)
    previous_data = (ver.day_anomalie_slope(time,seuil))
    for index, data in previous_data.items():
        print(index, data)