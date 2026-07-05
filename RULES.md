# GraphRAG — MCP Recording Rule

## 1. Tool Definition

**Tool name:** `record_resolution`  
**Description:** Record a newly resolved issue into the GraphRAG knowledge base (Neo4j). Called by the MCP server whenever a human resolves a problem.

---

## 2. Trigger Conditions

Call this tool **immediately after** an issue is resolved by a human operator. Do NOT call it for:
- Issues that were already resolved (duplicate detection handles this server-side)
- Issues matched to an existing entry with similarity > 0.92 (server will return `skipped`)
- Intermittent or unconfirmed root causes — wait for confirmation

---

## 3. Input Schema

```json
{
  "issue": {
    "title": "string (required) — Short description of the problem",
    "description": "string (required) — Detailed explanation",
    "severity": "string (optional, default: 'medium') — One of: low, medium, high, critical"
  },
  "symptoms": [
    {
      "name": "string (required) — Short symptom label",
      "description": "string (optional) — Detailed symptom observation"
    }
  ],
  "root_cause": {
    "description": "string (required) — What caused the issue",
    "category": "string (optional, default: 'general') — One of: application, infrastructure, network, security, database"
  },
  "resolution": {
    "summary": "string (required) — One-line summary of the fix",
    "steps": ["string (required) — Ordered list of action steps taken"]
  }
}
```

### Example Payload

```json
{
  "issue": {
    "title": "API rate limiting blocking legitimate users",
    "description": "Users reporting 429 Too Many Requests errors during normal usage.",
    "severity": "medium"
  },
  "symptoms": [
    {
      "name": "429 errors in production",
      "description": "API gateway returns HTTP 429 for authenticated user requests"
    },
    {
      "name": "User complaints of throttling",
      "description": "Support tickets reporting 'too many requests'"
    }
  ],
  "root_cause": {
    "description": "Rate limiter keyed on client IP instead of user ID, causing shared NAT users to exceed limits",
    "category": "application"
  },
  "resolution": {
    "summary": "Changed rate limiter to use user ID instead of IP address",
    "steps": [
      "Update rate limiter middleware to key on X-User-ID header",
      "Set per-user limit to 1000 requests/minute with burst of 2000",
      "Keep IP-based rate limiting for unauthenticated requests at 100 req/min",
      "Monitor 429 rate for 48 hours post-deploy"
    ]
  }
}
```

---

## 4. Tool Workflow

When this tool is called, the MCP server will:

```
1. VALIDATE — Check payload against JSON schema above
2. EMBED   — Generate 1024-dim vectors for all text fields using BAAI/bge-large-en-v1.5
3. DEDUP   — Query Neo4j for existing issues with cosine similarity > 0.92
   → If found: return {status: "skipped", existing_id: "..."}, do nothing else
   → If not found: proceed
4. CREATE  — Insert nodes (Issue, Symptom, RootCause, Resolution) into Neo4j
5. LINK    — Create relationships: HAS_SYMPTOM, INDICATES, RESOLVED_BY
6. RETURN  — {status: "created", issue_id: "..."}
```

---

## 5. Error Handling

| Scenario | Behaviour |
|---|---|
| DB connection failure | Return `{"status": "error", "message": "Database unavailable"}` |
| Validation failure | Return `{"status": "error", "message": "...", "missing_fields": [...]}` |
| Embedding model failure | Return `{"status": "error", "message": "Embedding service unavailable"}` |
| Partial insertion (node created but link failed) | Accept partial; return `{"status": "partial", "ids": {...}}` |

---

## 6. Retry Logic

- **Transient errors** (network, DB timeout, 5xx): Retry up to **3 times** with exponential backoff (1s, 2s, 4s).
- **Validation errors**: Do NOT retry — return error to caller immediately.
- **Idempotency**: The `issue_id` is derived from (title + description) hash via MERGE. Re-sending the same payload always produces the same result.

---

## 7. Idempotency & Deduplication

- Dedup is **server-side**: Neo4j `MERGE` ensures nodes are not duplicated on `title`/`name`/`description`.
- Vector similarity check (`cosine > 0.92`) catches semantically equivalent issues even if wording differs.
- If an issue exists with matching symptoms and resolution, the tool returns `skipped` without modification.

---

## 8. Consuming the Tool (MCP Server)

In your MCP server configuration, register the tool as:

```json
{
  "name": "record_resolution",
  "description": "Record a newly resolved issue into the GraphRAG knowledge base",
  "inputSchema": {
    "type": "object",
    "properties": {
      "issue": { "type": "object", "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
      }, "required": ["title", "description"]},
      "symptoms": {"type": "array", "items": {"type": "object", "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"}
      }, "required": ["name"]}},
      "root_cause": {"type": "object", "properties": {
        "description": {"type": "string"},
        "category": {"type": "string"}
      }},
      "resolution": {"type": "object", "properties": {
        "summary": {"type": "string"},
        "steps": {"type": "array", "items": {"type": "string"}}
      }}
    },
    "required": ["issue"]
  }
}
```

To invoke from MCP:

```
mcp_call("record_resolution", {
  "issue": {"title": "...", "description": "..."},
  "symptoms": [...],
  "root_cause": {...},
  "resolution": {...}
})
```
