from app.security import redact_sensitive, sanitize_output, tool_allowed, validate_prompt


def test_sensitive_data_redaction():
    text = "Contact dev@example.com for this test."
    redacted = redact_sensitive(text)
    assert "dev@example.com" not in redacted
    assert "[REDACTED_EMAIL]" in redacted


def test_tool_allowlist_is_default_deny():
    assert tool_allowed("knowledge_search")
    assert tool_allowed("calculator")
    assert not tool_allowed("admin_console")
    assert not tool_allowed("unknown_tool")


def test_prompt_size_policy():
    result = validate_prompt("A" * 4001)
    assert result.allowed is False


def test_prompt_policy_sanitizes_allowed_input():
    result = validate_prompt("Please summarize this for user@example.com")
    assert result.allowed is True
    assert "user@example.com" not in result.sanitized_text


def test_output_policy_redacts_sensitive_data():
    output = sanitize_output("Send the report to analyst@example.com")
    assert "analyst@example.com" not in output
