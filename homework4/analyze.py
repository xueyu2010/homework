 
'''
 This is a file that takes a values.csv file and benchmark symbol, then illustrate
 the fund perfromance with figure, and calculate key metric for portfolio, also
 compares with benchmark metrics
 
 usages:
 python analyze.py values.csv SPX
 
'''
import sys
import datetime as dt
import csv
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import copy
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import qstkutil.tsutil as tsu

debug = False
h = 16
closefield = "actual_close"

valueFilename="values.csv"
#
#can not read symbol with '$' from command line, so hard code the benchmark symbol here for future use
#
benchmark=["$SPX"]
figureName = "analyzeFigure"

# read file into memory
def analyzeValue(valueFilename=valueFilename, benchmark=benchmark,figureName=figureName, closefield=closefield):
    valueCSV = open(valueFilename, 'rU')
    reader = csv.reader(valueCSV, delimiter=',')
    timestamp = []
    values = []
    
    for row in reader:
        timestamp.append(dt.date(int(row[0]),int(row[1]),int(row[2])))
        values.append(float(row[3]))
    
    #
    # Plot portfolio value
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(timestamp, values)
    
    # adjust tick size 
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(6)
        
    plt.plot(timestamp, values)
    savefig(figureName,format='pdf')
    
    #
    # Compute Cumulative Return, Sharpe ratio, std of daily return for the portfolio
    #
    
    
    if debug:
        print "-----Before calculate-----"
        for v in values:
            print v
    
    daily_returns0 = tsu.daily(values)
    if debug:
        print "-----After calculate-----"
        for v in daily_returns0:
            print v
            
    final_return = values[len(values)-1]/values[0]-1
    print "Total Return:" , final_return
            
    mean = np.average(daily_returns0)
    print "Expected Return:", mean
    
    std2 = np.std(daily_returns0)
    print "Standard Deviation:", std2
    
    sharp_ratio = tsu.get_sharpe_ratio(daily_returns0)
    print "Calculated Sharpe Ratio:", tsu.sqrt(252) * mean/std2
    print "Get Sharpe Ration from QSTK:", sharp_ratio
    
    
    #
    # Calculate Benchmark metrics
    #
    timeofday = dt.timedelta(hours=h)
    timestamps = du.getNYSEdays(timestamp[0],timestamp[len(timestamp)-1],timeofday)
    dataobj = da.DataAccess('Yahoo')
    
    print "reading benchmark data...",benchmark
    close = dataobj.get_data(timestamps, benchmark, closefield)
    if debug:
        for time in timestamps:
            print time, close[benchmark[0]][time]
                            
    close = (close.fillna(method='ffill')).fillna(method='backfill')
    
    bValues = close.values
    print 
    final_return_b = (bValues[len(bValues)-1]/bValues[0])-1
    print benchmark,"Total Return:" , final_return_b
    
    # daily returns
    b_daily_returns0 = tsu.daily(bValues)
    mean = np.average(b_daily_returns0)
    print benchmark, "Expected Return:", mean
    
    std2 = np.std(b_daily_returns0)
    print benchmark,"Standard Deviation:", std2
    
    sharp_ratio = tsu.get_sharpe_ratio(b_daily_returns0)
    print benchmark,"Calculated Sharpe Ratio:", tsu.sqrt(252) * mean/std2
    print benchmark,"Get Sharpe Ration from QSTK:", sharp_ratio

if __name__ == '__main__':
    import sys
    if len(sys.argv)!=4:
        print "Error - Input arguements are not correct, expecting 4, but actual", len(sys.argv)

    valueFilename = str(sys.argv[1])
    #benchmark[] = str(sys.argv[2])
    figureName = sys.argv[3]
    
    if debug:
        print "value-file-name:", valueFilename
        print "benchmark-symbol:", benchmark