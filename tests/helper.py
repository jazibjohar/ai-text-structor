import os
import json
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from ai_text_structor.ai_text_structor import AITextStructor
import asyncio


def get_open_ai_model():
    return ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o")


def get_google_generative_ai_model():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=os.getenv("GOOGLE_AI_API_KEY"),
    )


def get_mistral():
    return ChatMistralAI(
        mistral_api_key=os.getenv("MISTRAL_AI_API_KEY"), model="open-mistral-7b"
    )


def load_json(file_path):
    with open(file_path, encoding="utf-8") as json_data:
        d = json.load(json_data)
        json_data.close()
        return d


models = {
    "gpt-4": get_open_ai_model(),
    "gemini-1.5-pro": get_google_generative_ai_model(),
    "mistral-7b": get_mistral(),
}


engine_config = load_json("engine.json")


def run_completion(model, content, engine_object):
    engine = AITextStructor(engine_object, model)

    async def execute_with_timing():
        start_time = asyncio.get_event_loop().time()
        result = await engine.execute(content)
        end_time = asyncio.get_event_loop().time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        return result

    return asyncio.run(execute_with_timing())


def process(model, content):
    return run_completion(models[model], content, engine_config)
