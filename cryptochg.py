import tweepy as tp
import time
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import table

url = 'https://api.coinmarketcap.com/v1/ticker/'
data = requests.get(url).json()

# create directory for dataframe image
if not os.path.exists('df_image'):
    os.makedirs('df_image')

# move to new directory
os.chdir('df_image')


def top_increase():
    ordered_data = sorted(data, key=lambda k:
    (float(k['percent_change_24h']), (k['percent_change_7d'])), reverse=True)[:5]
    raw_data_increase = {}

    for currency in ordered_data:
        rank = currency['rank']
        name = currency['name']
        percent_change_24h = currency['percent_change_24h']
        percent_change_7d = currency['percent_change_7d']
        price_usd = float(currency['price_usd'])
        price_usd = f'{price_usd:.2f}'

        raw_data_increase.setdefault('Rank', [])
        raw_data_increase['Rank'].append(rank)
        raw_data_increase.setdefault('Name', [])
        raw_data_increase['Name'].append(name)
        raw_data_increase.setdefault('Change last 24h (%)', [])
        raw_data_increase['Change last 24h (%)'].append(percent_change_24h)
        raw_data_increase.setdefault('Change last 7d (%)', [])
        raw_data_increase['Change last 7d (%)'].append(percent_change_7d)
        raw_data_increase.setdefault('Price(USD)', [])
        raw_data_increase['Price(USD)'].append(price_usd)
        # print(raw_data)

    df = pd.DataFrame(raw_data_increase, columns=['Rank', 'Name', 'Change last 24h (%)', 'Change last 7d (%)', 'Price(USD)'])

    # print(df.to_string(index=False))

    # set fig size
    fig, ax = plt.subplots(figsize=(9.5, 2.7))
    # no axes
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    # no frame
    ax.set_frame_on(False)
    # plot table
    tab = table(ax, df, rowLabels=['']*df.shape[0], loc='center')
    # set font manually
    tab.auto_set_font_size(False)
    tab.set_fontsize(10)
    # set scale
    tab.scale(1, 2.5)
    # save the result
    plt.savefig('cryptopinc.png')


top_increase()

# credentials to login to twitter api
consumer_key = 'BOT_CONSUMER_KEY'
consumer_secret = 'BOT_CONSUMER_SECRET'
access_token = 'BOT_ACCESS_TOKEN'
access_secret = 'BOT_ACCESS_SECRET'

# login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)


while True:
    for df_image in os.listdir('.'):
        api.update_with_media(df_image, status='Here are the top 5 coins that got their '
                                               'value increased the most in the last '
                                               '24 hours. #Cryptocurrency #Crypto')

        time.sleep(10800)





