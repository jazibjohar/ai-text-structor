# AI Engine UI

## Overview

This project provides a user interface (UI) for generating structured JSON templates used as inputs for Large Language Models (LLMs). The application implements a workflow-based approach to data collection, where data fields are defined separately from the workflows that collect them.

## Core JSON Structure

The JSON template is divided into two primary sections:

### 1. Data Definitions (`data`)

The `data` object defines all collectable data fields. Each field is defined as a key-value pair where:
- The key serves as a unique identifier for the field
- The value is an object containing:
  - `name`: Display name for the field
  - `description`: Detailed description of the field and its purpose
  - `prompt`: Text instructions for collecting the data
  - `type`: The data type expected (`string`, `numeric`, `list`, or `object`)
  - `attributes`: (Required for `object` type) Defines the structure of nested fields

Example data definition:
```json
{
    "user_name": {
        "name": "User Name",
        "description": "The full name of the user for identification purposes",
        "prompt": "What is your name?",
        "type": "string"
    },
    "address": {
        "name": "Address Information",
        "description": "Complete mailing address details for the user",
        "prompt": "Enter your address details",
        "type": "object",
        "attributes": {
            "street": "Street address including house number",
            "city": "City name"
        }
    }
}
```

### 2. Workflow Definitions (`workflow`)

The `workflow` object organizes the data collection process into logical steps. Each workflow is defined by a unique identifier and contains:

- `name`: Display name for the workflow step
- `description`: Detailed explanation of the workflow's purpose and process
- `prompt` or `explain`: Instructions for the step
  - `prompt`: Used for simple instruction steps
  - `explain`: Used for more detailed steps (requires dependencies)
- `requires`: Array of dependent workflow identifiers (optional for prompt-based workflows)
- `data`: Array of data field identifiers to collect (optional)

Example workflow definition:
```json
{
    "personal_info": {
        "name": "Personal Information",
        "description": "Collects basic personal identification details",
        "prompt": "Let's collect your basic information",
        "data": ["user_name"]
    },
    "address_details": {
        "name": "Address Collection",
        "description": "Gathers complete mailing address information",
        "explain": "Now we'll collect your address information",
        "requires": ["personal_info"],
        "data": ["address"]
    }
}
```

## Supported Data Types

1. **string**
   - Basic text input
   - Single-line or multi-line responses

2. **numeric**
   - Integer or decimal values
   - Suitable for ages, quantities, measurements

3. **list**
   - Array of values
   - Can collect multiple related items

4. **object**
   - Complex nested structures
   - Requires `attributes` definition
   - Each attribute represents a sub-field with its own prompt

## Workflow Types

### 1. Prompt-based Workflows
- Simple instruction steps
- Can optionally have dependencies (`requires` array is optional)
- If `requires` is specified, cannot depend on other prompt-based workflows
- Suitable for independent data collection or building on explanation workflows
- Example:
```json
{
    "basic_info": {
        "name": "Basic Information",
        "prompt": "Let's start with your basic details",
        "data": ["user_name", "age"]
    },
    "follow_up": {
        "name": "Follow-up Information",
        "prompt": "Let's add some additional context",
        "requires": ["detailed_explanation"],
        "data": ["extra_details"]
    }
}
```

### 2. Explanation-based Workflows
- More detailed instruction steps
- Must have `requires` array (required field)
- Can only depend on prompt-based workflows
- Cannot depend on other explanation-based workflows
- Will error if `requires` is missing, empty, or contains non-prompt workflows
- Example:
```json
{
    "advanced_info": {
        "name": "Additional Details",
        "explain": "Now that we have your basics, let's get more specific",
        "requires": ["basic_info"],  // Must reference prompt-based workflows only
        "data": ["interests", "preferences"]
    }
}
```

## Default Behavior

If no workflows are defined in the template, the engine will:
- Execute the data collection based on the `data` object directly
- Process fields in the order they are defined
- Skip workflow-specific validations and dependencies

## UI Implementation

The UI provides an interactive builder with three main sections:

1. **Data Field Configuration**
   - Field identifier creation
   - Prompt definition
   - Type selection
   - Attribute configuration for object types

2. **Workflow Configuration**
   - Workflow identifier creation
   - Name and instruction setting
   - Dependency selection
   - Data field assignment

3. **Preview and Validation**
   - Real-time JSON structure preview
   - Dependency validation
   - Data field reference checking
   - Type consistency verification

## Purpose and Usage

This template generator is designed to:
- Create structured data collection workflows
- Ensure logical progression through dependent steps
- Generate consistent JSON outputs for LLM processing
- Support various data collection scenarios

The resulting JSON templates can be used to:
- Guide users through complex data collection
- Validate input data against defined types
- Maintain dependencies between collection steps
- Generate structured inputs for LLM processing

## Technical Implementation

The application is built using Next.js and provides:
- Real-time template validation
- JSON structure verification
- Dependency graph validation
- Type checking for all data fields
- Interactive workflow building
- Preview generation

The system ensures that all workflows and data definitions maintain consistency and that all references between workflows and data fields are valid.