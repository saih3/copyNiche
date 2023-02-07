from typing import List
import os
import openai
import argparse
import re


MAX_INPUT_LENGTH = 12


def main():
    print("Running CopyNiche ❤️")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User input: {user_input}")

    if validate_length(user_input):
        result = generate_branding_snippet(user_input)
        keywords = generate_keywords(user_input)
    else:
        raise ValueError(
            f"Input length is too long. Must be under {MAX_INPUT_LENGTH}. Submitted input is {len(user_input)} characters long")


def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH


def generate_branding_snippet(prompt: str) -> str:
    openai.api_key = os.environ["OPENAI_API_KEY"]

    enriched_prompt = f"Generate upbeat branding for {prompt}"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="text-davinci-003", prompt=enriched_prompt, max_tokens=32)

    # Extract output text.
    branding_text: str = response["choices"][0]["text"]
    # Strip whitespace.
    branding_text = branding_text.strip()
    # Add ... to truncated statements.
    last_char = branding_text[-1]
    if last_char not in {".", "?", "!", ","}:
        branding_text += "..."

    print(branding_text)
    return branding_text


def generate_keywords(prompt: str) -> List[str]:
    openai.api_key = os.environ["OPENAI_API_KEY"]

    enriched_prompt = f"Generate related branding keywords for {prompt}"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="text-davinci-003", prompt=enriched_prompt, max_tokens=32)

    # Extract output text.
    branding_keywords: str = response["choices"][0]["text"]
    # Strip whitespace.
    branding_keywords = branding_keywords.strip()
    keywords_array = re.split(",|\n|;|-", branding_keywords)
    # lower case and remove strip whitespace at the beginning of words
    keywords_array = [k.lower().strip() for k in keywords_array]
    # only put strings that are not empty
    keywords_array = [k for k in keywords_array if len(k) > 0]

    print(keywords_array)
    return keywords_array


if __name__ == "__main__":
    main()
