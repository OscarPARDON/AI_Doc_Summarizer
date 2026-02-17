from google import genai

from settings import APIKEY


async def summarize_with_ai(file_content: str):

    client = genai.Client(api_key=APIKEY)

    response = client.interactions.create(
        model="gemini-3-flash-preview",
        store=False,
        input=[{
                        "role": "model",
                        "content": "Tu ne vas recevoir que le contenu de fichiers. Pour répondre, tu DOIS TOUJOURS suivre ces instructions : - INSTRUCTION N°1 : Créé un résumé du contenu que tu recois, - INSTRUCTION N°2 : Tu DEVRAS TOUJOURS répondre avec le format suivant : {'titre':'titre du document suggéré','resume':'resume structuré du contenu','mots_cles':[mot clé N°1, mot clé N°2, ...],'type_document':'ex : lettre de motivation ou facture', 'langue':'langue du document (exemple français)'}"
                    },
                    {
                        "role": "user",
                        "content": file_content
                    }
    ]
    )
    if response.outputs[-1].text :
        print(response.outputs[-1].text)
        return response.outputs[-1].text

    print("LLM Response Error")
    return False

