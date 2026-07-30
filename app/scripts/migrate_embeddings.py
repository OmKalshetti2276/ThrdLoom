import time

from voyageai.error import RateLimitError

from app.graph.connection import db
from app.services.embedding_service import generate_embedding


CATEGORY_FETCH = """
MATCH (c:Category)
RETURN elementId(c) AS id,
       c.name AS name
"""

CATEGORY_UPDATE = """
MATCH (c:Category)
WHERE elementId(c) = $id
SET c.embedding = $embedding
"""


PROBLEM_FETCH = """
MATCH (p:Problem)
RETURN
    elementId(p) AS id,
    p.title AS title,
    p.description AS description,
    p.symptoms AS symptoms,
    p.root_cause AS root_cause,
    p.solution AS solution
"""

PROBLEM_UPDATE = """
MATCH (p:Problem)
WHERE elementId(p) = $id
SET p.embedding = $embedding
"""


def get_embedding(text: str):

    while True:
        try:
            return generate_embedding(text)

        except RateLimitError:
            print("\n⚠ Rate limit reached.")
            print("Waiting 20 seconds...\n")
            time.sleep(20)


def migrate_categories():

    print("\n========== Migrating Categories ==========\n")

    with db.session() as session:

        categories = session.run(CATEGORY_FETCH)

        count = 0

        for record in categories:

            embedding = get_embedding(record["name"])

            session.run(
                CATEGORY_UPDATE,
                id=record["id"],
                embedding=embedding
            )

            count += 1
            print(f"[{count}] Updated Category -> {record['name']}")

    print(f"\nFinished Categories ({count})\n")


def migrate_problems():

    print("\n========== Migrating Problems ==========\n")

    with db.session() as session:

        problems = session.run(PROBLEM_FETCH)

        count = 0

        for record in problems:

            embedding_text = f"""
Title: {record["title"]}

Description: {record["description"]}

Symptoms:
{" ".join(record["symptoms"] or [])}

Root Cause:
{record["root_cause"]}

Solution:
{record["solution"]}
"""

            embedding = get_embedding(embedding_text)

            session.run(
                PROBLEM_UPDATE,
                id=record["id"],
                embedding=embedding
            )

            count += 1
            print(f"[{count}] Updated Problem -> {record['title']}")

    print(f"\nFinished Problems ({count})\n")


if __name__ == "__main__":

    start = time.time()

    migrate_categories()
    migrate_problems()

    print(f"\nMigration completed in {time.time() - start:.2f} seconds.")