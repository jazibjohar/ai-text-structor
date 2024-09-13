from langchain_core.runnables import RunnableParallel
from prompt_engine import prompt_builder_by_type
from operator import itemgetter

def get_keys(dict):
    return list(map(itemgetter(0), dict.items()))

def get_builder_for_intent(model, content, engine_object):
    aggregated_result, _ = _process_for_intent(model, content, engine_object)
    return aggregated_result

def _process_for_intent(model, content, engine_object, parent_key=None, parent_result=None):
    if parent_result is None:
        parent_result = {}
    if len(engine_object) == 0:
        return None, None
    
    intents_list = get_keys(engine_object)
    
    # sub intents are objects without type
    sub_intents = [
        intent for intent in intents_list if engine_object[intent].get("type") is None
    ]
    intents_to_process = [
        intent for intent in intents_list if intent not in sub_intents
    ]
    master_chains = {}
    master_args = {}
    for intent in intents_to_process:
        prompt_type = engine_object[intent].get("type")
        executor = prompt_builder_by_type[prompt_type]
        builder = executor(content, engine_object[intent], intent)
        chain = builder["prompts"] | model | builder["parser"]
        master_chains[intent] = chain
        master_args.update(builder["args"])

    master_args.update(parent_result)
    master_chains_executor = RunnableParallel(**master_chains)
    results = master_chains_executor.invoke(master_args)
    if parent_key is None:
        parent_result.update(results)


    for sub_intent in sub_intents:
        _, sub_intent_result = _process_for_intent(
            model, content, engine_object[sub_intent],sub_intent, parent_result
        )
        parent_result[sub_intent] = sub_intent_result

    return parent_result, results
