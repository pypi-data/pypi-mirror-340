"""Form wizard models."""

from typing import List, Literal, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, EmailStr


class BusinessInfo(BaseModel):
    description: str = Field(..., description="Brief description of your business or product")
    website: HttpUrl = Field(..., description="Your business website (if available)")
    email: EmailStr = Field(..., description="Contact email address")
    phone: str = Field(..., description="Contact phone number")
    industry: str = Field(..., description="Industry (e.g. Healthcare, Fintech)")
    type: Literal["b2b", "b2c", "internal", "custom"] = Field(
        ...,
        description="Type of customer interaction (b2b, b2c, internal use, or custom)"
    )


class BusinessGoals(BaseModel):
    goals: List[str] = Field(
        ...,
        min_items=1,
        max_items=3,
        description="Main goals of the business related to the form (1 to 3 items)"
    )


class BotSettings(BaseModel):
    bot_name: str = Field(..., description="Name of the assistant bot")
    completion_threshold: int = Field(
        100,
        ge=50,
        le=100,
        description="Form is considered completed when this percentage is reached (50–100)"
    )
    bot_style: str = Field(
        "friendly",
        description="Bot's communication style (e.g. formal, friendly, casual)"
    )
    use_emojis: bool = Field(
        True,
        description="Whether the bot is allowed to use emojis in its messages"
    )
    simulate_delay: bool = Field(
        True,
        description="Whether the bot should simulate a typing delay before responding"
    )
    welcome_message: str = Field(
        None,
        description="Text shown to users before they start filling out the form"
    )
    completion_message: str = Field(
        None,
        description="Text shown to users after they complete the form"
    )


class DocumentSettings(BaseModel):
    model_tier: Literal["low", "medium", "high"] = Field(
        "medium",
        description="AI model tier used to process and analyze the form (low = basic, high = advanced)"
    )

class DataRequest(BaseModel):
    business: BusinessInfo
    business_goals: BusinessGoals

class FormIntentRequest(BaseModel):
    data: DataRequest
    document: DocumentSettings
    bot: BotSettings
    notes: str = Field(..., description="Any additional thoughts or wishes")


class TestFormIntentRequest(BaseModel):
    """Testing form model"""

    data: DataRequest
    document: Dict[str, Any] = Field(default_factory=dict)
    bot: Dict[str, Any] = Field(default_factory=dict)
    notes: str = Field(..., description="Any additional thoughts or wishes")
