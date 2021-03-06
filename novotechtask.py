# -*- coding: utf-8 -*-
"""novotechtask.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PruvjjoFczRSWRUvXe4eM6BE2qEiEG9j
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')



#from google.colab import files
#uploaded = files.upload()

df=pd.read_csv('C:\\Users\\Bhor\\Downloads\\Stock_data\\stock30\\3IINFOTECH.csv')
df

df=df.set_index(pd.DatetimeIndex(df['Date'].values))

df

plt.figure(figsize=(12.2,4.5))
plt.title('Close price',fontsize=18)
plt.plot(df['Close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price',fontsize=18)
plt.show()

#Calculate short exponential moving average
ShortEMA = df.Close.ewm(span=5, adjust=False).mean()
#Calculate Middle/Medium exponential moving average
MiddleEMA = df.Close.ewm(span=21, adjust=False).mean()
#Calculate long/slow exponential moving average
LongEMA = df.Close.ewm(span=63,adjust= False).mean()

"""Visualize the closing price and the exponential moving averages """

plt.figure(figsize=(12.2,4.5))
plt.title('Close price',fontsize=18)
plt.plot(df['Close'], label= 'Close Price', color = 'blue')
plt.plot(ShortEMA, label = 'Short/Fast EMA', color ='red')
plt.plot(MiddleEMA, label='Middle/Medium EMA',color='orange')
plt.plot(LongEMA, label= 'Long/Slow EMA',color='green')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price',fontsize=18)
plt.show()

#Add exponential moving averages to the data set
df['Short'] = ShortEMA
df['Middle'] = MiddleEMA
df['Long'] = LongEMA

#show the data
df

#Create a function to buy and sell the stock (The trading strategy)
def buy_sell_function(data):
  buy_list = []
  sell_list = []
  flag_long = False
  flag_short = False
  
  for i in range(0,len(data)):
    if data['Middle'][i] < data['Long'][i] and data['Middle'][i] > data['Short'][i] and flag_long == False and flag_short == False:
      buy_list.append(data['Close'][i])
      sell_list.append(np.nan)
      flag_short = True
    elif data['Middle'][i] > data['Long'][i] and data['Middle'][i] < data['Short'][i] and flag_short == False and flag_long == False:
      buy_list.append(data['Close'][i])
      sell_list.append(np.nan)
      flag_long = True
    elif flag_short == True and data['Short'][i] > data['Middle'][i]:
      sell_list.append(data['Close'][i])
      buy_list.append(np.nan)
      flag_short = False
    elif flag_long == True and data['Short'][i] < data['Middle'][i]:
      sell_list.append(data['Close'][i])
      buy_list.append(np.nan)
      flag_long = False
    else:
      buy_list.append(np.nan)
      sell_list.append(np.nan)
  return(buy_list, sell_list)

#Add buy and send signals to the data set
df['Buy'] = buy_sell_function(df)[0]
df['Sell'] =buy_sell_function(df)[1]

plt.figure(figsize=(12.2,4.5))
plt.title('Close price',fontsize=18)
plt.plot(df['Close'], label= 'Close Price', color = 'blue',alpha=0.35)
plt.plot(ShortEMA, label = 'Short/Fast EMA', color ='red',alpha=0.35)
plt.plot(MiddleEMA, label='Middle/Medium EMA',color='orange',alpha=0.35)
plt.plot(LongEMA, label= 'Long/Slow EMA',color='green',alpha=0.35)
plt.scatter(df.index, df['Buy'],color='green',marker='^',alpha=1)
plt.scatter(df.index, df['Sell'],color='red',marker='v',alpha=1)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price',fontsize=18)
plt.show()

df=pd.read_csv('C:\\Users\\Bhor\\Downloads\\Stock_data\\stock30\\3IINFOTECH.csv').loc[: ,['Date','Close']]
rsi_period = 14
chg = df['Close'].diff(1)
gain = chg.mask(chg<0,0)
df['gain'] = gain
loss = chg.mask(chg>0,0)
df['loss']=loss
avg_gain = gain.ewm(com = rsi_period-1,min_periods=rsi_period).mean()
avg_loss = loss.ewm(com = rsi_period-1,min_periods=rsi_period).mean()
df['avg_gain'] = avg_gain
df['avg_loss'] = avg_loss
rs = abs(avg_gain/avg_loss)
rsi = 100 - (100/(1+rs))
df['rsi'] = rsi
print(df.head())
print(df.tail())
fig = plt.figure()
df=df.set_index(pd.DatetimeIndex(df['Date'].values))
#graphing period
start_day = '2019-05-29'
end_day='2020-05-29'
period =(df.index>=start_day)&(df.index<=end_day)
plt.subplot(211)
plt.title(f'rsi from {start_day} to {end_day}')
plt.ylabel('rsi',rotation=0)
graph_rsi =df.loc[period,'rsi'].resample('D').mean().plot()
plt.subplot(212)
plt.title(f'dji from {start_day} to {end_day}')
plt.ylabel('dji',rotation=0)
graph_rsi = df.loc[period,'Close'].resample('D').mean().plot()
plt.show()