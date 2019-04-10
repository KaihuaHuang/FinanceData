# FinanceData  
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Finance data retrieve library. A warp of yahoofinancials library for easy use. Thanks to yahoofinancials https://github.com/JECSand/yahoofinancials  
Current Version: v1.0  
Version Released: 4/10/2019  
Third-Party Dependency: yahoofinancials, numpy, pandas  
Report any bugs by opening an issue here: https://github.com/KaihuaHuang/FinanceData/issues  
## Methods
**1. getPrice(ticker,startDate,endDate,dateAscending = True)** 
> - Get the price series for single ticker
>  - ----Input----
>> ticker: ticker name for the stock  
>> startDate: the start date of price series, the format is 'YYYY-MM-DD'  
>> endDate: the end date of price series, the format is 'YYYY-MM-DD'  
>> dateAscending: whether rank the price series by date ascending, the default value is true  
> - ----output----
>> price series for multiple stocks in pandas DataFrame format and use date as index  

**2. getPriceTable(tickerList,startDate,endDate,dateAscending = True)**    
> - Get the price series for multiple tickers
> - ----Input-----
>> tickerList: ticker name for multiple stocks  
>> startDate: the start date of price series, the format is 'YYYY-MM-DD'  
>> endDate: the end date of price series, the format is 'YYYY-MM-DD'  
>> dateAscending: whether rank the price series by date ascending, the default value is true  
>> localCheck: loading local csv file, check the existing data see whether we need to retrieve data from Yahoo. The local file should contain date as index.  
>> update: whether to update local file  
> - ----output----
>> price series for single stock in pandas DataFrame format and use date as index

**3. getDetailPriceInfo(ticker, startDate, endDate, columns = ['close','date'], dateAscending = True, frequency = 'D')**
> - Get the aggregated detailed price series for single ticker, including open, high, low, close, adj_close, volume
> - ----Input-----
>> ticker: ticker name for single stocks  
>> startDate: the start date of price series, the format is 'YYYY-MM-DD'  
>> endDate: the end date of price series, the format is 'YYYY-MM-DD'  
>> columns: the columns in the output DataFrame, the default columns are 'close' and 'date'   
            avalible columns: ['date','open','high','close','adj_close', 'low', 'volume']  
>> dateAscending: whether rank the price series by date ascending, the default value is true  
>> frequency: aggregate frequency, default value is 'D', also accept 'W' for week and 'M' for month   
> - ----output----
>> aggregated price series for single stock

4. getVol(ticker,window = 365)  
5. getMarketCap(ticker)  

