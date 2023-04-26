from collections import namedtuple
import os
import yfinance as yf
import json as js
import datetime as dt


class basicClient:
    tickers = []
    
    def __new__(cls) -> 'basicClient':
        return super().__new__(cls)

    def __init__(self) -> None:
        pass

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
    # def __init__(self) -> None:
    #     pass

    # def __new__(cls) -> 'yahooClient':
    #     return super().__new__(cls)

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
    pass
    # def __init__(self, name=None, tickets=[], api_key=None, api_secret=None, api_passphrase=None) -> None:
    #     pass

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
