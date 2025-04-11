"""Simple test script for FormGeneratorService."""

import os
import asyncio
import json
from pydantic import ValidationError
from pydantic3.agents.wizards.form.form_generator import FormStructureGenerator
from pydantic3.agents.wizards.form.models import FormIntentRequest

# Test data for form generation
WIZARD_DATA = {
    "business": {
        "description": "We help small businesses manage their finances through a simple mobile app.",
        "website": "https://examplefinanceapp.com",
        "email": "support@examplefinanceapp.com",
        "phone": "+1-800-555-0199",
        "industry": "Fintech",
        "type": "b2b"
    },
    "business_goals": {
        "goals": [
            "Collect user feedback on new product features",
            "Qualify leads through a conversational form",
            "Automate onboarding process for new users"
        ]
    },
    "document": {
        "model_tier": "high"
    },
    "bot": {
        "bot_name": "FinBot",
        "completion_threshold": 90,
        "bot_style": "friendly",
        "use_emojis": True,
        "simulate_delay": True,
        "welcome_message": "👋 Hi there! Ready to make managing finances easier?",
        "completion_message": "Thanks! 🎉 We'll use your input to improve your experience."
    },
    "notes": "We plan to integrate this into our Telegram channel and website widget."
}

# test validation
try:
    form_intent = FormIntentRequest(**WIZARD_DATA)
    print("✅ Validation passed")
    print(form_intent)
except ValidationError as e:
    print(f"❌ Validation error: {e}")
    import traceback
    traceback.print_exc()


async def test_form_generator():
    """Test FormGeneratorService with parallel form generation."""
    # Get API key from environment
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        return

    print("🧪 Starting FormStructureGenerator test")
    print("🔄 Creating FormStructureGenerator...")
    generator = FormStructureGenerator(
        wizard_data=WIZARD_DATA,
        api_key=api_key
    )

    try:
        # Generate complete structure (overview + parallel form details)
        print("\n🔄 Generating complete form structure...")
        complete_structure = await generator.generate_complete_structure()

        # Print the results
        print("\n✅ Generated complete structure:")
        print(complete_structure)

        return complete_structure

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = asyncio.run(test_form_generator())
    if result:
        print("\n✅ Test completed successfully")
    else:
        print("\n❌ Test failed")
