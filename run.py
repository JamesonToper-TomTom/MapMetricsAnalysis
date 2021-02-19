import math
import os
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np


def run():
    print("Starting")
    # Hardcoded for now, location to a folder with 2 CSV files from mapmetrics
    dir = "Data/Updated/Brazil"

    # Get all the files in the folder
    files = os.listdir(dir)
    files.sort()

    # Dictionary of data with the (city,date) as its key. Mainly intended for future versions where multiple cities can
    # be overlaid at once. Partially irrelevant for this implementation
    data = {}
    cities = []
    dates = []
    print("Beginning file read...")
    for file in files:
        if "_Store" in file:
            continue
        # Based on the current formatting of MapMetrics CSVs, the _ splits up the name
        segments = file.strip().split("_")
        # The application_id is the second element, and will refer to the city
        city = segments[1]

        # Add the information to the dictionary
        if city not in cities:
            cities.append(city)
        date = segments[4][3:9]
        if date not in dates:
            dates.append(date)
        if city in data:
            data[city, date] += [date, pd.read_csv(dir + "/" + file).sort_values(by=['x', 'y'])]
        else:
            data[city, date] = [date, pd.read_csv(dir + "/" + file).sort_values(by=['x', 'y'])]
        print("File read")
    print("Read complete.")
    stats = []
    dates.sort()
    print(dates)

    # Use the parse function to simplify the data and then calculate the statistics on it.
    print("Beginning data compression...")

    # Again, originally built for multiple city comparisons. Will likely be useful in the future
    # Go through each city and date
    for city in cities:
        for date in dates:
            # Drop the irrelevant columns for memory
            data[(city, date)][1].drop(['pointCount', 'zoomLevel'], axis=1)
            # Append the result of the parse function to the stats list
            stats.append(parse(city, date, data))
            print("Month completed")
        print("City completed")
    print("Beginning stats.")
    # Turn the list into a dataframe table object
    df = pd.concat(stats, axis=0, ignore_index=True)
    # Run statistics on table. Plot function is also in here
    run_stats(df, dates)


def parse(city, date, data):
    """
    Parse function, which potentially allows multiple cities to be compared if the stats functions are adapted
    Takes in a city name, the date to process, and the data to work with
    The main goal is to simplify the data into a simple x,y,value,city,date table
    This way we can process the data and also keep track of the time period/location
    :param city: City name to use as a key to find data
    :param date: Date to define which part of the data to look at
    :param data: Raw CSV data from MapMetrics files
    :return: DataFrame with values loaded into x, y, value, city, and date columns
    """

    # DataFrame to populate
    trends = pd.DataFrame(columns=['x', 'y', 'value', 'city', 'date'])

    # Get the data using the two keys, and it's the second part of the tuple so grab the [1] object where its stored
    curr_data = data[city, date][1]

    # Grab the first X,Y values from their columns, use them to define a 0,0 coordinate
    x_origin = int(curr_data.iloc[0]['x'])
    y_origin = int(curr_data.iloc[0]['y'])

    # Progress to print out to console
    progress = 0

    # For each row in the CSV
    for index in range(len(curr_data['x'].values)):
        # Get the full row based on the column index
        row = curr_data.iloc[index]

        # Get the x and y values from the specific row, and subtract the origin to get the points in a 0,1,2,... format
        x = row['x'] - x_origin
        y = row['y'] - y_origin

        # Progress calculation to print
        print_prog = (progress / len(curr_data['x'].values)) * 100
        if print_prog % 25 < 0.5:
            print(int(print_prog), "%")
        progress += 1

        # Get the value from the row
        value = row['median']

        # Add a row to the table with all the information
        trends = trends.append({"x": x, "y": y, "value": value, "city": city, "date": date}, ignore_index=True)

    # Return populated table
    return trends


