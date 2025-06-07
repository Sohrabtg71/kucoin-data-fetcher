import requests
import pandas as pd
import time

def get_top_symbols():
    return [
        'BTC-USDT', 'ETH-USDT', 'BNB-USDT', 'ADA-USDT', 'XRP-USDT',
        'DOGE-USDT', 'DOT-USDT', 'UNI-USDT', 'LTC-USDT', 'LINK-USDT',
        'BCH-USDT', 'SOL-USDT', 'MATIC-USDT', 'XLM-USDT', 'ATOM-USDT',
        'FIL-USDT', 'TRX-USDT', 'ETC-USDT', 'EOS-USDT', 'AAVE-USDT',
        'NEO-USDT', 'XTZ-USDT', 'ALGO-USDT', 'VET-USDT', 'THETA-USDT',
        'KSM-USDT', 'EGLD-USDT', 'DASH-USDT', 'ZEC-USDT', 'SNX-USDT',
        'COMP-USDT', 'YFI-USDT', 'SUSHI-USDT', 'AVAX-USDT', 'FTM-USDT',
        'GRT-USDT', 'CRV-USDT', 'ENJ-USDT', 'CHZ-USDT', 'BAT-USDT',
        'MANA-USDT', 'REN-USDT', 'ZIL-USDT', '1INCH-USDT', 'OMG-USDT',
        'BNT-USDT', 'CEL-USDT', 'ANKR-USDT', 'RUNE-USDT', 'SKL-USDT'
    ]

def fetch_candles(symbol, interval='1hour', limit=50):
    url = 'https://api.kucoin.com/api/v1/market/candles'
    params = {
        'symbol': symbol,
        'type': interval
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            response_json = response.json()
            if 'data' not in response_json:
                print(f"❌ پاسخ نامعتبر برای {symbol}: {response_json}")
                return None

            data = response_json['data']
            if not data:
                print(f"ℹ️ دیتای خالی برای {symbol}")
                return None

            df = pd.DataFrame(data, columns=[
                'time', 'open', 'close', 'high', 'low', 'volume', 'turnover'
            ])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        else:
            try:
                response_json = response.json()
                print(f"❌ خطا برای {symbol}: {response_json}")
            except:
                print(f"❌ خطا در دریافت JSON برای {symbol}")
            return None
    except Exception as e:
        print(f"⚠️ استثنا در دریافت داده برای {symbol}: {e}")
        return None

def main():
    symbols = get_top_symbols()
    for symbol in symbols:
        df = fetch_candles(symbol)
        if df is not None:
            filename = f"{symbol.replace('-', '_')}_candles.csv"
            df.to_csv(filename, index=False)
            print(f"✅ داده‌های {symbol} ذخیره شد.")
        time.sleep(1)  # جلوگیری از بلاک شدن توسط KuCoin API

if name == "main":
    main()
