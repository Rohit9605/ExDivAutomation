import asyncio
import pickle
from market.market import Market
from util.generator import Generator
from stock.stock import Stock

asklist = []
openasklist = open("asklist.pickle", "wb")
pickle.dump(asklist, openasklist)
openasklist.close()

class Buylow:

    def __init__(self, session, account, base_url):
        self.session = session
        self.account = account
        self.base_url = base_url

    def start_script(self):
        loop = asyncio.get_event_loop()

        def calculatetodaysmovingaverage():
            # readasklist = open("asklist.pickle", "rb")
            # asklist = pickle.load(readasklist)
            # readasklist.close()

            # market = Market(self.session, self.base_url, self.account)
            # ask = market.quotes()
            
            # asklist.append(ask)
            # openasklist = open("asklist.pickle", "wb")
            # pickle.dump(asklist, openasklist)
            # openasklist.close()

            # print("Ask Price: ")
            # print(ask)
            count = 0
            print(f'loop count: {count}')
            count += 1

            #loop.call_later(3, calculatetodaysmovingaverage)#300, calculatetodaysmovingaverage)

        def createbuyorder():
            # readasklist = open("asklist.pickle", "rb")
            # asklist = pickle.load(readasklist)
            # readasklist.close()

            # total = 0
            # count = 0

            # for ask in asklist:
            #     total = ask + total
            #     count = count + 1

            # movingaverageFunc = lambda a, b: a / b
            # movingaverage = movingaverageFunc(total, count)
            # movingaverage = 120
            # print("Today's Moving Average: ")
            # print(movingaverage)
            market = Market(self.session, self.base_url, self.account)
            # ask = market.quotes()
            # if ask <= movingaverage:
            def buy():
                clientorderId = Generator.get_random_alphanumeric_string(20)
                account_value = market.getPortfolioCashValue()
                payload = """<PreviewOrderRequest>
                        <Order>
                            <Instrument>
                                <Product>
                                <securityType>EQ</securityType>
                                <symbol>{1}</symbol>
                                </Product>
                                <orderAction>{7}</orderAction>
                                <quantityType>QUANTITY</quantityType>
                                <quantity>100</quantity>
                            </Instrument>
                            <Instrument>
                                <Product>
                                <callPut>CALL</callPut>
                                <expiryDay>{2}</expiryDay>
                                <expiryMonth>{3}</expiryMonth>
                                <expiryYear>{4}</expiryYear>
                                <securityType>OPTN</securityType>
                                <strikePrice>{5}</strikePrice>
                                <symbol>{1}</symbol>
                                </Product>
                                <orderAction>{8}</orderAction>
                                <orderedQuantity>1</orderedQuantity>
                                <quantity>1</quantity>
                            </Instrument>
                            <allOrNone>FALSE</allOrNone>
                            <limitPrice>{6}</limitPrice>
                            <marketSession>REGULAR</marketSession>
                            <orderTerm>GOOD_FOR_DAY</orderTerm>
                            <priceType>NET_DEBIT</priceType>
                        </Order>
                        <clientOrderId>{0}</clientOrderId>
                        <orderType>BUY_WRITES</orderType>
                    </PreviewOrderRequest>"""
                            
                
                market.stop_loss()
                orderaction1 = "BUY"
                orderaction2 = "SELL_OPEN"
                data = Stock.getDataFrame()
                account_value = 100000
                for i in range(3):
                    if (account_value >= (100 * Stock.getLimitPrice(data.iloc[i]))):
                        account_value -= 100 * Stock.getLimitPrice(data.iloc[i])
                        expiry_date = Stock.getExpiryDate(data.iloc[i]).split("-")
                        payload = payload.format(clientorderId, Stock.getSymbol(data.iloc[i]), expiry_date[2], expiry_date[1], expiry_date[0], Stock.getStrikePrice(data.iloc[i]), round((Stock.getLimitPrice(data.iloc[i])), 2), orderaction1, orderaction2) #, ask, orderaction)
                        market.preview_order(payload, clientorderId, Stock.getSymbol(data.iloc[i]), expiry_date[2], expiry_date[1], expiry_date[0], Stock.getStrikePrice(data.iloc[i]), round((Stock.getLimitPrice(data.iloc[i])), 2), orderaction1, orderaction2)
                market.cash_in_early()
            loop.call_soon(buy)
        loop.call_later(3, createbuyorder)#300, createbuyorder)


        def renew_token():
            url = self.base_url + "/oauth/renew_access_token"

            response = self.session.get(url, header_auth=True)
            print(response)
            loop.call_later(7100, renew_token)

        loop.call_soon(calculatetodaysmovingaverage)
        loop.call_later(5,createbuyorder)#7200, createbuyorder)
        loop.call_later(7100, renew_token)
        loop.run_forever()