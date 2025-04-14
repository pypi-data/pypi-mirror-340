import requests
from typing import Dict, List, Any, TypeVar, cast

from .models import (
    ModelRequest, ModelResponse, REQUEST_TO_RESPONSE_MAP,
    PromptInjectionRequest, PromptInjectionResponse,
    ToxicLanguageRequest, ToxicLanguageResponse,
    TextMaskingRequest, TextMaskingResponse,
    TextClassificationRequest, TextClassificationResponse,
    EntityExtractionRequest, EntityExtractionResponse,
    TagsGenerationRequest, TagsGenerationResponse,
    MetadataExtractionRequest, MetadataExtractionResponse,
    AnswerVerificationRequest, AnswerVerificationResponse,
    ModelNames
)
from .constants import DEFAULT_API_URL
from .exceptions import (
    ApostrofoApiError, AuthenticationError, InvalidRequestError,
    ApiConnectionError, RateLimitError, ServiceError
)

T = TypeVar('T', bound=ModelRequest)
R = TypeVar('R', bound=ModelResponse)


class ApostrofoModelsClient:
    """
    Client for the Apostrofo Models API.

    This client provides methods to interact with various AI models provided by Apostrofo.
    """

    def __init__(
            self,
            api_key: str,
            base_url: str = DEFAULT_API_URL,
            timeout: int = 60
    ):
        """
        Initialize the Apostrofo Models client.

        Args:
            api_key: Your API key for authentication.
            base_url: The base URL of the API. Defaults to the standard Apostrofo API URL.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers to use for API requests.

        Returns:
            Dict containing headers with API key authentication.
        """
        return {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "Accept": "application/json"
        }

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle the API response and raise appropriate exceptions on error.

        Args:
            response: Response object from requests.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            AuthenticationError: If authentication failed.
            InvalidRequestError: If the request was invalid.
            RateLimitError: If rate limit is exceeded.
            ServiceError: If there's a server error.
            ApiConnectionError: If there's a connection error.
        """
        try:
            response_json = response.json()
        except ValueError:
            raise ApostrofoApiError(
                f"Invalid response from API: {response.text}",
                response.status_code,
                response
            )

        if response.status_code == 200:
            return response_json

        error_message = response_json.get('detail', 'Unknown error')

        if response.status_code == 401:
            raise AuthenticationError(error_message, response.status_code, response)
        elif response.status_code == 400:
            raise InvalidRequestError(error_message, response.status_code, response)
        elif response.status_code == 429:
            raise RateLimitError(error_message, response.status_code, response)
        elif 500 <= response.status_code < 600:
            raise ServiceError(error_message, response.status_code, response)
        else:
            raise ApostrofoApiError(error_message, response.status_code, response)

    def run_model(self, request: ModelRequest) -> ModelResponse:
        """
        Run a model with the provided request.

        Args:
            request: The model request.

        Returns:
            The model response.

        Raises:
            Various exceptions based on API response (see _handle_response).
        """
        url = f"{self.base_url}/models/run"

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                data=request.model_dump_json(),
                timeout=self.timeout
            )

            response_data = self._handle_response(response)

            # Get the response type based on the request type
            response_cls = REQUEST_TO_RESPONSE_MAP.get(type(request))
            if not response_cls:
                raise TypeError(f"Unknown request type: {type(request)}")

            return response_cls.model_validate(response_data)

        except requests.exceptions.Timeout:
            raise ApiConnectionError("Request timed out", None, None)
        except requests.exceptions.ConnectionError:
            raise ApiConnectionError("Connection error", None, None)
        except requests.exceptions.RequestException as e:
            raise ApiConnectionError(f"Request error: {str(e)}", None, None)

    def detect_prompt_injection(self, text: str) -> PromptInjectionResponse:
        """
        Detect prompt injection in the given text.

        Args:
            text: The text to analyze.

        Returns:
            PromptInjectionResponse containing the detection results.
        """
        request = PromptInjectionRequest(
            model_name=ModelNames.PROMPT_INJECTION,
            text=text
        )
        return cast(PromptInjectionResponse, self.run_model(request))

    def detect_toxic_language(self, text: str) -> ToxicLanguageResponse:
        """
        Detect toxic language in the given text.

        Args:
            text: The text to analyze.

        Returns:
            ToxicLanguageResponse containing the detection results.
        """
        request = ToxicLanguageRequest(
            model_name=ModelNames.TOXIC_LANGUAGE,
            text=text
        )
        return cast(ToxicLanguageResponse, self.run_model(request))

    def mask_text(self, text: str, tags: List[str]) -> TextMaskingResponse:
        """
        Mask entities in text with tags.

        Args:
            text: The text to process.
            tags: List of tags to identify in the text.

        Returns:
            TextMaskingResponse containing the masked text.
        """
        request = TextMaskingRequest(
            model_name=ModelNames.TEXT_MASKING,
            text=text,
            tags=tags
        )
        return cast(TextMaskingResponse, self.run_model(request))

    def classify_text(
            self,
            text: str,
            parameters: Dict[str, Any]
    ) -> TextClassificationResponse:
        """
        Classify text according to provided parameters.

        Args:
            text: The text to classify.
            parameters: Classification parameters.

        Returns:
            TextClassificationResponse containing the classification results.
        """
        request = TextClassificationRequest(
            model_name=ModelNames.TEXT_CLASSIFICATION,
            text=text,
            parameters=parameters
        )
        return cast(TextClassificationResponse, self.run_model(request))

    def extract_entities(
            self,
            text: str,
            entity_types: List[str]
    ) -> EntityExtractionResponse:
        """
        Extract entities from text.

        Args:
            text: The text to extract entities from.
            entity_types: Types of entities to extract.

        Returns:
            EntityExtractionResponse containing the extracted entities.
        """
        request = EntityExtractionRequest(
            model_name=ModelNames.ENTITY_EXTRACTION,
            text=text,
            entity_types=entity_types
        )
        return cast(EntityExtractionResponse, self.run_model(request))

    def generate_tags(
            self,
            text: str,
            parameters: Dict[str, Any]
    ) -> TagsGenerationResponse:
        """
        Generate tags from text.

        Args:
            text: The text to generate tags from.
            parameters: Tag generation parameters.

        Returns:
            TagsGenerationResponse containing the generated tags.
        """
        request = TagsGenerationRequest(
            model_name=ModelNames.TAGS_GENERATION,
            text=text,
            parameters=parameters
        )
        return cast(TagsGenerationResponse, self.run_model(request))

    def extract_metadata(
            self,
            text: str,
            parameters: Dict[str, Any]
    ) -> MetadataExtractionResponse:
        """
        Extract metadata from text.

        Args:
            text: The text to extract metadata from.
            parameters: Metadata parameters.

        Returns:
            MetadataExtractionResponse containing the extracted metadata.
        """
        request = MetadataExtractionRequest(
            model_name=ModelNames.METADATA_EXTRACTION,
            text=text,
            parameters=parameters
        )
        return cast(MetadataExtractionResponse, self.run_model(request))

    def verify_answer(
            self,
            question: str,
            answer: str
    ) -> AnswerVerificationResponse:
        """
        Verify an answer to a question.

        Args:
            question: The original question.
            answer: The answer to verify.

        Returns:
            AnswerVerificationResponse containing the verification results.
        """
        request = AnswerVerificationRequest(
            model_name=ModelNames.ANSWER_VERIFICATION,
            question=question,
            answer=answer
        )
        return cast(AnswerVerificationResponse, self.run_model(request))