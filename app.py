from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

portfolio = {
    "BTC": 0.5,
    "ETH": 2,
    "DOGE": 1000
}

def get_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get(symbol, {}).get("usd", None)
    except Exception:
        return None

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    result = []
    for coin, amount in portfolio.items():
        price = get_price(coin.lower())
        if price:
            result.append({
                "coin": coin,
                "amount": amount,
                "price_usd": price,
                "value_usd": round(price * amount, 2)
            })
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

