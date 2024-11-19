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

## Usage Example

Here's how to use the AI Engine:

```python
from ai_engine import AIEngine
from langchain_openai import ChatOpenAI

# Initialize model
model = ChatOpenAI(
    openai_api_key="your-key",
    model_name="gpt-4o"
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
engine = AIEngine(config, model)

# Execute
async def run():
    result = await engine.execute("Your content here")
    print(result)

# Run with asyncio
import asyncio
asyncio.run(run())
```


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
```bash
poetry install
```

### Publishing to PyPI (Work in progress)

The project uses GitHub Actions for automated publishing to PyPI. The workflow is triggered when you push a version tag.

1. Configure GitHub repository:
   - Go to repository Settings → Secrets and variables → Actions
   - Add a new secret named `PYPI_TOKEN` with your PyPI API token

2. Update the version in pyproject.toml:
```bash
poetry version patch  # For patch version bump
# or
poetry version minor  # For minor version bump
# or
poetry version major  # For major version bump
```

3. Commit your changes:
```bash
git add pyproject.toml
git commit -m "Bump version to x.y.z"
```

4. Create and push a version tag:
```bash
git tag vx.y.z  # Replace with your version (e.g., v1.0.0)
git push origin vx.y.z
```

The GitHub Action will automatically:
- Build the package
- Publish to PyPI
- Create a release on GitHub

Note: To publish to Test PyPI first, you can manually run:
```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi
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