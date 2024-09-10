
from models import get_open_ai_model, get_google_generative_ai_model, get_mistral
from build_model import build_pydantic_model,load_json
from langchain_core.output_parsers import JsonOutputParser
from completion import run_completion

models = {
    'gpt-4o': get_open_ai_model(),
    'gemini-1.5-pro': get_google_generative_ai_model(),
    'mistral-7b': get_mistral()
}
def process(request):
    request_json = request.get_json()
    model = request_json.get('model')
    if model not in models:
        return {"error": "Invalid model"}, 400
    # content = request_json.get('content')
    
    prompt_config = load_json('example_model.json')
    DynamicModel = build_pydantic_model(prompt_config["attributes"])
    parser = JsonOutputParser(pydantic_object=DynamicModel)
    return run_completion(
        models[request_json.get('model')],
        parser,
        request_json.get('content'),
        prompt_config["invocation_prompt"]
    )