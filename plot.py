# -*- coding: utf-8 -*-
"""plot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZwmITSjDRVwJoQVHQp84GFhmeCi1jGoj
"""

#importing libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px



df=pd.DataFrame(pd.read_csv("C:\\Users\\Bhor\\Downloads\\Stock_data\\stock30\\ABMINTLTD.csv"))
for i in ['open','high','low','close','volume']:
  df[i] = df[i].astype('float64')

set1 = {
    'x':  df.date,
    'open':df.open,
    'close':df.close,
    'high':df.high,
    'low':df.low,
    'type': 'candlestick',
}

# finding the moving average of 20 periods
avg_20 = df.close.rolling(window=20,min_periods=1).mean()
# finding the moving average of 50 periods
avg_50 = df.close.rolling(window=50,min_periods=1).mean()
# finding the moving average of 200 periods
avg_200 = df.close.rolling(window=200,min_periods=1).mean()

set2 = {
    'x':  df.date,
    'y':avg_20,
    'type':'scatter',
    'mode':'lines',
    'line': {
        'width': 1,
        'color': 'blue',
    },
    'name': 'Moving average of 20 periods'
}

set3 = {
    'x':  df.date,
    'y':avg_50,
    'type':'scatter',
    'mode':'lines',
    'line': {
        'width': 1,
        'color': 'yellow',
    },
    'name': 'Moving average of 50 periods'
}

set4 = {
    'x':  df.date,
    'y':avg_200,
    'type':'scatter',
    'mode':'lines',
    'line': {
        'width': 1,
        'color': 'black',
    },
    'name': 'Moving average of 200 periods'
}

data = [set1,set2,set3,set4]
# config graph layout
layout = go.Layout({
    'title':{
        'text': 'ABMINTLTD 2019-20',
        'font': {
            'size': 25
        }
    }
})

fig = go.Figure(data=data, layout=layout)
fig.show()