# AI Text Structor Documentation

## Overview
The AI Text Structor is a sophisticated system for executing structured data collection and workflow processing using Large Language Models (LLMs). It features parallel execution capabilities, caching, and a robust workflow management system.

## Core Components

### 1. AI Text Structor (`AITextStructor`)

The central orchestrator that manages:
- Workflow execution
- Data processing
- Result caching
- Parallel processing

Reference implementation:

```6:90:src/ai_text_structor.py
class AITextStructor:
    """
    Manages the execution of AI processing workflows and data operations
    """
    def __init__(self, engine_config, model, parallel: bool = True):
        """
        Initialize AITextStructor with configuration
        
        Args:
            engine_config (dict): Configuration containing data and workflow definitions
            model: The LangChain AI model to use for processing
            
        Raises:
            ValueError: If data is missing or empty in engine_config
            ValueError: If model is not provided
        """
        if not engine_config or 'data' not in engine_config or not engine_config['data']:
            raise ValueError("engine_config must contain non-empty data configuration")
        
        if not model:
            raise ValueError("A LangChain model must be provided")
            
        self.model = model
        self.data_executor = DataExecutor(engine_config['data'], model)
        self.workflow_executor = None
        self.data_cache = {}
        self.parallel = parallel
        self._cache_lock = asyncio.Lock()
        
        if 'workflow' in engine_config and engine_config['workflow']:
            self.workflow_executor = WorkflowExecutor(engine_config['workflow'], model)
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

    async def execute(self, content):
        """
        Execute AI processing based on configuration
        
        Args:
            content (str): Content to process
            
        Returns:
            dict: Results of processing
        """
        if not self.workflow_executor:
            return await self.execute_data(content)
        
        results = {}
        for workflow_id in self.workflow_executor.get_root_workflows():
            # Process data requirements
            data_requirements = self.workflow_executor.get_data_requirements(workflow_id)
            results[workflow_id] = await self.execute_data(content, data_requirements)
            
            workflow_executor = self.workflow_executor.get_workflow_executor_by_id(workflow_id)
            explain_workflow_id = workflow_executor(content)
            if not explain_workflow_id:
                continue
            
            explain_data_requirements = self.workflow_executor.get_data_requirements(explain_workflow_id)
            results[workflow_id][explain_workflow_id] = await self.execute_data(content, explain_data_requirements)
        
```


### 2. Data Executor (`DataExecutor`)

Manages data processing operations with support for:
- Multiple data types
- Dynamic executor initialization
- Chain execution

Reference implementation:

```6:92:src/data_executor.py
class DataExecutor:
    """
    Manages the execution and state management of data processing from prompts
    """
    def __init__(self, data_dict=None, model=None):
        """
        Initialize DataExecutor with a data dictionary and LangChain model
        
        Args:
            data_dict (dict): Dictionary containing data fields and their configurations
            model: LangChain AI model instance
            
        Raises:
            ValueError: If data_dict is None or empty
            ValueError: If model is None
        """
        if not data_dict:
            raise ValueError("data_dict must be provided and cannot be empty")
        if model is None:
            raise ValueError("model must be provided")
            
        self.data_dict = data_dict
        self.model = model
        self.executors = {}
        self._initialize_executors()
    
    def _initialize_executors(self):
        """
        Initialize executor functions that return chain components for each key.
        Each executor returns a dict with:
        - prompts: The prompts to be used
        - parser: Function to parse the output
        - args: Additional arguments for the chain
        """
        for key, config in self.data_dict.items():
            data_type = config.get('type')
            if not data_type:
                raise ValueError(f"Configuration for key '{key}' must specify a type")
                
            if data_type == 'object':
                self.executors[key] = lambda content, c=config, m=self.model: self._execute_chain(
                    run_completion_for_object(content, c), m
                )
            elif data_type == 'string':
                self.executors[key] = lambda content, c=config, m=self.model: self._execute_chain(
                    run_completion_for_string(content, c), m
                )
            elif data_type == 'numeric':
                self.executors[key] = lambda content, c=config, m=self.model: self._execute_chain(
                    run_completion_for_numeric(content, c), m
                )
            elif data_type == 'list':
                self.executors[key] = lambda content, c=config, m=self.model: self._execute_chain(
                    run_completion_for_list(content, c), m
                )
            else:
                raise ValueError(f"Invalid type '{data_type}' for key '{key}'")
    def _execute_chain(self, chain_components, model):
        """
        Execute a LangChain chain with the provided components
        
        Args:
            chain_components (dict): Dictionary containing prompts, parser, and args
            model: LangChain model instance
            
        Returns:
            The parsed result from the chain execution
        """
        prompts = chain_components["prompts"]
        parser = chain_components["parser"]
        args = chain_components["args"]
        
        chain = prompts | model | parser
        return chain.invoke(args)
    
    def get_executor(self, key):
        """
        Get executor function for a specific key
        
        Args:
            key (str): Key to fetch executor for
            
        Returns:
            callable: The executor function for the specified key
        """
        return self.executors.get(key)
```


