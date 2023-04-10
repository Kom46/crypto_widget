import yfinance as yf
import json as js
import datetime as dt

class yahooClient:
    def __init__(self) -> None:
        pass
    
    def getTickets(tickets = any, start = dt.date(), end = dt.date()):
        pass

class stockExchange:
    def __init__(self, name = None, tickets = [], api_key = None) -> None:
        self.name = name
        self.api_key = api_key
        self.tickets = tickets

class stockClient:
    def __init__(self) -> None:
        self.clients = []
        # load conig
        with open("parms.json", "r") as fd:
            config = js.load(fp=fd)
            for st in config["stock_exchange"]:
                self.stock = stockExchange(st["name"], st["tickets"], st["api_key"])
                
                