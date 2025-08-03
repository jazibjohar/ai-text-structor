"""Module for processing lists using LangChain with JSON output parsing."""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List
from langchain_core.messages import AIMessage


class ListModel(BaseModel):
    """Pydantic model for list items output."""

    items: List[str]


parser = JsonOutputParser(pydantic_object=ListModel)


def items_only_parser(output: AIMessage) -> List[str]:
    """
    Parse AIMessage output and extract items list.

    Args:
        output (AIMessage): The AI message containing JSON response

    Returns:
        List[str]: Extracted list of items
    """
    parsed = parser.parse(output.content)
    return parsed["items"]


EXTRACTION_PROMPT = """Be sure to return a valid json NOT encapsulated in markdown. Never use the invalid escape sequence \'
The output should be a JSON object with a single key 'items' containing an array of strings.

Formatting Instructions: {format_instructions}"""


def run_completion_for_list(content: str, engine_object: dict) -> dict:
    """
    Prepare completion parameters for list processing.

    Args:
        content (str): The content to process
        engine_object (dict): Configuration for the engine

    Returns:
        dict: Configuration for running the completion
    """
    prompt = engine_object.get("prompt")

    content_key = "content"
    prompt_key = "invocation_prompt"

    prompts = ChatPromptTemplate.from_messages(
        [
            ("user", "{" + content_key + "}"),
            ("user", "{" + prompt_key + "}"),
            ("user", EXTRACTION_PROMPT),
        ]
    )

    return {
        "prompts": prompts,
        "parser": items_only_parser,  # Use the wrapper parser instead
        "args": {
            "format_instructions": parser.get_format_instructions(),
            prompt_key: prompt,
            content_key: content,
        },
    }
