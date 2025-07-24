import datetime
from typing import Optional, List, Dict

# In-memory storage for conversations (production would use database)
conversations_store: Dict[str, Dict] = {}

# Maximum messages to keep in conversation history (to manage token limits)
MAX_CONVERSATION_HISTORY = 20


def create_conversation(conversation_id: str, property_context: Optional[dict] = None) -> None:
    """Create a new conversation in storage"""
    conversations_store[conversation_id] = {
        "messages": [],
        "created_at": datetime.datetime.now(),
        "last_message_at": datetime.datetime.now(),
        "property_context": property_context
    }
    print(f"📝 Created new conversation: {conversation_id}")


def add_message_to_conversation(conversation_id: str, role: str, content: str) -> None:
    """Add a message to the conversation history"""
    if conversation_id not in conversations_store:
        create_conversation(conversation_id)

    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.datetime.now()
    }

    conversations_store[conversation_id]["messages"].append(message)
    conversations_store[conversation_id]["last_message_at"] = datetime.datetime.now()

    # Limit conversation history to prevent token overflow
    if len(conversations_store[conversation_id]["messages"]) > MAX_CONVERSATION_HISTORY:
        # Keep the system message (if any) and the most recent messages
        messages = conversations_store[conversation_id]["messages"]
        system_messages = [msg for msg in messages if msg["role"] == "system"]
        recent_messages = messages[-(MAX_CONVERSATION_HISTORY-len(system_messages)):]
        conversations_store[conversation_id]["messages"] = system_messages + recent_messages
        print(f"🗂️ Trimmed conversation {conversation_id} to {len(conversations_store[conversation_id]['messages'])} messages")


def get_conversation_messages(conversation_id: str) -> List[Dict]:
    """Get all messages from a conversation"""
    if conversation_id not in conversations_store:
        return []
    return conversations_store[conversation_id]["messages"]


def build_openai_messages(conversation_id: str, system_prompt: str) -> List[Dict]:
    """Build OpenAI messages array with conversation history"""
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history
    conversation_messages = get_conversation_messages(conversation_id)
    for msg in conversation_messages:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    return messages


