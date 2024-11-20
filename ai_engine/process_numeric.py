from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage


def parse_output(output: AIMessage):
    try:
        return float(output.content)
    except ValueError:
        return None


def run_completion_for_numeric(content, engine_object):
    prompt = engine_object.get("prompt")
    prompt_key = "invocation_prompt"
    content_key = "content"
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
