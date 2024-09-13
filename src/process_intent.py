from langchain_core.runnables import RunnableParallel
from prompt_engine import prompt_builder_by_type
from operator import itemgetter
from process_string import run_for_intent_extraction


def get_keys(dict):
    all_keys = list(map(itemgetter(0), dict.items()))
    # removing prompt key
    return [key for key in all_keys if key != "prompt" and key != "explanation"]


def get_builder_for_intent(model, content, engine_object):
    aggregated_result, _ = _process_for_intent(model, content, engine_object)
    return aggregated_result


def _get_sub_intent_for_condition(model, content, engine_object):
    builder = run_for_intent_extraction(content, engine_object)
    chain = builder["prompts"] | model | builder["parser"]
    results = chain.invoke(builder["args"])
    return [results]


def _process_for_intent(
    model, content, engine_object, parent_key=None, parent_result=None
):
    if parent_result is None:
        parent_result = {}
    if len(engine_object) == 0:
        return None, None

    intents_list = get_keys(engine_object)

    # sub intents are objects without type
    sub_intents = [
        intent for intent in intents_list if engine_object[intent].get("type") is None
    ]
    attributes_for_extraction = [
        intent for intent in intents_list if intent not in sub_intents
    ]
    master_chains = {}
    master_args = {}
    for attribute in attributes_for_extraction:
        prompt_type = engine_object[attribute].get("type")
        executor = prompt_builder_by_type[prompt_type]
        builder = executor(content, engine_object[attribute], attribute)
        chain = builder["prompts"] | model | builder["parser"]
        master_chains[attribute] = chain
        master_args.update(builder["args"])

    master_args.update(parent_result)
    master_chains_executor = RunnableParallel(**master_chains)
    results = master_chains_executor.invoke(master_args)
    if parent_key is None:
        parent_result.update(results)

    # check if conditional intent
    prompt = engine_object.get("prompt")

    conditional_intents = []
    if prompt is not None:
        conditional_intents = _get_sub_intent_for_condition(
            model, content, engine_object
        )

    for conditional_intent in conditional_intents:
        conditional_engine_object = engine_object[conditional_intent]
        _, sub_intent_result = _process_for_intent(
            model,
            content,
            conditional_engine_object,
            conditional_intent,
            parent_result,
        )
        parent_result[conditional_intent] = sub_intent_result

    if len(conditional_intents) > 0:
        return parent_result, results

    for sub_intent in sub_intents:
        _, sub_intent_result = _process_for_intent(
            model, content, engine_object[sub_intent], sub_intent, parent_result
        )
        parent_result[sub_intent] = sub_intent_result

    return parent_result, results