### 3. Workflow Executor (`WorkflowExecutor`)

Handles workflow orchestration with:
- Dependency validation
- Root workflow identification
- Execution path management

Reference implementation:

```2:184:src/workflow_executor.py
class WorkflowExecutor:
    """
    Manages the execution and validation of workflows based on their dependencies
    """
    def __init__(self, workflow_dict=None, model=None):
        """
        Initialize WorkflowExecutor with a workflow dictionary and model
        
        Args:
            workflow_dict (dict): Dictionary containing workflow definitions
            model: The language model to use for execution
            
        Raises:
            ValueError: If workflow_dict is None or empty or if model is None
        """
        if not workflow_dict:
            raise ValueError("workflow_dict must be provided and cannot be empty")
        if not model:
            raise ValueError("model must be provided")
            
        self.workflow_dict = workflow_dict
        self.model = model
        self.prompt_workflows = {}  # Prompt-based workflows (independent execution steps)
        self.explain_workflows = {}  # Explanation-based workflows (dependent steps)
        self.explain_dependencies = {}  # Mapping of prompt workflows to their explain dependencies
        self.workflow_data = {}  # Mapping of workflows to their data requirements
        
        if self._validate():
            self._initialize()
    def _validate(self):
        """
        Validates workflow configurations
        
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If validation fails
        """
        for workflow_id, config in self.workflow_dict.items():
            # Check for either prompt or explain
            if not (config.get('prompt') or config.get('explain')):
                raise ValueError(f"Workflow '{workflow_id}' must have either 'prompt' or 'explain'")
            
            # Validate explain workflows have dependencies
            if config.get('explain') and not config.get('requires'):
                raise ValueError(f"Explain workflow '{workflow_id}' must have dependencies")
            
            # Validate explain workflows don't depend on other explain workflows
            if config.get('explain'):
                for dep in config.get('requires', []):
                    if self.workflow_dict.get(dep, {}).get('explain'):
                        raise ValueError(f"Explain workflow '{workflow_id}' cannot depend on another explain workflow")
            
            # Validate data field references exist
            if not isinstance(config.get('data', []), list):
                raise ValueError(f"Data field for workflow '{workflow_id}' must be a list")
            
            # Add new validations from documentation
            if config.get('prompt') and config.get('requires'):
                for dep in config.get('requires', []):
                    if self.workflow_dict.get(dep, {}).get('prompt'):
                        raise ValueError(
                            f"Prompt-based workflow '{workflow_id}' cannot depend on another prompt-based workflow"
                        )
            # Validate data types
            for data_field in config.get('data', []):
                if not isinstance(data_field, str):
                    raise ValueError(
                        f"Data field references in workflow '{workflow_id}' must be strings"
                    )
        
        return True
    def _initialize(self):
        """
        Initializes internal workflow mappings
        """
        for workflow_id, config in self.workflow_dict.items():
            # Store data requirements for all workflows
            self.workflow_data[workflow_id] = config.get('data', [])
            
            if config.get('prompt'):
                # Store prompt-based workflows
                self.prompt_workflows[workflow_id] = {
                    'prompt': config['prompt'],
                    'requires': config.get('requires', []),
                    'name': config.get('name', workflow_id),
                    'description': config.get('description', '')
                }
                
                # Initialize explain dependencies list
                self.explain_dependencies[workflow_id] = []
            
            if config.get('explain'):
                # Store explanation-based workflows
                self.explain_workflows[workflow_id] = {
                    'explain': config['explain'],
                    'requires': config.get('requires', []),
                    'name': config.get('name', workflow_id),
                    'description': config.get('description', '')
                }
                
                # Map explain workflows to their prompt workflow dependencies
                for dep in config.get('requires', []):
                    if dep in self.prompt_workflows:
                        self.explain_dependencies[dep].append(workflow_id)
    def get_root_workflows(self):
        """
        Returns prompt-based workflows with no dependencies
        
        Returns:
            dict: Dictionary of root workflow IDs and their prompts
        """
        return {
            wf_id: config['prompt'] 
            for wf_id, config in self.prompt_workflows.items() 
            if not config['requires']
        }
    
    def get_explain_dependencies(self, workflow_id):
        """
        Returns explain workflow IDs dependent on the given workflow
        
        Args:
            workflow_id (str): Workflow ID to get dependencies for
            
        Returns:
            list: List of dependent explain workflow IDs
        """
        return self.explain_dependencies.get(workflow_id, [])
    
    def get_data_requirements(self, workflow_id):
        """
        Returns data field requirements for a workflow
        
        Args:
            workflow_id (str): Workflow ID to get data requirements for
            
        Returns:
            list: List of required data field IDs
        """
        return self.workflow_data.get(workflow_id, [])
    def get_workflow_executor_by_id(self, workflow_id: str):
        """
        Returns a function that executes a specific workflow with pre-configured parameters
        
        Args:
            workflow_id (str): ID of the workflow to execute
            
        Returns:
            callable: Function that accepts content and returns the selected workflow path
            
        Raises:
            ValueError: If workflow_id is not found or is not a prompt-based workflow
        """
        if workflow_id not in self.prompt_workflows:
            raise ValueError(f"Workflow '{workflow_id}' not found or is not a prompt-based workflow")
        
        # Get the prompt workflow configuration
        workflow_config = self.prompt_workflows[workflow_id]
        
        # Create a dictionary of explain dependencies for this workflow
        explain_paths = {
            explain_id: self.explain_workflows[explain_id]['explain']
            for explain_id in self.explain_dependencies[workflow_id]
        }
        
        # Return a function that only needs content as an argument
        def executor(content: str) -> str:
            return process_workflow(
                model=self.model,
                content=content,
                workflow_prompt=workflow_config['prompt'],
                workflow_paths=explain_paths,
                context_data={}  # You might want to add context data handling here
            )
        
        return executor
```


