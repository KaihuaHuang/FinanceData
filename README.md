# FinanceData  
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Finance data retrieve library. A warp of yahoofinancials library for easy use. Thanks to yahoofinancials https://github.com/JECSand/yahoofinancials  
Current Version: v1.0  
Version Released: 10/23/2018  
Third-Party Dependency: yahoofinancials, numpy, pandas  
Report any bugs by opening an issue here: https://github.com/KaihuaHuang/FinanceData/issues  
## Methods
getPrice(ticker,startDate,endDate,dateAscending = True)  
getPriceTable(tickerList,startDate,endDate,dateAscending = True)  
getDetailPriceInfo(ticker, startDate, endDate, columns = ['close','date'], dateAscending = True, frequency = 'D')  
getVol(ticker,window = 365)  
getMarketCap(ticker)  

