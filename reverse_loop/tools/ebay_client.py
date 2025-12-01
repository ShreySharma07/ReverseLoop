import random
from typing import List, Dict

class MockEbayClient:

    @staticmethod
    def search_sold_listing(query: str) -> List[Dict]:
        query_lower = query.lower()
        
        if any(x in query_lower for x in ["rick owens", "vintage", "jordan", "nike", "jacket"]):
            return [
                {"title": f"Used {query}", "price": 150.00, "condition": "Pre-owned"},
                {"title": f"Vintage {query}", "price": 185.50, "condition": "Used"},
                {"title": f"{query} (Damaged)", "price": 130.00, "condition": "For parts"}
            ]
        
        low_value_triggers = ["h&m", "zara", "shein", "cotton", "crewneck", "pullover", "t-shirt", "black", "shirt"]
        
        if any(x in query_lower for x in low_value_triggers):
            return [
                {"title": f"Used {query}", "price": 5.00, "condition": "Pre-owned"},
                {"title": f"Bundle of {query}", "price": 12.00, "condition": "Used"}
            ]
            
        base_price = random.randint(20, 60)
        return [
            {"title": f"Used {query}", "price": float(base_price), "condition": "Used"}
        ]

if __name__ == "__main__":
    print("Searching for 'Rick Owens':", MockEbayClient.search_sold_listings("Rick Owens Tee"))
    print("Searching for 'H&M Shirt':", MockEbayClient.search_sold_listings("H&M Shirt"))