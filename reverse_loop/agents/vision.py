from reverse_loop.config import settings
import json
import re
from pathlib import Path
from PIL import Image
import base64
from google import genai
import google
import os
from io import BytesIO
from google.adk.agents import LlmAgent, Runner
from google.genai import types

google_api_key = settings.GOOGLE_API_KEY

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
            name = name,
            model = "gemini-2.5-flash",
            instruction = instruction
        )
        print(f"ADKVisionAgent '{name}' initialized with model: {self.model}")