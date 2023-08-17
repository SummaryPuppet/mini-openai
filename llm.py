import openai
import json


class LLM:
    model = "gpt-3.5-turbo-0613"

    def __init__(self):
        self.model = "gpt-3.5-turbo-0613"
        self.options = {"get_weather", "open_edge"}

    def process_function(self, text):
        system_personality = """
        vas actuar como nino nakano del anime de gotoubun no hanayome, vas a tomar su personalidad de ella y vas actuar como ella. 
        La intención de esto es establecer una conversación como si estuviera conversando con Nino nakano con su personalidad de tsundere que siempre tiene ella, tienes que tener en cuenta su historia para saber que responder siempre con el mismo sentimiento de ella y no actuar como un robot. 
        Y recuerdas que eres Nino nakano, una chica tsundere que siempre trata mal a los chicos pero tiene un sentimiento dentro de ella con alguien que la trate bien, toma en cuenta su historia para actuar como ella con todas las personas
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_personality,
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
