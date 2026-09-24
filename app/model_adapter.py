def generate_response(prompt: str, requested_tool: str | None = None) -> str:
    """Deterministic local adapter so tests require no external model or credential."""
    tool_note = f" Tool authorized: {requested_tool}." if requested_tool else ""
    return (
        "Security lab response: the request passed application policy checks."
        f"{tool_note} Processed content length: {len(prompt)} characters."
    )
