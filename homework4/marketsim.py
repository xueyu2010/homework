'''
This is a file that takes a values.csv file and benchmark symbol, then illustrate
the fund perfromance with figure, and calculate key metric for portfolio, also
compares with benchmark metrics

usages:
python marketsim.py 1000000 orders.csv values.csv
 
orders format:
date,symbol,buy/sell,shares

vlaues format:
date,value
Homework for market simulator
Author: Grace(Xue) Yu
'''


import datetime as dt
import csv
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import copy

debug=True

filename="orders.csv"
valueFile="values.csv"
baseCash=1000000

closefield = "actual_close"
h = 16
      
class Order:
    def __init__(self, date,symbol,order_type,shares):
        self.date = date
        self.symbol = symbol
        self.order_type = order_type
        self.shares = shares
        
    def __cmp__(self, other):
        assert isinstance(other, Order)
        return cmp(self.date,other.date)
    
    def __str__(self):
        return str(self.date)+"," +self.symbol +"," +self.order_type+","+ str(self.shares)
    
    def execute(self, price):
        # execute this order based on symbols, return the cash amount that earned or spent
        cash = self.shares * price
        if self.order_type.lower() == "sell":
            print self.date, "Sell " , str(self.shares), self.symbol, " with price=", price, "Got cash=" + str(cash)
            return cash
        elif self.order_type.lower() == "buy":
            print self.date, "Buy " , str(self.shares), self.symbol, " with prie = " , price, "Spent cash=" + str(-1 * cash)
            return -1 * cash
  
def parseFile(filename=filename):
    # Open CSV file and construct the map
    orderCSV = open(filename, 'rU')
    reader = csv.reader(orderCSV, delimiter=',')
    symbols = set()
    orders = []
    ordersMap = {}
    
    for row in reader:
        date = dt.date(int(row[0]), int(row[1]), int(row[2]))
        time = dt.datetime(date.year, date.month, date.day, h)
        order = Order(date, row[3],row[4],int(row[5]))
        print "Order: ", order
        orders.append(order)
        symbols.add(row[3])
        if time in ordersMap:
            ordersMap[time].append(order)
        else:
            orderList = []
            orderList.append(order)
            ordersMap[time] = orderList
    orders.sort()
    return [orders[0].date, orders[len(orders)-1].date, symbols, orders, ordersMap]


############ MAIN CODE #############


def generateValue(baseCash=baseCash, filename=filename,valueFile=valueFile, closefield=closefield):
    [startDate, endDate, symbols, orders, ordersMap] = parseFile(filename)
    if debug:
        print "start Date:", startDate, "End Date:", endDate
        for k in ordersMap.keys():
            print k
            for o in ordersMap[k]:
                print o
    # Get historical price data for adjusted close
    timeofday = dt.timedelta(hours=h)
    timestamps = du.getNYSEdays(startDate,endDate,timeofday)
    dataobj = da.DataAccess('Yahoo')
    
    print "reading data..."
    close = dataobj.get_data(timestamps, symbols, closefield)
    close = (close.fillna(method='ffill')).fillna(method='backfill')
    
    # Create Cash Arrayp
    cashList = {}
    currentValue = baseCash
    for time in timestamps:
        if time in ordersMap.keys():
            # update the cash since there is order
            for o in ordersMap[time]:
                currentValue = currentValue + o.execute(close[o.symbol][time])
        if debug:
            print time , "Current Cash: ", currentValue
        cashList[time] = currentValue
    
    # Create Ownership array date, symbol, share number
    owners = {}
    currentShare = {}
    for symbol in symbols:
        currentShare[symbol] = 0
        
    for time in timestamps:
        if time in ordersMap.keys():
            for o in ordersMap[time]:
                print "######Order : " , o
                if(o.order_type.lower() == "sell"):
                    currentShare[o.symbol] = currentShare[o.symbol] - o.shares
                    print "---deduct", o.shares, "from", o.symbol
                elif o.order_type.lower() == "buy":
                    currentShare[o.symbol] = currentShare[o.symbol] + o.shares
                    print "---add", o.shares, "to", o.symbol
        shares = copy.deepcopy(currentShare)
        owners[time] = shares
        
    # debug
    if debug:
        for time in timestamps:
            print time,owners[time]
    
    # compute the assets base on chasList and owners
    
    values = {}
    for time in timestamps:
        assetValue = 0
        for sym in owners[time]:
            if owners[time][sym] != 0:
                assetValue = assetValue + close[sym][time] * owners[time][sym]
                if debug:
                    print "---", sym, "has",owners[time][sym], "price=", close[sym][time]
           
        values[time] = cashList[time] + assetValue
        if debug:
            print "--- cashValue=",cashList[time]
            print "###Today's total value=", values[time]
    
    # Write to value.csv file
    valuesCSV = open(valueFile, 'wb')
    write = csv.writer(valuesCSV, delimiter=',')
    for k in sorted(values.iterkeys()):
        write.writerow([k.year, k.month, k.day, values[k]])
    print "Finished writing values to", valuesCSV


if __name__ == '__main__':
    import sys
    baseCash = float(sys.argv[1])
    filename = sys.argv[2]
    valueFile = sys.argv[3]
    generateValue(baseCash,filename,valueFile)
    
        
    