# AI Troubleshooting Assistant for Technology Operations

## Project Idea

Technology operations teams often lose time searching through scattered documents to fix common technical issues, such as a Payment API returning HTTP 500 errors. This project is a **knowledge-base-driven troubleshooting assistant**. A user describes a technical problem in plain English. The app finds the most relevant entry in a structured knowledge base and uses an LLM to turn it into a clear, step-by-step troubleshooting response.

Key idea: the AI only answers when a relevant knowledge base entry is found. If nothing matches, the app says so and asks for more details instead of guessing. This reduces made-up answers and saves API calls.

## How It Works

1. The user enters a technical problem in the Streamlit web interface.
2. The app compares the question to the JSON knowledge base using TF-IDF and cosine similarity.
3. A similarity threshold check is applied (score >= 0.20).
   - **Match found (score >= 0.20):** the retrieved KB entry and the question are sent to the Groq API (`openai/gpt-oss-20b`). The model generates a structured troubleshooting response, which is displayed in Streamlit.
   - **No match (score < 0.20):** the app shows "Problem not found in Knowledge Base" and asks the user for more details. The Groq API is not called.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.9+ |
| Web interface | Streamlit |
| Retrieval | TF-IDF and cosine similarity (scikit-learn) |
| Knowledge base | JSON file with 10 common technical issues |
| LLM | Groq API, model `openai/gpt-oss-20b` |
| Configuration | python-dotenv (API key in `.env`) |

## Knowledge Base Design

Each entry in the JSON knowledge base contains:

| Field | Description |
|---|---|
| ID | Unique knowledge-base ID (e.g. KB-001) |
| Issue | Problem description |
| Symptoms | Symptoms related to the problem |
| Diagnostic Checks | Steps to investigate the issue |
| Known Resolution | Documented resolution |
| Escalation Team | Team responsible for escalation |

Example: **KB-001**, Payment API returning HTTP 500 error. Escalation team: L3 Application Engineering.

## Project Structure

> Adjust file names below to match your actual project.

```
ai-troubleshooting-assistant/
├── app.py                 # Streamlit web interface and main workflow
├── retrieve.py            # TF-IDF + cosine similarity retrieval logic
├── knowledge_base.json    # Knowledge base with 10 technical issues
├── requirements.txt       # Python dependencies
├── .env                   # Groq API key (not committed to Git)
└── README.md              # Project documentation
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-troubleshooting-assistant.git
cd ai-troubleshooting-assistant
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, install the packages directly:

```bash
pip install streamlit scikit-learn groq python-dotenv
```

### 4. Add your Groq API key

Get a free API key from the [Groq Console](https://console.groq.com), then create a `.env` file in the project root:

```
GROQ_API_KEY=your_api_key_here
```

Never commit your `.env` file. Add it to `.gitignore`.

## Running the App

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

## Example Queries to Try

- "Payment API is returning a 500 error" (matches a KB entry)
- "Users are unable to log in" (matches a KB entry)
- "How do I bake a cake?" (no match, shows the "not found" message)

## Future Improvements

- Replace TF-IDF with semantic embeddings for better understanding of meaning and synonyms
- Expand the knowledge base beyond 10 issues, with an admin page to add or edit entries
- Add a user feedback option (helpful / not helpful) to improve retrieval over time
- Add chat history and multi-turn conversation support
- Integrate with ticketing tools (ServiceNow, Jira) to auto-create tickets and route to the escalation team
- Connect to monitoring and logging systems so alerts can map directly to KB entries
- Deploy the app (Streamlit Community Cloud, Docker, or cloud hosting)


**Bhavana Tongare**

Email: bhavanatongare@gmail.com
GitHub: github.com/Bhavana-Tongare
LinkedIn: linkedin.com/in/Bhavana-Tongare
