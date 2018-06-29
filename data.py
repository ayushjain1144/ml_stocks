"""for now we look for only one parameter
the debt/equity ratio"""

#pandas is used in data manipulation like openinng data in different formats
import pandas as pd

from bs4 import BeautifulSoup

#for command line like stuff
import os
import time
from datetime import datetime
from time import mktime

import matplotlib
import matplotlib.pyplot as plt
#import Tkinkter as tk

from matplotlib import style
style.use('dark_background')

import re

#path to unzipped data 

path = "/home/hp/Downloads/data/intraQuarter"

# preprocessing to extract out the relevant data

def find_percent_change(new_value, old_value):

	if old_value == 0 or old_value == 'N/A' or new_value == 'N/A':
		percent_change = 'N/A'
		return percent_change
	percent_change = (new_value - old_value)/old_value * 100
	return percent_change



def Key_Stats(gather=['Total Debt/Equity',
					  'Trailing P/E',
					  'Price/Sales',
					  'Price/Book',
					  'Profit Margin',
					  'Operating Margin',
					  'Return on Assets',
					  'Return on Equity',
					  'Revenue Per Share',
					  'Market Cap',
						'Enterprise Value',
						'Forward P/E',
						'PEG Ratio',
						'Enterprise Value/Revenue',
						'Enterprise Value/EBITDA',
						'Revenue',
						'Gross Profit',
						'EBITDA',
						'Net Income Avl to Common ',
						'Diluted EPS',
						'Earnings Growth',
						'Revenue Growth',
						'Total Cash',
						'Total Cash Per Share',
						'Total Debt',
						'Current Ratio',
						'Book Value Per Share',
						#'Cash Flow',
						'Beta',
						'Held by Insiders',
						'Held by Institutions',
						'Shares Short (as of',
						'Short Ratio',
						'Short % of Float',
						'Shares Short (prior ']):



	statspath = path+ '/_KeyStats'

	# list of all the directories in Key_stats folder
	stock_list = [x[0] for x in os.walk(statspath)]
	
	df = pd.DataFrame(columns = ['Date',
								'Unix',
								'Ticker',
								'Price',
								'stock_p_change',
								'SP500',
								'sp500_p_change',
								'Difference',
								##############
								'DE Ratio',
								'Trailing P/E',
								'Price/Sales',
								'Price/Book',
								'Profit Margin',
								'Operating Margin',
								'Return on Assets',
								'Return on Equity',
								'Revenue Per Share',
								'Market Cap',
								'Enterprise Value',
								'Forward P/E',
								'PEG Ratio',
								'Enterprise Value/Revenue',
								'Enterprise Value/EBITDA',
								'Revenue',
								'Gross Profit',
								'EBITDA',
								'Net Income Avl to Common ',
								'Diluted EPS',
								'Earnings Growth',
								'Revenue Growth',
								'Total Cash',
								'Total Cash Per Share',
								'Total Debt',
								'Current Ratio',
								'Book Value Per Share',
								#'Cash Flow',
								'Beta',
								'Held by Insiders',
								'Held by Institutions',
								'Shares Short (as of',
								'Short Ratio',
								'Short % of Float',
								'Shares Short (prior ',                                
								##############
								'Status'])


	ticker_list = []

	sp500_df = pd.read_csv("YAHOO-INDEX_GSPC.csv")

	for each_dir in stock_list[1:]:

		# collects all the files im a dir
		each_file = os.listdir(each_dir)
		# each ticker represents a company
		ticker = each_dir.split("/")[-1]
		ticker_list.append(ticker)
		
		new_value_sp500 = -1
		old_value_sp500 = -1
		new_value_stock = -1
		old_value_stock = -1

		# proceed only if dir contains any file
		if len(each_file) > 0:
			for file in each_file:

				#esch file's name is basically timestamp.html
				data_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')

				
				#	date_stamp_formatted = datetime.isofformat(date_stamp, '')
				unix_time = time.mktime(data_stamp.timetuple())
				
				#print(data_stamp, unix_time)
				full_file_path = each_dir + '/' + file
				source = open(full_file_path, 'r').read()
				soup = BeautifulSoup(source, 'html.parser')
			
				# it just captures the value of the equity-debt ratio we are looking for. Do Inspect element for better insight
				# some might not have DE ratio, so try block 
				try:

					value_list = []

					for each_data in gather:

						try:
							# matches the number of each_data we want

							regex = re.escape(each_data) + r'.*'
							if(each_data == "EBITDA" or each_data == "Revenue"):
								value = soup.find('td', text=re.compile(each_data + ':')).find_next_sibling().text

							value = soup.find('td', text=re.compile(regex)).find_next_sibling().text
							
							#print(value)
							#time.sleep(1)
							
							
							#value = value.group(1)

							#some data has M for million and B for billion
							
							if "B" in value:
								value = float(value.replace("B" , '')) * 1000000000

							elif "M" in value:
								value = float(value.replace("M", ''))* 1000000
							elif "K" in value:
								value = float(value.replace("K", ""))* 1000	

							elif "%" in value:
								value = float(value.replace("%", ''))
							elif "\n" in value:
								#print("yipee")
								value = value.replace("\n", '')
								value = float(value)				

							elif ' ' in value:
								print("yes")
								value = value.replace(" ", '')
								value = float(value)
							elif ',' in value:
								value  = value.replace(",", '')
								value = float(value) 	
							elif 'N/A' in value:
								value = 'N/A'
								#print("finally")				


							value_list.append(value)		
							

						except Exception as e:

							try:

								match = soup.find_all('td', class_ =  'yfnc_tablehead1')
								flag = 1
								if(each_data == "Revenue" or each_data == "EBITDA"):
									flag = 0

								for m in match:
									text = str(m.parent)
									

									if each_data in text:
										if(flag == 1):
											value = m.parent.find('td', class_ ='yfnc_tabledata1').text
											break
										else:
											flag = 1	
										

								if "B" in value:
									value = float(value.replace("B" , '')) * 1000000000

								elif "M" in value:
									value = float(value.replace("M", ''))* 1000000
								elif "K" in value:
									value = float(value.replace("K", ""))* 1000	

								elif "%" in value:
									value = float(value.replace("%", ''))

								elif "\n" in value:
									#print("happy")
									value = value.replace("\n", '')
									value = float(value)
			

								elif ' ' in value:
									value = value.replace(" ", '')
									value = float(value)

								elif ',' in value:
									value = value.replace(",", "")
									value = float(value)	
								elif 'N/A' in value:
									value = 'N/A'
									#print("phoda")			


								value_list.append(value)		

							except Exception as e:		
							# if something bad occurs like missing data
								#print(str(e), file, ticker, each_data, "ge")
							
								value = "N/A"
								value_list.append(value)

				
					try:

						#converting our unix time into the format of Yahoo-index.csv file
						sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')

						#grabbing the row having market close value for the date
						row = sp500_df[(sp500_df["Date"] == sp500_date)]

						#Grabbing thr market close value
						sp500_value = float(row["Adj Close"])

					#deals with the case when our DE ratio is obtained on a day whenmarket is closed

					except:

						# just shifting the day by three days back. DE ratio will not be affected by shifting a few days
						sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df["Date"] == sp500_date)]
						sp500_value = float(row["Adj Close"])

					# now we want the stock price to compare to the S&P 500 value
					try:
						stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])  

					except Exception as e:
						#occuring because source code looks like following
						# <span id="yfs_l10_afl">43.27</span>
						try:

							stock_price = source.split('</small><big><b>')[1].split('</b></big>')[0]
							# <span id="yfs_l10_afl">43.27</span>

							stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
							
							stock_price = float(stock_price.group(1))

						except Exception as e:
							
							try:
								#soup = BeautifulSoup(source, 'lxml')
								match  = soup.find('span', class_ = 'time_rtq_ticker' )
								stock_price = match.find('span').text
								stock_price = float(stock_price)

							except Exception as e:
								stock_price = 'N/A'
								#print("getha",str(e), file, ticker)	






					new_value_stock = stock_price
					new_value_sp500 = sp500_value
					if(old_value_stock == -1):
						stock_p_change = 'N/A'
						sp500_p_change = 'N/A'

					else:
						try:
							stock_p_change = find_percent_change(new_value_stock, old_value_stock)
							sp500_p_change = find_percent_change(new_value_sp500, old_value_sp500)	
						except Exception as e:
							pass
							#print("ewbbqwnqrwhw", str(e), file, ticker)	

					old_value_stock = new_value_stock
					old_value_sp500 = new_value_sp500
					if(stock_p_change == 'N/A' or sp500_p_change == 'N/A'):
						
						status = 'N/A'
						difference = 'N/A'
					else:	 
						difference = stock_p_change - sp500_p_change

						if(stock_p_change > sp500_p_change):
							status = "outperform"

						# considering the equality case too.		
						else:
							status = "underperform"	

						
						


						#if value_list.count(re.compile(r'.*?(N/A).*?')) > 0:
						#	pass
						
						try:

							df = df.append({'Date':data_stamp,
									'Unix':unix_time,
									'Ticker':ticker,
									
									'Price':stock_price,
									'stock_p_change':stock_p_change,
									'SP500':sp500_value,
									'sp500_p_change':sp500_p_change,
									'Difference':difference,
									'DE Ratio':value_list[0],
									'Trailing P/E':value_list[1],
									'Price/Sales':value_list[2],
									'Price/Book':value_list[3],
									'Profit Margin':value_list[4],
									'Operating Margin':value_list[5],
									'Return on Assets':value_list[6],
									'Return on Equity':value_list[7],
									'Revenue Per Share':value_list[8],
									'Market Cap':value_list[9],
									 'Enterprise Value':value_list[10],
									 'Forward P/E':value_list[11],
									 'PEG Ratio':value_list[12],
									 'Enterprise Value/Revenue':value_list[13],
									 'Enterprise Value/EBITDA':value_list[14],
									 'Revenue':value_list[15],
									 'Gross Profit':value_list[16],
									 'EBITDA':value_list[17],
									 'Net Income Avl to Common ':value_list[18],
									 'Diluted EPS':value_list[19],
									 'Earnings Growth':value_list[20],
									 'Revenue Growth':value_list[21],
									 'Total Cash':value_list[22],
									 'Total Cash Per Share':value_list[23],
									 'Total Debt':value_list[24],
									 'Current Ratio':value_list[25],
									 'Book Value Per Share':value_list[26],
									 #'Cash Flow':value_list[27],
									 'Beta':value_list[27],
									 'Held by Insiders':value_list[28],
									 'Held by Institutions':value_list[29],
									 'Shares Short (as of':value_list[30],
									 'Short Ratio':value_list[31],
									 'Short % of Float':value_list[32],
									 'Shares Short (prior ':value_list[33],
									'Status':status},
								   ignore_index=True)
							#print(df)

						except Exception as e:
							print(str(e), "df_entry")
							time.sleep(15)	
								
			
				except Exception as e:
					pass
					#print("Ist try box")
					#print(str(e), file, ticker)


	# finally saves all the relevant data to a csv file				
	df.to_csv('TotalDebtEquity.csv')
				
Key_Stats()




