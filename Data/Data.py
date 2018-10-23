# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 09:17:25 2018

@author: William Huang
"""

import pandas as pd
from yahoofinancials import YahooFinancials
import datetime as dt
import numpy as np
import math

class FinanceData:
    def __init__(self, approach = 'Yahoo'):
		# Initialize the parameters
		# ----Input-----
		# approach: specify the data source, in current version, the Yahoo is the only available one
		# ----output----
        if(approach not in ['Yahoo']):
            raise Exception("Invalid approach, only allowed Yahoo , not", approach)
        self.approach = approach
    
    def columnNameMapping(columns):
		# Mapping the column names from different data source to unitized names
		# ----Input-----
		# columns: the original column names
		# ----output----
		# unitized column names
        '''Quandl column names: 'ticker','date','open','high','low','close','adj_close','volume'''
        '''Yahoo column name: 'adjclose', 'close', 'date', 'formatted_date', 'high', 'low', 'open','volume'''
        modifiedColumns = columns.copy()
        if('date' in columns):
            modifiedColumns[modifiedColumns.index('date')] = 'formatted_date'
        if('adj_close' in columns):
            modifiedColumns[modifiedColumns.index('adj_close')] = 'adjclose'
        return modifiedColumns
    
    def getPrice(self,ticker,startDate,endDate,dateAscending = True):
		# Get the price seires for single ticker
		# ----Input-----
		# ticker: ticker name for the stock
		# startDate: the start date of price series, the format is 'YYYY-MM-DD'
		# endDate: the end date of price series, the format is 'YYYY-MM-DD'
		# dateAscending: whether rank the price series by date ascending, the default value is true
		# ----output----
		# price series for multiple stocks in pandas DataFrame formate and use date as index
        if(self.approach == 'Yahoo'):
            table = YahooFinancials(ticker)
            table = pd.DataFrame(table.get_historical_price_data(startDate,endDate,'daily')[ticker]['prices'])
            table = table[['adjclose','formatted_date']]
            table.columns = [ticker,'date']
            table = table.sort_values(by = 'date',axis = 0,ascending = dateAscending)
            table = table.set_index('date')
            table.index = pd.to_datetime(table.index)
            return table
		
		
	def getPriceTable(self,tickerList,startDate,endDate,dateAscending = True):
		# Get the price seires for multiple tickers
		# ----Input-----
		# tickerList: ticker name for multiple stocks
		# startDate: the start date of price series, the format is 'YYYY-MM-DD'
		# endDate: the end date of price series, the format is 'YYYY-MM-DD'
		# dateAscending: whether rank the price series by date ascending, the default value is true
		# ----output----
		# price series for single stock in pandas DataFrame formate and use date as index
        tables = []
        for ticker in tickerList:
            tables.append(self.getPrice(ticker,startDate,endDate,dateAscending = True))
			
        return pd.concat(tables,axis = 1)
	
	def getDetailPriceInfo(self, ticker, start_date, end_date, columns = ['close','date'], dateAscending = True, frequency = 'D')
		# Get the aggregated detailed price seires for single ticker, including open, high, low, close, adj_close, volume
		# ----Input-----
		# ticker: ticker name for single stocks
		# startDate: the start date of price series, the format is 'YYYY-MM-DD'
		# endDate: the end date of price series, the format is 'YYYY-MM-DD'
		# columns: the columns in the output DataFrame, the default columns are 'close' and 'date' 
		# dateAscending: whether rank the price series by date ascending, the default value is true
		# frequency: aggregate frequency, default value is 'D', also accept 'W' for week and 'M' for month 
		# ----output----
		# aggregated price sereis for single stock
		if(frequency not in ['D','W','M']):
            raise Exception('''invalid frequency, available range ['D','W','M']''', frequency)

        available_Columns = ['date','open','high','close','adj_close', 'low', 'volume']
        for column in columns:
            if(column not in available_Columns):
                raise Exception('''invalid column names, available range ['date','open','high','close','adj_close', 'low', 'volume']''', column)
        if('date' not in columns):
            columns.append('date')
		
		
		if(self.approach == 'Yahoo'):
            table = YahooFinancials(ticker)
            table = pd.DataFrame(table.get_historical_price_data(startDate,endDate,'daily')[ticker]['prices'])
            newColumns = FinanceData.columnNameMapping(columns)
            table = table[newColumns]
            table.columns = columns
		if('date' in columns):
            table = table.sort_values(by = 'date',axis = 0,ascending = dateAscending)
		table = table.set_index('date')
        table.index = pd.to_datetime(table.index)
		
		if(frequency == 'D'):
            return table
        else:
            result = []
            for column in columns:
                if(column in ['open']):
                    result.append(table.resample(frequency).first()[column])
                elif(column in ['close','adj_close']):
                    result.append(table.resample(frequency).last()[column])
                elif(column in ['high']):
                    result.append(table.resample(frequency).max()[column])
                elif(column in ['low']):
                    result.append(table.resample(frequency).min()[column])
                elif (column in ['volume']):
                    result.append(table.resample(frequency).sum()[column])
            return(pd.concat(result,axis=1))
		
		
		
    def getMarketCapThread(self,df,start,end):
        for i in range(start,end):
            try:
                df.loc[i,'MarketCap'] = self.getMarketCap(df.loc[i,'Ticker'])
            except:
                df.loc[i, 'MarketCap'] = None

    def getMarketCaps(self,df,threads = 5):
        # if the parameter is a list of tickers
        if(isinstance(df,list)):
            df = pd.DataFrame(df,columns = ['Ticker'])
        if('Ticker' not in df.columns):
            raise Exception("Ticker column should be named as 'Ticker'")

        df['MarketCap'] = 0
        args = [x for x in range(0,len(df),int(len(df)/threads+2))]
        args.append(len(df))
        threads = []

        for i in range(len(args) - 1):
            t = threading.Thread(target=self.getMarketCapThread, args=(df,args[i], args[i + 1]))
            threads.append(t)

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

        return df

    #df1 and df2 should use date as index
    #dataFrame joins on right
    def dataMatching(self,df1,df2):
        df = pd.merge(df1, df2.iloc[:, :1], how='right', left_index=True, right_index=True).iloc[:,:-1].fillna(method='ffill')
        return df




            
    def getVol(self,ticker,window = 365):
        endDate = dt.date.today().isoformat()
        startDate = (dt.date.today() - dt.timedelta(window)).isoformat()
        price = self.getPrice(ticker,startDate,endDate)
        logReturn = np.diff(np.log(price),axis = 0)
        return logReturn.std()*math.sqrt(252)

    def getMarketCap(self, ticker):
        dataSource = YahooFinancials(ticker)
        return dataSource.get_summary_data()[ticker]['marketCap']

    def gettable(self, ticker, start_date, end_date, columns, frequency = 'D', path = './Data'):
        if(frequency not in ['D','W','M']):
            raise Exception('''invalid frequency, available range ['D','W','M']''', frequency)

        available_Columns = ['date','open','high','close','adj_close', 'low', 'volume']
        for column in columns:
            if(column not in available_Columns):
                raise Exception('''invalid column names, available range ['date','open','high','close','adj_close', 'low', 'volume']''', column)
        if('date' not in columns):
            columns.append('date')

        try:
            table = pd.read_csv(path+'/'+ticker+'.csv')[columns]
        except:
            raise Exception('cannot find the file', path+ticker+'.csv')

        if(start_date < table['date'].min()):
            raise Exception('start date out of range, it cannot be earlier than', table['date'].min())
        if(end_date > table['date'].max()):
            raise Exception('start date out of range, it cannot be latter than', table['date'].max())
        table = table[table['date'] >= start_date]
        table = table[table['date'] <= end_date]
        table = table.reset_index(drop=True)
        table = table.set_index('date')
        table.index = pd.to_datetime(table.index)

        if(frequency == 'D'):
            return table
        else:
            result = []
            for column in columns:
                if(column in ['open']):
                    result.append(table.resample(frequency).first()[column])
                elif(column in ['close','adj_close']):
                    result.append(table.resample(frequency).last()[column])
                elif(column in ['high']):
                    result.append(table.resample(frequency).max()[column])
                elif(column in ['low']):
                    result.append(table.resample(frequency).min()[column])
                elif (column in ['volume']):
                    result.append(table.resample(frequency).sum()[column])
            return(pd.concat(result,axis=1))


