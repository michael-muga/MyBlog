import unittest
from app.models import Quote

class TestQuote(unittest.TestCase):
    def setUp(self):
        self.quote = Quote("Cheborgei", "Tomorrow is never promised")

    def test_instance(self):
        self.assertTrue(isinstance(self.quote, Quote))

    def test_init(self):
        self.assertEqual(self.quote.author, "Cheborgei")
        self.assertEqual(self.quote.quote, "Tomorrow is never promised")