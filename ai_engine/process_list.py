from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List


class ListModel(BaseModel):
    items: List[str]


extraction_prompt = """Be sure to return a valid json NOT encapsulated in markdown. Never use the invalid escape sequence \'
The output should be a JSON object with a single key 'items' containing an array of strings.

Formatting Instructions: {format_instructions}"""


def run_completion_for_list(content, engine_object):
    prompt = engine_object.get("prompt")
    parser = JsonOutputParser(pydantic_object=ListModel)

    content_key = 'content'
    prompt_key = 'invocation_prompt'

    prompts = ChatPromptTemplate.from_messages(
        [
            ("user", "{" + content_key + "}"),
            ("user", "{" + prompt_key + "}"),
            ("user", extraction_prompt),
        ]
    )

    return {
        "prompts": prompts,
        "parser": parser,
        "args": {
            "format_instructions": parser.get_format_instructions(),
            prompt_key: prompt,
            content_key: content,
        },
    }
