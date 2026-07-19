# 📄 AI Invoice Data Extractor

> **The Problem:** Small businesses spend 15-20 hours/week manually entering data from unstructured, messy PDFs.
> 
> **The Solution:** This app automatically parses PDFs, forces a Large Language Model (via OpenRouter) to extract the data into a strict JSON schema, and mathematically validates the totals before exporting to CSV.

## 🚀 Features

- **Structured AI Output:** Uses `pydantic` and the `openai` SDK to force the LLM to return clean, predictable JSON data (no conversational hallucinations).
- **The "Hallucination Moat":** A dedicated validator checks the AI's math (`Subtotal + Tax == Total`). If the math fails, the invoice is flagged for human review.
- **Separation of Concerns:** Modular backend architecture (`parser.py`, `ai_extract.py`, `validator.py`) separating the dumb text extraction from the smart business logic.
- **Safety Guardrails:** Hard limits on PDF page counts to prevent API token limit crashes and cost overruns.
- **Streamlit Dashboard:** A clean, drag-and-drop web UI for end-users to process batches of invoices and download CSV reports.

## 🛠️ Architecture

```text
extractor/
├── parser.py           # Uses pdfplumber to rip raw text
├── ai_extract.py       # Pydantic schema + OpenRouter(OpenAI SDK) API call
├── validator.py        # Business logic & math validation
└── exporter.py         # Converts extracted JSON to Pandas DataFrame -> CSV
```

## 💻 How to Run Locally

1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Add your OpenRouter API key to a `.env` file (`OPENROUTER_API_KEY=your_key`)
6. Run the app: `streamlit run app.py`

## 🔮 Roadmap (V2 Enterprise Upgrades)
- **Async Processing:** Implement `asyncio` to batch process 50+ invoices concurrently.
- **Network Retries:** Implement `tenacity` for exponential backoff if the AI API times out.
- **Structured Logging:** Add server-side logging for production monitoring.
