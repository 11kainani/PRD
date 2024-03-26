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

### Documentations 

The python documentation are all in the html/project directory in html format. You can visualize them directly using your favourite browser. 

## Usage

Explain how to use your project. Provide examples or code snippets if applicable.

## Documentation

Link to or include documentation for your project, such as API references or user guides.
