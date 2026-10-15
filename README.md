# MemoryOS — Persistent Memory for AI Assistants

**Team:** HackX  
**Track:** AI / Cybersecurity (select the track that matches the event rules)

## Problem
AI assistants can struggle to retain useful context between separate conversations. Users may have to repeat their goals, preferences, and ongoing project details, which can make assistance feel fragmented and less personalized.

## Proposed solution
MemoryOS is a prototype for a user-controlled memory layer. It lets users save important context, retrieve relevant memories, and review, edit, or delete what is stored. The current prototype uses SQLite persistence, lightweight rule-based memory extraction, and keyword-based retrieval. It is intentionally designed so these baseline components can later be upgraded with embeddings and an LLM.

## Current features
- Local persistent storage with SQLite
- Rule-based detection of common memory phrases
- Keyword-based memory retrieval
- Memory vault to add, review, edit, and delete memories
- Streamlit web interface
- No paid API key required for the current prototype

## Run locally
1. Install Python 3.10 or newer.
2. Clone or download this repository.
3. In a terminal, enter the project folder.
4. Create and activate a virtual environment (optional but recommended).
5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the app:

   ```bash
   streamlit run app.py
   ```

7. Open the local URL shown in the terminal.

## Demo flow
1. Enter: `I'm learning Python and I want to build an AI project for a hackathon.`
2. Click **Remember useful details**.
3. Search for `Python hackathon`.
4. Open **Memory Vault** and edit or delete a memory.
5. Refresh the app and confirm the memory remains saved.

## Architecture
- `app.py`: Streamlit UI, rule-based extraction, SQLite storage, and keyword retrieval.
- `requirements.txt`: Python dependency list.
- `memoryos.db`: created locally when the app runs; not included in Git.

## Limitations and future work
This is an early prototype, not a complete autonomous memory system. The current version does not use an LLM, vector embeddings, semantic search, contradiction resolution, encryption, or multi-user authentication. Future work could add semantic retrieval, LLM-powered extraction and responses, memory confidence/expiry, and stronger privacy controls.

## Privacy
The prototype stores data in a local SQLite database. Do not enter sensitive personal information. If deployed publicly, storage isolation, authentication, and privacy protections must be added before real users use it.

## Team contribution
Add each teammate's actual contribution before final submission.

## License
This project is released under the MIT License. See `LICENSE`.