def run_stats(df, dates):
    """
    Stats program that currently works with two dates, but was originally built and can be adapted to handle a range
    of months by modifying the for loop
    Takes in the trends data and the dates to process. It runs through each tile and grabs the future value to compare
    Also keeps a running tally of the median to calculate average median
    :param df: Trend data table
    :param dates: Dates to process
    :return:
    """

    print("Stats begun")

    # Simplify data into x, y, values. This implementation doesn't require city and date columns
    array = {"x": df['x'].values, "y": df['y'].values, "values": df['value'].values}
    # Create a table to hold all the points for the plotting function
    trends = pd.DataFrame(columns=['x', 'y', 'value'])

    # Average median counters
    avg_before = 0
    avg_after = 0

    # Calculate how many values we need to process for the loop
    values_len = len(array['values']) // len(dates)

    # For every tile, we have two dates. It skips every other value, as the adjacent index is the future value
    for i in range(0, values_len, 2):
        # Grab the starting value for the tile
        start = array['values'][i * len(dates)]
        # Grab future ending value for the tile
        end = array['values'][i * len(dates) + 1]
        # Calculate the overall change in the tile as a percentage
        change = (end - start) / start * 100

        # Soft filter to get rid of extremely noisy tiles; planes, trains, etc.
        # If they have a median over 8, it's likely a bad tile
        if start < 8 and end < 8:
            # Sum the median totals
            avg_before += start
            avg_after += end

            # Store the X and Y as a simple var
            x_val = int(df['x'][i * len(dates)])
            y_val = int(df['y'][i * len(dates)])

            # Add a point to the plot
            trends = trends.append({"x": x_val, "y": y_val, "value": change}, ignore_index=True)
    # Calculate averages
    before_med = avg_before / values_len
    after_med = avg_after / values_len

    print()
    print("---------------------------------------")
    print("Average Starting Median:", str(before_med)[0:6])
    print("Average Ending Median:", str(after_med)[0:6])
    print("Percent Median Change (Negative is better):", str((after_med - before_med) / before_med * 100)[0:6])
    print("Overall Geographical Improvement:", str(calc_averages(trends))[0:6])
    print("---------------------------------------")

    # UNCOMMENT TO SHOW PLOT
    # plot(trends)


def plot(stats):
    """
    Generate plot chart using matplotlib
    :param stats: The compressed CSV data to chart
    :return: None
    """

    print("Starting subplot")
    # Create the container for the plot
    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    # Generate the histogram using numpy, and bins for every 10 percent increment from -100 to 100
    view_counts, view_bins = np.histogram(stats['value'], bins=range(-100, 100,
                                                                     10))  # bins=(-100,-50,-25,-10,-5,-1,0,1,5,10,25,50,100))

    # Setting up the graph styling

    # Generate the tick lines for the x axis
    ticks = list(range(len(view_bins) - 1))
    # Shifting code to align the ticks with the interval ranges
    for i in range(len(ticks)):
        ticks[i] = ticks[i] + 0.5
    # Plot the histogram using matplotlib bar graph
    ax.bar(ticks, view_counts, width=1, edgecolor='k')
    # Set the tick labels
    ax.set_xticks(range(len(view_bins)))
    ax.set_xticklabels(view_bins[:])
    # Turn the x axis labels
    plt.setp(ax.get_xticklabels(), rotation=70, horizontalalignment='center')

    # Set y axis labels
    ax.set_ylabel('# Of Tiles')
    ax.set_xlabel('Percentage Change')

    print("Showing Plot")
    plt.show()


def calc_averages(data):
    """
    Calculates the overall average percent change of each tile over the entire area
    :param data: CSV file loaded into a dataframe. Median values are under the data['value'] key
    :return: Average percent change over a given area and timeframe
    """
    calc_counts, calc_bins = np.histogram(data['value'],
                                          bins=range(-100, 100))

    # Number of improved tiles
    improved = 0
    # Number of worsening tiles
    worsened = 0
    # Total number of tiles
    total = 0

    # The counts are arranged in a histogram, so this loop scans from the outside inwards and sums the counts of each
    # grouping of tiles.
    for i in range(math.ceil(len(calc_counts) / 2)):
        # Grab the count from opposing ends of the list
        impr = calc_counts[i]
        wor = calc_counts[len(calc_counts) - i - 1]

        # Accumulate the total number of tiles measured
        total += impr + wor
        # Sum the improved tiles
        improved += impr
        # Sum the worsened tiles
        worsened += wor
    # Return the percentage out of 100 of tiles that improved versus worsened
    return ((improved - worsened) / total) * 100


start = time.time()
run()
now = time.time() - start
# print(now)
