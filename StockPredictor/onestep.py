import pandas as pd
import os
import urllib
import json
import datetime as dt
import matplotlib.pyplot as plt
import sklearn.preprocessing as sp
import numpy as np

data_source = 'kaggle' # alphavantage or kaggle
name = input("Enter the company name : ")
if data_source == 'alphavantage':
    # ====================== Loading Data from Alpha Vantage ==================================

    api_key = 'JOV7WPU358OY49HM'
    # American Airlines stock market prices
    ticker = "AAL"

    # JSON file with all the stock market data for AAL from the last 20 years
    url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)

    # Save data to this file
    file_to_save = 'stock_market_data-%s.csv'%ticker

    # If you haven't already saved data,
    # Go ahead and grab the data from the url
    # And store date, low, high, volume, close, open values to a Pandas DataFrame
    if not os.path.exists(file_to_save):
        with urllib.request.urlopen(url_string) as url:
            data = json.loads(url.read().decode())
            # extract stock market data
            data = data['Time Series (Daily)']
            df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
            for k,v in data.items():
                date = dt.datetime.strptime(k, '%Y-%m-%d')
                data_row = [date.date(),float(v['3. low']),float(v['2. high']),
                            float(v['4. close']),float(v['1. open'])]
                df.loc[-1,:] = data_row
                df.index = df.index + 1
        print('Data saved to : %s'%file_to_save)
        df.to_csv(file_to_save)

    # If the data is already there, just load it from the CSV
    else:
        print('File already exists. Loading data from CSV')
        df = pd.read_csv(file_to_save)

else:

    # ====================== Loading Data from Kaggle ==================================
    # You will be using HP's data. Feel free to experiment with other data.
    # But while doing so, be careful to have a large enough dataset and also pay attention to the data normalization
    name = name + '.us.txt'
    df = pd.read_csv(os.path.join('Data\\Stocks',name),delimiter=',',usecols=['Date','Open','High','Low','Close'])
    print('Loaded data from the Kaggle repository')

df = df.sort_values('Date')
df.head()

'''plt.figure(figsize = (18,9))
plt.plot(range(df.shape[0]),(df['Low']+df['High'])/2.0)
plt.xticks(range(0,df.shape[0],500),df['Date'].loc[::500],rotation=45)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Mid Price',fontsize=18)
plt.show()'''

high_prices = df.loc[:,'High'].values
low_prices = df.loc[:,'Low'].values
mid_prices = (high_prices+low_prices)/2.0

'''train_data = mid_prices[:11000]
test_data = mid_prices[11000:]'''

scaler = sp.MinMaxScaler()
'''train_data = train_data.reshape(-1,1)
test_data = test_data.reshape(-1,1)'''
mid_prices = mid_prices.reshape(-1,1)
scaler.fit(mid_prices)
mid_prices = scaler.transform(mid_prices)

'''smoothing_window_size = 2500
for di in range(0,10000,smoothing_window_size):
    scaler.fit(mid_prices[di:di+smoothing_window_size,:])
    mid_prices[di:di+smoothing_window_size,:] = scaler.transform(mid_prices[di:di+smoothing_window_size,:])

# You normalize the last bit of remaining data
scaler.fit(mid_prices[di+smoothing_window_size:,:])
mid_prices[di+smoothing_window_size:,:] = scaler.transform(mid_prices[di+smoothing_window_size:,:])'''

# Reshape both train and test data
mid_prices = mid_prices.reshape(-1)

# Normalize test data
#test_data = scaler.transform(test_data).reshape(-1)
#train_data = train_data.reshape(-1)
# Now perform exponential moving average smoothing
# So the data will have a smoother curve than the original ragged data

EMA = 0.0
gamma = 0.1
for ti in range(mid_prices.size):
  EMA = gamma*mid_prices[ti] + (1-gamma)*EMA
  mid_prices[ti] = EMA

# Used for visualization and test purposes
#all_mid_data = np.concatenate([train_data,test_data],axis=0)


predict_date = input("Enter date for prediction (YYYY-MM-DD) :")
date_list = pd.Index(df.loc[:,'Date'])
N = date_list.get_loc(predict_date)

window_size = 100
#N = train_data.size

run_avg_predictions = []
run_avg_x = []

mse_errors = []

running_mean = 0.0
run_avg_predictions.append(running_mean)

decay = 0.5

for pred_idx in range(1,N+1):

    '''if pred_idx >= N:
        date = dt.datetime.strptime(k, '%Y-%m-%d').date() + dt.timedelta(days=1)
    else:
        date = df.loc[pred_idx,'Date']'''


    running_mean = running_mean*decay + (1.0-decay)*mid_prices[pred_idx-1]
    run_avg_predictions.append(running_mean)
    mse_errors.append((run_avg_predictions[-1]-mid_prices[pred_idx])**2)
    #run_avg_x.append(date)

predict_x = run_avg_predictions[-1]
actual_x = mid_prices[N].reshape(1,1)

predict_x = scaler.inverse_transform(predict_x.reshape(1,1))
actual_x = scaler.inverse_transform(actual_x)
print("Predicted value : ", predict_x[0][0])
print("Actual value : ", actual_x[0][0])