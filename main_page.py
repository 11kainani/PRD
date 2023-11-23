import tkinter as tk
from tkinter import ttk

class mainpage(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pubstack: Timeseries Visualization")
        self.geometry("720x550")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=1)  # For left_bar
        self.grid_columnconfigure(1, weight=4) 
        self.grid_rowconfigure(0, weight=1)
        
        # Containers
        left_bar = tk.Frame(self, bg="black")
        left_bar.grid(row=0, column=0, sticky="nsew")  # Expand both vertically and horizontally*
        left_bar.grid_columnconfigure(0, weight=1)
        left_bar.grid_rowconfigure(0,weight=1)
        left_bar.grid_rowconfigure(1,weight=1)
        

        # Sub container (Seuil) for left_bar container
        seuil_container = tk.Frame(left_bar, bg="black")
        seuil_container.grid(row=1, column=0, sticky="nsew")
        
        self.ecart_type = tk.StringVar()
        self.ecart_type.set("66")
        
        #Radio button to set the threshold for the standard deviation
        radio_button_frame = tk.Frame(seuil_container)
        radio_button_frame.pack()
        
        radio_button_ecartType_66 = tk.Radiobutton(radio_button_frame, text="66%", variable=self.ecart_type, value="66")
        radio_button_ecartType_95 = tk.Radiobutton(radio_button_frame, text="95%", variable=self.ecart_type, value="95")
        radio_button_ecartType_99 = tk.Radiobutton(radio_button_frame, text="99%", variable=self.ecart_type, value="99")
        
       
        radio_button_ecartType_66.pack()
        radio_button_ecartType_95.pack()
        radio_button_ecartType_99.pack()
        
        # Create a button to retrieve the selected value and store it
        get_value_button = tk.Button(seuil_container, text="Get Selected Value", command=self.get_ecart_type)
        get_value_button.pack()
        
        # Sub container (Filter) for left_bar container
        filter_container = tk.Frame(left_bar, bg="red")
        filter_container.grid(row=0, column=0, sticky="nsew")
        
        # Container for the graphe on the right
        graph_bar = tk.Frame(self)
        graph_bar.grid(row=0, column=1, sticky="nsew")
        graph_bar.grid_columnconfigure(0,weight=1)
        graph_bar.grid_columnconfigure(2,weight=1)
        graph_bar.grid_columnconfigure(1,weight=8)
        graph_bar.grid_rowconfigure(0,weight=1)
        graph_bar.grid_rowconfigure(1,weight=4)
        graph_bar.grid_rowconfigure(2,weight=1)
        
        #sub container for the results 
        result_container = tk.Frame(graph_bar)
        result_container.grid(row= 2, column=1, sticky="nsew")
       
        title_results = tk.Label(result_container, text="Results" ,fg="black", font=("Helvetica", 18))
        title_results.pack(side="top", fill="x")
        
        
    def get_ecart_type(self):
        selected_value = self.ecart_type.get()
        print("Selected Ecart Type:", selected_value)
   
# Start the main event loop
if __name__ == "__main__":
    app = mainpage()
    app.mainloop()
