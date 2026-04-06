def extract_text_from_response(resp) -> str:
    # Best-case: some SDKs expose .text
    text = getattr(resp, "text", None)
    if isinstance(text, str) and text:
        return text

    msg = getattr(resp, "message", None)
    if isinstance(msg, dict):
        content = msg.get("content", [])
        parts = []
        for item in content:
            # Common shape: {"type": "text", "text": "..."}
            if isinstance(item, dict) and item.get("type") == "text" and "text" in item:
                parts.append(item["text"])
            # Fallback: if "text" exists directly
            elif isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
        if parts:
            return "\n".join(parts)

    # Last resort: stringify the whole response for debugging
    return str(resp)