## Supported Data Types

### 1. String Type
- Basic text processing
- Direct string output
- Simple prompt structure


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


### 2. Numeric Type
- Numerical value extraction
- Float parsing
- Validation handling


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


### 3. Object Type
- Complex structured data
- Pydantic model validation
- Dynamic attribute handling


```16:51:src/process_object.py
def build_pydantic_model(attributes):
    obj = from_json(json.dumps(attributes), allow_partial=True)
    annotated_fields = {}
    for key, value in obj.items():
        annotated_fields[key] = Annotated[type(value), Field(description=value)]
    DynamicModel = create_model("DynamicModel", **annotated_fields)
    return DynamicModel


def run_completion_for_object(content, engine_object, parent=None):
    invocation_prompt = engine_object.get("prompt")
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


### 4. List Type
- Array processing
- JSON array output
- Structured list handling


```18:40:src/process_list.py
def run_completion_for_list(content, engine_object, parent=None):
    prompt = engine_object.get("prompt")
    parser = JsonOutputParser(pydantic_object=ListModel)
    
    content_key, prompt_key = get_content_and_invocation_key(parent)

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


## Execution Flow

### 1. Request Processing

```13:24:src/main.py
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
     
```


### 2. Parallel Execution
The engine supports parallel processing of data executors:

```38:62:src/ai_text_structor.py
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


### 3. Caching
Implements result caching for efficiency:

```93:112:src/ai_text_structor.py
    async def _get_or_execute_data(self, data_key: str, content: str):
        """
        Get data from cache or execute data executor if not cached
        
        Args:
            data_key (str): Key for the data executor
            content (str): Content to process
            
        Returns:
            The result of the data execution or cached value
        """
        cache_key = f"{data_key}"
        async with self._cache_lock:
            if cache_key not in self.data_cache:
                executor = self.data_executor.get_executor(data_key)
                loop = asyncio.get_running_loop()
                self.data_cache[cache_key] = await loop.run_in_executor(
                    None, executor, content
                )
            return self.data_cache[cache_key]
```


## Configuration Structure

### 1. Data Configuration
```json
{
  "field_name": {
    "type": "string|numeric|object|list",
    "prompt": "Instruction for LLM",
    "attributes": {}, // Required for object type
    "name": "Display Name",
    "description": "Field description"
  }
}
```

### 2. Workflow Configuration
```json
{
  "workflow_id": {
    "name": "Workflow Name",
    "description": "Purpose description",
    "prompt": "Prompt-based instruction",
    "explain": "Explanation-based instruction",
    "requires": ["dependent_workflows"],
    "data": ["required_data_fields"]
  }
}
```

## Key Features

### 1. Parallel Processing
- Concurrent data execution
- Async/await pattern
- Resource optimization

### 2. Result Caching
- In-memory cache
- Thread-safe operations
- Cache key management

### 3. Model Support
Supports multiple LLM providers:

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


## Implementation Rules

### 1. Workflow Validation
- No circular dependencies
- Valid dependency chains
- Required field validation

### 2. Data Processing
- Type-specific processors
- Structured output formats
- Error handling

### 3. Execution Order
- Parallel when possible
- Sequential for dependencies
- Cached result reuse

## Error Handling

### 1. Configuration Validation
- Type checking
- Required fields
- Dependency validation

### 2. Runtime Errors
- Model errors
- Parser failures
- Invalid responses

### 3. Data Validation
- Type validation
- Format checking
- Schema validation

## Extension Points

### 1. New Data Types
- Add processor in `src/process_*.py`
- Register in `prompt_builder_by_type`
- Implement parser

### 2. New Models
- Add to `models.py`
- Implement model interface
- Register in model dictionary

## Performance Considerations

### 1. Caching Strategy
- Memory management
- Cache invalidation
- Thread safety

### 2. Parallel Processing
- Resource allocation
- Task coordination
- Error propagation

## Best Practices

### 1. Configuration
- External configuration files
- Environment variables
- Clear naming conventions

### 2. Development
- Type annotations
- Documentation
- Error handling
- Test coverage

### 3. Deployment
- Environment setup
- API key management
- Resource monitoring

This documentation reflects the current implementation with its parallel processing capabilities, caching system, and robust workflow management while maintaining extensibility and reliability.