# ThrdLoom

**Your team has already solved this bug. ThrdLoom helps you find that out before you waste another afternoon rediscovering it.**

---

## The Problem

Every engineering team has the same quiet tax on its time: someone spends two hours debugging an issue, fixes it, and the fix disappears into a Slack thread, a closed ticket, or a comment nobody will search for again. Six months later, a different engineer — or an AI coding agent — hits the same wall and starts from zero.

The reason this keeps happening isn't a lack of documentation. It's that documentation and issue trackers are built around exact keyword matches. If the fix was logged as "Redis connection pool exhaustion" and the next person searches "app hangs under load," they'll never find it — even though it's the same bug.

## What ThrdLoom Does

ThrdLoom is an organizational memory layer that understands *meaning*, not just keywords. Describe an issue in plain language, and it retrieves the closest matching problems your team has already solved — ranked by semantic similarity, not string overlap.

**The core idea in one line:** turn tribal knowledge into something queryable, by anyone, in their own words — including AI agents debugging on your team's behalf.

### Why this actually matters
- **For engineering teams:** cuts down repeated debugging cycles and shortens onboarding, since new hires can query past incidents instead of interrupting a senior engineer.
- **For AI coding agents:** gives them a memory of your codebase's actual failure history — something no LLM has out of the box — via MCP integration.
- **For the org:** knowledge stops being locked in one person's head or a stale wiki page; it becomes a living, searchable graph that gets more valuable with every issue logged.

---

## How It Works

**Search:** You describe an issue → Voyage AI embeds it into a vector → Neo4j's vector index finds the nearest past issues → you get back the most relevant historical fixes, ranked by relevance.

**Add:** Before a new issue gets stored, ThrdLoom checks whether something nearly identical already exists (via embedding similarity) and rejects duplicates — so the graph stays clean instead of accumulating five slightly-different copies of the same bug report.

```
                  User / AI Agent
                         │
                         ▼
                  FastAPI Backend
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
         Voyage AI           Neo4j Graph DB
      Sentence Embeddings     + Vector Index
                 │
                 ▼
        Semantic Search Engine
```

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | FastAPI | Fast, async, clean OpenAPI docs out of the box |
| Database | Neo4j | Graph structure fits how issues, categories, and solutions actually relate |
| Embeddings | Voyage AI (`voyage-4-lite`) | High-quality, low-latency semantic embeddings |
| Similarity | Cosine similarity over Neo4j's vector index | Fast nearest-neighbor retrieval at scale |
| Validation | Pydantic | Strict, predictable request/response contracts |
| Agent Integration | Model Context Protocol (in progress) | Lets AI coding agents query this memory directly, not just humans |

---

## API at a Glance

**`POST /search-issue`** — describe a problem, get back the Top-K most similar past issues and their resolutions.

**`POST /add-issue`** — log a new issue; automatically validated, embedded, checked for duplicates, and stored.

---

## Example in Action

**1. Search for an issue in plain language:**

Someone hits a FastAPI reload bug and describes it their own way — not the exact wording used when it was first logged. ThrdLoom still finds it, ranked by relevance:

![Search issue request](docs/screenshots/search_issue_request.png)
![Search issue response](docs/screenshots/search_issue_response.png)

**2. Add a genuinely new issue:**

![Add new issue request](docs/screenshots/sample_issue_request.png)
![Add new issue response](docs/screenshots/sample_issue_response.png)

**3. Try to add it again (near-duplicate):**

Same issue, described slightly differently. Instead of creating a duplicate entry, ThrdLoom recognizes it's already been logged and rejects it:

![Duplicate issue request](docs/screenshots/duplicate_issue_request.png)
![Duplicate issue response](docs/screenshots/duplicate_issue_response.png)

---

## Project Structure

```text
app/
├── graph/          # Neo4j queries and graph logic
├── models/         # Pydantic schemas
├── routers/        # API route definitions
├── services/       # Embedding, similarity, business logic
├── scripts/
│   ├── seed_data.py
│   └── migrate_embeddings.py
└── main.py
```

---

## Where This Is Headed

Working today: the FastAPI backend, Neo4j-backed semantic search, duplicate detection, and Voyage AI embeddings — the full search/add loop is functional end-to-end.

Next up:
- **MCP Server** — so AI coding agents can query ThrdLoom directly during debugging, not just humans through the API
- **Agent Integration** — closing the loop so agents can both search *and* log new resolved issues automatically
- **Authentication** — team-level access control
- **Frontend Dashboard** — a browsable view into the organization's accumulated knowledge, for people who'd rather click than curl

---

*ThrdLoom exists because the best engineering knowledge shouldn't require remembering who solved it, or how they phrased the ticket.*