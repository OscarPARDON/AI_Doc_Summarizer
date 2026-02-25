import json
import logging
import re
from typing import Union
from google import genai
from settings import APIKEY, MODEL_PROMPT

logger = logging.getLogger(__name__)

async def summarize_with_ai(file_content: str) -> Union[str, bool] :
    """ Send the content of the file to the AI API for summarization, return the result"""

    try :
        client = genai.Client(api_key=APIKEY)
        # Call to the gemini API
        response = client.interactions.create(
            model="gemini-3-flash-preview",
            store=False,
            input=[
                {
                    "role": "model",
                    "content": MODEL_PROMPT
                },
                {
                    "role": "user",
                    "content": file_content
                }
            ]
        )
    except Exception as e:
        logger.exception(msg=f"Error in gemini api call : {e}")
        return False

    # Extract and clean the response
    if response.outputs[-1].text:
        raw_text = response.outputs[-1].text.strip()
        cleaned = re.sub(r"^```json|```$", "", raw_text, flags=re.MULTILINE).strip()

        # Try to convert the response into a JSON
        try:
            parsed_json = json.loads(cleaned)
            return parsed_json
        except json.JSONDecodeError as e:
            logger.exception(msg=f"Gemini response serializing error : {e}")
            return False

    logger.warning(msg="Empty response from gemini API")
    return False