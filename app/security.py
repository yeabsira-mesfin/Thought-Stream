import hashlib
import re
from dataclasses import dataclass


SENSITIVE_PATTERNS = [
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_KEY]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "[REDACTED_API_KEY]"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
]

ALLOWED_TOOLS = {"knowledge_search", "calculator"}


@dataclass(frozen=True)
class ValidationResult:
    allowed: bool
    reason: str
    sanitized_text: str


def redact_sensitive(text: str) -> str:
    output = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        output = pattern.sub(replacement, output)
    return output


def validate_prompt(text: str) -> ValidationResult:
    if not isinstance(text, str):
        return ValidationResult(False, "prompt must be text", "")
    stripped = text.strip()
    if not stripped:
        return ValidationResult(False, "prompt is required", "")
    if len(stripped) > 4000:
        return ValidationResult(False, "prompt exceeds 4000 characters", "")
    return ValidationResult(True, "allowed", redact_sensitive(stripped))


def tool_allowed(tool_name: str | None) -> bool:
    return tool_name is None or tool_name in ALLOWED_TOOLS


def sanitize_output(text: str) -> str:
    return redact_sensitive(text)


def event_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
