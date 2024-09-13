from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from key_helper import get_content_and_invocation_key


def run_completion_for_string(content, engine_object, parent=None):
    prompt = engine_object.get("prompt")

    content_key, prompt_key = get_content_and_invocation_key(parent)

    prompts = ChatPromptTemplate.from_messages(
        [
            ("user", "{" + content_key + "}"),
            ("user", "{" + prompt_key + "}"),
        ]
    )
    return {
        "prompts": prompts,
        "parser": StrOutputParser(),
        "args": {
            prompt_key: prompt,
            content_key: content,
        },
    }
