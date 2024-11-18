import json
from pydantic_core import from_json
from pydantic import Field, create_model
from typing import Annotated

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from key_helper import get_content_and_invocation_key

extraction_prompt = """Be sure to return a valid json NOT encapsulated in markdown.  Never use the invalid escape sequence \'

Formatting Instructions: {format_instructions}"""


def build_pydantic_model(attributes):
    obj = from_json(json.dumps(attributes), allow_partial=True)
    annotated_fields = {}
    for key, value in obj.items():
        annotated_fields[key] = Annotated[type(value), Field(description=value)]
    DynamicModel = create_model("DynamicModel", **annotated_fields)
    return DynamicModel


def run_completion_for_object(content, engine_object, parent=None):
    invocation_prompt = engine_object.get("prompt")
    attributes = engine_object.get("attributes")
    DynamicModel = build_pydantic_model(attributes)
    parser = JsonOutputParser(pydantic_object=DynamicModel)

    content_key, prompt_key = get_content_and_invocation_key(parent)
    
    extraction_prompt.format(format_instructions=parser.get_format_instructions())

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
            prompt_key: invocation_prompt,
            content_key: content,
        },
    }
