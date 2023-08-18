import openai
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

from transcriber import Transcriber
from llm import LLM
from tts import TTS
from command import Command

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/openai")
def openai():
    openai.api_key = request.get_json()

    return {"result": "ok"}


@app.post("/audio")
def audio():
    if os.path.exists("./static/response.mp3"):
        os.remove("./static/response.mp3")

    audio = request.files.get("audio")

    transcribed = Transcriber()
    text = transcribed.transcribe(audio)

    llm = LLM()
    function_name, args, message = llm.process_function(text)

    if function_name is not None:
        tts_file = Command().execute(function_name, args)

        return {"result": "ok", "text": message.get("content"), "file": tts_file}

    else:
        tts_file = TTS().process(message.get("content"))
        return {"result": "ok", "text": message.get("content"), "file": tts_file}
