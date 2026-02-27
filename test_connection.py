import os
from openai import OpenAI
from dotenv import load_dotenv


def test_connection():
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"API Key present: {bool(api_key)}")

    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found.")
        return

    models_to_test = [
        "arcee-ai/trinity-large-preview:free",
        "stepfun/step-3.5-flash:free",
    ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    for model in models_to_test:
        print(f"\n--- Testing model: {model} ---")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say 'OK'"}],
                max_tokens=10,
            )
            content = response.choices[0].message.content.strip()
            print(f"Response: {content}")
            print(f"SUCCESS: {model} is reachable.")
        except Exception as e:
            print(f"FAILED: {model} - {e}")


if __name__ == "__main__":
    test_connection()
