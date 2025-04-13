# pyhowto

[![CI](https://github.com/ablil/pyhowto/actions/workflows/ci.yaml/badge.svg?event=push)](https://github.com/ablil/pyhowto/actions/workflows/ci.yaml)

Simply [howdoi](https://github.com/gleitz/howdoi) but **AI Powered**.

A minimalist command-line tool that fetches concise technical solutions from AI providers (OpenAI, Gemini, DeepSeek).
Like howdoi, but with modern AI capabilities.

## Installation

```shell
pip instal pyhowdoi
```

## Usage

**Basic**

```shell
howto get current timestamp in bash
# output: `date +%s` (seconds since epoch) or `date +"%Y-%m-%d %H:%M:%S"` (human-readable)
```

**Switch AI provider**

```shell
howto --provider deepseek get current timestamp in bash
`date +%s` (seconds since epoch) or `date +"%Y-%m-%d %H:%M:%S"` (human-readable)
```

Supported AI providers:

| AI provider      | Required env key | Model            |
|------------------|------------------|------------------|
| gemini (default) | GEMINI_API_KEY   | gemini-1.5-flash |
| deepseek         | DEEPSEEK_API_KEY | deepseek-chat    |
| openai           | OPENAI_API_KEY   | gpt-4o           |
