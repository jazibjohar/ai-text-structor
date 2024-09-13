from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from key_helper import get_content_and_invocation_key
from operator import itemgetter
from langchain_core.messages import AIMessage



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


def build_output_expectations(engine_object):
    all_keys = list(map(itemgetter(0), engine_object.items()))
    # removing prompt key and explanation key
    all_intents = [key for key in all_keys if key != "prompt" and key != "explanation"]
    # if sub intents have explaination then build a dictionary of sub intents with explaination
    intents_with_explanation = [
        intent
        for intent in all_intents
        if engine_object[intent].get("explanation") is not None
    ]
    # constructing prompt for ai model to tell model to return key if the content matches explanation for the key

    key_explanation_text = ""
    for intent in intents_with_explanation:
        key_explanation_text += (
            f"Key: {intent} Explanation: {engine_object[intent].get('explanation')}\n"
        )

    key_explanation_text += "Only return one key value in the result from the keys mentioned above if the content matches the explanation for the key. No explanation is needed"
    return key_explanation_text

def parse_key(output: AIMessage):
    try:
        return output.content.replace('Key:','').strip()
    except ValueError:
        return None

def run_for_intent_extraction(content, engine_object):
    prompt = engine_object.get("prompt")
    content_key = "content"
    prompt_key = "invocation_prompt"

    output_expectation = build_output_expectations(engine_object)

    prompts = ChatPromptTemplate.from_messages(
        [
            ("user", "{" + content_key + "}"),
            ("user", "{" + prompt_key + "}"),
            ("user", output_expectation),
        ]
    )
    return {
        "prompts": prompts,
        "parser": parse_key,
        "args": {
            prompt_key: prompt,
            content_key: content,
        },
    }
