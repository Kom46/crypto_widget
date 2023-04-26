import unittest
from unittest.mock import MagicMock
from finance import *

class TestBasicClient(unittest.TestCase):
    def test_getTicket(self):
        client = basicClient()
        self.assertIsNone(client.getTicket())
        self.assertEqual(client.getTicket("AAPL"), "AAPL")
    
    def test_getTickets(self):
        client = basicClient()
        tickets = [{"name": "Apple", "ticket": "AAPL"}, {"name": "Microsoft", "ticket": "MSFT"}]
        expected = [namedtuple('Ticket', ['name', 'ticketData'])("Apple", "AAPL"), 
                    namedtuple('Ticket', ['name', 'ticketData'])("Microsoft", "MSFT")]
        self.assertEqual(client.getTickets(tickets), expected)
        
class TestYahooClient(unittest.TestCase):
    def test_getTicket(self):
        client = yahooClient()
        client.getTicket = MagicMock(return_value=(100, {"regularMarketOpen": 100}))
        self.assertEqual(client.getTicket("AAPL"), (100, {"regularMarketOpen": 100}))
        client.getTicket.assert_called_once_with("AAPL")
    
    def test_getTicket_no_price(self):
        client = yahooClient()
        client.getTicket = MagicMock(return_value=(None, {"regularMarketOpen": None}))
        self.assertEqual(client.getTicket("AAPL"), (None, {"regularMarketOpen": None}))
        client.getTicket.assert_called_once_with("AAPL")
        
class TestStockExchange(unittest.TestCase):
    def test_getStockPrices(self):
        client = stockExchange("yahoo", ["AAPL", "MSFT"])
        client.client.getTickets = MagicMock(return_value=[namedtuple('Ticket', ['name', 'ticketData'])("Apple", (100, {"regularMarketOpen": 100})),
        namedtuple('Ticket', ['name', 'ticketData'])("Microsoft", (200, {"regularMarketOpen": 200}))])
        self.assertEqual(client.getStockPrices(), [100, 200])
        client.client.getTickets.assert_called_once_with(tickets=["AAPL", "MSFT"])

class TestStockClient(unittest.TestCase):
    def test_getCurrentPrices(self):
        client = stockClient()
        client.stocks = [stockExchange("yahoo", ["AAPL", "MSFT"])]
        client.stocks[0].getStockPrices = MagicMock(return_value=[100, 200])
        self.assertEqual(client.getCurrentPrices(), [100, 200])
        client.stocks[0].getStockPrices.assert_called_once()

if __name__ == '__main__':
    unittest.main()