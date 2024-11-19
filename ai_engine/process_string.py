from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def run_completion_for_string(content, engine_object):
    prompt = engine_object.get("prompt")

    content_key = 'content'
    prompt_key = 'invocation_prompt'
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
