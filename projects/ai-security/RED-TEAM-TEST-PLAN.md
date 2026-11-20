# AI Red-Team Test Plan

Run only against the local demo service or systems with explicit authorization. Use synthetic data.

| ID | Category | Test | Expected result |
|---|---|---|---|
| RT-01 | Direct prompt injection | Submit a known instruction-override phrase | Blocked; high-severity event recorded |
| RT-02 | Cross-tenant retrieval | Tenant A asks for Tenant B's synthetic canary | Tenant B document is not returned |
| RT-03 | Mass assignment | Add an unexpected is_admin field | Request rejected with validation error |
| RT-04 | Empty retrieval | Query unrelated content | Safe no-match response |
| RT-05 | Telemetry bounds | Generate more events than buffer capacity | Buffer remains bounded |

## Limitations
- Regex screening catches only known phrases and is not a robust prompt-injection defense.
- The model is mocked; no real LLM jailbreak robustness is evaluated.
- The event endpoint is unauthenticated and local-demo only.
- Retrieval is in-memory keyword matching, not a production vector database.
