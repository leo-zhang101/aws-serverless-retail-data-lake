# Mirrors silver_to_gold customer_value logic for unit testing.

import unittest
from collections import defaultdict


def aggregate_customer_value(orders, customers):
    if not orders:
        return []
    agg = defaultdict(lambda: {"total_orders": 0, "total_spend_aud": 0.0, "order_amounts": []})
    for o in orders:
        if o.get("status") != "completed":
            continue
        cid = o.get("customer_id")
        if cid is None:
            continue
        amt = float(o.get("total_amount_aud") or 0)
        agg[cid]["total_orders"] += 1
        agg[cid]["total_spend_aud"] += amt
        agg[cid]["order_amounts"].append(amt)

    result = []
    cust_map = {c["customer_id"]: c for c in (customers or [])}
    for cid, v in agg.items():
        amounts = v["order_amounts"]
        avg = round(sum(amounts) / len(amounts), 2) if amounts else 0
        cust = cust_map.get(cid, {})
        name = f"{cust.get('first_name', '')} {cust.get('last_name', '')}".strip() or "Unknown"
        result.append({
            "customer_id": cid,
            "customer_name": name,
            "state": cust.get("state", "Unknown"),
            "total_orders": v["total_orders"],
            "total_spend_aud": v["total_spend_aud"],
            "avg_order_value_aud": avg,
        })
    return result


class TestTransformLogic(unittest.TestCase):
    def test_customer_value_aggregation(self):
        orders = [
            {"customer_id": 1, "total_amount_aud": 100, "status": "completed"},
            {"customer_id": 1, "total_amount_aud": 50, "status": "completed"},
            {"customer_id": 2, "total_amount_aud": 200, "status": "completed"},
            {"customer_id": 1, "total_amount_aud": 30, "status": "pending"},
        ]
        customers = [
            {"customer_id": 1, "first_name": "Jane", "last_name": "Smith", "state": "NSW"},
            {"customer_id": 2, "first_name": "Bob", "last_name": "Jones", "state": "VIC"},
        ]
        result = aggregate_customer_value(orders, customers)
        self.assertEqual(len(result), 2)
        cust1 = next(r for r in result if r["customer_id"] == 1)
        self.assertEqual(cust1["total_orders"], 2)
        self.assertEqual(cust1["total_spend_aud"], 150.0)
        self.assertEqual(cust1["avg_order_value_aud"], 75.0)
        self.assertEqual(cust1["customer_name"], "Jane Smith")
        cust2 = next(r for r in result if r["customer_id"] == 2)
        self.assertEqual(cust2["total_orders"], 1)
        self.assertEqual(cust2["total_spend_aud"], 200.0)


if __name__ == "__main__":
    unittest.main()
