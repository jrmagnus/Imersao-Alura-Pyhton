import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet

start_date = '2020-01-01'
end_date = '2023-12-31'
stock = 'JNJ'
# stock = input("Enter the stock symbol (e.g., PETR4.SA, JNJ): ")
# start_date = input("Enter the start date (YYYY-MM-DD): ")
# end_date = input("Enter the end date (YYYY-MM-DD): ")

df_stock = yf.download(stock, start=start_date, end=end_date)
df_stock = df_stock.reset_index()

data_traine = df_stock[df_stock['Date'] < '2023-07-31']
data_test = df_stock[df_stock['Date'] >= '2023-07-31']

data_prophet_traine = data_traine[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

model = Prophet(weekly_seasonality=True,
        yearly_seasonality=True,
        daily_seasonality=False)

model.add_country_holidays(country_name='US')

model.fit(data_prophet_traine)

future = model.make_future_dataframe(periods=150)
predict = model.predict(future)

plt.figure(figsize=(14, 8))
plt.plot(data_traine['Date'], data_traine['Close'], label='Trainig Data', color='blue')
plt.plot(data_test['Date'], data_test['Close'], label='Real Data (Test)', color='green')
plt.plot(predict['ds'], predict['yhat'], label='Predict', color='orange', linestyle='--')

plt.axvline(data_traine['Date'].max(), color='red', linestyle='--', label='Predict Start')
plt.xlabel('Date')
plt.ylabel('Close')
plt.title('Predict, Close Price x Real Data')
plt.legend()
plt.show()