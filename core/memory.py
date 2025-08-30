import streamlit as st
from datetime import datetime
from typing import Any

def init_session(ss: Any):
    """Initializes the session state for messages if not already present."""
    if "messages" not in ss:
        ss.messages = []

def add_message(ss: Any, role: str, content: str, msg_type: str = "text"):
    """
    Adds a message to the session state with a role, content, timestamp, and type.
    msg_type can be 'text' or 'image'.
    """
    ts = datetime.now().strftime("%H:%M:%S")
    ss.messages.append({"role": role, "content": content, "timestamp": ts, "type": msg_type})

def get_messages(ss: Any):
    """Returns the list of messages from the session state."""
    return ss.get("messages", [])

def get_api_ready_messages(ss: Any):
    """

    Returns a clean list of messages (only role and content) for API calls.
    Filters out image generation messages to keep the text model's context clean.
    """
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in ss.messages
        if msg.get("type", "text") == "text" # Only include text messages for the LLM context
    ]

def clear_messages(ss: Any):
    """Clears all messages from the session state."""
    ss.messages = []