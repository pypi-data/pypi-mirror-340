# Jemma: Your Command-Line Coding Assistant



[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)

[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-brightgreen)](https://cloud.google.com/vertex-ai/docs/generative-ai/models/gemini)

[![Colorama](https://img.shields.io/badge/colorama-terminal%20colors-brightgreen)](https://pypi.org/project/colorama/)



![Jemma](jemma.jpeg)



## Overview



Jemma is a free and open-source command-line tool that brings the power of Google's Gemini API to your terminal.  Get instant coding assistance, codebase explanations, and more, all without leaving your workflow.



## Features



*   **Interactive Code Sessions:**  Ask Jemma coding questions and receive real-time suggestions.

*   **Codebase Explanation:**  Understand complex projects quickly with Jemma's detailed codebase analysis.

*   **Command Watching:**  Let Jemma monitor the output of your commands and provide insights.

*   **Code Editing:**  Automatically apply fixes and features to your code with Jemma's edit capabilities.



## Installation



```bash

pip install .

```



## Configuration



Before using Jemma, you need to configure your Google Gemini API key. You have two options:



1.  **Using the `jemma-init` command:**

   ```bash

   jemma-init

   ```

   This will prompt you to enter your API key, which will be stored in `~/.jemma/config`.



2.  **Setting the `GEMINI_API_KEY` environment variable:**

   ```bash

   export GEMINI_API_KEY="YOUR_API_KEY"

   ```



You can further configure Jemma using the `jemma-configure` command to select your preferred model and adjust settings like temperature and max output tokens.



```bash

jemma-configure

```



## Usage



Jemma provides several commands to help you with your coding tasks:



*   **Interactive Code Session:**

   ```bash

   jemma --chat

   ```

   Starts an interactive session where you can ask coding questions.



*   **Codebase Explanation:**

   ```bash

   jemma --explain

   ```

   Provides a detailed explanation of your codebase.



*   **Command Watching:**

   ```bash

   jemma --watch "pytest"

   ```

   Watches the output of the `pytest` command and provides analysis.



*   **Code Editing:**

   ```bash

   jemma --edit "Fix the bug in the login function"

   ```

   Asks Jemma to help you fix bugs or add features to your code.



## Roadmap



- [x] Fix configuration and improve the use of the configuration file

- [x] Fix edit with line enumeration

- [x] Add support for multiple models (Gemini Pro, etc.)

- [x] Implement configuration via command-line arguments

- [ ] Create command for starting new projects

- [ ] Improve error handling and logging

- [ ] Add unit tests

- [ ] MIT license
