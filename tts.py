from dotenv import load_dotenv
import os
import requests


class TTS:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv("ELEVENLABS_API_KEY")

    def process(self, text: str):
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/jsCqWAovK2LkecY7zXl4"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.key,
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        }

        filename = "response.mp3"

        response = requests.post(url, json=data, headers=headers)

        with open("static/" + filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        return filename
