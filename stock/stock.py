#from statsmodels.regression.rolling import RollingOLS
#import matplotlib.pyplot as plt
#import statsmodels.api as sm
import yfinance as yfin
#import yahoo_fin.options as ops
#from yahoo_fin.stock_info import get_data
#import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import datetime as dt
import math
import os
import io
from pytz import timezone
from pandas_datareader import data as wb
from scipy.stats import norm
from market.market import Market

class Stock:

    def __init__(self, session, account, base_url):
        self.session = session
        self.account = account
        self.base_url = base_url

    # def getTickers():
    #     pd.set_option('expand_frame_repr', False)
    #     pd.options.display.max_rows = None

    #     today_obj = dt.datetime.strptime(dt.datetime.now().astimezone(timezone('America/Chicago')).strftime('%Y-%m-%d'), "%Y-%m-%d")
    #     today_str = today_obj.strftime('%Y-%m-%d')

    #     df = pd.read_csv(os.path.abspath("dividend_kings.csv"))
    #     df = df [['Ticker']]
    #     #df['ex_div_date'] = ""
    #     for ticker in df['Symbol'].to_list()[:7270]:
    #         fundamentals = robin.robinhood.stocks.get_fundamentals(ticker)[0]
    #         if (fundamentals != None and 'ex_dividend_date' in fundamentals.keys() and fundamentals['ex_dividend_date'] != None):
    #             days_to_exdividend = (dt.datetime.strptime(fundamentals['ex_dividend_date'], '%Y-%m-%d') - today_obj).days + 1
    #             #print(ticker,days_to_exdividend,fundamentals['ex_dividend_date'], today_str)
    #             if (days_to_exdividend > 1 and days_to_exdividend <= dtd_threshold):
    #                 df.loc[df['Symbol'] == ticker, 'ex_div_date'] = fundamentals['ex_dividend_date']


    #     df = df[df['ex_div_date'] != '']
    #     df = df.sort_values(by='ex_div_date', ascending=True)
    #     #print(df)
    #     return((df['Symbol'].to_list()))
    #     #print(df['Symbol'].to_list())

    def getLowestPrice(ticker, expiration_date):
        yfin.pdr_override()
        data = pd.DataFrame()
        data[ticker] = wb.get_data_yahoo(ticker, start='2014-1-1')['Adj Close']
        log_returns = np.log(1 + data.pct_change())
        #  log_returns.tail()
        #  data.plot(figsize=(10,6));
        #  log_returns.plot(figsize = (10,6))
        u = log_returns.mean()
        var = log_returns.var()
        #  var
        drift = u - (0.5 * var)
        #  drift
        stdev = log_returns.std()
        #  stdev
        # type(drift)

        # type(stdev)
        np.array(drift)
        #  drift.values
        #  stdev.values
        norm.ppf(0.95)
        x = np.random.rand(10,2)
        #  x
        norm.ppf(x)
        Z = norm.ppf(np.random.rand(10, 2))
        #  Z
        t_intervals = 1000
        iterations = 10
        daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(t_intervals, iterations)))
        daily_returns
        S0 = data.iloc[-1]
        #  S0
        price_list = np.zeros_like(daily_returns)
        #  price_list
        price_list[0] = S0
        #  price_list
        for t in range(1, t_intervals):
            price_list[t] = price_list[t-1] * daily_returns[t]
        #  price_list

        #calculate the number of days between today and expiration date
        delta = dt.datetime.strptime(expiration_date, f'%Y-%m-%d') - dt.datetime.today()
        days = delta.days
        #find lowest price
        lowest = price_list[days-1][0]
        for i in range(price_list.shape[1]):
            #for k in range(len(price_list.rows))
            if (price_list[days-1][i] < lowest):
                lowest = price_list[days-1][i]
        return(lowest)
        #find highest price
        # highest = price_list[999][0]
        # for i in range(price_list.shape[1]):
        #   if(price_list[999][i] > highest):
        #     highest = price_list[999][i]
        # highest
        # plt.figure(figsize = (10,6))
        # plt.plot(price_list)

        #Gets all the options data for a stock - adds useful columns below


    def getOptions(self, ticker):
        market = Market(self.session, self.base_url, self.account)
        #print(market.getCallData(ticker))
        out = pd.DataFrame()

        today_obj = dt.datetime.strptime(dt.datetime.now().astimezone(timezone('America/Chicago')).strftime(f'%Y-%m-%d'), f"%Y-%m-%d")
        today_str = today_obj.strftime(f'%Y-%m-%d')

        days_from_today = (today_obj + dt.timedelta(days=120)).strftime(f'%Y-%m-%d')

        fundamentals = market.getFundamentals(ticker)
        print(fundamentals)

        exDividendDate = fundamentals['All']['exDividendDate']
        exDividendDate = dt.datetime.fromtimestamp(exDividendDate).strftime(f'%Y-%m-%d')
        # fundamentals = robin.robinhood.stocks.get_fundamentals(ticker)[0]
        # if (fundamentals == None or 'ex_dividend_date' not in fundamentals.keys() or fundamentals['ex_dividend_date'] == None):
        #     return out

        # ex_div_date = fundamentals['ex_dividend_date']

        #days_to_exdividend includes today
        days_to_exdividend = (dt.datetime.strptime(exDividendDate, f'%Y-%m-%d') - today_obj).days

        #choose the days to exdividend
        if (exDividendDate <= today_str or days_to_exdividend >= 7):
            return out

        #gets only option dates that are feasible
        # options_data = robin.robinhood.options.get_chains(ticker)
        # if (options_data == None):
        #     return out

        #call_exp_dates = market.getCallData(ticker)["OptionDetails"]
        
        # num_exp_dates = len(market.getExpirationDates(ticker))     
        # option_data = []
        # for i in range(num_exp_dates):
        #     option_data += market.getCallData(ticker, market.getExpirationDates(ticker))
        # for expiration_date in expiration_dates:
        #     expiration_date
        # for i in range(len(option_data)):
        #     expiration_date = "20" + option_data[i]["Call"]['osiKey'][6:8] + "-" + \
        #     option_data[i]["Call"]['osiKey'][8:10] + "-" + option_data[i]["Call"]['osiKey'][10:12]
        #     expiration_dates.append(expiration_date)

        expiration_dates = market.getExpirationDates(ticker)
        print(expiration_dates)   
        dates = []
        for i in range(len(expiration_dates)):
            date = f"{expiration_dates[i]['year']}-{expiration_dates[i]['month']}-{expiration_dates[i]['day']}"
            if(dt.datetime.strptime(date, f'%Y-%m-%d') <= dt.datetime.strptime(days_from_today, f'%Y-%m-%d') \
                and dt.datetime.strptime(date, f'%Y-%m-%d') > dt.datetime.strptime(exDividendDate, f'%Y-%m-%d') \
                and dt.datetime.strptime(date, f'%Y-%m-%d') > dt.datetime.strptime(today_str, f'%Y-%m-%d')):
                dates.append(expiration_dates[i])
        qdiv = market.getFundamentals(ticker)['All']["dividend"]



        for expiration_date in dates:
            data = market.getCallData(ticker, str(expiration_date['year']), str(expiration_date['month']), str(expiration_date['day']))
            print(data)
            df = pd.json_normalize(data)
            print(df)
            #print(df.columns)
            try:
                #creating new columns
                df['symbol'] = df['Call.optionRootSymbol']
                df['strike_price'] = df['Call.strikePrice']
                df['ask_price'] = df['Call.ask']
                df['bid_price'] = df['Call.bid']
                df['volume'] = df['Call.volume']
                df['open_interest'] = df['Call.openInterest']
                #removing all columns except for those above
                df = df[['symbol', 'strike_price', 'ask_price', 'bid_price', 'volume', 'open_interest']]
                #adding new columns
                df['qdiv'] = qdiv
                df['ex_div_date'] = exDividendDate
                df['dtd'] = days_to_exdividend
                df['exp_date'] = f"{expiration_date['year']}-{expiration_date['month']}-{expiration_date['day']}"
                df['dte'] = (dt.datetime.strptime(expiration_date, f'%Y-%m-%d') - today_obj).days
                df['stock_price'] = (pd.to_numeric(market.getFundamentals(ticker)['All']['ask'] + market.getFundamentals(ticker)['All']['bid']))/2
                df['strike_price'] = pd.to_numeric(df['strike_price'])
                df['ask_price'] = pd.to_numeric(df['ask_price'])
                df['bid_price'] = pd.to_numeric(df['bid_price'])
                df.insert(4, 'mark_price', (df['ask_price'] + df['bid_price']) / 2)
                #Get both qdiv and call premium if wait until expiry
                df['annual_profit_perc'] = 365 * 100 * (df['qdiv'] + (df['mark_price'] + df['strike_price'] - df['stock_price'])) / (df['stock_price'] - df['mark_price']) / df['dte']
                #Get only the call premium if exercised early
                df['annual_profit_exer'] = 365 * 100 * (df['mark_price'] + df['strike_price'] - df['stock_price']) / (df['stock_price'] - df['mark_price']) / df['dtd']
                df['lowest_price'] = self.getLowestPrice(ticker, expiration_date)
                df['limit_price'] = df['stock_price'] - df['mark_price']
                out = pd.concat([out,df], ignore_index=True)
            except:
                print("Data is missing for " + ticker)
            #   print(out)

        #Can choose annual_profit (a percent) - profit_threshold will convert that to daily_profit_threshold
        annual_profit = 5
        annual_profit_exer = 5

        #Defining the thresholds
        dif_threshold = 0
        #volume_threshold = 10
        daily_profit_threshold = annual_profit/365
        daily_profit_if_exer = annual_profit_exer/365
        open_interest_threshold = 100
        qdiv_threshold = 0.1

        #Returning the rows that meets the criteria
        if not out.empty:

            #If strike_price and stock_price are far enough from each other
            out = out[100 * (out['stock_price'] - out['strike_price']) / (out['stock_price']) >= dif_threshold]
        # else:
        #     return out
            #If stock is liquid enough
            #out = out[out['volume'] >= volume_threshold]
            out = out[out['open_interest'] >= open_interest_threshold]

            #If the sell call has extrinsic value greater than or equal to a percentage of the quarterly dividend
            out = out[(out['ask_price'] + out['bid_price']) / 2 + out['strike_price'] - out['stock_price'] >=  qdiv_threshold * out['qdiv']]

            #If daily profit percent will be enough
            out = out[100 * out['qdiv'] / out['strike_price'] / out['dte'] >= daily_profit_threshold]

            #If daily profit percent based on exercise will be enough
            out = out[100 * (out['mark_price'] + out['strike_price'] - out['stock_price']) / (out['stock_price'] - out['mark_price']) / out['dtd'] >= daily_profit_if_exer]

            #If the strike price is lower than the MC simulation's lowest predicted price
            #This is the last check since it is the most computationally expensive
            out = out[out['strike_price'] < out['lowest_price']]
        return(out)

    def getDataFrame(self):
        final = pd.DataFrame()
        # df = pd.read_csv(os.path.abspath("dividend_kings.csv"))
        # tickers = list(df['Ticker'].values)
        # tickers = si.tickers_dow()
        # tickers = ['JNJ', 'UAL']
        sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        # sp500['Symbol'] = sp500['Symbol'].str.replace('.', '-')
        # tickers.extend(sp500['Symbol'].unique().tolist())   
        tickers = (sp500['Symbol'].unique().tolist()) 
        
        print(tickers)
        #tickers.extend(pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0])
        #print(tickers)
        #tickers.extend(getTickers(7))
        #print(tickers)
        #tickers = list(set(tickers))
        
        tickers.sort()

        count = 1
        for ticker in tickers:
            #print(count, ticker)
            count += 1
            out_options = self.getOptions(ticker)
            final = pd.concat([final, out_options], ignore_index=True)
            try:
                final = final.sort_values(by='annual_profit_perc', ascending=False)
            except:
                print(ticker + ' is giving an error.')
        return final.iloc[:3]

    def getSymbol(df):
        return df['symbol']
    

    def getExpiryDate(df):
        return df['exp_date']
    

    def getLimitPrice(df):
        return df['limit_price']
    

    def getStrikePrice(df):
        return df['strike_price']
    
