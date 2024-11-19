# AI Engine

## Core Concepts
The AI Engine is a flexible system for structured data collection and workflow processing using LLMs. It processes JSON-based configurations to orchestrate complex data extraction and decision-making workflows.

### Key Components
1. **Data Definitions** - Define collectable fields with specific types:
   - `string` - Text-based responses
   - `numeric` - Numerical values
   - `object` - Complex nested structures
   - `list` - Array processing

2. **Workflow Definitions** - Organize execution flow:
   - Prompt-based workflows (independent)
   - Explanation-based workflows (dependent)

## Implementation Details
The implementation provides several sophisticated features:

1. **AIEngine Class**
   - Central orchestrator
   - Parallel execution support
   - Result caching
   - Workflow management

2. **Executors**
   - `DataExecutor` - Handles data processing operations
   - `WorkflowExecutor` - Manages workflow orchestration

3. **Key Features**
   - Parallel processing
   - Thread-safe caching
   - Multiple LLM provider support
   - Robust error handling
   - Extensible architecture

## Project Setup

### Prerequisites
1. Install direnv:
```bash
# macOS
brew install direnv

# Linux
curl -sfL https://direnv.net/install.sh | bash
```

2. Install devbox:
```bash
curl -fsSL https://get.jetpack.io/devbox | bash
```

### Project Setup
1. Clone the repository:
```bash
git clone https://github.com/your-org/ai-engine.git
cd ai-engine
```

2. Create `.envrc` file:
```bash
export OPENAI_API_KEY="your-key-here"
export GOOGLE_AI_API_KEY="your-key-here"
export MISTRAL_AI_API_KEY="your-key-here"
```

3. Allow direnv:
```bash
direnv allow
```

4. Initialize devbox:
```bash
devbox init
```

5. Install dependencies:
```bash
devbox install
```

6. Start the development shell:
```bash
devbox shell
```

7. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Or through devbox (devbox should already install it)
```bash
devbox add poetry
```

8. Install project dependencies through Poetry:
```
poetry install
```




### Running the Project
1. Start the server:
```bash
python src/main.py
```

2. Make API requests:
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "content": "Your text here",
    "file_path": "path/to/config.json"
  }'
```

The project uses modern development tools (devbox and direnv) to ensure consistent development environments and secure credential management. The implementation supports parallel processing, caching, and multiple LLM providers while maintaining a clean, extensible architecture.

## Future Work

### RAG (Retrieval Augmented Generation) Integration
The AI Engine roadmap includes implementing robust RAG capabilities:

1. **Document Processing**
   - PDF, markdown, and plain text ingestion
   - Document chunking and preprocessing
   - Metadata extraction and indexing

2. **Vector Store Integration**
   - Support for multiple vector databases (Pinecone, Weaviate, etc.)
   - Efficient similarity search
   - Hybrid search capabilities

3. **Context Enhancement**
   - Dynamic context window management
   - Relevance scoring and filtering
   - Context compression techniques

4. **Advanced Features**
   - Multi-document reasoning
   - Cross-reference validation
   - Source attribution and citation
   - Incremental learning capabilities

These enhancements will enable the AI Engine to:
- Process and understand large document collections
- Provide more accurate and contextual responses
- Support domain-specific knowledge bases
- Maintain traceability to source materials