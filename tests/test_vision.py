import pytest
import json
from pathlib import Path
from reverse_loop.agents.vision import ADKVisionAgent

# --- 1. Unit Test: Logic Only (No API) ---
def test_json_cleaning_logic():
    """
    Verifies that the agent can strip Markdown backticks
    and parse JSON, even if the LLM is chatty.
    """
    agent = ADKVisionAgent()
    
    # Simulate a messy response from the LLM
    messy_output = """
    Here is the analysis of your image:
    ```json
    {
        "item_name": "Test Shoe",
        "condition_grade": 8
    }
    ```
    Hope this helps!
    """
    
    # We test the private method directly
    cleaned = agent._clean_json_text(messy_output)
    
    assert cleaned["item_name"] == "Test Shoe"
    assert cleaned["condition_grade"] == 8

# --- 2. Integration Test: Real API Call ---
@pytest.mark.skipif(not Path("data/inputs/test_shoe.jpg").exists(), reason="No test image found")
def test_vision_analysis_live():
    """
    Actually calls Gemini. Only runs if you have a test image.
    """
    agent = ADKVisionAgent()
    image_path = "data/inputs/test_shoe.jpg"
    
    result = agent.analyze_image(image_path)
    
    # We check the STRUCTURE, not the exact values (since AI changes)
    assert "item_name" in result
    assert "condition_grade" in result
    assert isinstance(result["detected_defects"], list)
    
    # Sanity check: Grade should be between 1 and 10
    assert 1 <= result["condition_grade"] <= 10