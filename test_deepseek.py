#!/usr/bin/env python3
"""
Quick test script to verify DeepSeek API integration
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_deepseek_connection():
    """Test basic DeepSeek API connection"""
    print("Testing DeepSeek API connection...")

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ ERROR: DEEPSEEK_API_KEY not found in .env file")
        return False

    print(f"✓ API Key found: {api_key[:10]}...")

    try:
        # Initialize DeepSeek client
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

        # Test with a simple prompt
        print("\nSending test request to DeepSeek...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Generate a simple multiple choice question about Python programming. Return only a JSON object with keys: question, options (array of 4), correct_answer."}
            ],
            max_tokens=500,
            temperature=0.7
        )

        print("✓ DeepSeek API response received!")
        print(f"\nTokens used: {response.usage.prompt_tokens + response.usage.completion_tokens}")
        print(f"\nResponse:\n{response.choices[0].message.content}")

        return True

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_deepseek_connection()
    if success:
        print("\n✅ DeepSeek integration is working correctly!")
    else:
        print("\n❌ DeepSeek integration test failed. Please check your API key and connection.")
