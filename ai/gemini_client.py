import json
import os

from google import genai
from google.genai import types


class GeminiClient:
    """
    Small wrapper around Google's Gemini API.

    Responsibilities:
        - Initialize Gemini client
        - Send content relevance requests
        - Request structured JSON output
        - Parse and validate the response

    This class does NOT calculate the final creator score.
    """

    MODEL = "gemini-3.1-flash-lite"

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise RuntimeError(
                "GEMINI_API_KEY environment variable "
                "is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    # =====================================================
    # Content Relevance
    # =====================================================

    def analyze_content_relevance(
        self,
        prompt: str
    ) -> dict:

        if not prompt or not prompt.strip():

            raise ValueError(
                "Gemini prompt cannot be empty."
            )

        response_schema = {
            "type": "object",

            "properties": {

                "relevance_score": {
                    "type": "number",
                    "description": (
                        "Content relevance score from "
                        "0 to 100."
                    )
                },

                "campaign_match": {
                    "type": "string",
                    "enum": [
                        "strong",
                        "good",
                        "weak",
                        "none"
                    ]
                },

                "confidence": {
                    "type": "number",
                    "description": (
                        "Confidence in the assessment "
                        "from 0 to 100."
                    )
                },

                "reasons": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": (
                        "Short factual reasons supporting "
                        "the relevance assessment."
                    )
                },

                "matched_topics": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": (
                        "Topics or product themes in the "
                        "creator content that match the campaign."
                    )
                },

                "missing_topics": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": (
                        "Important campaign topics that are "
                        "not clearly demonstrated."
                    )
                }
            },

            "required": [
                "relevance_score",
                "campaign_match",
                "confidence",
                "reasons",
                "matched_topics",
                "missing_topics"
            ]
        }

        try:

            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_json_schema=response_schema,
                )
            )

        except Exception as ex:

            raise RuntimeError(
                "Gemini API request failed: "
                f"{type(ex).__name__}: {ex}"
            ) from ex

        # =================================================
        # Extract Response
        # =================================================

        response_text = getattr(
            response,
            "text",
            None
        )

        if not response_text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        # =================================================
        # Parse JSON
        # =================================================

        try:

            result = json.loads(
                response_text
            )

        except json.JSONDecodeError as ex:

            raise RuntimeError(
                "Gemini returned invalid JSON.\n"
                f"Response:\n{response_text}"
            ) from ex

        # =================================================
        # Validate Result
        # =================================================

        result = self._validate_result(
            result
        )

        return result

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def _validate_result(
        result: dict
    ) -> dict:

        if not isinstance(
            result,
            dict
        ):

            raise RuntimeError(
                "Gemini response must be a JSON object."
            )

        # -----------------------------------------
        # Required fields
        # -----------------------------------------

        required_fields = [
            "relevance_score",
            "campaign_match",
            "confidence",
            "reasons",
            "matched_topics",
            "missing_topics"
        ]

        for field in required_fields:

            if field not in result:

                raise RuntimeError(
                    "Gemini response is missing "
                    f"required field: {field}"
                )

        # -----------------------------------------
        # Relevance score
        # -----------------------------------------

        try:

            relevance_score = float(
                result["relevance_score"]
            )

        except (
            TypeError,
            ValueError
        ):

            raise RuntimeError(
                "Gemini relevance_score must be numeric."
            )

        result["relevance_score"] = max(
            0.0,
            min(
                relevance_score,
                100.0
            )
        )

        # -----------------------------------------
        # Confidence
        # -----------------------------------------

        try:

            confidence = float(
                result["confidence"]
            )

        except (
            TypeError,
            ValueError
        ):

            raise RuntimeError(
                "Gemini confidence must be numeric."
            )

        result["confidence"] = max(
            0.0,
            min(
                confidence,
                100.0
            )
        )

        # -----------------------------------------
        # Campaign match
        # -----------------------------------------

        valid_matches = {
            "strong",
            "good",
            "weak",
            "none"
        }

        campaign_match = str(
            result["campaign_match"]
        ).strip().lower()

        if campaign_match not in valid_matches:

            raise RuntimeError(
                "Gemini returned invalid "
                f"campaign_match: {campaign_match}"
            )

        result["campaign_match"] = (
            campaign_match
        )

        # -----------------------------------------
        # Reasons
        # -----------------------------------------

        if not isinstance(
            result["reasons"],
            list
        ):

            result["reasons"] = [
                str(
                    result["reasons"]
                )
            ]

        result["reasons"] = [
            str(reason).strip()

            for reason
            in result["reasons"]

            if str(reason).strip()
        ]

        # -----------------------------------------
        # Matched topics
        # -----------------------------------------

        if not isinstance(
            result["matched_topics"],
            list
        ):

            result["matched_topics"] = []

        result["matched_topics"] = [
            str(topic).strip()

            for topic
            in result["matched_topics"]

            if str(topic).strip()
        ]

        # -----------------------------------------
        # Missing topics
        # -----------------------------------------

        if not isinstance(
            result["missing_topics"],
            list
        ):

            result["missing_topics"] = []

        result["missing_topics"] = [
            str(topic).strip()

            for topic
            in result["missing_topics"]

            if str(topic).strip()
        ]

        return result
    