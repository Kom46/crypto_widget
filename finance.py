from collections import namedtuple
import os
import yfinance as yf
import json as js
import datetime as dt
from kucoin.client import Client as kc
from kucoin.exceptions import *
from array import *



class basicClient:
    __tickers = []
    
    @property
    def tickers(self):
        return self.__tickers
    
    @tickers.setter
    def tickers(self, value = None):
        if value == None:
            return
        
        if isinstance(value, list):
        # if value is array
            for t in value:
                self.__update_ticker(t)
        else:
        # if it is one ticket
            self.__update_ticker(value)
        # sort tickers by name
        print(self.__tickers)
        self.__tickers.sort(key=lambda x: x["name"])
        print(self.__tickers)

    def __update_ticker(self, value):
        found = False
        if len(self.__tickers) != 0:
            for tt in self.__tickers:
                if value["name"] == tt["name"]:
                    self.__tickers[self.__tickers.index(tt)] = value
                    found = True
        if not found:
            self.__tickers.append(value)
    
    def __init__(self, config = None, api_key = "") -> None:
        self.__api_key  = api_key
    
    @property
    def _api_key(self):
        return self.__api_key
    
    @_api_key.getter
    def _api_key(self):
        return self.__api_key
    
    @_api_key.setter
    def _api_key(self, value):
        if not isinstance(value, str):
            raise TypeError("API key must be a string!")
        self.__api_key = value

    def __new__(cls) -> 'basicClient':
        return super().__new__(cls)
    
    def apiError(self):
        print(f"One of api keys for class {self.__class__.__name__} is missing!")
    
    def getTicket(self, ticket: str  = ""):
        data = None
        if ticket != None:
            data = ticket
        return data

    def getTickets(self, tickets=any):
        data = []
        ticketClass = namedtuple('Ticket', ['name', 'ticketData'])
        for ticket in tickets:
            data.append(ticketClass(
                ticket["name"], self.getTicket(ticket["symbol"])))
        return data


class yahooClient(basicClient):

    def getTicket(self, ticket: str = None, start=dt.datetime.today(), end=dt.datetime.today()):
        result = None
        if super().getTicket(ticket) != None:
            ticker = yf.Ticker(ticket)
            data = ticker.get_info()
            # data = ticker.history(start=start, end=end)
            price = None
            try:
                price = data["regularMarketOpen"]
            except:
                pass
            result = data
        return result

# TODO: implement kucoin crypto exchange
class kucoinClient(basicClient):
    
    def __init__(self, config = None) -> None:
        if config != None:
            StockApi = namedtuple('StockApi', [ 'secret', 'passphrase', 'sandbox'])
            self.__api = StockApi()
            try:
                self._api_key = config["api_key"]
                self.__api.secret = config["api_secret"]
                self.__api.passphrase = config["api_passphrase"]
                self.__api.sandbox = config["sandbox"]
            except:
                super().apiError(self)
                
            self.__client = kc(self._api_key, self.__api.secret, 
                                self.__api.passphrase, self.__api.sandbox)
            
            assert(self.__client != None)
            
    
    def getTicket(self, ticket: str = None):
        result = None
        if super().getTicket(ticket) != None:
            try:
                result = self.__client.get_ticker(ticket)
            except Exception as e:
                if isinstance(e, KucoinRequestException):
                    print("Kucoin client get_currency request failed cause of" 
                                                                "network error!")
                if isinstance(e, KucoinAPIException):
                    print("Kucoin client get_currency request failed cause of" 
                                                                    "API error!")
        return result
                
    def getTickets(self, tickets=any):
        # using basicClass API
        return super().getTickets(tickets)
    
class coinmarketcapClient(basicClient):
    def __init__(self, config=None) -> None:
        super().__init__(config)
    
    def getTicket(self, ticket: str = None):
        return super().getTicket(ticket)
    
    def getTickets(self, tickets=any):
        return super().getTickets(tickets)

stockClients = {"yahoo": yahooClient, "kucoin": kucoinClient, 
                "coinmarketcap": coinmarketcapClient}

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
        return self.client.getTickets(tickets=self.__tickets)


params_filename = "params.json"
params_file = f"{os.path.dirname(os.path.abspath(__file__))}/{params_filename}"


class stockClient:
    def __init__(self) -> None:
        self.__stocks = []
        # load config
        with open(params_file, "r") as fd:
            config = js.load(fp=fd)
            for st in config["stock_exchange"]:
                self.__stocks.append(stockExchange(st))

    def getCurrentPrices(self):
        result = []
        for stock in self.__stocks:
            if stock.client != None:
                result.append(stock.getStockPrices())
        return result

