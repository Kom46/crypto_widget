from collections import namedtuple
import os
import yfinance as yf
import json as js
import datetime as dt
from kucoin.client import Client as kc
from kucoin.exceptions import *


class basicClient:
    tickers = []
    
    def __new__(cls) -> 'basicClient':
        return super().__new__(cls)

    def __init__(self, config = None) -> None:
        pass
    
    def apiError(self):
        print(f"One of api keys for class {self.__class__.__name__} is missing!")
    
    def getTicket(self, ticket: str = None):
        data = None
        if ticket != None:
            data = ticket
        return data

    def getTickets(self, tickets=any, start=dt.datetime.now(), end=dt.datetime.now()):
        data = []
        ticketClass = namedtuple('Ticket', ['name', 'ticketData'])
        for ticket in tickets:
            data.append(ticketClass(
                ticket["name"], self.getTicket(ticket["ticket"])))
        return data


class yahooClient(basicClient):

    def getTicket(self, ticket: str = None, start=dt.datetime.today(), end=dt.datetime.today()):
        if super().getTicket(ticket) != None:
            ticker = yf.Ticker(ticket)
            data = ticker.get_info()
            # data = ticker.history(start=start, end=end)
            price = None
            try:
                price = data["regularMarketOpen"]
            except:
                pass
            result = price, data
        return result

# TODO: implement kucoin crypto exchange
class kucoinClient(basicClient):
    
    def __init__(self, config = None) -> None:
        result = False
        if config != None:
            StockApi = namedtuple('StockApi', ['key', 'secret', 'passphrase', 'sandbox'])
            self.__api = StockApi()
            try:
                self.__api.key = config["api_key"]
                self.__api.secret = config["api_secret"]
                self.__api.passphrase = config["api_passphrase"]
                self.__api.sandbox = config["sandbox"]
            except:
                super().apiError(self)
                
            self.__client = kc(self.__api.key, self.__api.secret, 
                                self.__api.passphrase, self.__api.sandbox)
            if self.__client != None:
                result = True

        return result
    
    def getTicket(self, ticket: str = None):
        result = None
        if super().getTicket(ticket) != None:
            try:
                result = self.__client.get_ticker(ticket)["price"]
            except Exception as e:
                if isinstance(e, KucoinRequestException):
                    print("Kucoin client get_currency request failed cause of" 
                                                                "network error!")
                if isinstance(e, KucoinAPIException):
                    print("Kucoin client get_currency request failed cause of" 
                                                                    "API error!")
                
        return result
    
    def getTickets(self, tickets=any, start=dt.datetime.now(), end=dt.datetime.now()):
        # using basicClass API
        return super().getTickets(tickets, start, end)
    
    

stockClients = {"yahoo": yahooClient, "kucoin": kucoinClient}

class stockExchange:
    def __init__(self, stock) -> None:
        self.__name = stock["name"]
        self.__tickets = stock["tickets"]
        if self.__name != None:
            try:
                self.__client = stockClients[self.__name]()
            except KeyError:
                self.__client = None
    @property
    def client(self):
        return self.__client

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def getStockPrices(self):
        tickets = self.client.getTickets(tickets=self.__tickets)
        result = []
        for ticket in tickets:
            result.append(ticket.ticketData[0])
        return result


params_filename = "params.json"
params_file = f"{os.path.dirname(__file__)}/{params_filename}"


class stockClient:
    def __init__(self) -> None:
        self.__stocks = []
        # load config
        with open(params_file, "r") as fd:
            config = js.load(fp=fd)
            for st in config["stock_exchange"]:
                self.__stocks.append(stockExchange(st))

    def getCurrentPrices(self):
        for stock in self.__stocks:
            if stock.client != None:
                return stock.getStockPrices()
