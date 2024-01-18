import os
import matplotlib as plt
import pandas as pd

class Evaluate():

    
    def __init__(self):
        self.data_directory = 'data'
        self.site_focus = None
        """the site (with corresponds to the directory) we want to focus on
        """

    def select_site(self):
        """Selection of the {site_focus} variable
        """
        directories = os.listdir(self.data_directory)
        print(directories)

    def show_result_graph(): 
        res = pd.read_csv("data/0a1b3040-2c06-4cce-8acf-38d6fc99b9f7/results/r_2023-09-30_0a1b3040-2c06-4cce-8acf-38d6fc99b9f7.csv")
        res = res[["z_score_revenue_modified","z_score_auctions_modified","z_score_impressions_modified"]]
        plt.figure(figsize=(10, 5))
        plt.subplot(3, 1, 1)
        plt.plot(res['z_score_revenue_modified'], marker='o')
        plt.title('Z-Score Revenue Modified')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.subplot(3, 1, 2)
        plt.plot(res['z_score_auctions_modified'], marker='o')
        plt.title('Z-Score Auctions Modified')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.subplot(3, 1, 3)
        plt.plot(res['z_score_impressions_modified'], marker='o')
        plt.title('Z-Score Impressions Modified')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.tight_layout()
        plt.show()

        
        
if __name__ == "__main__":
    ""