import pandas as pd
import datetime
from pycoingecko import CoinGeckoAPI
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def candlestick_chart():
    # Get Bitcoin price data from CoinGecko
    cg = CoinGeckoAPI()
    bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='cad', days=30)
    bitcoin_price_data = bitcoin_data['prices']
    data = pd.DataFrame(bitcoin_price_data, columns=['TimeStamp', 'Price'])

    # Convert timestamp to date
    data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))

    # Group data by date and calculate candlestick values
    candlestick_data = data.groupby(data.date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})

    # Create Plotly candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                    open=candlestick_data['Price']['first'],
                    high=candlestick_data['Price']['max'],
                    low=candlestick_data['Price']['min'],
                    close=candlestick_data['Price']['last'])
                    ])
    fig.update_layout(xaxis_rangeslider_visible=True)

    # Convert Plotly chart to JSON and return
    return jsonify(fig.to_json())

if __name__ == '__main__':
    app.run()
