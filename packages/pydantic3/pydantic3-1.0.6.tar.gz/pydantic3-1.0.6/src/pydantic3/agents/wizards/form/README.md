# Form Generation System

This module implements an AI-powered form generation system that helps create complex, multi-level form structures based on business requirements. The system uses LLM (Large Language Models) to generate both the high-level form structure and detailed field definitions.

## Architecture Overview

The form generation system is composed of several components that work together:

1. **FormWizard**: Main entry point that guides users through collecting requirements
2. **FormStructureGenerator**: Orchestrates the generation of the complete form structure
3. **FormDetailGenerator**: Handles parallel generation of detailed form definitions

## Components

### FormWizard

The `FormWizard` class serves as a conversational interface for collecting business requirements. It:

- Uses `FormProcessor` to handle the conversation flow
- Collects information about the business, its goals, and form requirements
- Monitors form completion progress
- Triggers form structure generation when the form reaches 100% completion
- Uses `TestFormIntentRequest` for development and testing scenarios

### FormStructureGenerator

The `FormStructureGenerator` orchestrates the generation of the complete form structure:

- Generates the high-level structure overview (document metadata, list of forms)
- Creates a `FormDetailGenerator` instance to handle form details
- Runs parallel generation of all form details via independent LLM instances
- Combines all results into a complete form structure

### FormDetailGenerator

The `FormDetailGenerator` specializes in generating detailed form definitions:

- Creates a separate LLM provider for each form to enable true parallelism
- Generates detailed field definitions based on the form's purpose
- Handles various field types, validation, relationships between forms
- Ensures proper formatting of the generated data

## Data Models

The system uses several Pydantic models:

1. **FormStructureOverview**: Contains the document metadata and list of forms
2. **FormDetail**: Contains detailed form definition with fields and relationships
3. **FormIntentRequest**: Used by the wizard to collect information from the user
4. **TestFormIntentRequest**: Special model with optional fields for testing and development

### Test Model

The `TestFormIntentRequest` model is specifically designed for testing and development:

```python
class TestFormIntentRequest(BaseModel):
    """Testing form model with all fields made optional for dynamic filling by LLM."""

    business: Optional[Dict[str, Any]] = Field(default_factory=dict)
    business_goals: Optional[Dict[str, Any]] = Field(default_factory=dict)
    document: Optional[Dict[str, Any]] = Field(default_factory=dict)
    bot: Optional[Dict[str, Any]] = Field(default_factory=dict)
    notes: Optional[str] = None
```

This model makes all fields optional, allowing for dynamic filling through the conversation with LLM.

## Workflow

1. **User Interaction**:
   - User interacts with the `FormWizard` through a conversational interface
   - System collects information about business, goals, and form requirements
   - The conversation continues until all necessary information is collected

2. **Form Structure Generation**:
   - When the form reaches 100% completion, `generate_form_structure` is triggered
   - `FormStructureGenerator` first generates a high-level structure overview
   - Then it delegates the generation of detailed form definitions to `FormDetailGenerator`

3. **Parallel Form Generation**:
   - `FormDetailGenerator` generates detailed forms in parallel using separate LLM providers
   - Each form gets its own provider instance, ensuring true parallelism
   - This approach significantly reduces the total generation time, especially for multiple forms

4. **Final Output**:
   - The system combines all generated data into a complete form structure
   - The output includes document metadata, forms with detailed field definitions, and explanations

## Performance Optimization

The system is optimized for performance through:

1. **True Parallel Processing**:
   - Each form generation gets its own independent provider instance
   - No shared state between requests that could cause bottlenecks
   - Runs simultaneously rather than sequentially

2. **Efficient Resource Management**:
   - Creates providers on-demand when needed
   - No persistent connections taking up resources
   - Clean separation of responsibilities between components

3. **Efficient Task Orchestration**:
   - Uses `asyncio.gather()` to manage parallel tasks
   - Collects all results into a unified structure
   - Total processing time depends only on the slowest form (not the sum of all)

4. **Clear Separation of Concerns**:
   - Each class has a specific, well-defined responsibility
   - `FormStructureGenerator` handles orchestration
   - `FormDetailGenerator` focuses on form details

## Example Usage

```python
# Create a FormWizard instance
wizard = FormWizard.from_env()

# Start a session
session_id = await wizard.start_session()

# Process user messages until form is complete
response = await wizard.process_message("I need a form for user feedback")
# ... more messages ...

# When response.session_info.metadata.progress reaches 100%,
# form generation is automatically triggered
complete_structure = await wizard.generate_form_structure(response.user_form)
```

## Testing

The system includes comprehensive testing tools:

1. **form_wizard_test.py**: Tests the conversational form collection process
2. **form_generator_test.py**: Tests the parallel form structure generation

The test files demonstrate proper usage and can be used to validate functionality.

## Generated Form Structure

The final output is a nested JSON structure with:

- Document metadata (title, description)
- List of forms with their detailed definitions
- Each form contains:
  - Basic properties (name, title, description)
  - List of fields with complete definitions
  - Relationships between forms (if any)
- An explanation of the overall form structure
