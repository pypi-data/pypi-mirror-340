from typing import Dict, List, Optional, Union, Any, Literal, Type, TypeVar, get_type_hints
from pydantic import BaseModel, Field
from .constants import ModelNames


class ModelRequestBase(BaseModel):
    """Base model for all model inference requests"""
    model_name: ModelNames = Field(..., description="Name of the model to use")


# Parameter schemas
class ClassificationParameterProperties(BaseModel):
    values: Optional[List[str]] = Field(None, description="List of allowed values for this classification")


class ClassificationParameter(BaseModel):
    description: str = Field(..., description="Description of what this classification parameter represents")
    type: Literal["string", "boolean"] = Field(..., description="Type of the parameter")
    properties: Optional[ClassificationParameterProperties] = Field(None, description="Additional properties")


class TagsParameterProperties(BaseModel):
    max: Optional[int] = Field(None, description="Maximum number of tags to generate")


class TagsParameter(BaseModel):
    description: str = Field(..., description="Description of what these tags represent")
    properties: Optional[TagsParameterProperties] = Field(None, description="Additional properties")


class MetadataParameterProperties(BaseModel):
    fields: Optional[List[str]] = Field(None, description="List of fields to extract")


class MetadataParameter(BaseModel):
    description: str = Field(..., description="Description of the metadata to extract")
    properties: Optional[MetadataParameterProperties] = Field(None, description="Additional properties")


# Guardrails models
class PromptInjectionRequest(ModelRequestBase):
    text: str = Field(..., description="Text to analyze for prompt injection")


class PromptInjectionResponse(BaseModel):
    is_injection: bool = Field(..., description="Whether prompt injection was detected")
    confidence: int = Field(..., description="Confidence score of the detection")
    explanation: str = Field(..., description="Explanation of the detection")
    analysis: Dict[str, Any] = Field(..., description="Detailed analysis of injection techniques")
    formatted_output: str = Field(..., description="Human-readable formatted output")


class ToxicLanguageRequest(ModelRequestBase):
    text: str = Field(..., description="Text to analyze for toxic content")


class ToxicLanguageResponse(BaseModel):
    is_toxic: bool = Field(..., description="Whether toxic language was detected")
    toxicity_score: int = Field(..., description="Toxicity score")
    explanation: str = Field(..., description="Explanation of the detection")
    categories: Dict[str, Any] = Field(..., description="Detailed analysis by category")
    formatted_output: str = Field(..., description="Human-readable formatted output")


# Data Processing models
class TextMaskingRequest(ModelRequestBase):
    text: str = Field(..., description="Text to process")
    tags: List[str] = Field(..., description="Tags to identify in text")


class TextMaskingResponse(BaseModel):
    tagged_pairs: List[List[str]] = Field(..., description="List of [word, tag] pairs")
    bracketed_text: str = Field(..., description="Text with tags in brackets")
    tags: List[str] = Field(..., description="Tags used for identification")


class TextClassificationRequest(ModelRequestBase):
    text: str = Field(..., description="Text to classify")
    parameters: Dict[str, ClassificationParameter] = Field(
        ...,
        description="Classification parameters that specify what needs to be classified"
    )


class TextClassificationResponse(BaseModel):
    results: Dict[str, Any] = Field(..., description="Classification results")


class EntityExtractionRequest(ModelRequestBase):
    text: str = Field(..., description="Text to extract entities from")
    entity_types: List[str] = Field(..., description="Types of entities to extract")


class EntityExtractionResponse(BaseModel):
    entities: Dict[str, List[str]] = Field(..., description="Extracted entities by type")


# Content Enhancement models
class TagsGenerationRequest(ModelRequestBase):
    text: str = Field(..., description="Text to generate tags from")
    parameters: Dict[str, TagsParameter] = Field(
        ...,
        description="Tag generation parameters that specify what tags to generate"
    )


class TagsGenerationResponse(BaseModel):
    results: Dict[str, List[str]] = Field(..., description="Generated tags by category")


class MetadataExtractionRequest(ModelRequestBase):
    text: str = Field(..., description="Text to extract metadata from")
    parameters: Dict[str, MetadataParameter] = Field(
        ...,
        description="Metadata parameters that specify what metadata to extract"
    )


class MetadataExtractionResponse(BaseModel):
    results: Dict[str, Dict[str, str]] = Field(..., description="Extracted metadata")


# Validation models
class AnswerVerificationRequest(ModelRequestBase):
    question: str = Field(..., description="Original question")
    answer: str = Field(..., description="Answer to verify")


class AnswerVerificationResponse(BaseModel):
    is_accurate: Optional[Union[bool, str]] = Field(..., description="Accuracy assessment")
    confidence: int = Field(..., description="Confidence score of verification")
    explanation: str = Field(..., description="Explanation of verification")
    corrections: Dict[str, Any] = Field(..., description="Corrections to inaccuracies")
    formatted_output: str = Field(..., description="Human-readable formatted output")


# Map of request types to response types
REQUEST_TO_RESPONSE_MAP = {
    PromptInjectionRequest: PromptInjectionResponse,
    ToxicLanguageRequest: ToxicLanguageResponse,
    TextMaskingRequest: TextMaskingResponse,
    TextClassificationRequest: TextClassificationResponse,
    EntityExtractionRequest: EntityExtractionResponse,
    TagsGenerationRequest: TagsGenerationResponse,
    MetadataExtractionRequest: MetadataExtractionResponse,
    AnswerVerificationRequest: AnswerVerificationResponse,
}

# Type aliases for Union types
ModelRequest = Union[
    PromptInjectionRequest,
    ToxicLanguageRequest,
    TextMaskingRequest,
    TextClassificationRequest,
    EntityExtractionRequest,
    TagsGenerationRequest,
    MetadataExtractionRequest,
    AnswerVerificationRequest,
]

ModelResponse = Union[
    PromptInjectionResponse,
    ToxicLanguageResponse,
    TextMaskingResponse,
    TextClassificationResponse,
    EntityExtractionResponse,
    TagsGenerationResponse,
    MetadataExtractionResponse,
    AnswerVerificationResponse,
]

# Create a mapping of model names to request classes
MODEL_NAME_TO_REQUEST_CLASS = {
    ModelNames.PROMPT_INJECTION: PromptInjectionRequest,
    ModelNames.TOXIC_LANGUAGE: ToxicLanguageRequest,
    ModelNames.TEXT_MASKING: TextMaskingRequest,
    ModelNames.TEXT_CLASSIFICATION: TextClassificationRequest,
    ModelNames.ENTITY_EXTRACTION: EntityExtractionRequest,
    ModelNames.TAGS_GENERATION: TagsGenerationRequest,
    ModelNames.METADATA_EXTRACTION: MetadataExtractionRequest,
    ModelNames.ANSWER_VERIFICATION: AnswerVerificationRequest,
}