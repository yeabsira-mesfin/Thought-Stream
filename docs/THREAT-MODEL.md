# AI Application Threat Model

## Protected assets

- User-provided sensitive information
- Authorized tool capabilities
- Application policy configuration
- Model outputs returned to users
- Security audit metadata

## Trust boundaries

1. User input entering the application
2. Sanitized input entering the model adapter
3. Model output returning to application code
4. Tool requests crossing from an AI workflow to an external capability
5. Security events entering the logging system

## Primary risks and controls

| Risk | Defensive control |
| --- | --- |
| Sensitive data enters the AI workflow | Redact recognized secrets and personal identifiers before processing |
| AI feature receives excessive capability | Allowlist tools and deny unknown capabilities |
| Oversized or malformed input affects availability | Enforce schema and length limits |
| Sensitive content appears in output | Apply output filtering before response |
| Logs become a secondary data leak | Log event identifiers and decisions instead of raw prompts |
| Security behavior regresses | Run automated policy and API tests on every change |

## Design principle

Authorization belongs in deterministic application code, not in a model response. The application decides which capabilities are available before any model adapter is called.

## Production hardening

A production deployment would add strong user identity, tenant-aware data authorization, external secret management, rate limits, structured security telemetry, content provenance, retention controls, and human approval for high-impact actions.
