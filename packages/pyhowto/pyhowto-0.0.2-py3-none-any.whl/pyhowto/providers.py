#!/usr/bin/env python3
import os

import google.generativeai as genai
from openai import OpenAI

prompt = """
how to {}


Give concise and short solution/answer, to the point.
If the answer is technical, just give the technical solution.
Keep in mind the answer will be displayed on Terminal.
"""


def ask_deepseek(howto: str) -> str:
    assert 'DEEPSEEK_API_KEY' in os.environ.keys(), "missing env variable DEEPSEEK_API_KEY"
    client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")
    message = [{"role": "user", "content": prompt.format(howto)}]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=message
    )
    return response.choices[0].message.content


def ask_gemini(howto: str) -> str:
    assert 'GEMINI_API_KEY' in os.environ.keys(), "missing env variable GEMINI_API_KEY"
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt.format(howto))
    return response.text


def ask_openai(howto: str) -> str:
    assert 'OPENAI_API_KEY' in os.environ.keys(), "missing env variable OPENAI_API_KEY"
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.responses.create(
        model="gpt-4o",
        input=prompt.format(howto)
    )
    return response.output_text


if __name__ == '__main__':
    question = 'substitute string in bash'
    print(ask_gemini(question))
