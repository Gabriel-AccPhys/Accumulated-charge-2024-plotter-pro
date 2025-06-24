#CODE TO PLOT cumulative charge for CEBAF 09/20/2024

# importing modules
from math import nan
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import datetime
import os # added this to handle the csv files
import glob # added this to handle the csv files

#-----------------------------------------PLOTTER FUNCTION------------------------------ 

def plotter(file_name, x_1, y_1, x_2, y_2, y_3, Max_Index, Max_Charge):

    # Legend labels
    my_labels_1 = ['Charge per day', 'Day when photocathode position was reset']
    my_labels_2 = ['Cumulative charge']
    
    # Define the size of the plot and the font size
    plt.rcParams["figure.figsize"] = [20.5, 17]
    plt.rcParams.update({'font.size': 25})
    
    fig, ax1 = plt.subplots() 

    # Adds a grid
    plt.grid(True) # controls Grid
    
    color = 'tab:red'
    ax1.set_xlabel('Date [yyyy]') # Label of the x-axis

    ax1.set_ylabel('Charge [C]') # Label of the left y-axis
            
    ax1.plot(x_1, y_1, "ob") # Calls x_1 and y_1 dataframe columns to be plotted on the left side, "ob" means blue dots 
    ax1.plot(x_2, y_2, "o", color = 'cyan') # Calls x_2 and y_2 dataframe columns to be plotted on the left side, "og" means green dots 
    ax1.tick_params(axis='y')
    ax1.set_ylim(0, 400) # Sets the left side y-axis limit adding 50 kV to the max voltage Max_V
    
    ax2 = ax1.twinx()  # Instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Cumulative charge [kC]')  # Set the right side y-axis label
    ax2.plot(x_2, y_3 / 1000, marker='o', linestyle = 'dashed', linewidth = 2, markersize = 12, color = 'red') # Plots x_2 and y_3, who should be the selected radiation monitor column
    ax2.tick_params(axis='y')
    ax2.set_ylim(0, 5) # Sets the right side y-axis limit

    # Legend labels, locations
    ax1.legend(labels = my_labels_1, loc = 'upper left')
    ax2.legend(labels = my_labels_2, loc = 'upper right')
    
    # Adds a title to the plot with the file name, used to track data sets
    #plt.title('file name: ' + file_name) 

    # Recieves the max voltage Max_V from the dataframe and adds a note with the value at the location where it first ocurred
    #ax2.annotate(str(float("{:.2f}".format(Max_Charge))) + ' kC', xy=(Max_Index, Max_Charge/1000 + 4.6), xytext=(Max_Index, Max_Charge + 0.15), arrowprops=dict(facecolor='black', shrink=0.05),)

    # Can turn this on  in case the label is slightly clipped
    # fig.tight_layout()  

    # Save the plot to file with the file_name variable as file name lol 
    plt.savefig(file_name + 'zero-method.png') #save plot to png file
    
    # Show the plot
    plt.show() 

#----------------------------------------- MAIN CODE ----------------------------------- 
# Read the file name
print ("Process started")

# Either take the folder name as an input or define it as a constant string value
#path=input()
path = 'Accumulated charge CEBAF 2024'

#path = os.getcwd() This line was now asigned by reading the input
txt_files = glob.glob(os.path.join(path, "*.txt"))

# loop over the list of csv files in the folder

for f in txt_files:
    
    # Print the location and filename
    print('Location:', f)
    print('File Name:', f.split("\\")[-1])
    
    # Read the txt file and store it in dataframe
    df = pd.read_csv(f, sep='\t', header = 0, names = ['DATE', 'TIME', 'SPOT', 'LASER', 'WAVELENGTH', 'POWER', 'QE', 'CHARGE'], parse_dates = ['DATE']) 
    display(df)

    df = df.sort_values(by = ["DATE"], ascending = True)
    
    df = df.drop_duplicates(subset=['DATE'])
    print('Data frame content WITHOUT DUPLICATES:')
    display(df)
    print()
    
    # Calculate step size for the elapsed time column 
    Step_size = (df['DATE'].iloc[1] - df['DATE'].iloc[0]).total_seconds()
    print('Step size is:', Step_size)
    print('iloc 0 is:', df['DATE'].iloc[0])
    print('iloc 1 is:', df['DATE'].iloc[1])
    
    # Dropping the rows from dataframe when HV_On is 0, that means PS is OFF 
    #df.drop(df[df.HV_On == 0].index, inplace = True)
        
    # Add column with cumulative hrs to dataframe
    df['Cumulative time [hrs]'] = (np.arange(0, 0+len(df)*Step_size, Step_size))/3600

    # Print the data frame content
    print('Data frame content:')
    display(df)
    print()


    # Constants 
    zero_indices = df[df['CHARGE'] == 0].index
    previous_values = df['CHARGE'].shift(1).loc[zero_indices]
    previous_dates = df['DATE'].shift(1).loc[zero_indices]
    result = pd.DataFrame({'index':zero_indices, 'previous_value': previous_values, 'previous_date': previous_dates})
    total_sum = result['previous_value'].sum()
    result['running_sum'] = result['previous_value'].cumsum()
    Max_Acc_Charge = result['running_sum'].max()
    print("Max_Acc_Charge: ", Max_Acc_Charge)
    Max_Value_Index = result[['running_sum']].idxmax()
    Label_x_position = result.loc[Max_Value_Index, 'previous_date']
    print("Label_x_position: ", Label_x_position)
    
    print('Result data frame content:')
    display(result)
    print()
    
    # Troubleshooting: Print entire data frame
    # print(result.to_string())

    # Troubleshooting: Write data frame to file
    #result.to_csv('result_DataFrame.csv')
    
    if total_sum > 1000:
        print('Total accumulated charge is: ' + str(total_sum/1000) + ' kC')
    else: 
        print('Total accumulated charge is: ' + str(total_sum) + ' C')
      
    plotter(f, df['DATE'], df['CHARGE'], result['previous_date'], result['previous_value'], result['running_sum'], Label_x_position, Max_Acc_Charge/1000)
    
print('Done!')