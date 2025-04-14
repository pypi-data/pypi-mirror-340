[![PyPI version](https://badge.fury.io/py/geegle.svg)](https://badge.fury.io/py/geegle)
[![Python version](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](https://www.apache.org/licenses/LICENSE-2.0)

# Geegle
Geegle is a CLI chat app that combines web search, academic research, and session management using SQLite for local data storage. It uses APIs from OpenAI, Tavily, and Exa to provide answers with web sources, for users seeking information directly from their terminal.

# Features

* Real-Time Web Search: Integrates Tavily for up-to-date web information
* Academic Research: Uses Exa to fetch research papers and scholarly content
* Session Management: Store and switch between multiple conversation sessions using SQLite
* Model Selection: Choose between different AI models (GPT-3.5, GPT-4, Claude, etc.)
* Prompt Customization: Create and manage custom system prompts to tailor responses
* Command Autocomplete: Tab completion for commands and arguments
* Interactive Menus: User-friendly navigation for all features
* Data Export: Export session data to JSON files for backup or sharing

# Installation
Follow these steps to set up Geegle on your system.

## Prerequisites

Python: Version 3.7 or higher
pip: Latest version recommended

# Install the package

```bash 
pip install geegle
```

# Configuration

Geegle requires API keys for OpenAI, Tavily, and Exa. You can configure them in three ways:

1. First-Time Setup Wizard

When you first run Geegle, it will prompt you to enter your API keys if they aren't found:

```bash
geegle
```

You'll be prompted to enter your API keys, which will be saved in ~/.geegle/config.json

2. Environment Variables
You can set the following environment variables:

```bash
export OPENAI_API_KEY=your_openai_api_key
export TAVILY_API_KEY=your_tavily_api_key
export EXA_API_KEY=your_exa_api_key
```

You can get these API keys from:

https://platform.openai.com/docs/overview
https://tavily.com/
https://exa.ai/

# Usage

Start the application:

```bash
geegle
```

# Quick Start:

1. Type a question (e.g., "What's the capital of France?") and press Enter.
2. Use commands (starting with /) to manage sessions or data.
3. Press Tab to autocomplete commands and arguments.
4. Type exit to quit.


# Commands
## Basic Commands

```bash
/clear: Clears the current session's conversation history.
/clear all: Deletes all session data (requires confirmation).
/export [filename]: Exports all sessions to a JSON file (default: sessions_export.json).
/help: Shows a list of commands and usage instructions.
```

## Session Management

```bash
/session: Opens the session management menu.
/session [name]: Switches directly to the specified session.
```

## Model Selection

```bash
/model: Opens the model selection menu.
/model [name]: Switches directly to the specified model.
```

Available models:

* gpt-3.5-turbo
* gpt-4-turbo-preview
* gpt-4o
* claude-3-opus-20240229
* claude-3-sonnet-20240229
* claude-3-haiku-20240307


## Prompt Customization

```bash
/prompt: Opens the prompt customization menu.
/prompt [template_name]: Uses the specified prompt template.
/prompt [text]: Sets a custom system prompt.
```

Default templates:

* default: General assistant
* concise: Brief, factual responses
* detailed: In-depth analysis
* coding: Code-focused assistance

## Keyboard Shortcuts

Tab: Autocomplete commands and arguments
↑/↓: Navigate command history
exit: Exits the application

# Examples

## Creating a new session

```bash
/session
# Select "n" to create a new session
# Enter "product-research"
# Now you're in a new conversation session
```

## Switching models
```bash
/model
# View available models and select one
# Or use direct command: /model gpt-4o
```

## Customizing prompts
```bash
/prompt
# Create a custom prompt or use a template
# Or use direct command: /prompt coding
```

# Advanced Usage

## Autocomplete
Press Tab to complete commands and arguments:

```bash
/m[Tab]       # Completes to "/model"
/model g[Tab]  # Shows available models starting with "g"
/session p[Tab] # Completes to existing sessions starting with "p"
```

## Multi-line Prompts
When creating custom prompts, you can enter multiple lines:

```bash
/prompt
# Select "c" to create custom prompt
# Enter your prompt, press Enter twice when done
```

## Adding Custom Models

You can add custom models through the model menu:
```bash
/model
# Select "a" to add a custom model
# Enter the model identifier
```

# Contributing
See CONTRIBUTING.md for details on how to contribute to this project.

# License
This project is licensed under the Apache License 2.0 - see the License file for details.