#!/usr/bin/env python3

import argparse

from . import providers

def main():
    parser = argparse.ArgumentParser(
        prog='howto',
        description='Ask AI who to do something',
        epilog='still in beta/development',
        add_help=False
    )

    parser.add_argument("-p", "--provider", choices=['gemini', 'deepseek', 'openai'], default='gemini',
                        help='AI provider (default: gemini)')
    parser.add_argument("question", nargs=argparse.REMAINDER)

    args = parser.parse_args()
    question = ' '.join(args.question)
    provider = args.provider

    if provider == 'gemini':
        print(providers.ask_gemini(question))
    elif provider == 'deepseek':
        print(providers.ask_deepseek(question))
    elif provider == 'openai':
        print(providers.ask_openai(question))
    else:
        raise Exception("unknown AI provider")
