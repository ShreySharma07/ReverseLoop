
import json
import re
import asyncio
from pathlib import Path
from PIL import Image
from io import BytesIO
import os

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.genai import types

from reverse_loop.config import settings
from google.adk.sessions import InMemorySessionService

os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

class ADKVisionAgent(LlmAgent):
    def __init__(self, name: str = 'VisionInspector'):
        instruction = (
            "Act as an expert warehouse inspector and data translator. "
            "Your sole task is to analyze the provided item image and output a single, raw JSON object."
            "The JSON object MUST contain the following fields: "
            "'item_name' (string, specific name and model), "
            "'brand' (string, manufacturer name), "
            "'condition_grade' (integer 1-10, 10 is perfect), "
            "'detected_defects' (list of strings, e.g., ['tear', 'stain']), and "
            "'estimated_era' (string, e.g., '1990s', 'Modern')."
            "DO NOT include any conversational text, markdown formatting (like ```json`), or explanation."
        )

        super().__init__(
            name=name,
            model="gemini-2.5-pro", 
            instruction=instruction
        )
        print(f"ADKVisionAgent '{name}' initialized.")

    def _clean_json_text(self, text: str) -> dict:
        """
        Parses the JSON string into a Dictionary.
        """
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            json_str = text.strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return {"error": "JSON_PARSE_FAILED", "raw_output": text}

    def analyze_image(self, image_path: str) -> dict:
        """
        Synchronous wrapper to run the async analysis.
        This matches what your test expects: agent.analyze_image()
        """
        return asyncio.run(self._analyze_image_async(image_path))

    async def _analyze_image_async(self, image_path: str) -> dict:
        session_service = InMemorySessionService()
        
        await session_service.create_session(app_name = 'agents', user_id = "user_01",session_id="session_01")
        
        runner = Runner(
            agent=self, 
            app_name="agents", 
            session_service=session_service
        )
        
        try:
            path_obj = Path(image_path)
            if not path_obj.exists():
                return {"error": f"File not found: {image_path}"}

            img = Image.open(path_obj)
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()
            
            user_message = types.Content(
                role="user",
                parts=[
                    types.Part(text="Analyze this item and provide the structured output immediately."),
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                ]
            )
        except Exception as e:
            return {"error": f"Image prep failed: {e}"}

        final_text = ""
        
        async for event in runner.run_async(
            user_id="user_01",
            session_id="session_01",  
            new_message=user_message
        ):
            if event.content and event.content.parts:
                part = event.content.parts[0]
                if part.text:
                    final_text += part.text

        return self._clean_json_text(final_text)

if __name__ == "__main__":
    TEST_IMAGE_PATH = "data/inputs/shirt_torn.jpeg"
    Path("data/inputs").mkdir(parents=True, exist_ok=True)
    
    # if not Path(TEST_IMAGE_PATH).exists():
    #     img = Image.new('RGB', (100, 100), color = 'red')
    #     img.save(TEST_IMAGE_PATH)

    vision_agent = ADKVisionAgent()
    
    final_data = vision_agent.analyze_image(TEST_IMAGE_PATH)

    print("\n--- FINAL OUTPUT ---")
    print(json.dumps(final_data, indent=4))