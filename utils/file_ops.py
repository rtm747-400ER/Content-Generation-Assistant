import os

def export_chat_as_txt(messages, filename="chat_history.txt"):
    """
    Export chat history as a .txt file.
    messages: list of dicts with keys [role, content, timestamp]
    """
    with open(filename, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(f"[{msg['timestamp']}] {msg['role'].capitalize()}: {msg['content']}\n")
    return filename


def export_chat_as_md(messages, filename="chat_history.md"):
    """
    Export chat history as a .md file.
    messages: list of dicts with keys [role, content, timestamp]
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Chat History\n\n")
        for msg in messages:
            role = "**User**" if msg["role"] == "user" else "**Assistant**"
            f.write(f"- *{msg['timestamp']}* {role}: {msg['content']}\n")
    return filename
