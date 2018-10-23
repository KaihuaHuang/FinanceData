# FinanceData  
Finance data retrieve library. A warp of yahoofinancials library for easy use. Thanks to yahoofinancials https://github.com/JECSand/yahoofinancials  
Current Version: v1.0  
Version Released: 10/23/2018  
Third-Party Dependency: yahoofinancials, numpy, pandas  
Report any bugs by opening an issue here: https://github.com/KaihuaHuang/VaR/issues  
## Methods
getPrice(ticker,startDate,endDate,dateAscending = True)  
getPriceTable(tickerList,startDate,endDate,dateAscending = True)  
getDetailPriceInfo(ticker, startDate, endDate, columns = ['close','date'], dateAscending = True, frequency = 'D')  
getVol(ticker,window = 365)  
getMarketCap(ticker)  

