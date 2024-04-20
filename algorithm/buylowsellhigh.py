import asyncio
import pickle
from market.market import Market
from util.generator import Generator
from stock.stock import Stock
import pandas as pd
import time 

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
            def renew_token():
                url = self.base_url + "/oauth/renew_access_token"

                response = self.session.get(url, header_auth=True)
                print(response)
                #loop.call_later(7100, renew_token)

            def buy():
                clientorderId = Generator.get_random_alphanumeric_string(20)
                account_value = market.getPortfolioCashValue()
                # payload = """<PreviewOrderRequest>
                #         <Order>
                #             <Instrument>
                #                 <Product>
                #                 <securityType>EQ</securityType>
                #                 <symbol>UAL</symbol>
                #                 </Product>
                #                 <orderAction>{2}</orderAction>
                #                 <quantityType>QUANTITY</quantityType>
                #                 <quantity>100</quantity>
                #             </Instrument>
                #             <Instrument>
                #                 <Product>
                #                 <callPut>CALL</callPut>
                #                 <expiryDay>19</expiryDay>
                #                 <expiryMonth>04</expiryMonth>
                #                 <expiryYear>2024</expiryYear>
                #                 <securityType>OPTN</securityType>
                #                 <strikePrice>39</strikePrice>
                #                 <symbol>UAL</symbol>
                #                 </Product>
                #                 <orderAction>SELL_OPEN</orderAction>
                #                 <orderedQuantity>1</orderedQuantity>
                #                 <quantity>1</quantity>
                #             </Instrument>
                #             <allOrNone>FALSE</allOrNone>
                #             <limitPrice>{1}</limitPrice>
                #             <marketSession>REGULAR</marketSession>
                #             <orderTerm>GOOD_FOR_DAY</orderTerm>
                #             <priceType>NET_DEBIT</priceType>
                #         </Order>
                #         <clientOrderId>{0}</clientOrderId>
                #         <orderType>BUY_WRITES</orderType>
                #     </PreviewOrderRequest>"""
                # payload = """<PreviewOrderRequest>
                #                 <Order>
                #                     <Instrument>
                #                         <Product>
                #                         <securityType>EQ</securityType>
                #                         <symbol>DIS</symbol>
                #                         </Product>
                #                         <orderAction>BUY</orderAction>
                #                         <quantityType>QUANTITY</quantityType>
                #                         <quantity>100</quantity>
                #                     </Instrument>
                #                     <Instrument>
                #                         <Product>
                #                         <callPut>CALL</callPut>
                #                         <expiryDay>19</expiryDay>
                #                         <expiryMonth>04</expiryMonth>
                #                         <expiryYear>2024</expiryYear>
                #                         <securityType>OPTN</securityType>
                #                         <strikePrice>110</strikePrice>
                #                         <symbol>DIS</symbol>
                #                         </Product>
                #                         <orderAction>SELL_OPEN</orderAction>
                #                         <orderedQuantity>1</orderedQuantity>
                #                         <quantity>1</quantity>
                #                     </Instrument>
                #                     <allOrNone>FALSE</allOrNone>
                #                     <limitPrice>35/limitPrice>
                #                     <marketSession>REGULAR</marketSession>
                #                     <orderTerm>GOOD_FOR_DAY</orderTerm>
                #                     <priceType>NET_DEBIT</priceType>
                #                 </Order>
                #                 <clientOrderId>{0}</clientOrderId>
                #                 <orderType>BUY_WRITES</orderType>
                #             </PreviewOrderRequest>"""

                #   payload = """<PreviewOrderRequest>
                #                 <orderType>EQ</orderType>
                #                 <clientOrderId>{0}</clientOrderId>
                #                 <Order>
                #                     <allOrNone>false</allOrNone>
                #                     <priceType>LIMIT</priceType>
                #                     <orderTerm>GOOD_FOR_DAY</orderTerm>
                #                     <marketSession>REGULAR</marketSession>
                #                     <stopPrice></stopPrice>
                #                     <limitPrice>{1}</limitPrice>
                #                     <Instrument>
                #                         <Product>
                #                             <securityType>EQ</securityType>
                #                             <symbol>DIS</symbol>
                #                         </Product>
                #                         <orderAction>{2}</orderAction>
                #                         <quantityType>QUANTITY</quantityType>
                #                         <quantity>1</quantity>
                #                     </Instrument>
                #                 </Order>
                #             </PreviewOrderRequest>"""
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
                renew_token()
                market.stop_loss()
                # orderaction1 = "BUY"
                # orderaction2 = "SELL_OPEN"
                data = Stock.getDataFrame()
                for i in range(len(data)):
                    if (account_value >= (100 * Stock.getLimitPrice(data.iloc[i]))):
                        account_value -= 100 * Stock.getLimitPrice(data.iloc[i]) 
                        clientorderId = Generator.get_random_alphanumeric_string(20)   
                        symbol = Stock.getSymbol(data.iloc[i])
                        expiry_date = Stock.getExpiryDate(data.iloc[i]).split("-")
                        strikeprice = Stock.getStrikePrice(data.iloc[i])   
                        limitprice = Stock.getLimitPrice(data.iloc[i])
                        orderaction1 = "BUY"
                        orderaction2 = "SELL_OPEN"    
                        new_payload = payload.format(clientorderId, symbol, expiry_date[2], expiry_date[1], expiry_date[0], strikeprice, round(limitprice, 2), orderaction1, orderaction2)
                        market.preview_order(new_payload, clientorderId, symbol, expiry_date[2], expiry_date[1], expiry_date[0], strikeprice, round(limitprice, 2), orderaction1, orderaction2)
                    #     if (account_value >= (100 * Stock.getLimitPrice(data.iloc[i]))):
                #         account_value -= 100 * Stock.getLimitPrice(data.iloc[i])
                #         expiry_date = Stock.getExpiryDate(data.iloc[i]).split("-")
                #         print(Stock.getStrikePrice(data.iloc[i]))                   
                #         payload_update = payload.format(clientorderId, Stock.getSymbol(data.iloc[i]), expiry_date[2], expiry_date[1], expiry_date[0], Stock.getStrikePrice(data.iloc[i]), round((Stock.getLimitPrice(data.iloc[i])), 2), orderaction1, orderaction2) #, ask, orderaction)
                #         print(payload_update)
                        
                #         #time.sleep(60)
                #         market.preview_order(payload_update, clientorderId, Stock.getSymbol(data.iloc[i]), expiry_date[2], expiry_date[1], expiry_date[0], Stock.getStrikePrice(data.iloc[i]), round((Stock.getLimitPrice(data.iloc[i])), 2), orderaction1, orderaction2)
                # payload_new = payload.format(clientorderId)
                # market.preview_order(payload_new, clientorderId)
                market.cash_in_early()
            loop.call_soon(buy)
        loop.call_later(3, createbuyorder)    
            

            


        # def renew_token():
        #     url = self.base_url + "/oauth/renew_access_token"

        #     response = self.session.get(url, header_auth=True)
        #     print(response)
        #     loop.call_later(7100, renew_token)

        loop.call_soon(calculatetodaysmovingaverage)
        loop.call_later(5,createbuyorder)#7200, createbuyorder)
        #loop.call_later(7100, renew_token)
        loop.run_forever()

        #8201c4ae9815589e35c2b474c19e863d
        #02969e4763bc75a8e74d9f9b39e528b82e320a5e5fde9cacdfbedb5ee12700a4