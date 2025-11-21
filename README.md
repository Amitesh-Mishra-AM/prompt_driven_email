# 📧 Prompt-Driven Email Productivity Agent

An intelligent, prompt-driven email agent built with **Streamlit** and **Google Gemini**. [cite\_start]This application processes an inbox to categorize emails, extract actionable tasks, and generate auto-replies based on user-defined prompts[cite: 5, 6, 7, 8, 9].

## 🚀 Features

  * **Prompt-Driven Architecture:** The "brain" of the agent. [cite\_start]Users can edit the specific prompts used for categorization, extraction, and drafting[cite: 9, 38].
  * [cite\_start]**Automated Ingestion:** Loads a mock inbox and processes emails to tag them (e.g., "Important", "Spam") and extract tasks (JSON format)[cite: 6, 30, 35].
  * [cite\_start]**Chat Agent:** A chat interface to "talk" to your inbox (e.g., "Summarize this email", "What do I need to do?")[cite: 8, 31, 109].
  * [cite\_start]**Draft Generator:** Auto-generates reply drafts based on selected tones (Professional, Casual, etc.) without sending them automatically[cite: 7, 36, 49].
  * [cite\_start]**Safe & Robust:** Handles API rate limits gracefully and ensures drafts are stored locally for review[cite: 47, 48, 49].

## 🛠️ Prerequisites

  * **Python 3.8+**
  * **Google Gemini API Key** (Free to obtain from [Google AI Studio](https://aistudio.google.com/))

## 📦 Installation

1.  **Clone the repository** (or unzip the project folder):

    ```bash
    git clone <your-repo-url>
    cd email-productivity-agent
    ```

2.  **Install dependencies**:

    ```bash
    pip install streamlit google-generativeai python-dotenv
    ```

## ⚙️ Configuration

1.  Create a file named `.env` in the root directory of the project.
2.  Add your Google Gemini API key to the file:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```
    *Note: Do not commit this file to version control.*

## ▶️ How to Run

Run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

[cite\_start]The application will open automatically in your default web browser at `http://localhost:8501`[cite: 17].

## 📖 Usage Guide

### [cite\_start]1. Loading the Inbox & Processing [cite: 18, 34]

  * Navigate to the **"📥 Inbox & Processing"** tab.
  * The **Mock Inbox** (`mock_inbox.json`) is loaded automatically on startup.
  * Click the **"Run AI Processing"** button.
  * **Note:** The agent processes emails slowly (1 email every 4 seconds) to respect the Free Tier rate limits of the Gemini API.
  * Once finished, you will see tags (e.g., `📂 Newsletter`) and Action Items (e.g., `⚡ Task: Submit Report`) on the email cards.

### [cite\_start]2. Configuring Prompts ("The Brain") [cite: 19, 29, 90]

  * Open the **Sidebar** on the left.
  * Scroll to the **"🧠 Prompt Brain"** section.
  * Here you can edit the instructions the AI uses.
      * *Example:* Change the "Categorization Prompt" to include a new category like "Urgent Finance".
  * Click **"Save Prompts"** to apply changes immediately.

### [cite\_start]3. Chatting with the Agent [cite: 31, 109]

  * Navigate to the **"🤖 Email Agent Chat"** tab.
  * Select an email from the dropdown menu to set the context.
  * Type a question in the chat bar, such as:
      * *"Summarize this email in 3 bullet points."*
      * *"What is the deadline mentioned?"*

### [cite\_start]4. Generating Drafts [cite: 133, 136]

  * Navigate to the **"✍️ Draft Generator"** tab.
  * Select an email you wish to reply to.
  * Choose a **Tone** (Professional, Casual, Urgent).
  * (Optional) Add specific instructions (e.g., "Tell them I'm out of office").
  * Click **"Generate Draft"**. The AI will write a response which you can edit and save.

## 📂 Project Structure

  * [cite\_start]`app.py`: The main entry point containing the Streamlit UI logic[cite: 42].
  * `llm_service.py`: Handles communication with the Google Gemini API, including model auto-discovery and rate limiting.
  * [cite\_start]`prompt_manager.py`: Manages loading, saving, and resetting prompt templates[cite: 38].
  * [cite\_start]`mock_inbox.json`: Contains the sample email data used for the assignment[cite: 54].
  * `.env`: Stores sensitive API keys (not included in repo).

## 🛡️ Troubleshooting

  * **Error: 429 Quota Exceeded:** The app is running too fast for the free API key. The `app.py` includes a built-in delay (`time.sleep(4)`). Do not remove this delay.
  * **Error: Model Not Found:** The `llm_service.py` script automatically scans your account for available models. Ensure your API key has "Generative Language API" enabled in Google Cloud.