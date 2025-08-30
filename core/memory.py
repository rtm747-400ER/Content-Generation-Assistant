from datetime import datetime

def init_session(session_state):
    """Initialize chat memory if not already present."""
    if "messages" not in session_state:
        session_state.messages = []


def add_message(session_state, role, content):
    """Add a message (user or assistant) to memory."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": timestamp
    })


def get_messages(session_state):
    """Return all stored messages."""
    return session_state.messages


def clear_messages(session_state):
    """Clear chat history."""
    session_state.messages = []

def get_api_ready_messages(session_state):
    """
    Return chat history stripped of timestamps for API calls.
    Keeps memory intact but prepares messages for model input.
    """
    return [{"role": m["role"], "content": m["content"]} for m in get_messages(session_state)]
