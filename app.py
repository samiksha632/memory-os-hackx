import sqlite3
import re
from datetime import datetime
import streamlit as st

DB_PATH = "memoryos.db"

st.set_page_config(page_title="MemoryOS | HackX", page_icon="🧠", layout="wide")

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'General',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

conn = connect()

def all_memories():
    return conn.execute("SELECT * FROM memories ORDER BY updated_at DESC").fetchall()

def save_memory(content, category="General", memory_id=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if memory_id:
        conn.execute("UPDATE memories SET content=?, category=?, updated_at=? WHERE id=?",
                     (content.strip(), category, now, memory_id))
    else:
        conn.execute("INSERT INTO memories(content, category, created_at, updated_at) VALUES(?,?,?,?)",
                     (content.strip(), category, now, now))
    conn.commit()

def delete_memory(memory_id):
    conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
    conn.commit()

def extract_candidates(text):
    """Lightweight, transparent baseline extraction; not an LLM."""
    patterns = [
        r"(?:i am|i'm|my name is|i study|i'm studying|i study at|i want to|my goal is|i like|i prefer|i am interested in|i'm interested in|i am learning|i'm learning|i have started learning)\s+[^.!?\n]+",
        r"(?:remember that|please remember)\s+[^.!?\n]+"
    ]
    found = []
    for pattern in patterns:
        found.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    cleaned = []
    for item in found:
        item = item.strip(" .")
        if item and item.lower() not in [x.lower() for x in cleaned]:
            cleaned.append(item)
    return cleaned

def search_memories(query, memories):
    words = {w.lower() for w in re.findall(r"[a-zA-Z0-9]+", query) if len(w) > 2}
    scored = []
    for m in memories:
        content_words = {w.lower() for w in re.findall(r"[a-zA-Z0-9]+", m["content"]) if len(w) > 2}
        score = len(words & content_words)
        if score:
            scored.append((score, m))
    return [m for _, m in sorted(scored, key=lambda x: (x[0], x[1]["updated_at"]), reverse=True)]

st.title("🧠 MemoryOS")
st.caption("Persistent, user-controlled memory for more context-aware AI conversations")
st.info("HackX prototype • This demo stores memories locally in SQLite. The current extraction and search are rule/keyword based; no external AI API is required.")

tab_chat, tab_memories, tab_about = st.tabs(["💬 Try MemoryOS", "🗂️ Memory Vault", "ℹ️ About"])

with tab_chat:
    st.subheader("Conversation")
    st.write("Share a detail you want MemoryOS to remember, or ask a question that may connect to an existing memory.")
    user_text = st.text_area("Your message", placeholder="Example: I'm learning Python and I want to build an AI project for a hackathon.", height=110, key="message")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🧠 Remember useful details", type="primary", use_container_width=True):
            if not user_text.strip():
                st.warning("Enter a message first.")
            else:
                candidates = extract_candidates(user_text)
                if candidates:
                    existing = [m["content"].lower() for m in all_memories()]
                    added = 0
                    for candidate in candidates:
                        if candidate.lower() not in existing:
                            save_memory(candidate, "Personal context")
                            added += 1
                    st.success(f"Processed {len(candidates)} candidate memory/memories. Added {added} new item(s).")
                    st.write("**Detected candidates:**")
                    for c in candidates:
                        st.write("• " + c)
                else:
                    st.warning("No clear memory phrase detected. Try starting with “I am…”, “I want to…”, “I prefer…”, or “Remember that…”. You can also add a memory manually in Memory Vault.")
    with col2:
        if st.button("🔎 Find relevant memories", use_container_width=True):
            if not user_text.strip():
                st.warning("Enter a question or topic first.")
            else:
                matches = search_memories(user_text, all_memories())
                if matches:
                    st.success(f"Found {len(matches)} relevant memory/memories.")
                    for m in matches[:5]:
                        st.markdown(f"**{m['category']}** · {m['updated_at']}")
                        st.write(m["content"])
                        st.divider()
                else:
                    st.info("No matching memories found yet. Add some memories first, then search using related words.")

    st.caption("Privacy note: this prototype keeps its database in the project folder on the machine where it runs. Avoid entering sensitive personal information.")

with tab_memories:
    st.subheader("Your Memory Vault")
    st.write("Review, add, edit, and delete stored memories. You stay in control.")
    with st.expander("➕ Add a memory manually"):
        new_content = st.text_input("Memory", key="new_memory")
        new_category = st.selectbox("Category", ["Personal context", "Goals", "Preferences", "Projects", "Learning", "General"], key="new_category")
        if st.button("Save memory"):
            if new_content.strip():
                save_memory(new_content, new_category)
                st.success("Memory saved.")
                st.rerun()
            else:
                st.warning("Please enter a memory.")
    memories = all_memories()
    if not memories:
        st.info("No memories yet. Add one above or use the conversation tab.")
    for m in memories:
        with st.container(border=True):
            st.markdown(f"**#{m['id']} · {m['category']}**")
            st.write(m["content"])
            st.caption(f"Created: {m['created_at']} · Updated: {m['updated_at']}")
            edit_col, delete_col = st.columns([4, 1])
            with edit_col:
                with st.expander("Edit"):
                    edit_content = st.text_input("Update memory", value=m["content"], key=f"edit_content_{m['id']}")
                    edit_category = st.selectbox("Category", ["Personal context", "Goals", "Preferences", "Projects", "Learning", "General"], index=["Personal context", "Goals", "Preferences", "Projects", "Learning", "General"].index(m["category"]) if m["category"] in ["Personal context", "Goals", "Preferences", "Projects", "Learning", "General"] else 5, key=f"edit_cat_{m['id']}")
                    if st.button("Save changes", key=f"save_{m['id']}"):
                        if edit_content.strip():
                            save_memory(edit_content, edit_category, m["id"])
                            st.success("Updated.")
                            st.rerun()
            with delete_col:
                if st.button("🗑️ Delete", key=f"delete_{m['id']}"):
                    delete_memory(m["id"])
                    st.rerun()

with tab_about:
    st.subheader("What this prototype demonstrates")
    st.markdown("""
- **Persistent memory:** information remains in SQLite between app sessions.
- **Memory extraction:** a transparent baseline detects a few common personal-context phrases.
- **Memory retrieval:** keyword overlap finds memories related to a query.
- **Memory management:** users can inspect, edit, and delete stored information.
- **User control:** the memory vault makes stored context visible.

### Current limitations
This is an early prototype. It does not yet use an LLM, embeddings, semantic search, automatic contradiction resolution, or multi-user authentication. Keyword search can miss related meanings. These are possible future improvements, not completed features.
""")
    st.subheader("Suggested demo")
    st.markdown("""
1. In **Try MemoryOS**, enter: `I'm learning Python and I want to build an AI project for a hackathon.`
2. Click **Remember useful details**.
3. Search for `Python hackathon`.
4. Open **Memory Vault** to edit or delete a saved memory.
5. Refresh the app to demonstrate that memories persist.
""")
