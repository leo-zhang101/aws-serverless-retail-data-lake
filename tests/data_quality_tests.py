import unittest

class TestDataQuality(unittest.TestCase):

    def test_orders_amount_positive(self):
        amount = 10
        self.assertGreater(amount, 0)

    def test_customer_id_not_null(self):
        customer_id = "C123"
        self.assertIsNotNone(customer_id)

    def test_order_id_unique(self):
        order_ids = [1,2,3,4]
        self.assertEqual(len(order_ids), len(set(order_ids)))

if __name__ == "__main__":
    unittest.main()
