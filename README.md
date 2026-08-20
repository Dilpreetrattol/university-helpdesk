# TIET Fresher Help Desk

A Retrieval-Augmented Generation (RAG) chatbot that answers first-year student questions
about Thapar Institute of Engineering and Technology (TIET), Patiala — hostels, fees,
scholarships, admissions, and campus life — strictly from official institute documents.

## How it works

- `pdfs/` holds the official TIET prospectus/policy PDFs.
- `ingest.py` loads those PDFs, splits them into chunks, embeds them with a local
  HuggingFace sentence-transformer model, and builds a vector index in `storage/`.
- `inject_tables.py` additionally injects clean, hand-verified text for tables and facts
  that don't survive raw PDF text extraction well (fee tables, seat matrices, hostel
  name/fee mappings, refund policy, hostel rules and timings, etc.).
- `app.py` is a Streamlit chat UI that queries the index and answers using Google Gemini,
  citing the source document for every answer.
- `query.py` is a command-line alternative for quick testing (uses Groq instead of Gemini).

## Setup

1. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys:
   ```
   GEMINI_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   ```
3. Build the index (run once, and again whenever `pdfs/` or `inject_tables.py` changes):
   ```
   python ingest.py
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```

## Notes

- The assistant only answers from the documents in `pdfs/` plus the curated data in
  `inject_tables.py` — it will not use outside/general knowledge.
- `storage/` (the built index) is not committed; regenerate it locally with `ingest.py`.
