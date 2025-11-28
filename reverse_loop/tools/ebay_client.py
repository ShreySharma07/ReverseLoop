import random
from typing import List, Dict

class MockEbayClient:

    @staticmethod
    def search_sold_listing(query: str)->List[dict]:

        query_lower = query.lower()

        if 'rick owens' in query_lower or 'vintage' in query_lower or 'jordan' in query_lower:
            return {
                {"title": f"Used {query}", "price": 150.00, "condition": "Pre-owned"},
                {"title": f"Vintage {query} - Distressed", "price": 185.50, "condition": "Used"},
                {"title": f"{query} (Torn/Damaged)", "price": 130.00, "condition": "For parts"}
            }
        
        elif "h&m" in query_lower or "shein" in query_lower or "zara" in query_lower:
            return [
                {"title": f"Used {query}", "price": 5.00, "condition": "Pre-owned"},
                {"title": f"Bundle of {query}", "price": 12.00, "condition": "Used"}
            ]
        
        else:
            base_price = random.randint(20, 60)
            return [
                {"title": f"Used {query}", "price": float(base_price), "condition": "Used"},
                {"title": f"{query} Good Cond", "price": float(base_price + 10), "condition": "Used"}
            ]

if __name__ == "__main__":
    print("Searching for 'Rick Owens':", MockEbayClient.search_sold_listings("Rick Owens Tee"))
    print("Searching for 'H&M Shirt':", MockEbayClient.search_sold_listings("H&M Shirt"))