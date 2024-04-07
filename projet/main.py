from file_manager import FileManager
from calculation import Calculation
from model_generator import Model_generator
from verification import Verification


if __name__ == "__main__":
    #FileManager("519a0d18-032d-4027-bd7f-21a1c39e8d89.csv")
    directory = "data/f6b6b7f3-abad-46ed-8d39-1d36e6eed9ea"
    cal = Calculation(directory)
    ver = Verification(directory)
    min_serie = 10
    min_drop = 2
    date = "2023-10-05"
    for seuil in range(2,6):
        print('*'*50)
        print("Seuil Test : ", seuil)
        mean = False 
        if mean: 
            cal.day_mean_simple_verification(date)
            ver.day_mean_analyze_and_print_results(date,seuil,min_serie,min_drop)
        else:    
            ver.day_analyze_and_print_results(directory,date,seuil,min_serie,min_drop)

           

    