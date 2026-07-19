from app.graph.connection import (db, GraphDB)
from app.services.embedding_service import generate_embedding


def create_category(name: str):
    category_embedding=generate_embedding(name)

    query = """
    MERGE (c:Category {name: $name})
    ON CREATE SET
        c.id = randomUUID(),
        c.embedding = $category_embedding
    ON MATCH SET
        c.embedding = $category_embedding

    RETURN c
    """

    with db.session() as session:
        result = session.run(
            query,
            name=name,
            category_embedding =category_embedding
        )

        return result.single()["c"]
    
def get_category(name: str):
    query = """
    MATCH (c:Category {name: $name})
    RETURN c
    """

    with db.session() as session:
        result = session.run(query, name=name)
        record = result.single()

        return record["c"] if record else None
    


def create_problem(category_name, problem):

    text = f"""
    Title: {problem['title']}

    Description: {problem['description']}

    Symptoms:
        {' '.join(problem['symptoms'])}

    Root Cause:
    {problem['root_cause']}
    """

    problem_embedding=generate_embedding(text)

    query = """
    MATCH (c:Category {name: $category_name})

    MERGE (p:Problem {title: $title})
    ON CREATE SET
        p.id = randomUUID(),
        p.description = $description,
        p.symptoms = $symptoms,
        p.root_cause = $root_cause,
        p.solution = $solution,
        p.embedding = $embedding,
        p.status = $status

    MERGE (c)-[:HAS_PROBLEM]->(p)

    RETURN p
    """

    return GraphDB().execute_query(
        query,
        {
            "category_name": category_name,
            "title": problem["title"],
            "description": problem["description"],
            "symptoms": problem["symptoms"],
            "root_cause": problem["root_cause"],
            "solution": problem["solution"],
            "embedding": problem_embedding,
            "status": problem["status"],
        },
    )


def get_all_categories():
    query = """
    MATCH (c:Category)
    RETURN c.name AS name, c.embedding AS embedding
    """

    return GraphDB().execute_query(query)




def get_problems_by_category(category_name):
    query = """
    MATCH (c:Category {name:$name})-[:HAS_PROBLEM]->(p:Problem)

    RETURN
        p.id AS id,
        p.title AS title,
        p.description AS description,
        p.symptoms AS symptoms,
        p.root_cause AS root_cause,
        p.solution AS solution,
        p.embedding AS embedding,
        p.status AS status
    """

    return GraphDB().execute_query(
        query,
        {
            "name": category_name
        }
    )
