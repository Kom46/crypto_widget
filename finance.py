from collections import namedtuple
import os
import yfinance as yf
import json as js
import datetime as dt


class basicClient:
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
    def __init__(self) -> None:
        pass

    def __new__(cls) -> 'yahooClient':
        return super().__new__(cls)

    def getTicket(self, ticket: str = None, start=dt.datetime.today(), end=dt.datetime.today()):
        result = super().getTicket(ticket)
        if result != None:
            ticker = yf.Ticker(ticket)
            data = ticker.history(start=start, end=end)
            price = None
            try:
                price = data["Close"][0]
            except:
                pass
            result = price, data
        return result


stockClients = {"yahoo": yahooClient}

class stockExchange:
    def __init__(self, name=None, tickets=[], api_key=None) -> None:
        self.name = name
        self.api_key = api_key
        self.tickets = tickets
        if name != None:
            try:
                self.client = stockClients[name]()
            except KeyError:
                self.client = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def get_stock_price(self):
        price = self.client.getTickets(tickets=self.tickets)
        return price


params_filename = "params.json"
params_file = f"{os.path.dirname(__file__)}/{params_filename}"


class stockClient:
    def __init__(self) -> None:
        self.stocks = []
        # load config
        with open(params_file, "r") as fd:
            config = js.load(fp=fd)
            for st in config["stock_exchange"]:
                self.stocks.append(stockExchange(
                    st["name"], st["tickets"], st["api_key"]))

    def getCurrentPrices(self):
        for stock in self.stocks:
            if stock.client != None:
                return stock.get_stock_price()
