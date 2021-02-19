# MapMetrics Analysis
The program functions by taking in two files, each from two different time periods for the same geographical location. The functions scan over each tile and calculate the change in median over the time period. It also calculates the average median for each time period and calculates the change between months. 

##Running
#### Changing cities
To change the files that the program processes, the **dir** var on line 12 is currently where you change the file location. It currently expects a folder with two MapMetrics jobs using the same bouding box.
###### Example City Setup
![](https://raw.githubusercontent.com/JamesonToper-TomTom/MapMetricsAnalysis/main/README/file_example.png)

###### Changing Directory
![](https://raw.githubusercontent.com/JamesonToper-TomTom/MapMetricsAnalysis/main/README/dir_example.png)

#### Example Output

    ---------------------------------------
    Average Starting Median: 1.1416
    Average Ending Median: 1.1236
    Percent Median Change (Negative is better): -1.571
    Overall Geographical Improvement: 5.4545
    ----------------------------------------
The starting median is the average of the first month, the ending median is the last month. The percent change in median should go down for improvement, as it will get smaller as traces are more aligned to the map. The Geographical Improvement is the average percent change in median over all tiles, which should show a positive number for improvement.


