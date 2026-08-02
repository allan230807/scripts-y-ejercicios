import os
import json
import requests
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from dotenv import load_dotenv
from google import genai

load_dotenv()   
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_tickers():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df = df[df['symbol'].str.endswith('USDT')]
    df['priceChangePercent'] = df['priceChangePercent'].astype(float)
    df['lastPrice'] = df['lastPrice'].astype(float)
    gainers = df.nlargest(15, 'priceChangePercent')[['symbol', 'priceChangePercent', 'lastPrice']]
    losers = df.nsmallest(15, 'priceChangePercent')[['symbol', 'priceChangePercent', 'lastPrice']]
    return gainers, losers

def get_order_book(symbol):
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=50"
    ob = requests.get(url).json()
    bids = sum([float(x[1]) for x in ob.get('bids', [])])
    asks = sum([float(x[1]) for x in ob.get('asks', [])])
    return bids, asks

def get_klines(symbol, limit=500):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit={limit}"
    data = requests.get(url).json()
    close = np.array([float(x[4]) for x in data])
    return close

def analyze_market_with_gemini():
    gainers, losers = get_tickers()
    market_data = {"gainers": gainers.to_dict('records'), "losers": losers.to_dict('records')}
    for item in market_data["gainers"] + market_data["losers"]:
        symbol = item["symbol"]
        prices = get_klines(symbol, 100)
        mean_p = np.mean(prices)
        std_p = np.std(prices)
        item["z_score"] = (item["lastPrice"] - mean_p) / std_p if std_p > 0 else 0
        item["bids_vol"], item["asks_vol"] = get_order_book(symbol)
    
    prompt = f"Filtra y ordena esta lista de tokens colocando primero aquellos con un Z-score mayor a 3 o menor a -3 (desviaciones estándar), indicando si están sobrecomprados o sobrevendidos basándote en el Z-score y el desbalance del order book (bids_vol vs asks_vol). Devuelve solo la lista estructurada.\n\nDatos:\n{json.dumps(market_data)}"
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    print(response.text)

def calculate_hurst(ts):
    lags = range(2, 20)
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2.0

def ou_process(ts):
    ts_shift = ts[:-1]
    ts_current = ts[1:]
    X = sm.add_constant(ts_shift)
    model = sm.OLS(ts_current, X).fit()
    theta = -np.log(model.params[1])
    mu = model.params[0] / (1 - model.params[1])
    sigma = np.std(model.resid) * np.sqrt(-2 * np.log(model.params[1]) / (1 - model.params[1]**2))
    return theta, mu, sigma

def run_montecarlo(S0, mu, sigma, days=30, sims=5000):
    dt = 1
    paths = np.zeros((sims, days))
    paths[:, 0] = S0
    for t in range(1, days):
        Z = np.random.standard_normal(sims)
        paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    return paths

def run_deep_analysis(symbol):
    prices = get_klines(symbol, 1000)
    btc_prices = get_klines("BTCUSDT", 1000)
    
    min_len = min(len(prices), len(btc_prices))
    prices = prices[-min_len:]
    btc_prices = btc_prices[-min_len:]
    
    score, pvalue, _ = coint(prices, btc_prices)
    hurst_exp = calculate_hurst(prices)
    theta, mu, sigma = ou_process(prices)
    
    bids, asks = get_order_book(symbol)
    imbalance = bids / (bids + asks) if (bids + asks) > 0 else 0
    
    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns)
    regime = "High Volatility (Breakdown Risk)" if volatility > np.percentile(returns, 90) else "Stable"
    
    mc_paths = run_montecarlo(prices[-1], np.mean(returns), volatility, days=30, sims=5000)
    mc_mean_end = np.mean(mc_paths[:, -1])
    
    stats_report = {
        "symbol": symbol,
        "cointegration_vs_BTC_pvalue": pvalue,
        "hurst_exponent": hurst_exp,
        "ou_theta_reversion_speed": theta,
        "ou_mu_long_term_mean": mu,
        "microstructure_bid_ask_imbalance": imbalance,
        "regime": regime,
        "montecarlo_expected_price": mc_mean_end,
        "current_price": prices[-1]
    }
    
    prompt = f"Analiza estos resultados estadísticos cuantitativos para el token {symbol}. Evalúa la cointegración (p-value), la velocidad de reversión (Hurst y theta del proceso OU), ineficiencias de microestructura (imbalance del order book), el régimen de volatilidad y el precio esperado tras un Montecarlo de 5000 iteraciones. Determina, paso a paso, si es estadísticamente probable un movimiento de reversión a la media.\n\nDatos:\n{json.dumps(stats_report)}"
    
    response = client.models.generate_content(model="gemini-2.5-pro", contents=prompt)
    print("\n--- ANÁLISIS ESTADÍSTICO FINAL ---")
    print(response.text)

if __name__ == "__main__":
    analyze_market_with_gemini()
    seleccion = input("\nIngresa el símbolo del token a analizar profundamente (ej. BTCUSDT): ").strip().upper()
    run_deep_analysis(seleccion)