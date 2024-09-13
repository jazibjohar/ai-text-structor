from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from key_helper import get_content_and_invocation_key


def parse_output(output: AIMessage):
    try:
        return float(output.content)
    except ValueError:
        return None


def run_completion_for_numeric(content, engine_object, parent=None):
    prompt = engine_object.get("prompt")
    content_key, prompt_key = get_content_and_invocation_key(parent)
    prompts = ChatPromptTemplate.from_messages(
        [
            ("user", "{" + content_key + "}"),
            ("user", "{" + prompt_key + "}"),
            ("user", "output only numeric value"),
        ]
    )
    args = {
        prompt_key: prompt,
        content_key: content,
    }

    return {
        "prompts": prompts,
        "parser": parse_output,
        "args": args,
    }
