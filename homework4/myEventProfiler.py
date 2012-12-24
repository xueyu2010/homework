'''
Homework 2 for Computational Invests I on coursera.com
This code is very simiar to tutorial9.py
@author: Grace Yu
@contact: graceyuxue@gmail.com  
@summary: Event Profiler for SP500 stocks during Jan.1.2008 to Dec.31.2009
'''

import pandas
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep
import csv

storename = "Yahoo"
actual_close_field = "actual_close"
target_price = 5.0
marketSymbol = "SPY"
order_filename = "orders.csv"
sell = "Sell"
buy = "Buy"
shares = 100
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)
symbolList = "sp5002012"
eventFilename="fiveDollarEvent"

################# Construct Event ##################
def findEvents(symbols, startday, endday, verbose=False, generateOrders=False,targetPrice=target_price):
    
    # Reading data
    timeofday=dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(startday,endday,timeofday)
    dataobj = da.DataAccess(storename)
    if verbose:
        print __name__ + " reading data from " + storename
    
    # Read 'actual close' field data value
    actual_close = dataobj.get_data(timestamps, symbols, actual_close_field)
    
    # trim the data - removing the NaN values from the matrix
    #actual_close = (actual_close.fillna(method='ffill')).fillna(method='backfill')
       
    np_eventmat = copy.deepcopy(actual_close)  
    
    # create event matrix with np value
    for sym in symbols:
        for t in timestamps:
            np_eventmat[sym][t]=np.NAN
            
    # Create Trading Orders File based on Event
    if generateOrders:
        orderCSV = open(order_filename, "wb")
        write = csv.writer(orderCSV, delimiter=',')
    
    
    # fill in event
    event_count=0
    for symbol in symbols:
        for t in range(1, len(actual_close[symbol])):
            if(actual_close[symbol][t-1]>= targetPrice and actual_close[symbol][t]< targetPrice):
                if generateOrders:
                    # generate a order Buy and Sell after 5 trading days
                    write.writerow([timestamps[t].year, timestamps[t].month, timestamps[t].day, symbol, buy, str(shares)])
                    if t + 5 < len(timestamps):
                        fiveDaysLater = timestamps[t+5]
                    else:
                        fiveDaysLater = timestamps[len(timestamps)-1]
                    write.writerow([fiveDaysLater.year, fiveDaysLater.month, fiveDaysLater.day, symbol, sell, str(shares)])
                if verbose:
                    print __name__ + " found event for symbol: " + symbol, actual_close[symbol][t-1] , actual_close[symbol][t]
                np_eventmat[symbol][t] = 1.0
                event_count = event_count +1
    # print out event matrix for debug
    
    print __name__ + "Event Matrix"
    for sym in symbols:
        for t in range(1, len(actual_close[sym])):
            if(np_eventmat[sym][t] == 1.0):
                print timestamps[t] , sym , " has event"
    print "####### Found ", event_count, " in total #######"
    return np_eventmat

def generateOrdersByEvent(targetPrice=target_price, startday=startday, endday=endday, symbolList=symbolList, eventFilename=eventFilename):
    print "Event analysis for", targetPrice, "$, save order to", order_filename
    print "Start from:", startday, " - End to:", endday, "Get from symbol list", symbolList
    
    # get symbols from QSData/Yahoo
    dataobj = da.DataAccess('Yahoo')
    symbols = dataobj.get_symbols_from_list(symbolList);
    symbols.append(marketSymbol)
    
    
    # start from 2008,1,1 to 2009, 12,31

    eventMatrix = findEvents(symbols, startday, endday, True, True,targetPrice)
    eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,lookback_days=20,lookforward_days=20,verbose=True)
    eventProfiler.study(filename=eventFilename, plotErrorBars=True, plotMarketNeutral=True, plotEvents=True,marketSymbol='SPY')

    
    
################## MAIN CODE ###################
if __name__ == '__main__':
    print "Event analysis for", target_price, "$, save order to", order_filename
    print "Start from:", startday, " - End to:", endday, "Get from symbol list", symbolList
    
    # get symbols from QSData/Yahoo
    dataobj = da.DataAccess('Yahoo')
    symbols = dataobj.get_symbols_from_list(symbolList);
    symbols.append(marketSymbol)
    
    
    # start from 2008,1,1 to 2009, 12,31

    eventMatrix = findEvents(symbols, startday, endday, verbose=True, generateOrders=True)
    eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,lookback_days=20,lookforward_days=20,verbose=True)
    eventProfiler.study(filename=eventFilename, plotErrorBars=True, plotMarketNeutral=True, plotEvents=True,marketSymbol='SPY')



            
        
