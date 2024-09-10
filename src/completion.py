import json
from langchain_core.prompts import ChatPromptTemplate

extraction_prompt = """Be sure to return a valid json NOT encapsulated in markdown.  Never use the invalid escape sequence \'

Formatting Instructions: {format_instructions}"""

def run_completion(model, parser, content, invocation_prompt):
    string_prompt = ChatPromptTemplate.from_messages([
        ("system", content),
        ("user", "{input}")
    ])
    string_chain = string_prompt | model
    string_output = string_chain.invoke({"input": invocation_prompt})
    
    parse_prompt = ChatPromptTemplate.from_messages([
        ("system", extraction_prompt),
        ("user", "{phrase}")
    ])
    parse_chain = parse_prompt | model
    parsed_output = parse_chain.invoke({
        "phrase": string_output,
        "format_instructions": parser.get_format_instructions(),
    })
    return json.loads(parsed_output.content)