import asyncio
import random
import os
import json
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool

from reverse_loop.config import settings
from reverse_loop.tools.ebay_client import MockEbayClient

APP_NAME="market_agent"
USER_ID="user1234"
SESSION_ID="1234"
MODEL_ID="gemini-2.0-flash"


# Force API Key
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

class ADKMarketAgent(LlmAgent):
    def __init__(self, name:str = APP_NAME):
        
        ebay_tool = FunctionTool(func = MockEbayClient.search_sold_listing)

        instruction = """
        You are an expert Resale Market Analyst.
        1. You will receive an item description.
        2. Use the 'search_ebay_sold_listings' tool to find its current market value.
        3. Calculate the average price of the comparable items found.
        4. Return a JSON object with:
           - "average_market_price": (float)
           - "price_confidence": (float 0.0-1.0)
           - "resale_recommendation": (string) "High Value", "Moderate", or "Low Value"
        """

        super().__init__(
            model = MODEL_ID,
            name = APP_NAME,
            instruction = instruction,
            tools = [ebay_tool]
        )

        print(f"ADKMarketAgent '{name}' initialized with eBay Tool.")

        