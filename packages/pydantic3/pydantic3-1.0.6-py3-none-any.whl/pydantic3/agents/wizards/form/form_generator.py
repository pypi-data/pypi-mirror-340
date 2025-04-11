from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, model_validator
import yaml
import asyncio

from ....utils import LogConsole, SimpleLogger
from ...providers.openrouter import OpenRouterProvider


class Document(BaseModel):
    title: str = Field(description="Title of the document")
    description: str = Field(description="Description of the document")


class FormDetail(BaseModel):
    """Response format for detailed form definition."""
    name: str = Field(description="Unique name identifier for the form")
    title: str = Field(description="Display title for the form")
    description: str = Field(description="Description of the form's purpose")
    is_root_form: bool = Field(description="Whether this is the root form")
    fields: List[Dict[str, Any]] = Field(
        description="List of fields in this form with complete definitions"
    )
    relationships: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Relationships between this form and other forms, each with target_form and field_name properties"
    )


class FormStructureOverview(BaseModel):
    """Response format for initial form structure overview."""
    document: Document = Field(
        description="Document metadata including title and description"
    )
    forms: List[FormDetail] = Field(
        description="List of form definitions with name, title, and description only (no fields yet)"
    )
    explanation: str = Field(
        description="Brief explanation of the overall form structure and how it meets the business goals"
    )


class CompleteFormStructure(BaseModel):
    document: Document = Field(description="Document metadata including title and description")
    forms: List[FormDetail] = Field(description="List of form definitions with name, title, and description only (no fields yet)")
    explanation: str = Field(description="Brief explanation of the overall form structure and how it meets the business goals")


class FormDetailGenerator:
    """Generator for detailed form definitions."""

    def __init__(self, wizard_data: Dict[str, Any], model_name: str, api_key: Optional[str] = None):
        self.wizard_data = wizard_data
        self.model_name = model_name
        self.api_key = api_key
        self.logger = SimpleLogger("form_detail_generator")

    def create_provider(self) -> OpenRouterProvider:
        """Create a new OpenRouter provider instance."""
        return OpenRouterProvider(
            api_key=self.api_key,
            model_name=self.model_name,
        )

    async def generate_form_detail(self, form_info: Dict[str, str], is_root: bool) -> FormDetail:
        """Generate detailed definition for a specific form including all fields."""
        provider = self.create_provider()

        # make flat yaml from the wizard_data
        flat_wizard_data = yaml.dump(self.wizard_data)
        schema = FormDetail.model_json_schema()

        prompt = f"""
Now, create detailed field definitions for the "{form_info['name']}" form.

## FORM CONTEXT
Form Name: {form_info['name']}
Form Title: {form_info.get('title', form_info['name'])}
Form Description: {form_info.get('description', '')}
Is Root Form: {"Yes" if is_root else "No"}

## BUSINESS CONTEXT
{flat_wizard_data}

## AVAILABLE FIELD TYPES
- TEXT: For free text input
- NUMBER: For numerical values
- DATE: For date selection
- TIME: For time selection
- BOOLEAN: For yes/no questions
- SELECT: For single option from a list (include 'options' in settings)
- MULTISELECT: For multiple options from a list (include 'options' in settings)
- FORMULA: For calculated fields
- EMAIL: For email addresses
- PHONE: For phone numbers
- URL: For web addresses
- CURRENCY: For monetary values
- RELATION: For linking to another form (specify the target form name)

## RELATION FIELDS INSTRUCTIONS
When creating RELATION type fields, you MUST:
1. Set the type to "RELATION"
2. Include a "target_form" property in the settings object with the exact name of the target form

## FORM RELATIONSHIPS
For related forms, you must explicitly define relationships in the "relationships" array. Each relationship should include:
- "target_form": The name of the related form
- "field_name": The name of the field in this form that relates to the target form

## OUTPUT REQUIREMENTS
Provide a detailed definition including:
1. Complete list of fields with names, titles, descriptions, types, required flag
2. For SELECT and MULTISELECT fields, include options in the settings
3. For RELATION fields, ALWAYS specify target_form in the settings property
4. Proper ordering of fields for a good user experience
5. Define any relationships to other forms in the "relationships" array

Each field should have the following attributes:
- name: A unique identifier (snake_case)
- title: Display title (human-readable)
- description: Helpful description text
- type: One of the field types above
- required: true/false
- order: Numerical order of appearance
- settings: Any additional settings (options for SELECT, target_form for RELATION, etc.)

Return valid JSON object based on the following JSON schema:
{schema}
"""

        # Generate response using the OpenRouter provider
        system_message = "You are an expert form designer AI assistant that creates detailed field definitions for forms. Pay special attention to RELATION type fields, ensuring they always have a target_form in their settings. For any form relationships, always define them properly in the relationships array."
        response_json = await provider.json_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.2
        )

        # Convert the JSON response to the FormDetail model
        try:
            return FormDetail.model_validate(response_json)
        except Exception as e:
            self.logger.error(f"Error parsing FormDetail: {str(e)}")
            self.logger.error(f"Response JSON: {response_json}")
            raise ValueError(f"Failed to parse form detail: {str(e)}")


