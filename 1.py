import os
import datetime
import csv
import pytz
import azure.cognitiveservices.speech as speechsdk
#from openai import OpenAI
import openai

# Azure Speech configuration
SPEECH_KEY = "55d11eb5446d48caa11abbd23a6abddf"
SPEECH_REGION = "eastus"

import os

import openai
openai.api_key = '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'
os.environ["OPENAI_API_KEY"] = "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"

# Initialize OpenAI client
#openai_client = OpenAI()

def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    else:
        print("Sorry, I did not understand that.")
        # Return an empty string instead of None to avoid AttributeError when calling .lower()
        return ""

def text_to_speech(text: str):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()

def generate_summary(chat_history):
    # Logic to generate summary from chat history
    lines = chat_history.split('\n')
    summary = "Conversation Summary:\n"
    for line in lines:
        if line.startswith("Customer:") or line.startswith("Chatbot:"):
            summary += line + "\n"
    return summary

def get_current_time():
    timezone = pytz.timezone("America/Los_Angeles")
    now = datetime.datetime.now(timezone)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def read_prompt_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        prompt_parts = []
        for row in reader:
            question = row['Questions']
            answer = row['Answers']
            prompt_parts.append(f"{question}: {answer}")
        return "\n".join(prompt_parts)

def chatbot_response(message, chat_history, summary, current_time, prompt):
    # Corrected to use the full_prompt which includes the latest message.
    full_prompt = f"""
    Current Time: {current_time}
    {prompt}
    {chat_history}
    Customer: {message}
    Agent:"""

    chat_history += f"\nCustomer: {message}"

    # Call OpenAI GPT-3 API to generate response using the full_prompt
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=full_prompt,  # Corrected to use full_prompt instead of prompt
        temperature=0.5,
        max_tokens=150,
        stop=["\n", " Agent:", " Customer:"]
    )

    if response.choices:
        chatbot_reply = response.choices[0].text.strip()
    else:
        chatbot_reply = "No response generated."

    chat_history += f"\nChatbot: {chatbot_reply}"

    return chatbot_reply, chat_history

chat_history = ""
summary = ""
prompt_file_path = "pool-cleaning-prompt.csv"
prompt = read_prompt_from_csv(prompt_file_path)

while True:
    current_time = get_current_time()
    
    customer_question_raw = from_mic()

    # Check if customer_question_raw is not None before proceeding
    if customer_question_raw is not None:
        customer_question = customer_question_raw.lower()  # Convert to lowercase for comparison
        
        # if "thank you" in customer_question or "bye" in customer_question:
        if "bye" in customer_question:
            summary = generate_summary(chat_history)
            print("summary>>>>>>>>>>", summary)
            text_to_speech("You're welcome! Goodbye!")
            print("Chatbot: You're welcome! Goodbye!")
            break

        chatbot_reply, chat_history = chatbot_response(customer_question, chat_history, summary, current_time, prompt)
        
        # Speak response
        text_to_speech(chatbot_reply)
        
        print("Chatbot:", chatbot_reply)
    else:
        print("Please try speaking again.")
