import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np

#Use global variables for list of hours and sales so accessable in both functions
hours = []
sales = []


"""
This function creates the scatter plot. It will open the file, pull the data, 
split it into two lists, then create a scatter plot with those two lists.
The plot is done using MatPlotLib.
"""
def create_scatter():
    
    data = open("proj1data.txt", "r")
    data_parsed = [line.strip().split(",") for line in data]

    """
    reverse iterate because deleting entries while iterating over list
    can cause issues.
    """

    #Remove all NaN entries from the list.
    for entry in reversed(data_parsed):
        if not entry[1].isdigit():
            data_parsed.remove(entry)

    #Tell the program to use the global variables.
    global hours, sales
    hours = [int(entry[0]) for entry in data_parsed]
    sales = [int(entry[1]) for entry in data_parsed]

    #Get the slope and intercept for the regression line.
    regression_info = create_regression()
                      
    #Create the scatter plot.
    colors = (0,0,0)
    plt.scatter(hours, sales, s=np.pi, alpha=0.5)
    plt.title('CS 678 Proj 1')
    plt.xlabel('Hours')
    plt.ylabel('Sales')

    #Get a list of the values of regression for each hour.
    regrline_values = [regression_info[0] * i + regression_info[1] for i in range(0, len(data_parsed))]  
    plt.plot(regrline_values, c=colors)

    plt.show()

"""
This function gets the slope and intercept for the regression line
using the least-squares method.
"""
def create_regression():
    #Get numbers for least-squares method.
    sum_x = sum(hours)
    sum_y = sum(sales)
    sum_xy = sum([hours[i] * sales[i] for i in range(len(hours))])
    sum_x2 = sum([hour * hour for hour in hours])
    sum_y2 = sum([sale * sale for sale in sales])
    N = len(hours)    

    slope = ((N * sum_xy) - (sum_x * sum_y))/((N * sum_x2) - (sum_x)**2)
    intercept = (sum_y - (slope * sum_x))/N
    return [slope, intercept]

create_scatter()
