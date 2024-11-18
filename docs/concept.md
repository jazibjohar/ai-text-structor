Here's a comprehensive documentation update for the AI Engine:

# AI Engine Documentation

## Overview
The AI Engine is a flexible system for executing structured data collection and workflow processing using Large Language Models (LLMs). It processes JSON-based configurations to orchestrate complex data extraction and decision-making workflows.

## Core Components

### 1. Data Definitions (`data`)

The `data` object defines collectable fields and their extraction parameters. Each field is configured as:

```json
{
  "field_name": {
    "name": "Display Name",
    "description": "Field purpose description",
    "prompt": "Instruction for LLM",
    "type": "string|numeric|object|list",
    "attributes": {} // Required for object type
  }
}
```

#### Supported Data Types

1. **string**
   - Text-based responses
   - Uses `StrOutputParser` for extraction
   - Reference implementation: 

```9:27:src/process_string.py
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
```


2. **numeric**
   - Numerical values (integers or floats)
   - Automatically converts responses to float
   - Reference implementation:

```13:32:src/process_numeric.py
def run_completion_for_numeric(content, engine_object, parent=None):
    prompt = engine_object.get("prompt")
    content_key, prompt_key = get_content_and_invocation_key(parent)
    prompts = ChatPromptTemplate.from_messages(
        [
            ("user", "{" + content_key + "}"),
            ("user", "{" + prompt_key + "}"),
            ("user", "output only numeric value"),
        ]
    )
    args = {
        prompt_key: prompt,
        content_key: content,
    }

    return {
        "prompts": prompts,
        "parser": parse_output,
        "args": args,
    }
```


3. **object**
   - Complex nested structures
   - Uses Pydantic models for validation
   - Requires `attributes` definition
   - Reference implementation:

```16:51:src/process_object.py
def build_pydantic_model(attributes):
    obj = from_json(json.dumps(attributes), allow_partial=True)
    annotated_fields = {}
    for key, value in obj.items():
        annotated_fields[key] = Annotated[type(value), Field(description=value)]
    DynamicModel = create_model("DynamicModel", **annotated_fields)
    return DynamicModel


def run_completion_for_object(content, engine_object, parent=None):
    invocation_prompt = engine_object.get("invocation_prompt")
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
```


### 2. Workflow Definitions (`workflow`)

Workflows organize the execution flow and dependencies. Each workflow is defined as:

```json
{
  "workflow_name": {
    "name": "Display Name",
    "description": "Workflow purpose",
    "prompt": "Simple instruction step",
    "explain": "Detailed instruction (for dependent steps)",
    "requires": ["dependent_workflow_ids"],
    "data": ["data_field_ids"]
  }
}
```

#### Workflow Types

1. **Prompt-based Workflows**
   - Independent execution steps
   - Uses `prompt` for instructions
   - `requires` field is optional
   - Cannot require other prompt-based workflows
   - Direct data collection

2. **Explanation-based Workflows**
   - Dependent execution steps
   - Uses `explain` for instructions
   - `requires` field is mandatory
   - Must require at least one prompt-based workflow
   - Can only require prompt-based workflows
   - Cannot depend on other explanation-based workflows

## Execution Flow

1. **Configuration Loading**

```11:24:src/main.py
def process(request):
    request_json = request.get_json()
    model = request_json.get('model')
    if model not in models:
        return {"error": "Invalid model"}, 400
    content = request_json.get('content')
    file_path = request_json.get('file_path')
    
    prompt_config = load_json(file_path)
    return run_completion(
        models[model],
        content,
        prompt_config
    )
```


2. **Workflow Processing**
   - Identifies workflow type
   - Validates dependencies
   - Executes data collection
   - Reference implementation:

```5:21:src/completion.py
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
```


3. **Data Collection**
   - Processes each field based on type
   - Uses appropriate parser
   - Handles nested structures
   - Reference implementation:

```5:9:src/prompt_engine.py
prompt_builder_by_type = {
    "object": run_completion_for_object,
    "string": run_completion_for_string,
    "numeric": run_completion_for_numeric,
}
```


## Design Principles

1. **Modularity**
   - Each data type has its dedicated processor
   - Clear separation between workflow and data processing
   - Extensible type system

2. **Dependency Management**
   - Explicit workflow dependencies
   - Validation before execution
   - Results propagation between steps

3. **Error Handling**
   - Type validation
   - Parser-specific error handling
   - Clear error messages

4. **Model Flexibility**
   - Supports multiple LLM providers
   - Consistent interface across models
   - Reference implementation:

```7:23:src/models.py
def get_open_ai_model():
    return ChatOpenAI(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        model_name='gpt-4o'
    )

def get_google_generative_ai_model():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=os.getenv('GOOGLE_AI_API_KEY'),
    )
    
def get_mistral():
    return ChatMistralAI(
        mistral_api_key=os.getenv('MISTRAL_AI_API_KEY'),
        model='open-mistral-7b'
    )
```


## Assumptions and Limitations

1. **Data Types**
   - All data types must have corresponding processors
   - Object types require valid attribute definitions
   - List types must specify element structure

2. **Workflows**
   - Cannot have circular dependencies
   - Explanation-based workflows:
     - Must have `requires` field
     - Can only depend on prompt-based workflows
   - Prompt-based workflows:
     - `requires` field is optional
     - Cannot depend on other prompt-based workflows
   - Workflow names must be unique

3. **Execution**
   - Sequential processing of dependencies
   - Parallel execution of independent fields
   - Results are accumulated hierarchically

## Default Behavior

When no workflow is defined:
1. Direct data collection from `data` object
2. Sequential processing of fields
3. No dependency validation
4. Flat result structure

## Error Cases

1. **Invalid Configuration**
   - Missing required fields
   - Invalid type definitions
   - Circular dependencies

2. **Runtime Errors**
   - Parser failures
   - LLM API errors
   - Invalid response formats

3. **Dependency Errors**
   - Missing required workflows
   - Invalid dependency chains:
     - Prompt workflow requiring another prompt workflow
     - Explanation workflow depending on non-prompt workflow
     - Explanation workflow without any dependencies
   - Missing `requires` field in explanation workflow

This documentation reflects the current implementation while providing a clear structure for future extensions and modifications.