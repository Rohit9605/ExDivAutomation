import configparser
import json
import logging
from logging.handlers import RotatingFileHandler
from util.generator import Generator
import datetime as dt

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)

# loading configuration file
config = configparser.ConfigParser()
config.read('config.ini')

class Market:

    def __init__(self, session, base_url, account):
        self.session = session
        self.base_url = base_url
        self.account = account

    def quotes(self):
        """
        Calls quotes API to provide quote details for equities, options, and mutual funds

        :param self: Passes authenticated session in parameter
        """
        symbol = "DIS"

        # URL for the API endpoint
        url = self.base_url + "/v1/market/quote/" + symbol + ".json"

        # Make API call for GET request
        headers = {"Connection": "close"}
        response = self.session.get(url, headers=headers)
        logger.debug("Request Header: %s", response.request.headers)

        if response is not None and response.status_code == 200:

            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

            # Handle and parse response
            print("")
            data = response.json()
            if data is not None and "QuoteResponse" in data and "QuoteData" in data["QuoteResponse"]:
                for quote in data["QuoteResponse"]["QuoteData"]:
                    if quote is not None and "All" in quote and "ask" in quote["All"] and "askSize" in quote["All"]:
                        ask = quote["All"]["ask"]
                        return ask
            else:
                # Handle errors
                if data is not None and 'QuoteResponse' in data and 'Messages' in data["QuoteResponse"] \
                        and 'Message' in data["QuoteResponse"]["Messages"] \
                        and data["QuoteResponse"]["Messages"]["Message"] is not None:
                    for error_message in data["QuoteResponse"]["Messages"]["Message"]:
                        print("Error: " + error_message["description"])
                else:
                    print("Error: Quote API service error")
        else:
            logger.debug("Response Body: %s", response)
            print("Error: Quote API service error")

    def getPortfolioCashValue(self):
        
        """
        Calls quotes API to provide quote details for equities, options, and mutual funds

        :param self: Passes authenticated session in parameter
        """

        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/portfolio.json"

        # Make API call for GET request
        headers = {"Connection": "close"}
        payload = {
            "totalsRequired": True
        }
        response = self.session.get(url, headers=headers, params=payload)
        logger.debug("Request Header: %s", response.request.headers)

        if response is not None and response.status_code == 200:

            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

            # Handle and parse response
            print("")
            data = response.json()
            print(data)
            if data is not None and "PortfolioResponse" in data and "Totals" in data["PortfolioResponse"] and "cashBalance" in data["PortfolioResponse"]["Totals"]:
                return data["PortfolioResponse"]["Totals"]["cashBalance"]
            #else:
                # Handle errors
                # if data is not None and 'PortfolioResponse' in data and 'Messages' in data["QuoteResponse"] \
                #         and 'Message' in data["PortfolioResponse"]["Messages"] \
                #         and data["PortfolioResponse"]["Messages"]["Message"] is not None:
                #     for error_message in data["QuoteResponse"]["Messages"]["Message"]:
                #         print("Error: " + error_message["description"])
                # else:
                #     print("Error: Quote API service error")
        else:
            logger.debug("Response Body: %s", response)
            print("Error: Quote API service error")

    
    def preview_order(self, req, clientId, symbol, day, month, year, strikeprice, limitprice, orderaction1, orderaction2):

        """
        Call preview order API based on selecting from different given options

        :param self: Pass in authenticated session and information on selected account
        """

        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/orders/preview.json"

        # Add parameters and header information
        headers = {"Content-Type": "application/xml", "consumerKey": config["DEFAULT"]["CONSUMER_KEY"]}
        # Make API call for POST request
        response = self.session.post(url, header_auth=True, headers=headers, data=req)
        logger.debug("Request Header: %s", response.request.headers)
        logger.debug("Request payload: %s", req)

        # Handle and parse response
        if response is not None and response.status_code == 200:
            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            data = response.json()
            print("\nPreview Order:")

            if data is not None and "PreviewOrderResponse" in data and "PreviewIds" in data["PreviewOrderResponse"]:
                for previewids in data["PreviewOrderResponse"]["PreviewIds"]:
                    print(previewids["previewId"])
                    self.place_order(clientId, symbol, day, month, year, strikeprice, previewids["previewId"], limitprice, orderaction1, orderaction2)
            else:
                # Handle errors
                data = response.json()
                if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                    print("Error: " + data["Error"]["message"])
                else:
                    print("Error: Preview Order API service error")

            if data is not None and "PreviewOrderResponse" in data and "Order" in data["PreviewOrderResponse"]:
                for orders in data["PreviewOrderResponse"]["Order"]:

                    if orders is not None and "Instrument" in orders:
                        for instrument in orders["Instrument"]:
                            if instrument is not None and "orderAction" in instrument:
                                print("Action: " + instrument["orderAction"])
                            if instrument is not None and "quantity" in instrument:
                                print("Quantity: " + str(instrument["quantity"]))
                            if instrument is not None and "Product" in instrument \
                                    and "symbol" in instrument["Product"]:
                                print("Symbol: " + instrument["Product"]["symbol"])
                            if instrument is not None and "symbolDescription" in instrument:
                                print("Description: " + str(instrument["symbolDescription"]))

                if orders is not None and "priceType" in orders and "limitPrice" in orders:
                    print("Price Type: " + orders["priceType"])
                    if orders["priceType"] == "MARKET":
                        print("Price: MKT")
                    else:
                        print("Price: " + str(orders["limitPrice"]))
                if orders is not None and "orderTerm" in orders:
                    print("Duration: " + orders["orderTerm"])
                if orders is not None and "estimatedCommission" in orders:
                    print("Estimated Commission: " + str(orders["estimatedCommission"]))
                if orders is not None and "estimatedTotalAmount" in orders:
                    print("Estimated Total Cost: " + str(orders["estimatedTotalAmount"]))
            else:
                # Handle errors
                data = response.json()
                if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                    print("Error: " + data["Error"]["message"])
                else:
                    print("Error: Preview Order API service error")
        else:
            # Handle errors
            data = response.json()
            if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                print("Error: " + data["Error"]["message"])
            else:
                print("Error: Preview Order API service error")

    def place_order(self, clientId, symbol, day, month, year, strikeprice, previewIds, limitprice, orderaction1, orderaction2):

        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/orders/place.json"

        # Add parameters and header information
        headers = {"Content-Type": "application/xml", "consumerKey": config["DEFAULT"]["CONSUMER_KEY"]}

        # Add payload for POST Request
        payload = """<PlaceOrderRequest>
                                <Order>
                                    <Instrument>
                                        <Product>
                                        <securityType>EQ</securityType>
                                        <symbol>{1}</symbol>
                                        </Product>
                                        <orderAction>{8}</orderAction>
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
                                        <orderAction>{9}</orderAction>
                                        <orderedQuantity>1</orderedQuantity>
                                        <quantity>1</quantity>
                                    </Instrument>
                                    <allOrNone>FALSE</allOrNone>
                                    <limitPrice>{7}</limitPrice>
                                    <marketSession>REGULAR</marketSession>
                                    <orderTerm>GOOD_FOR_DAY</orderTerm>
                                    <priceType>NET_DEBIT</priceType>
                                </Order>
                                <clientOrderId>{0}</clientOrderId>
                                <orderType>BUY_WRITES</orderType>
                                <PreviewIds>
                                    <previewId>{6}</previewId>
                                </PreviewIds>
                            </PlaceOrderRequest>"""
        
        payload = payload.format(clientId, symbol, day, month, year, strikeprice, previewIds, limitprice, orderaction1, orderaction2)#orderaction
        #payload = payload.format(clientId, limitprice, previewIds, orderaction)
        response = self.session.post(url, header_auth=True, headers=headers, data=payload)
        logger.debug("Request Header: %s", response.request.headers)
        logger.debug("Request payload: %s", payload)
        print(payload)
        print(response)

        if response is not None and response.status_code == 200:
            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
        else:
            # Handle errors
            data = response.json()
            if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                print("Error: " + data["Error"]["message"])
            else:
                print("Error: Place Order API service error")
    
    def stop_loss(self):
        """
        Calls quotes API to provide quote details for equities, options, and mutual funds

        :param self: Passes authenticated session in parameter
        """

        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/portfolio.json"

        # Make API call for GET request
        headers = {"Connection": "close"}
        payload = {
            "totalsRequired": True
        }
        response = self.session.get(url, headers=headers, params=payload)
        logger.debug("Request Header: %s", response.request.headers)

        if response is not None and response.status_code == 200:

            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

            # Handle and parse response
            print("")
            data = response.json()
            print(data)
            if (data is not None and "PortfolioResponse" in data and "AccountPortfolio" in data["PortfolioResponse"]
            and "position" in data["PortfolioResponse"]["AccountPortfolio"]):
                #looping through the positions
                for position in data["PortfolioResponse"]["AccountPortfolio"]["Position"]:
                    
                    marketPrice = position["marketValue"]
                    strikePrice = position["Product"]["strikePrice"]
                    symbol = position["symbolDescription"]
                    expiryYear = position["Product"]["expiryYear"]
                    expiryMonth = position["Product"]["expiryMonth"]
                    expiryDay = position["Product"]["expiryDay"]
                    limitPrice = strikePrice

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
                    
                orderaction1 = 'SELL'
                orderaction2 = 'BUY_CLOSE'
                if(marketPrice <= strikePrice):
                    clientorderId = Generator.get_random_alphanumeric_string(20)
                    payload = payload.format(clientorderId, symbol, expiryDay, expiryMonth, expiryYear, strikePrice, limitPrice, orderaction1, orderaction2) #, ask, orderaction)
                    self.preview_order(payload, clientorderId, symbol, expiryDay, expiryMonth, expiryYear, strikePrice, limitPrice, orderaction1, orderaction2)       
                    
            #else:
                # Handle errors
                # if data is not None and 'PortfolioResponse' in data and 'Messages' in data["QuoteResponse"] \
                #         and 'Message' in data["PortfolioResponse"]["Messages"] \
                #         and data["PortfolioResponse"]["Messages"]["Message"] is not None:
                #     for error_message in data["QuoteResponse"]["Messages"]["Message"]:
                #         print("Error: " + error_message["description"])
                # else:
                #     print("Error: Quote API service error")
        else:
            logger.debug("Response Body: %s", response)
            print("Error: Quote API service error")
    
    def cash_in_early(self):
        """
        Calls quotes API to provide quote details for equities, options, and mutual funds

        :param self: Passes authenticated session in parameter
        """

        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/portfolio.json"

        # Make API call for GET request
        headers = {"Connection": "close"}
        payload = {
            "totalsRequired": True
        }
        response = self.session.get(url, headers=headers, params=payload)
        logger.debug("Request Header: %s", response.request.headers)

        if response is not None and response.status_code == 200:

            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

            # Handle and parse response
            print("")
            data = response.json()
            print(data)
            if (data is not None and "PortfolioResponse" in data and "AccountPortfolio" in data["PortfolioResponse"]
            and "position" in data["PortfolioResponse"]["AccountPortfolio"]):
                #looping through the positions
                #for i in range(len(data["PortfolioResponse"]["AccountPortfolio"]["Position"])):
                for position in data["PortfolioResponse"]["AccountPortfolio"]["Position"]:
                    
                    #used to calculate the expectedPctReturn
                    askPrice =         position["CompleteView"]["ask"]
                    bidPrice =         position["CompleteView"]["bid"]
                    expiryYear =       position["Product"]["expiryYear"]
                    expiryMonth =      position["Product"]["expiryMonth"]
                    expiryDay =        position["Product"]["expiryDay"]
                    markPrice = (askPrice + bidPrice)/2
                    strikePrice =      position["Product"]["strikePrice"]
                    symbol =           position["symbolDescription"]
                    limitPrice = markPrice
                    daysToExpiration = position["OptionsWatchView"]["expiryDay"]                   
                    pricePaid =        position["pricePaid"]                   
                    qdiv =             data["PortfolioResponse"]["AccountPortfolio"]["CompleteView"]["Dividend"]/4
                    
                    #used to check if buy_write should be sold
                    pctChange = data["PortfolioResponse"]["AccountPortfolio"]["Position"]["changePct"]
                    expectedPctReturn = (strikePrice - pricePaid + qdiv)/(daysToExpiration) * 100 * 365

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
                    
                orderaction1 = 'SELL'
                orderaction2 = 'BUY_CLOSE'
                if(pctChange > expectedPctReturn):
                    clientorderId = Generator.get_random_alphanumeric_string(20)
                    payload = payload.format(clientorderId, symbol, expiryDay, expiryMonth, expiryYear, strikePrice, limitPrice, orderaction1, orderaction2) #, ask, orderaction)
                    self.preview_order(payload, clientorderId, symbol, expiryDay, expiryMonth, expiryYear, strikePrice, limitPrice, orderaction1, orderaction2)       
                    
            #else:
                # Handle errors
                # if data is not None and 'PortfolioResponse' in data and 'Messages' in data["QuoteResponse"] \
                #         and 'Message' in data["PortfolioResponse"]["Messages"] \
                #         and data["PortfolioResponse"]["Messages"]["Message"] is not None:
                #     for error_message in data["QuoteResponse"]["Messages"]["Message"]:
                #         print("Error: " + error_message["description"])
                # else:
                #     print("Error: Quote API service error")
        else:
            logger.debug("Response Body: %s", response)
            print("Error: Quote API service error")
        