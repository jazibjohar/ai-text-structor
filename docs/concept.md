# AI Text Structor Documentation

## Overview
The AI Text Structor is an asynchronous system for executing structured data collection and workflow processing using Large Language Models (LLMs). It processes JSON-based configurations to orchestrate complex data extraction and decision-making workflows.

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
   - Reference implementation in:

```5:23:ai_engine/process_string.py
def run_completion_for_string(content, engine_object):
    prompt = engine_object.get("prompt")

    content_key = 'content'
    prompt_key = 'invocation_prompt'
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
   - Reference implementation in:

```12:32:ai_engine/process_numeric.py
def run_completion_for_numeric(content, engine_object):
    prompt = engine_object.get("prompt")
    prompt_key = 'invocation_prompt'
    content_key = 'content'
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
   - Reference implementation in:

```24:51:ai_engine/process_object.py
def run_completion_for_object(content, engine_object):
    invocation_prompt = engine_object.get("prompt")
    attributes = engine_object.get("attributes")
    DynamicModel = build_pydantic_model(attributes)
    parser = JsonOutputParser(pydantic_object=DynamicModel)

    content_key = 'content'
    prompt_key = 'invocation_prompt'

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


4. **list**
   - Array of string values
   - Uses JsonOutputParser with ListModel
   - Reference implementation in:

```17:40:ai_engine/process_list.py
def run_completion_for_list(content, engine_object):
    prompt = engine_object.get("prompt")
    parser = JsonOutputParser(pydantic_object=ListModel)

    content_key = 'content'
    prompt_key = 'invocation_prompt'

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
            prompt_key: prompt,
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

## Usage Example

Here's how to use the AI Text Structor:

```python
from ai_engine import AITextStructor
from langchain_openai import ChatOpenAI

# Initialize model
model = ChatOpenAI(
    openai_api_key="your-key",
    model_name="gpt-4"
)

# Configure engine
config = {
    "data": {
        "summary": {
            "type": "string",
            "prompt": "Summarize the content"
        }
    },
    "workflow": {
        "analyze": {
            "prompt": "Analyze the content",
            "data": ["summary"]
        }
    }
}

# Initialize engine
engine = AITextStructor(config, model)

# Execute
async def run():
    result = await engine.execute("Your content here")
    print(result)

# Run with asyncio
import asyncio
asyncio.run(run())
```

## Design Principles

1. **Asynchronous Execution**
   - Parallel processing of independent tasks
   - Efficient handling of multiple LLM calls
   - Reference implementation in:

```44:68:ai_engine/ai_engine.py
    async def execute_data(self, content: str, data_ids: Union[str, List[str]] = None):
        """
        Execute specific data IDs or all available data executors

        Args:
            content (str): Content to process
            data_ids (Union[str, List[str]], optional): Specific data ID(s) to execute

        Returns:
            dict: Results of processing
        """
        if isinstance(data_ids, str):
            data_ids = [data_ids]

        execute_ids = data_ids or list(self.data_executor.executors)

        if self.parallel:
            tasks = [self._get_or_execute_data(key, content) for key in execute_ids]
            results_list = await asyncio.gather(*tasks)
            return dict(zip(execute_ids, results_list))
        else:
            results = {}
            for key in execute_ids:
                results[key] = await self._get_or_execute_data(key, content)
            return results
```


2. **Dependency Management**
   - Explicit workflow dependencies
   - Validation before execution
   - Results propagation between steps

3. **Error Handling**
   - Type validation
   - Parser-specific error handling
   - Clear error messages

4. **Model Flexibility**
   - Supports multiple LLM providers (OpenAI, Google, Mistral)
   - Consistent interface across models
   - Reference implementation in:

```10:24:tests/helper.py
def get_open_ai_model():
    return ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o")


def get_google_generative_ai_model():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=os.getenv("GOOGLE_AI_API_KEY"),
    )


def get_mistral():
    return ChatMistralAI(
        mistral_api_key=os.getenv("MISTRAL_AI_API_KEY"), model="open-mistral-7b"
    )
```


## Assumptions and Limitations

1. **Data Types**
   - All data types must have corresponding processors
   - Object types require valid attribute definitions
   - List types must specify element structure

2. **Workflows**
   - Cannot have circular dependencies
   - Explanation-based workflows must have dependencies
   - Prompt-based workflows cannot depend on other prompt-based workflows
   - Workflow names must be unique

3. **Execution**
   - Asynchronous processing of independent tasks
   - Sequential processing of dependencies
   - Results are accumulated hierarchically

For a complete example implementation, see tests/test_standup.py which demonstrates processing a standup meeting transcript through the workflow engine. The test shows how the engine handles complex, multi-speaker content while maintaining context and extracting structured information from natural conversations.