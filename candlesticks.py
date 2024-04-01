import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# start_date = '2023-01-01'
# end_date = '2023-12-31'
# stock = 'PETR4.SA'
stock = input("Enter the stock symbol (e.g., PETR4.SA): ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

df_stock = yf.download(stock, start=start_date, end=end_date)
print(df_stock)

df_stock['Close'].plot(figsize=(11,6))
plt.title('Price ' + stock)
plt.legend("Close")
plt.savefig(stock + '_' + start_date + '_' + end_date + '_lines.png')

df = df_stock.copy()
df['Dates'] = df.index
df['Dates'] = df['Dates'].apply(mdates.date2num)
print(df)

# make an candlestick by hand
fig, ax = plt.subplots(figsize=(40,8))
width = 0.7

for i in range(len(df)):
  if df['Close'].iloc[i] > df['Open'].iloc[i]:
      color = 'green'
  else:
      color = 'red'
  ax.plot([df['Dates'].iloc[i], df['Dates'].iloc[i]],
          [df['Low'].iloc[i], df['High'].iloc[i]],
          color=color,
          linewidth=1)
  ax.add_patch(plt.Rectangle((df['Dates'].iloc[i] - width/2.1, min(df['Open'].iloc[i], df['Close'].iloc[i])),
                             width,
                             abs(df['Close'].iloc[i] - df['Open'].iloc[i]),
                             facecolor=color))

df['ma7'] = df['Close'].rolling(window=7).mean()
df['ma21'] = df['Close'].rolling(window=21).mean()

ax.plot(df['Dates'], df['ma7'], color='gray', label='Median 7 Days')
ax.plot(df['Dates'], df['ma21'], color='purple', label='Median 21 Days')

ax.legend()

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

plt.title('Candlestick Graph '+ stock)
plt.xlabel('Date')
plt.ylabel('Price')

plt.grid(1)

plt.show()

# easyer way using plotly.graph_objects
fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=("Candlestick Chart"), vertical_spacing=0.3)

fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             name='Candlestick'),
              row=1,
              col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=df['ma7'],
                         mode='lines',
                         name='Median 7 Days'),
              row=1,
              col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=df['ma21'],
                         mode='lines',
                         name='Median 21 Days'),
              row=1,
              col=1)

fig.show()

# an easyest way using the API
mpf.plot(df_stock,
         type='candle',
         figsize=(40,8),
         volume=True,
         mav=(7,21),
         style='yahoo',
         tight_layout=True,
         savefig=stock + '_' + start_date + '_' + end_date + '_CS.png')