class FormStructureGenerator:
    """Service for multi-step form generation process."""

    def __init__(self, wizard_data: Dict[str, Any], model_name: str = "openai/gpt-4o-mini-2024-07-18", api_key: Optional[str] = None):
        self.wizard_data = wizard_data
        self.model_name = model_name
        self.api_key = api_key

        self.logger = SimpleLogger("form_structure_generator")
        self.console = LogConsole(name="form_structure_generator")

        if not api_key:
            self.logger.warning("No API key provided, will use environment variable")

    def create_provider(self) -> OpenRouterProvider:
        """Create a new OpenRouter provider instance."""
        return OpenRouterProvider(
            api_key=self.api_key,
            model_name=self.model_name,
        )

    async def generate_structure_overview(self) -> FormStructureOverview:
        """Generate the high-level structure of forms without detailed fields."""
        provider = self.create_provider()

        # make flat yaml from the wizard_data
        flat_wizard_data = yaml.dump(self.wizard_data)
        schema = FormStructureOverview.model_json_schema()

        prompt = f"""
Create a hierarchical form structure for a business application.

## ABOUT THE BUSINESS
{flat_wizard_data}

## TASK
Create a logical hierarchy of forms to achieve these business goals. Think carefully about how to organize this into a root form and necessary subforms.

## OUTPUT REQUIREMENTS
For this step, just provide:
1. The document title and description
2. A list of forms with their names, titles, and brief descriptions (no fields yet)
3. An explanation of the forms and their relationships

Return valid JSON object based on the following JSON schema:
{schema}
"""

        # Generate response using the OpenRouter provider
        system_message = "You are an expert form designer AI assistant that creates comprehensive form structures for businesses."
        response_json = await provider.json_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.2
        )

        # Convert the JSON response to the FormStructureOverview model
        try:
            return FormStructureOverview.model_validate(response_json)
        except Exception as e:
            self.logger.error(f"Error parsing FormStructureOverview: {str(e)}")
            self.logger.error(f"Response JSON: {response_json}")
            raise ValueError(f"Failed to parse structure overview: {str(e)}")

    async def generate_complete_structure(self) -> CompleteFormStructure:
        """Generate complete form structure including all details."""
        # First, generate the structure overview
        structure_overview = await self.generate_structure_overview()

        # Create FormDetailGenerator instance
        detail_generator = FormDetailGenerator(
            wizard_data=self.wizard_data,
            model_name=self.model_name,
            api_key=self.api_key
        )

        # Create tasks for parallel form detail generation
        tasks = []
        for i, form in enumerate(structure_overview.forms):
            is_root = i == 0  # First form is root
            # Convert FormDetail to dictionary before passing to generate_form_detail
            form_dict = {
                "name": form.name,
                "title": form.title,
                "description": form.description
            }
            task = detail_generator.generate_form_detail(form_dict, is_root)
            tasks.append(task)

        # Execute all tasks in parallel
        form_details = await asyncio.gather(*tasks)

        # Return complete structure
        return CompleteFormStructure(
            document=structure_overview.document,
            forms=form_details,
            explanation=structure_overview.explanation
        )
