import os

from google import genai


def main():

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY environment variable "
            "is not configured."
        )

    print(
        "✓ GEMINI_API_KEY detected"
    )

    client = genai.Client(
        api_key=api_key
    )

    print(
        "Sending test request..."
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=(
            "Reply with exactly one word: "
            "READY"
        )
    )

    print()
    print(
        "Gemini response:"
    )

    print(
        response.text
    )


if __name__ == "__main__":
    main()