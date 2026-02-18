import json
import re
from google import genai
from settings import APIKEY


async def summarize_with_ai(file_content: str):

    client = genai.Client(api_key=APIKEY)

    response = client.interactions.create(
        model="gemini-3-flash-preview",
        store=False,
        input=[
            {
                "role": "model",
                "content": """Tu ne vas recevoir que le contenu de fichiers.
Tu DOIS répondre UNIQUEMENT avec du JSON valide.
Ne mets PAS de ```json.
Ne mets PAS de texte avant ou après.
Format EXACT attendu :
{
  "titre": "...",
  "resume": "...",
  "mots_cles": ["..."],
  "type_document": "...",
  "langue": "..."
}"""
            },
            {
                "role": "user",
                "content": file_content
            }
        ]
    )

    if response.outputs[-1].text:
        raw_text = response.outputs[-1].text.strip()

        cleaned = re.sub(r"^```json|```$", "", raw_text, flags=re.MULTILINE).strip()

        try:
            parsed_json = json.loads(cleaned)
            return parsed_json
        except json.JSONDecodeError as e:
            print("Erreur JSON:", e)
            print("Contenu reçu:", cleaned)
            return False

    return False
