import unittest
from unittest.mock import MagicMock, patch
import datetime as dt
from finance import basicClient, yahooClient, kucoinClient, coinmarketcapClient, stockClients, stockExchange, stockClient

class TestClients(unittest.TestCase):

    def setUp(self):
        self.basic_client = basicClient()
        self.yahoo_client = yahooClient()
        self.kucoin_client = kucoinClient()
        self.coinmarketcap_client = coinmarketcapClient()

    def test_basic_client_api_key(self):
        with self.assertRaises(TypeError):
            self.basic_client._api_key = 123
    
    def test_getTicket_with_valid_ticket(self):
        self.yahoo_client.getTicket = MagicMock(return_value=(10, {'data': 'test_data'}))
        self.assertEqual(self.yahoo_client.getTicket("AAPL"), (10, {'data': 'test_data'}))

    def test_getTicket_with_none_ticket(self):
        self.assertIsNone(self.yahoo_client.getTicket())

    def test_kucoin_client_init_success(self):
        kucoin_client = kucoinClient(config={'api_key': 'test_api_key', 'api_secret': 'test_secret', 'api_passphrase': 'test_pass', 'sandbox': True})
        self.assertEqual(kucoin_client._api_key, 'test_api_key')

    def test_kucoin_client_init_failure(self):
        kucoin_client = kucoinClient(config={'api_key': 'test_api_key'})
        self.assertIsNone(kucoin_client._kucoinClient__client)
    
    def test_getTickets_with_any_tickets(self):
        self.assertEqual(self.coinmarketcap_client.getTickets(), [])

    def test_getTickets_with_valid_tickets(self):
        tickets = [{'name': 'AAPL', 'ticket': 'AAPL'}, {'name': 'GOOG', 'ticket': 'GOOG'}, {'name': 'TSLA', 'ticket': 'TSLA'}]
        self.assertEqual(self.yahoo_client.getTickets(tickets), [('AAPL', None), ('GOOG', None), ('TSLA', None)])

class TestStockExchange(unittest.TestCase):

    def setUp(self):
        self.yahoo_exchange = stockExchange({'name': 'yahoo', 'tickets': [{'name': 'AAPL', 'ticket': 'AAPL'}]})
        self.invalid_exchange = stockExchange({'name': 'test_exchange', 'tickets': [{'name': 'test_ticket', 'ticket': 'TEST_TICKET'}]})

    def test_yahoo_exchange_init(self):
        self.assertIsNotNone(self.yahoo_exchange.client)

    def test_invalid_exchange_init(self):
        self.assertIsNone(self.invalid_exchange.client)

    def test_getStockPrices(self):
        self.yahoo_exchange.client.getTickets = MagicMock(return_value=[('AAPL', (10, {'data': 'test_data'}))])
        self.assertEqual(self.yahoo_exchange.getStockPrices(), [10])

class TestStockClient(unittest.TestCase):

    @patch('my_module.os.path.dirname')
    @patch('my_module.js.load')
    def test_init_stockClient(self, mock_js_load, mock_dirname):
        mock_dirname.return_value = '/test'
        mock_js_load.return_value = {'stock_exchange': [{'name': 'yahoo','tickets': [{'name': 'AAPL','ticket': 'AAPL'}]}]}
        stock_client = stockClient()
        self.assertEqual(stock_client.getCurrentPrices(), [10])

if __name__ == '__main__':
    unittest.main()
