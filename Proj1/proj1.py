import matplotlib.pyplot as plt
import numpy as np

#declare these lists globally to use in both functions
hours = []
sales = []

"""
Creates the scatter plot, and plots the regression and the quadratic fit to it
"""
def create_scatter():
    
    data = open("proj1data.txt", "r")
    data_parsed = [line.strip().split(",") for line in data]
    
    #reverse iterate because deleting entries while iterating forward can be problematic
    for entry in reversed(data_parsed):
        if not entry[1].isdigit():
            data_parsed.remove(entry)

    #used to tell function to use global declaration
    global hours, sales
    hours = [int(entry[0]) for entry in data_parsed]
    sales = [int(entry[1]) for entry in data_parsed]

    #example outlier
    hours.append(745)
    sales.append(20000)

    #info for regression fit
    regression_info = create_regression()

    #creates the scatter plot, adds labels
    plt.scatter(hours, sales, s=np.pi, alpha=0.5)
    plt.title('CS 678 Proj 1')
    plt.xlabel('Hours')
    plt.ylabel('Sales')
    ax = plt.gca()
    ax.text(0.41, 0.91,
            "Regression line: y = " + str(round(regression_info[0], 2)) + "x + " + str(round(regression_info[1], 2)),
            fontsize=10, transform=ax.transAxes)

    #set line colors and get the y values for each line
    regr_colors = (1,0,0)
    regrline_values = [regression_info[0] * i + regression_info[1] for i in range(len(data_parsed))]

    #plot lines
    plt.plot(regrline_values, c=regr_colors, linewidth=2)

    #if using polynomials as well, use a legend and cycling colors, then add the polynomials using numpy library
    add_polynomial = True
    if (add_polynomial):
        min = 1
        max = 15
        step = 2
        cm = plt.get_cmap('gist_rainbow')
        ax.set_prop_cycle(color=[cm(1.*i/15) for i in range(15)])
        legend_list = [str(i) + " degree polynomial" for i in range(min, max, step)]
        legend_list.insert(0, "Regression line")

        #plot lines
        for i in range(min, max, step):
            polyfit_info = np.poly1d(np.polyfit(np.array(hours), np.array(sales), i))
            polyfit_values = polyfit_info(hours)
            ax.plot(hours, polyfit_values, linewidth=1)
        
        #must be after lines are plotted
        ax.legend(legend_list)
        
    #show the graph
    plt.show()

"""
Get the slope and intercept for the least-squares regression.
"""
def create_regression():
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
