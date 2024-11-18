import functions_framework
from flask import jsonify
from models import get_open_ai_model, get_google_generative_ai_model, get_mistral
from engine_config import load_json
from completion import run_completion
from pydantic import BaseModel

models = {
    "gpt-4": get_open_ai_model(),
    "gemini-1.5-pro": get_google_generative_ai_model(),
    "mistral-7b": get_mistral(),
}


class ProcessRequest(BaseModel):
    model: str
    content: str


engine_config = load_json("engine.json")


def process(model, content):
    return run_completion(models[model], content, engine_config)


@functions_framework.http
def process_request(request):
    try:
        request_json = request.get_json()
        req = ProcessRequest(**request_json)

        if not req.model:
            req.model = "gemini-1.5-pro"
        elif req.model not in models:
            return jsonify({"error": "Invalid model"}), 400

        result = process(req.model, req.content)

        return jsonify(result), 200

    except (ValueError, KeyError) as e:  # For JSON parsing and dict access errors
        return jsonify({"error": str(e)}), 400
    except (RuntimeError, TypeError) as e:  # Handle specific operational errors
        print(f"Operation error: {str(e)}")
        return jsonify({"error": "Operation failed"}), 500
