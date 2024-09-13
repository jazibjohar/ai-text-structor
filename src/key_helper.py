def get_content_and_invocation_key(parent = None):
    content_key = "content"
    prompt_key = "invocation_prompt"
    if parent is not None:
        prompt_key = f"{parent}_invocation_prompt"
    return content_key, prompt_key