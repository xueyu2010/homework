import myEventProfiler
import marketsim
import datetime as dt
import analyze


target_price = 5.0
order_filename = "orders.csv"
shares = 100
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)
symbolList = "sp5002012"
eventFilename="fiveDollarEvent"
valueFile = "values.csv"
marketSymbol = ["$SPX"]
figureName = "analyzeChart"
closefield = "actual_close"

baseCash=50000

print "-------------Looking for qualified Events-----------"
myEventProfiler.generateOrdersByEvent(target_price, startday, endday, symbolList, eventFilename)

print "-------------Market Analysis for the Orders----------"
marketsim.generateValue(baseCash, order_filename,valueFile,closefield)

print "-------------Analyze Portfolio Values-----------------"
analyze.analyzeValue(valueFile, marketSymbol,figureName,closefield)