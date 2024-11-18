from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Any

def process_workflow(
    model: Any,
    content: str,
    workflow_prompt: str,
    workflow_paths: dict[str, str],
    context_data: dict[str, str]
) -> str:
    """
    Process workflow to determine which path to take based on the initial prompt and possible paths
    
    Args:
        model: LangChain model instance to use for completion
        content (str): Input content to analyze
        workflow_prompt (str): Initial workflow prompt
        workflow_paths (dict[str, str]): Dictionary of possible workflow paths and their explanations
        context_data (dict[str, str]): Context data for variable replacement
        
    Returns:
        str: Selected workflow path key
    """
    # Construct the options string
    options = "\n".join([f"- {key}: {value}" for key, value in workflow_paths.items()])
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a workflow analyzer. Based on the content and description, "
                  "select ONE of the provided workflow types. Respond ONLY with the workflow key."),
        ("user", "Content: {content}"),
        ("user", "Task: {workflow_prompt}"),
        ("user", "Available workflows:\n{options}"),
    ])
    
    # Set up the chain with the provided model and string parser
    chain = prompt | model | StrOutputParser()
    
    # Replace variables in workflow prompt with context data
    for key, value in context_data.items():
        workflow_prompt = workflow_prompt.replace(f"{{{key}}}", str(value))

    # Execute the chain
    result = chain.invoke({
        "content": content,
        "workflow_prompt": workflow_prompt,
        "options": options,
    })
    
    # Clean and validate the result
    selected_workflow = result.strip().lower()
    if selected_workflow not in workflow_paths:
        raise ValueError(f"Model returned invalid workflow: {selected_workflow}")
        
    return selected_workflow
