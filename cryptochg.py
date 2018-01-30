import tweepy as tp
import time
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import table

url = 'http://coincap.io/front'
data = requests.get(url).json()

if not os.path.exists('df_image'):
    os.makedirs('df_image')

os.chdir('df_image')


def top_increase():
    top100_data = sorted(data, key=lambda k: (float(k['mktcap'])), reverse=True)[:100]
    ordered_data = sorted(top100_data, key=lambda k: (float(k['cap24hrChange'])), reverse=True)[:5]
    raw_data_increase = {}

    for currency in ordered_data:
        name = currency['long']
        market_cap = float(currency['mktcap'])
        market_cap_rounded = f'{market_cap:,.2f}'
        percent_change_24 = currency['cap24hrChange']
        price = float(currency['price'])
        price_rounded = f'{price:.2f}'

        raw_data_increase.setdefault('Name', [])
        raw_data_increase['Name'].append(name)
        raw_data_increase.setdefault('Market Cap(USD)', [])
        raw_data_increase['Market Cap(USD)'].append(market_cap_rounded)
        raw_data_increase.setdefault('%24hr', [])
        raw_data_increase['%24hr'].append(percent_change_24)
        raw_data_increase.setdefault('Price(USD)', [])
        raw_data_increase['Price(USD)'].append(price_rounded)
        

    df = pd.DataFrame(raw_data_increase, columns=['Name', 'Market Cap(USD)', '%24hr', 'Price(USD)'])

    print(df.to_string(index=False))

    # set fig size
    fig, ax = plt.subplots(figsize=(6.8, 2))
    # no axes
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    # no frame
    ax.set_frame_on(False)
    # plot table
    tab = table(ax, df, rowLabels=['']*df.shape[0], loc='center')
    # set font manually
    tab.auto_set_font_size(False)
    tab.set_fontsize(8.8)
    # set scale
    tab.scale(1, 1.8)
    # save the result
    plt.savefig('cryptopinc.png')


top_increase()

consumer_key = 'BOT_CONSUMER_KEY'
consumer_secret = 'BOT_CONSUMER_SECRET'
access_token = 'BOT_ACCESS_TOKEN'
access_secret = 'BOT_ACCESS_SECRET'

# login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)


while True:
    for image in os.listdir('.'):
        api.update_with_media(image, status='Here are the top 5 coins that got their '
                                            'value increased the most during the '
                                            'last 24 hours. #Cryptocurrency #Crypto #Altcoins')

        time.sleep(43200)





