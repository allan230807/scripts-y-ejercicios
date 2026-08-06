import os
import time
import json
import requests
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No se encontró la GEMINI_API_KEY. Configúrala en tu entorno o archivo .env")

client = genai.Client(api_key=api_key)

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

def get_klines(symbol, limit=500):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit={limit}"
    data = requests.get(url).json()
    
    opens = np.array([float(x[1]) for x in data])
    closes = np.array([float(x[4]) for x in data])
    volumes = np.array([float(x[5]) for x in data]) 
    return opens, closes, volumes

def get_order_book_or_proxy(symbol, opens, closes, volumes):
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=50"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            ob = response.json()
            bids = sum([float(x[1]) for x in ob.get('bids', [])])
            asks = sum([float(x[1]) for x in ob.get('asks', [])])
            if bids > 0 or asks > 0:
                return bids, asks
    except Exception:
        pass
    
    # Proxy de microestructura si el Order Book no responde
    recent_opens = opens[-20:]
    recent_closes = closes[-20:]
    recent_volumes = volumes[-20:]
    
    green_mask = recent_closes >= recent_opens
    red_mask = recent_closes < recent_opens
    
    simulated_bids = np.sum(recent_volumes[green_mask])
    simulated_asks = np.sum(recent_volumes[red_mask])
    
    return simulated_bids, simulated_asks

def analyze_market_with_gemini():
    print("Escaneando el mercado (esto tomará unos segundos para evitar límites de API)...")
    gainers, losers = get_tickers()
    market_data = {"gainers": gainers.to_dict('records'), "losers": losers.to_dict('records')}
    
    for item in market_data["gainers"] + market_data["losers"]:
        symbol = item["symbol"]
        opens, closes, volumes = get_klines(symbol, 100)
        
        mean_p = np.mean(closes)
        std_p = np.std(closes)
        item["z_score"] = (item["lastPrice"] - mean_p) / std_p if std_p > 0 else 0
        
        item["bids_vol"], item["asks_vol"] = get_order_book_or_proxy(symbol, opens, closes, volumes)
        time.sleep(0.15) # Prevención de baneo por Rate Limits de Binance
    
    prompt = f"Filtra y ordena esta lista de tokens colocando primero aquellos con un Z-score mayor a 3 o menor a -3, indicando si están sobrecomprados o sobrevendidos basándote en el Z-score y el desbalance del order book (bids_vol vs asks_vol). Devuelve solo la lista estructurada.\n\nDatos:\n{json.dumps(market_data)}"
    
    response = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
    print(response.text)

def calculate_hurst(ts):
    lags = range(2, 20)
    tau = [np.std(ts[lag:] - ts[:-lag]) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] 

def ou_process(ts):
    ts_shift = ts[:-1]
    ts_current = ts[1:]
    X = sm.add_constant(ts_shift)
    model = sm.OLS(ts_current, X).fit()
    
    if model.params[1] >= 1 or model.params[1] <= 0:
         return 0.0, np.mean(ts), np.std(ts)

    theta = -np.log(model.params[1])
    mu = model.params[0] / (1 - model.params[1])
    sigma = np.std(model.resid) * np.sqrt(-2 * np.log(model.params[1]) / (1 - model.params[1]**2))
    return theta, mu, sigma

def run_montecarlo(S0, mu, sigma, steps=30, sims=5000):
    dt = 1 
    paths = np.zeros((sims, steps))
    paths[:, 0] = S0
    for t in range(1, steps):
        Z = np.random.standard_normal(sims)
        paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    return paths

def run_deep_analysis(symbol):
    print(f"\nExtrayendo datos y calculando métricas cuantitativas para {symbol}...")
    opens, prices, volumes = get_klines(symbol, 1000)
    _, btc_prices, _ = get_klines("BTCUSDT", 1000)
    
    min_len = min(len(prices), len(btc_prices))
    prices = prices[-min_len:]
    btc_prices = btc_prices[-min_len:]
    
    # NUEVO: Modelado sobre el Spread relativo a BTC
    spread = prices / btc_prices
    
    _, pvalue, _ = coint(prices, btc_prices)
    hurst_exp = calculate_hurst(spread)
    theta, mu, sigma = ou_process(spread)
    
    bids, asks = get_order_book_or_proxy(symbol, opens, prices, volumes)
    imbalance = bids / (bids + asks) if (bids + asks) > 0 else 0
    
    # CORRECCIÓN: Retornos Logarítmicos
    log_returns = np.log(prices[1:] / prices[:-1])
    rolling_vol = pd.Series(log_returns).rolling(window=24).std().dropna()
    current_vol = rolling_vol.iloc[-1]
    hist_90th_vol = np.percentile(rolling_vol, 90)
    regime = "High Volatility (Breakdown Risk)" if current_vol > hist_90th_vol else "Stable"
    
    # Montecarlo sigue usando el precio nominal para simular riesgo direccional
    mc_paths = run_montecarlo(prices[-1], np.mean(log_returns), current_vol, steps=72, sims=5000)
    mc_mean_end = np.mean(mc_paths[:, -1])
    
    stats_report = {
        "symbol": symbol,
        "cointegration_vs_BTC_pvalue": pvalue,
        "spread_hurst_exponent": hurst_exp,
        "spread_ou_theta_reversion": theta,
        "spread_ou_mu_target": mu,
        "current_spread": spread[-1],
        "microstructure_bid_ask_imbalance": imbalance,
        "current_hourly_vol": current_vol,
        "volatility_regime": regime,
        "montecarlo_expected_price_72h": mc_mean_end,
        "current_price": prices[-1]
    }
    
    prompt = f"Actúa como un analista cuantitativo. Analiza estos resultados estadísticos para {symbol}. \n1. Evalúa la cointegración con BTC (p-value).\n2. Analiza el comportamiento del SPREAD ({symbol}/BTC) usando el Exponente de Hurst y la velocidad de reversión Theta (modelo OU) respecto a su media objetivo (mu). Determina si el spread está estirado.\n3. Evalúa la presión en el order book (imbalance) y el régimen de volatilidad direccional.\n4. Cruza el riesgo direccional del Montecarlo (a 72h) con el modelo de reversión del spread para dar una conclusión estadística final.\n\nDatos:\n{json.dumps(stats_report)}"
    
    response = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
    print("\n--- ANÁLISIS ESTADÍSTICO FINAL ---")
    print(response.text)

if __name__ == "__main__":
    analyze_market_with_gemini()
    seleccion = input("\nIngresa el símbolo del token a analizar profundamente (ej. BTCUSDT): ").strip().upper()
    run_deep_analysis(seleccion)