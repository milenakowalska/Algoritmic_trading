import matplotlib.pyplot as plt
import pandas as pd
import os

facebook_data = os.path.join(os.path.dirname(__file__), 'FB.csv')
df = pd.read_csv(facebook_data)

data = pd.DataFrame()
data['Adj Close'] = df['Adj Close']
data['moving_avg_50'] = df['Adj Close'].rolling(window=50).mean()
data['moving_avg_200'] = df['Adj Close'].rolling(window=200).mean()

plt.style.use('seaborn')
plt.plot(data['Adj Close'], label='Facebook', alpha = 0.4)
plt.plot(data['moving_avg_50'], label='50-day moving avg.', alpha = 0.4)
plt.plot(data['moving_avg_200'], label='200-day moving avg.', alpha = 0.4)


# Buy when  50-day moving avg. goes above the 200-day moving avg.
# Sell when  50-day moving avg. goes below the 200-day moving avg.


def golden_cross(data):
    avg_50 = data['moving_avg_50']
    avg_200 = data['moving_avg_200'] 
    prices = data['Adj Close']
    indicator = 0

    sell = []
    buy = []

    for value in range(len(data)):
        if avg_50[value] > avg_200[value]:
            if indicator != 1:
                buy.append(prices[value])
                sell.append(None)
                indicator = 1
            else:
                buy.append(None)
                sell.append(None)
        elif avg_50[value] < avg_200[value]:
            if indicator != 2:
                buy.append(None)
                sell.append(prices[value])
                indicator = 2
            else:
                buy.append(None)
                sell.append(None)
        else:
            buy.append(None)
            sell.append(None)
    
    return (sell, buy)

sell_values, buy_values = golden_cross(data)

data['sell_indicator'] = sell_values
data['buy_indicator'] = buy_values

plt.plot(sell_values, color='red', marker = 'v', label='Sell')
plt.plot(buy_values, color='green', marker = '^', label='Buy')

plt.title('Facebook Golden Crosses')
plt.ylabel('Price in USD')
plt.xlabel('2006-01-01 - 2020-07-26')
plt.legend()
plt.show()

