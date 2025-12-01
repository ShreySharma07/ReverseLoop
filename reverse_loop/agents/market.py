import asyncio
import random
import os
import json
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.genai import types

from reverse_loop.config import settings
from reverse_loop.tools.ebay_client import MockEbayClient

APP_NAME="agents"
USER_ID="user1234"
SESSION_ID = "session_market_01"
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

    def analyze_market_value(self, item_description: str)->dict:
        return asyncio.run(self._analyze_async(item_description))
    
    async def _analyze_async(self, item_description: str) -> dict:

        session_service = InMemorySessionService()
        await session_service.create_session(app_name = APP_NAME,user_id = USER_ID,session_id = SESSION_ID)

        runner = Runner(agent = self, app_name = APP_NAME, session_service = session_service)

        final_text = ""
        print(f"Searching market for: {item_description}...")

        user_msg = types.Content(
            role = 'user',
            parts = [types.Part(text=f"Find market value for: {item_description}")]
        )

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=user_msg
        ):
            if event.content and event.content.parts:
                part = event.content.parts[0]
                if part.text:
                    final_text += part.text
        
        try:
            import re
            match = re.search(r"(\{.*\})", final_text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return json.loads(final_text)
        except:
            return {"error": "Failed to parse market data", "raw": final_text}

if __name__ == "__main__":
    agent = ADKMarketAgent()
    
    print("\n--- TEST 1: Rick Owens ---")
    result = agent.analyze_market_value("Rick Owens Raw War Distressed T-shirt")
    print(json.dumps(result, indent=2))
    
    print("\n--- TEST 2: Old H&M Shirt ---")
    result = agent.analyze_market_value("H&M Cotton T-Shirt")
    print(json.dumps(result, indent=2))