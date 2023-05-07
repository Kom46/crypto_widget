import unittest
from unittest.mock import MagicMock, patch

from finance import (
    basicClient,
    yahooClient,
    kucoinClient,
    coinmarketcapClient,
    stockExchange,
    stockClient,
    stockClients
)


class TestBasicClient(unittest.TestCase):
    def test_tickers_property(self):
        client = basicClient()
        client.tickers = [{"name": "Bitcoin", "symbol": "BTC"}, {
            "name": "Apple", "symbol": "AAPL"}]
        self.assertEqual(client.tickers, [{"name": "Apple", "symbol": "AAPL"}, {
                         "name": "Bitcoin", "symbol": "BTC"}])

    def test_tickers_property_with_array(self):
        client = basicClient()
        client.tickers = [{"name": "AAPL"}, {"name": "GOOG"}]
        self.assertEqual(client.tickers, [{"name": "AAPL"}, {"name": "GOOG"}])

    def test_tickers_property_with_array_should_sort_by_name(self):
        client = basicClient()
        client.tickers = [{"name": "GOOG"}, {"name": "AAPL"}]
        self.assertEqual(client.tickers, [{"name": "AAPL"}, {"name": "GOOG"}])

    def test_get_ticket(self):
        client = basicClient()
        self.assertEqual(client.getTicket("AAPL"), None)

    def test_get_tickets(self):
        client = basicClient()
        tickets = [{"name": "AAPL", "symbol": "AAPL"}]
        client.tickers = tickets
        self.assertEqual(client.getTickets(tickets),
                         [client.getTicket("AAPL")])


class TestYahooClient(unittest.TestCase):
    def test_get_ticket(self):
        client = yahooClient()
        client.getTicket = MagicMock(return_value={"test": "test"})
        self.assertEqual(client.getTicket("AAPL"), {"test": "test"})


class TestKucoinClient(unittest.TestCase):
    def test_get_ticket_should_return_none(self):
        client = kucoinClient()
        self.assertEqual(client.getTicket("AAPL"), None)


class TestCoinmarketcapClient(unittest.TestCase):
    def test_get_ticket(self):
        client = coinmarketcapClient()
        self.assertEqual(client.getTicket("AAPL"), None)


class TestStockExchange(unittest.TestCase):
    @patch.object(stockClients, 'yahooClient', spec=yahooClient)
    def test_get_stock_prices(self, yahoo_client):
        response = [{"name": "AAPL", "ticket": "AAPL"}]
        yahoo_client.getTickets = MagicMock(return_value=response)
        client = stockExchange({"name": "yahoo", "tickets": response})
        self.assertEqual(client.getStockPrices(), ["test"])

    def test_get_stock_prices_with_none_client(self):
        client = stockExchange({"name": "yahoo", "tickets": []})
        self.assertEqual(client.getStockPrices(), [])


class TestStockClient(unittest.TestCase):
    @patch.object(stockExchange, 'getStockPrices')
    def test_get_current_prices(self, mock_get_price):
        mock_get_price.return_value = ["test"]
        result = stockClient().getCurrentPrices()
        self.assertEqual(result, [["test"]])


if __name__ == "__main__":
    unittest.main()
