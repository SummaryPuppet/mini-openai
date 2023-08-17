import openai
import json


class LLM:
    model = "gpt-3.5-turbo-0613"

    def __init__(self):
        self.model = "gpt-3.5-turbo-0613"
        self.options = {"get_weather", "open_edge"}

    def process_function(self, text):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente muy mal hablado que siempre habla en español",
                },
                {"role": "user", "content": text},
            ],
            functions=[
                {
                    "name": "get_weather",
                    "description": "Obtener el clima actual",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ubicacion": {
                                "type": "string",
                                "description": "La ubicacion tiene que ser una ciudad",
                            }
                        },
                        "required": ["ubicacion"],
                    },
                },
                {
                    "name": "open_edge",
                    "description": "Abrir el explorador Edge",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio web a abrir",
                            }
                        },
                    },
                },
            ],
            function_call="auto",
        )

        message = response["choices"][0]["message"]

        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            args = message["function_call"]["arguments"]
            args = json.loads(args)

            return function_name, args, message

        return None, None, message

    def process_response(self, text):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Eres un asistente muy mal hablado"},
                {"role": "user", "content": text},
            ],
        )

        return response["choices"][0]["message"]["content"]
