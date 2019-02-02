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
import threading
from bdateutil import isbday
from bdateutil import relativedelta

import holidays

class FinanceData:
	def __init__(self, approach = 'Yahoo'):
		# Initialize the parameters
		# ----Input-----
		# approach: specify the data source, in current version, the Yahoo is the only available one
		# ----output----
		if(approach not in ['Yahoo']):
			raise Exception("Invalid approach, only allowed Yahoo , not", approach)
		self.approach = approach

	@staticmethod
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
		# Get the price series for single ticker
		# ----Input-----
		# ticker: ticker name for the stock
		# startDate: the start date of price series, the format is 'YYYY-MM-DD'
		# endDate: the end date of price series, the format is 'YYYY-MM-DD'
		# dateAscending: whether rank the price series by date ascending, the default value is true
		# ----output----
		# price series for multiple stocks in pandas DataFrame format and use date as index
		startDate = dt.datetime.strptime(startDate, '%Y-%m-%d').date()
		endDate = dt.datetime.strptime(endDate, '%Y-%m-%d').date()

		if (startDate > endDate):
			raise Exception('startDate is later than endDate')
		#table = YahooFinancials(ticker)
		#yahooPrices = table.get_historical_price_data(startDate.isoformat(), endDate.isoformat(), 'daily')[ticker]['prices']
		if(self.approach == 'Yahoo'):
			try:
				table = YahooFinancials(ticker)
				yahooPrices = table.get_historical_price_data(startDate.isoformat(),endDate.isoformat(),'daily')[ticker]['prices']
				table = pd.DataFrame(yahooPrices)
				table = table[['adjclose','formatted_date']]
				table.columns = [ticker,'date']
				table = table.sort_values(by = 'date',axis = 0,ascending = dateAscending)
				table = table.set_index('date')
				table.index = pd.to_datetime(table.index)
			except:
				table = pd.DataFrame(columns = [ticker,'date'])
				table = table.set_index('date')
			return table

	def getPriceTable(self,tickerList,startDate = None,endDate = None,localCheck = None,dateAscending = True, update = False):
		# Get the price series for multiple tickers
		# ----Input-----
		# tickerList: ticker name for multiple stocks
		# startDate: the start date of price series, the format is 'YYYY-MM-DD'
		# endDate: the end date of price series, the format is 'YYYY-MM-DD'
		# dateAscending: whether rank the price series by date ascending, the default value is true
		# localCheck: loading local csv file, check the existing data see whether we need to retrieve data from Yahoo. The local file should contain date as index.
		# update: whether to update local file
		# ----output----
		# price series for single stock in pandas DataFrame format and use date as index

		if(endDate == None):
			endDate = dt.date.today() + relativedelta(bdays=-1,holidays = holidays.US())
		else:
			endDate = dt.datetime.strptime(endDate, '%Y-%m-%d').date()
		if(startDate == None):
			startDate = endDate + relativedelta(bdays=-252,holidays = holidays.US())
		else:
			startDate = dt.datetime.strptime(startDate,'%Y-%m-%d').date()


		if(startDate > endDate):
			raise Exception('startDate is later than endDate')

		if (isinstance(tickerList, str)):
			tickerList = [tickerList, ]

		if(localCheck!=None):
			try:
				localFile = pd.read_csv(localCheck,index_col='date',parse_dates=True)
			except:
				raise Exception('Read Local File Error')

			if(np.all([ticker in localFile.columns for ticker in tickerList]) == False):
				raise Exception('''Local File Columns Doesn't Match Ticker List''')

			# Make sure it's business day
			if(isbday(startDate,holidays = holidays.US()) == False):
				startDateCehck = startDate + relativedelta(bdays=1)
			else:
				startDateCehck = startDate

			if (isbday(endDate, holidays=holidays.US()) == False):
				endDateCehck = endDate + relativedelta(bdays=-1)
			else:
				endDateCehck = endDate




			if(startDateCehck in localFile.index and endDateCehck in localFile.index):
				return localFile[startDate.isoformat():endDate.isoformat()]

			if(startDate < localFile.index[0].date()):
				readStart = startDate
				if(endDate <= localFile.index[-1].date()):
					readEnd = localFile.index[0].date()
				else:
					readEnd = endDate
			else:
				readStart = localFile.index[-1].date()
				readEnd = endDate


			tables = []

			for ticker in tickerList:
				# print(ticker)
				tables.append(self.getPrice(ticker, readStart.isoformat(), readEnd.isoformat(), dateAscending=True))
			missingComponents = pd.concat(tables,axis = 1)
			localFile = pd.concat([localFile, missingComponents], axis=0).sort_index(ascending=True)
			localFile = localFile[~localFile.index.duplicated()]
			if(update):
				localFile.to_csv(localCheck,index = True)
			return localFile[startDate.isoformat():endDate.isoformat()]


		tables = []
		for ticker in tickerList:
			tables.append(self.getPrice(ticker,startDate.isoformat(),endDate.isoformat(),dateAscending = True))
			
		return pd.concat(tables,axis = 1)
	
	def getDetailPriceInfo(self, ticker, startDate, endDate, columns = ['close','date'], dateAscending = True, frequency = 'D'):
		# Get the aggregated detailed price series for single ticker, including open, high, low, close, adj_close, volume
		# ----Input-----
		# ticker: ticker name for single stocks
		# startDate: the start date of price series, the format is 'YYYY-MM-DD'
		# endDate: the end date of price series, the format is 'YYYY-MM-DD'
		# columns: the columns in the output DataFrame, the default columns are 'close' and 'date' 
		# dateAscending: whether rank the price series by date ascending, the default value is true
		# frequency: aggregate frequency, default value is 'D', also accept 'W' for week and 'M' for month 
		# ----output----
		# aggregated price series for single stock
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
		
	def getVol(self,ticker,window = 365):
		# calculate stock volatility
		# ----Input-----
		# ticker: ticker name for the stock
		# window: look back window to calculate volatility, default is 365 days
		# ----output----
		# stock volatility
		endDate = dt.date.today().isoformat()
		startDate = (dt.date.today() - dt.timedelta(window)).isoformat()
		price = self.getPrice(ticker,startDate,endDate)
		logReturn = np.diff(np.log(price),axis = 0)
		return logReturn.std()*math.sqrt(252)

	def getMarketCap(self, ticker):
		# retrieve stock market cap
		# ----Input-----
		# ticker: ticker name for the stock
		# ----output----
		# stock market cap
		dataSource = YahooFinancials(ticker)
		return dataSource.get_summary_data()[ticker]['marketCap']

	def getMarketCapThread(self,df,start,end):
		# retrieve stock market cap in ticker list from index start to end
		# ----Input-----
		# df: DataFrame includes one ticker column
		# start: start index
		# end: end index
		# ----output----
		# DataFrame with stock market cap information in MarketCap column
		for i in range(start,end):
			try:
				df.loc[i,'MarketCap'] = self.getMarketCap(df.loc[i,'Ticker'])
			except:
				df.loc[i, 'MarketCap'] = None

	def getMarketCaps(self,df,threads = 5):
		# retrieve stock market cap in ticker list
		# ----Input-----
		# df: DataFrame includes one ticker column
		# threads: the number of threads to retrieve market cap
		# ----output----
		# DataFrame with stock market cap information in MarketCap column
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

	def dataMatching(self,df1,df2):
		# df1 and df2 should use date as index
		# dataFrame joins on right
		df = pd.merge(df1, df2.iloc[:, :1], how='right', left_index=True, right_index=True).iloc[:,:-1].fillna(method='ffill')
		return df





