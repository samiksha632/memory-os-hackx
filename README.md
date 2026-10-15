# MemoryOS — Persistent Memory for AI Assistants

**Team Name:** HackX
**Project Domain:** Artificial Intelligence
**Project Type:** AI Memory and Personalization System

## Problem Statement

AI assistants often struggle to retain useful context across separate conversations. Users may need to repeatedly explain their preferences, goals, past decisions, and ongoing projects. This can lead to fragmented interactions and less personalized assistance.

## Our Solution

MemoryOS is a prototype of an intelligent memory system designed to help AI assistants retain, organize, retrieve, and update relevant information from previous interactions.

Our goal is to provide more continuous, context-aware, and personalized AI experiences while giving users control over their stored memories.

## Current Features

* Persistent memory storage using SQLite.
* Rule-based detection of certain useful details from user messages.
* Keyword-based retrieval of relevant memories.
* Interface for adding, viewing, editing, and deleting memories.
* Local storage that preserves memories between application sessions.

## Technology Stack

* **Python:** Application logic.
* **Streamlit:** Interactive web interface.
* **SQLite:** Persistent memory storage.
* **GitHub:** Source code management and collaboration.

## How to Run

1. Install Python 3.10 or newer.

2. Clone or download this repository.

3. Open a terminal in the project directory.

4. Install dependencies:

   `pip install -r requirements.txt`

5. Run the application:

   `streamlit run app.py`

6. Open the local URL displayed in the terminal.

## Demo Workflow

1. Enter a message containing information you want the system to remember.
2. Click **Remember useful details**.
3. Search for related information using the memory retrieval feature.
4. Open the Memory Vault to review, edit, or delete saved memories.
5. Restart or refresh the application to verify that stored memories persist.

## Future Improvements

* LLM-powered memory extraction and response generation.
* Semantic search using embeddings.
* Better handling of updated or contradictory memories.
* Memory relevance scoring and expiration.
* Enhanced privacy and user controls.

## Current Limitations

This prototype currently uses rule-based extraction and keyword-based retrieval. It does not yet implement LLM-powered responses, semantic search, automatic contradiction resolution, or multi-user authentication.

## Privacy

The current prototype stores memories in a local SQLite database. Users should avoid entering sensitive personal information.

## License

This project is licensed under the MIT License.
