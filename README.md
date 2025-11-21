An intelligent, prompt-driven email agent built with **Streamlit** and **Google Gemini**. This project processes an inbox to categorize emails, extract actionable tasks, and generate reply drafts using configurable prompts.

## 🚀 Features

- **Prompt-Driven Architecture:** Users can edit the prompts used for categorization, extraction, and drafting.
- **Automated Ingestion:** Loads a mock inbox and processes emails to tag them (e.g., "Important", "Spam") and extract tasks (JSON format).
- **Chat Agent:** A chat interface to ask questions about individual emails (summaries, deadlines, actions).
- **Draft Generator:** Auto-generates reply drafts across tones (Professional, Casual, Urgent) for review before sending.
- **Rate-limit aware:** Built-in pacing and error handling to reduce hitting free-tier rate limits.

## 🛠️ Prerequisites

- **Python 3.8+**
- **Google Gemini API Key** (obtain from Google AI Studio or Google Cloud Console)

## 📦 Installation

1. Clone the repository (or unzip the project folder):

```bash
git clone git@github.com:Amitesh-Mishra-AM/prompt_driven_email.git
cd prompt_driven_email
```

2. Install dependencies:

```bash
pip install streamlit google-generativeai python-dotenv
```

Notes:
- If you prefer a requirements file, create one with the packages above and run `pip install -r requirements.txt`.

## ⚙️ Environment / API Key

1. In the project root (the same folder as `app.py`), create a file named `.env`.

2. Add your Google Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

- Do not commit `.env` to version control. Add it to `.gitignore` if not already ignored.
- The app uses `python-dotenv` to load `.env`. If you prefer not to use `.env`, you can set the environment variable manually.

Windows (cmd.exe) example without a .env file:

```cmd
set GEMINI_API_KEY=your_actual_api_key_here
streamlit run app.py
```

Or one-liner:

```cmd
set GEMINI_API_KEY=your_actual_api_key_here && streamlit run app.py
```

Mac/Linux (bash/zsh) example:

```bash
export GEMINI_API_KEY=your_actual_api_key_here
streamlit run app.py
```

## ▶️ Run the App

From the project root run:

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser if it doesn't open automatically.

## 📖 Usage Guide

### 1. Loading the Inbox & Processing

- Navigate to the **"📥 Inbox & Processing"** tab.
- The Mock Inbox (`mock_inbox.json`) is loaded automatically on startup.
- Click **"Run AI Processing"** to process emails. The app paces requests to avoid hitting free-tier API limits.

### 2. Editing Prompts ("The Brain")

- Open the **Sidebar** and go to **"🧠 Prompt Brain"** to edit or save prompt templates used by the agent.

### 3. Chatting with the Agent

- Use the **"🤖 Email Agent Chat"** tab to ask questions about an email (summaries, deadlines, next steps).

### 4. Generating Drafts

- Use the **"✍️ Draft Generator"** tab to generate reply drafts. Choose a tone and optionally add instructions before generating.

## 📂 Project Structure

- `app.py`: The main entry point containing the Streamlit UI logic.
- `llm_service.py`: Handles communication with the Google Gemini API (model auto-discovery and configuration).
- `prompt_manager.py`: Manages loading, saving, and resetting prompt templates.
- `mock_inbox.json`: Sample email data used for testing.
- `.env`: Stores sensitive API keys (not included in the repo).

## 🛡️ Troubleshooting

- **Error: 429 Quota Exceeded:** The app may be running too quickly for your API key. A delay is enforced in `app.py` to reduce this — do not remove it unless you understand the quota implications.
- **Error: Model Not Found:** `llm_service.py` scans available models. Ensure your API key has the "Generative Language API" enabled in Google Cloud and that the key is valid.