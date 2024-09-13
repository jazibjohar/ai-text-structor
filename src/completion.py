from prompt_engine import prompt_builder_by_type
from process_intent import get_builder_for_intent


def run_completion(model, content, engine_object):
    prompt_type = engine_object.get("type")
    if prompt_type is None:
        return get_builder_for_intent(model, content, engine_object)
    
    if prompt_type not in prompt_builder_by_type:
        raise ValueError(f"Prompt builder {type} invalid")

    get_prompt = prompt_builder_by_type[prompt_type]
    builder = get_prompt(content, engine_object)
    prompts = builder.get("prompts")
    args = builder.get("args")
    parser = builder.get("parser")
    if prompts is None or parser is None:
        raise ValueError("Invalid prompts or parser")
    chain =  prompts | model | parser
    return chain.invoke(args)
