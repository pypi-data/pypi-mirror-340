# pyhowto


<h1 align="center">howto</h1>
<h2 align="center">Another <a href="https://github.com/gleitz/howdoi">howdoi</a> but <strong>AI Powered</strong></h2>
<p align="center"><strong>
A minimalist command-line tool that fetches concise technical solutions from AI providers (OpenAI, Gemini, DeepSeek).
with AI capabilities.
</strong></p>

[![CI](https://github.com/ablil/pyhowto/actions/workflows/ci.yaml/badge.svg?event=push)](https://github.com/ablil/pyhowto/actions/workflows/ci.yaml)

## Installation

```shell
pip instal pyhowdoi
```

## Usage

**Basic**

```shell
$ howto get current timestamp in bash
> `date +%s` (seconds since epoch) or `date +"%Y-%m-%d %H:%M:%S"` (human-readable)
```

**Switch AI provider**

```shell
$ howto --provider deepseek get current timestamp in bash
> `date +%s` (seconds since epoch) or `date +"%Y-%m-%d %H:%M:%S"` (human-readable)
```

Supported AI providers:

| AI provider      | Required env key | Model            |
|------------------|------------------|------------------|
| gemini (default) | GEMINI_API_KEY   | gemini-1.5-flash |
| deepseek         | DEEPSEEK_API_KEY | deepseek-chat    |
| openai           | OPENAI_API_KEY   | gpt-4o           |
