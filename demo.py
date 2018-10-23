from Data import FinanceData

if __name__ == '__main__':
	dataSource = FinanceData()
	startDate = '2017-01-01'
	endDate = '2018-01-01'
	ticker = 'AMZN'
	tickerList = ['AMZN','GS']

	print('\nGet price series for single ticker')
	print(dataSource.getPrice(ticker,startDate,endDate,dateAscending = True).head(10))

	print('\nGet price series for several ticker')
	print(dataSource.getPriceTable(tickerList, startDate, endDate, dateAscending=True).head(10))

	print('\n Get aggregated information for single stock')
	print('Available aggregate frequency: D, W, M')
	print('Available column names: open, high, low, close, adj_close, volume')
	print(dataSource.getDetailPriceInfo(ticker, startDate, endDate,columns = ['open','close','high','volume'], frequency= 'W', dateAscending=True).head(10))

	print('\nGet stock volatility')
	print(dataSource.getVol(ticker,window = 252))

	print('\nGet stock market cap')
	print(dataSource.getMarketCap(ticker))
