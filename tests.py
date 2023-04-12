import unittest
import datetime as dt
from unittest.mock import patch, MagicMock
from finance import basicClient, yahooClient, stockExchange, stockClient

class TestBasicClient(unittest.TestCase):    
    def setUp(self):
        self.client = basicClient()

    def test_getTicket(self):
        self.assertIsNone(self.client.getTicket())
        self.assertEqual(self.client.getTicket("AAPL"), "AAPL")

    def test_getTickets(self):
        tickets = {"tickets": [{"name": "Apple", "ticket": "AAPL"}, {"name": "Microsoft", "ticket": "MSFT"}]}
        expected = [("Apple", "AAPL"), ("Microsoft", "MSFT")]
        self.assertEqual(self.client.getTickets(tickets), expected)
        
class TestYahooClient(unittest.TestCase):
    def setUp(self):
        self.client = yahooClient()

    @patch("main.yf.Ticker")
    def test_getTicket(self, mock_ticker):
        mock_data = MagicMock()
        mock_data.__getitem__.return_value = 100
        mock_ticker.return_value.history.return_value = {"Close": [100]}
        self.assertEqual(self.client.getTicket("AAPL", start=dt.datetime(2021, 1, 1), end=dt.datetime(2021, 1, 2)), (100, {"Close": [100]}))

class TestStockExchange(unittest.TestCase):
    def setUp(self):
        self.exchange = stockExchange("yahoo", ["AAPL", "MSFT"], "api_key")
    def test_init(self):
        self.assertEqual(self.exchange.name, "yahoo")
        self.assertEqual(self.exchange.tickets, ["AAPL", "MSFT"])
        self.assertEqual(self.exchange.api_key, "api_key")
        self.assertIsInstance(self.exchange.client, yahooClient)
        
class TestStockClient(unittest.TestCase):
    def setUp(self):
        self.client = stockClient()

    @patch("finance.open")
    def test_init(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = '{"stock_exchange": [{"name": "yahoo", "tickets": ["AAPL", "MSFT"], "api_key": "api_key"}]}'
        self.assertEqual(len(self.client.stock), 1)
        self.assertIsInstance(self.client.stock[0], stockExchange)

if __name__ == '__main__':
    unittest.main()