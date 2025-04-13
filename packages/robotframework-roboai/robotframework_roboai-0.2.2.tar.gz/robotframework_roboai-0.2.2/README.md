# 🤖 RoboAI – AI-Powered Library for Robot Framework

**RoboAI** is a custom AI library for [Robot Framework](https://robotframework.org/) that integrates with OpenAI to bring intelligence to your automation tests. You can ask AI questions, classify text, generate dynamic data, translate input, intelligently find elements, and more — all directly within your `.robot` test cases.

---

## 🚀 Features

- 💬 **Ask GPT** anything from your tests
- 🧠 **Classify text** with AI logic (e.g., logs, messages, errors)
- 🌍 **Translate text** into different languages and input into fields
- ⬇️ **Find elements within a parent section** using AI
- 🔍 **Auto-correct XPath** if the given one fails
- 🔑 Easy-to-use **custom keywords** for Robot Framework
- ♻️ Extendable with more AI tools (Claude, Gemini, local LLMs)

---

## 🛠️ Installation

```bash
pip install robotframework-roboai
```

---

## 💡 Example Usage

```robot
*** Settings ***
Library    RoboAI
Library    SeleniumLibrary

*** Test Cases ***
Ask Something
    ${response}=    Ask GPT    What is the capital of France?
    Log    ${response}

Translate And Input
    Input Text In Other Language    xpath://input[@id='name']    Hello    Spanish

Find Element In Section
    ${xpath}=    Extract XPath From Section Using AI    xpath://div[@class='form']    A button that submits the form    //button
    Click Element    xpath=${xpath}

Handle Broken XPath
    ${corrected_xpath}=    Fix XPath Using AI    //button[@id='submit']
    Click Element    xpath=${corrected_xpath}
```

---

## 📊 Roadmap

- [x] Basic GPT integration
- [x] Text classification
- [x] Translation support
- [x] AI element discovery from sections
- [x] XPath correction
- [ ] Support for local LLMs
- [ ] Caching + learning from successful XPath resolutions

---

## 🌐 License

MIT

---

Made with ❤️ by RoboAI
