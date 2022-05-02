from datetime import datetime
from pycoingecko import CoinGeckoAPI
import pandas as pd
import datetime



def coingeko_api_data(name = 'bitcoin', curr = 'usd', days = '90'):
    
    """
        funkcja laczy sie z api, pobiera dane i zapisuje do df
        
        parametry funkcji -> 
        name: nazwa kryptowaluty 
        curr: waluta
        days: x ostatnich dni

    """
        
    #Laczenie z API
    cg = CoinGeckoAPI()
    
    data = cg.get_coin_market_chart_by_id(id=name,vs_currency=curr,days=days)
    
    df_0 = pd.DataFrame.from_dict(data)
    
    #Przetwarzanie df
    prices = []
    market_caps = []
    total_volumes = []
    timestamp = []
    for i,item in df_0.iterrows():
        
        x = df_0['prices'][i][1]
        x1 = df_0['market_caps'][i][1]
        x2 = df_0['total_volumes'][i][1]
        x3 = df_0['prices'][i][0]
        
        prices.append(x)
        market_caps.append(x1)
        total_volumes.append(x2)
        timestamp.append(x3)
    
    
            
    df_1 = pd.DataFrame(data={'prices':prices,
                              'market_caps':market_caps,
                              'total_volumes':total_volumes,
                              'timestamp':timestamp})
    
    df_1['crypto'] = name
    
    #Przetwarzanie daty
    date = []
    for i,item in df_1.iterrows():
        x = df_1['timestamp'][i]
        y = datetime.datetime.fromtimestamp(x/1e3)
        date.append(y)
        
    df_1['date'] = date
    
    df_1 = df_1.rename(columns={'prices':'price','total_volumes':'total_volume','crypto':'name'})
    
    df_1 = df_1[['date','name','price','total_volume','market_caps']]
    df_1['currency'] = curr

    return df_1