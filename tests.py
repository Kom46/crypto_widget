from io import StringIO
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

    @patch("finance.yf.Ticker")
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
    def test_get_stock_price(self):
        stock_exchange = stockExchange("yahoo", ["AAPL", "MSFT"], "api_key")
        stock_exchange.client.getTickets = MagicMock(return_value=[(100, {"Close": [100]}), (200, {"Close": [200]})])
        expected_result = [100, 200]
        self.assertEqual(stock_exchange.get_stock_price(), expected_result)
        
class TestStockClient(unittest.TestCase):
    def setUp(self):
        self.client = stockClient()

    @patch("finance.open")
    def test_init(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = '{"stock_exchange": [{"name": "yahoo", "tickets": ["AAPL", "MSFT"], "api_key": "api_key"}]}'
        self.assertEqual(len(self.client.stocks), 1)
        self.assertIsInstance(self.client.stocks[0], stockExchange)
    
    def test_getCurrentPrices(self):
        stock_client = stockClient()
        stock_client.stocks = [stockExchange("yahoo", ["AAPL", "MSFT"], "api_key")]
        stock_client.stocks[0].client.getTickets = MagicMock(return_value=[(100, {"Close": [100]}), (200, {"Close": [200]})])
        expected_output = "AAPL: 100\nMSFT: 200\n"
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_output:
            result = stock_client.getCurrentPrices()
            for price in result:
                print(f"{price[0]}: {price[1]['Close']}\n")
            self.assertEqual(fake_output.getvalue().strip(), expected_output)

if __name__ == '__main__':
    unittest.main()