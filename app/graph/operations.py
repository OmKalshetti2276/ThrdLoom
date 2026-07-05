from __future__ import annotations

import uuid
from typing import Any

from src.graph.connection import db


def _node_id() -> str:
    return str(uuid.uuid4())


def create_issue(title: str, description: str, embedding: list[float], severity: str = "medium") -> dict[str, Any]:
    nid = _node_id()
    with db.session() as session:
        session.run(
            """MERGE (n:Issue {title: $title, description: $description})
               ON CREATE SET n.id = $id, n.severity = $severity, n.embedding = $embedding
               ON MATCH SET n.embedding = $embedding""",
            id=nid, title=title, description=description, severity=severity, embedding=embedding,
        )
        result = session.run(
            "MATCH (n:Issue {title: $title, description: $description}) RETURN n.id AS id",
            title=title, description=description,
        )
        row = result.single()
        return {"id": row["id"], "type": "Issue"}


def create_symptom(name: str, description: str, embedding: list[float]) -> dict[str, Any]:
    nid = _node_id()
    with db.session() as session:
        session.run(
            """MERGE (n:Symptom {name: $name})
               ON CREATE SET n.id = $id, n.description = $description, n.embedding = $embedding
               ON MATCH SET n.embedding = $embedding, n.description = $description""",
            id=nid, name=name, description=description, embedding=embedding,
        )
        result = session.run("MATCH (n:Symptom {name: $name}) RETURN n.id AS id", name=name)
        row = result.single()
        return {"id": row["id"], "type": "Symptom"}


def create_root_cause(description: str, category: str, embedding: list[float]) -> dict[str, Any]:
    nid = _node_id()
    with db.session() as session:
        session.run(
            """MERGE (n:RootCause {description: $description})
               ON CREATE SET n.id = $id, n.category = $category, n.embedding = $embedding
               ON MATCH SET n.embedding = $embedding, n.category = $category""",
            id=nid, description=description, category=category, embedding=embedding,
        )
        result = session.run(
            "MATCH (n:RootCause {description: $description}) RETURN n.id AS id",
            description=description,
        )
        row = result.single()
        return {"id": row["id"], "type": "RootCause"}


def create_resolution(summary: str, steps: list[str], embedding: list[float]) -> dict[str, Any]:
    nid = _node_id()
    with db.session() as session:
        session.run(
            """MERGE (n:Resolution {summary: $summary})
               ON CREATE SET n.id = $id, n.steps = $steps, n.embedding = $embedding
               ON MATCH SET n.embedding = $embedding, n.steps = $steps""",
            id=nid, summary=summary, steps=steps, embedding=embedding,
        )
        result = session.run(
            "MATCH (n:Resolution {summary: $summary}) RETURN n.id AS id",
            summary=summary,
        )
        row = result.single()
        return {"id": row["id"], "type": "Resolution"}


def link_issue_to_symptom(issue_id: str, symptom_id: str):
    with db.session() as session:
        session.run(
            "MATCH (i:Issue {id: $iid}), (s:Symptom {id: $sid}) MERGE (i)-[:HAS_SYMPTOM]->(s)",
            iid=issue_id, sid=symptom_id,
        )


def link_symptom_to_cause(symptom_id: str, cause_id: str):
    with db.session() as session:
        session.run(
            "MATCH (s:Symptom {id: $sid}), (c:RootCause {id: $cid}) MERGE (s)-[:INDICATES]->(c)",
            sid=symptom_id, cid=cause_id,
        )


def link_cause_to_resolution(cause_id: str, resolution_id: str):
    with db.session() as session:
        session.run(
            "MATCH (c:RootCause {id: $cid}), (r:Resolution {id: $rid}) MERGE (c)-[:RESOLVED_BY]->(r)",
            cid=cause_id, rid=resolution_id,
        )


def link_symptom_to_symptom(from_id: str, to_id: str):
    with db.session() as session:
        session.run(
            "MATCH (a:Symptom {id: $a}), (b:Symptom {id: $b}) MERGE (a)-[:LEADS_TO]->(b)",
            a=from_id, b=to_id,
        )
