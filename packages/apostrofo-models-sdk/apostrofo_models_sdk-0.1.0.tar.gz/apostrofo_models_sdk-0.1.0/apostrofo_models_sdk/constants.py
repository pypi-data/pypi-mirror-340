from enum import Enum, auto


class ModelNames(str, Enum):
    # Guardrail Models
    PROMPT_INJECTION = "prompt_injection"
    TOXIC_LANGUAGE = "toxic_language"

    # Data Processing Models
    TEXT_MASKING = "text_masking"
    ENTITY_EXTRACTION = "entity_extraction"
    TEXT_CLASSIFICATION = "text_classification"

    # Content Enhancement Models
    TAGS_GENERATION = "tags_generation"
    METADATA_EXTRACTION = "metadata_extraction"

    # Validation Models
    ANSWER_VERIFICATION = "answer_verification"


DEFAULT_API_URL = "http://0.0.0.0:8000"
# API_VERSION = "v1"