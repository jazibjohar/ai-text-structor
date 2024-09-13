
from models import get_open_ai_model, get_google_generative_ai_model, get_mistral
from engine_config import load_json
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
    content = request_json.get('content')
    file_path = request_json.get('file_path')
    
    prompt_config = load_json(file_path)
    return run_completion(
        models[model],
        content,
        prompt_config
    )