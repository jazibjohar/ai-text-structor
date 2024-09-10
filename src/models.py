import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI


def get_open_ai_model():
    return ChatOpenAI(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        model_name='gpt-4o'
    )

def get_google_generative_ai_model():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=os.getenv('GOOGLE_AI_API_KEY'),
    )
    
def get_mistral():
    return ChatMistralAI(
        mistral_api_key=os.getenv('MISTRAL_AI_API_KEY'),
        model='open-mistral-7b'
    )