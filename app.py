from fastapi import FastAPI, HTTPException
import os
import datetime
import pytz
import openai
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechRecognizer

app = FastAPI()

# Replace these with your actual keys and paths
SPEECH_KEY = "55d11eb5446d48caa11abbd23a6abddf"
SPEECH_REGION = "eastus"
OPENAI_API_KEY = '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'

# Configure API keys
openai.api_key = OPENAI_API_KEY

# Initialize chat history
chat_history = ""
summary = ""

@app.get("/")
async def read_root():
    return {"message": "Chatbot Service is Running"}

@app.post("/chat/")
async def chat(message: str):
    global chat_history, summary
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    current_time = get_current_time()
    chatbot_reply, chat_history = chatbot_response(message, chat_history, summary, current_time, prompt="")
    
    return {"message": message, "reply": chatbot_reply}

def chatbot_response(message, chat_history, summary, current_time, prompt):
    # Simplified for demonstration, integrate your logic here
    full_prompt = f"{message}"
    
    # Assuming a simple echo function for demonstration
    chatbot_reply = f"Echo: {message}"

    return chatbot_reply, chat_history + "\n" + f"Customer: {message}\nChatbot: {chatbot_reply}"

def get_current_time():
    timezone = pytz.timezone("America/Los_Angeles")
    now = datetime.datetime.now(timezone)
    return now.strftime("%Y-%m-%d %H:%M:%S")
