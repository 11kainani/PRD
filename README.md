# Pubstack : Anomaly Detection on Trafic Curves

## Description

The project aims to develop a comprehensive tool for analyzing website traffi data and detecting anomalies. By using statistical analysis, the tool aims to identify unusual patterns or deviations from expected behavior in various metrics.

## Features

* Data Loading and Preprocessing:
  * Load the main data file containing website traffic metrics.
  * Preprocess the data to handle missing values, format conversion, and indexing by date and time.
* Model Generation
  * Generate models based on historical data (per day of the week, weekly, week-end  
* Anomaly Detection
  * Calculate z-scores to quantify the deviation of data points from the expected distribution.
  * Identify anomalies by comparing z-scores against predefined thresholds.
* Data Verification and Validation
  * Verify the integrity of data and results through consistency checks and cross-validation.
  * Validate anomaly detection results.  
 
## Installation

1. Clone the repository
2. Navigate to the project directory
3. Download the necessary dependencies necessary for the project
```
pip install -r requirements.txt
```
4. Initialize FileManager
```
FileManager = FileManager("[location_of_the_main_file].csv")
```
The function initializes the project 

4. Now that the project has been initialized, 

### Setting up the data files

For this projet, all that is need is a folder in the working project directory named "data" that contains the main csv named "data.csv".



## Usage

### FileManager:
The user starts by using the FileManager class to manage their data files. They provide the path to the main CSV file containing their data.
This class helps organize the data and prepare it for further analysis.
###Calculation:
After setting up the file management, the user creates a Calculation object. This object allows them to perform various calculations and analyses on the data.
For example, they can calculate rolling averages, exponential moving averages, or other statistical measures using this object.
### Verification:
Alongside calculations, the user also needs to verify the results of their analyses. They use the Verification class for this purpose.
The verification process likely involves checking for anomalies, outliers, or inconsistencies in the data or calculated metrics.
### ModelGenerator:
Additionally, the user can generate models based on their data using the ModelGenerator class.
These models provide baseline or reference values for comparison during analysis and verification.
### Day Mean Analysis:
To analyze specific days, the user selects a date and sets a threshold for analysis.
The Verification object is then used to perform a day mean analysis on the selected date, comparing the calculated metrics against the specified threshold.

### Example

```
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
        time = "2023-10-10"
        ver.day_mean_analyze_and_print_results(time,seuil)
```

## Documentation

To generate the documentation, follow these steps:
a. Open the html/index.html file using your browser to view the documentation
### If the documentation directory named "html" isn't visible
1. Install pdoc: If you haven't already installed pdoc, you can do so using pip --> ```pip install pdoc```
2. Generate HTML documentation: This foollowing command forces```pdoc --html . --force```
3. View the documentation: Using you browser, open the html/index.html file to view the files

If you make changes to the code and want to update the documentation, repeat the creation of the documentation regenerate the HTML files with the latest changes. Then, refresh the documentation page in your browser to see the updates.
