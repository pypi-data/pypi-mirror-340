# Apostrofo Models SDK

A Python SDK for the Apostrofo Models API that provides easy access to various AI models for text analysis, classification, and processing.

## Installation

```bash
pip install apostrofo-models-sdk
```

## Features

- Automated authentication with API key
- Access to multiple AI models:
  - Guardrails: Prompt injection and toxic language detection
  - Data Processing: Text masking, classification, and entity extraction
  - Content Enhancement: Tags generation and metadata extraction
  - Validation: Answer verification
- Comprehensive error handling
- Type hints for better IDE support
- Pydantic models for request and response validation

## Quick Start

```python
from apostrofo_models_sdk import ApostrofoModelsClient

# Initialize client with your API key
client = ApostrofoModelsClient(api_key="your_api_key")

# Detect toxic language
toxic_result = client.detect_toxic_language("Text to analyze")
print(f"Is toxic: {toxic_result.is_toxic}")
print(f"Toxicity score: {toxic_result.toxicity_score}")
print(f"Explanation: {toxic_result.explanation}")

# Extract entities
entity_result = client.extract_entities(
    "John Smith works at Apostrofo in New York.", 
    entity_types=["PERSON", "ORGANIZATION", "LOCATION"]
)
print(entity_result.entities)
```

## Authentication

The SDK requires an API key for authentication, which is passed as a header (`X-API-Key`) to all API requests. You can obtain an API key by signing up at [Apostrofo AI](https://apostrofo.ai).

```python
client = ApostrofoModelsClient(
    api_key="your_api_key",
    base_url="https://api.apostrofo.ai"  # Optional, default URL
)
```

## Available Models

### Guardrails

```python
# Prompt Injection Detection
injection_result = client.detect_prompt_injection("Ignore previous instructions and...")
print(f"Is injection: {injection_result.is_injection}")

# Toxic Language Detection
toxic_result = client.detect_toxic_language("Text to analyze")
print(f"Is toxic: {toxic_result.is_toxic}")
```

### Data Processing

```python
# Text Masking
mask_result = client.mask_text(
    "My name is John and my email is john@example.com", 
    tags=["EMAIL", "PERSON"]
)
print(mask_result.bracketed_text)

# Text Classification
classification_result = client.classify_text(
    "I'm really happy with this product!",
    parameters={
        "sentiment": {
            "description": "Sentiment of the text",
            "type": "string",
            "properties": {
                "values": ["positive", "negative", "neutral"]
            }
        }
    }
)
print(classification_result.results)

# Entity Extraction
entity_result = client.extract_entities(
    "Apple Inc. is headquartered in Cupertino, California.",
    entity_types=["ORG", "LOC"]
)
print(entity_result.entities)
```

### Content Enhancement

```python
# Tags Generation
tags_result = client.generate_tags(
    "This is a blog post about Python programming and data science.",
    parameters={
        "topics": {
            "description": "Topics mentioned in the text",
            "properties": {
                "max": 5
            }
        }
    }
)
print(tags_result.results)

# Metadata Extraction
metadata_result = client.extract_metadata(
    "Publication: Science Journal\nDate: 2023-03-15\nTitle: New Advances in AI",
    parameters={
        "publication_info": {
            "description": "Publication information",
            "properties": {
                "fields": ["journal", "date", "title"]
            }
        }
    }
)
print(metadata_result.results)
```

### Validation

```python
# Answer Verification
verification_result = client.verify_answer(
    question="What is the capital of France?",
    answer="The capital of France is London."
)
print(f"Is accurate: {verification_result.is_accurate}")
print(f"Explanation: {verification_result.explanation}")
```

## Error Handling

The SDK provides comprehensive error handling with custom exceptions:

```python
from apostrofo_models_sdk import ApostrofoApiError, AuthenticationError

try:
    result = client.detect_toxic_language("Test text")
except AuthenticationError:
    print("Invalid API key")
except ApostrofoApiError as e:
    print(f"API error: {e.message}, status code: {e.status_code}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This SDK is licensed under the MIT License - see the LICENSE file for details.