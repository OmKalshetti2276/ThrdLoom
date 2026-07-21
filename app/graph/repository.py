from app.graph.connection import (db, GraphDB)
from app.models.requests import AddIssueRequest


def create_category(
    name: str,
    embedding: list[float]
):
    query = """
    MERGE (c:Category {name: $name})
    ON CREATE SET
        c.id = randomUUID(),
        c.embedding = $embedding

    RETURN c
    """
    return GraphDB().execute_query(
    query,
    {
        "name": name,
        "embedding": embedding
    }
    )
    
    

def get_category_names():
    query = """
    MATCH (c:Category)
    RETURN c.name AS name
    ORDER BY c.name
    """

    return GraphDB().execute_query(query)



def get_category(name: str):
    query = """
    MATCH (c:Category {name: $name})
    RETURN c
    """

    with db.session() as session:
        result = session.run(query, name=name)
        record = result.single()

        return record["c"] if record else None
    



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




def find_top_k_similar_problems(
    category_name: str,
    embedding: list[float],
    k: int = 5
):
        query ="""
        MATCH (c:Category {name: $category})-[:HAS_PROBLEM]->(p:Problem)
        CALL db.index.vector.queryNodes(
        'problem_embedding_index',
        $k,
        $embedding
        )
        YIELD node, score
        WHERE node = p
        RETURN
        node.id AS id,
        node.title AS title,
        node.description AS description,
        score
        ORDER BY score DESC
        """

        return GraphDB().execute_query(
    query,
    {
        "category": category_name,
        "embedding": embedding,
        "k": k
    }
)



def create_problem(
    category_name: str,
    request: AddIssueRequest,
    embedding: list[float]
):
    query = """
    MATCH (c:Category {name: $category_name})

    CREATE (p:Problem {
        id: randomUUID(),
        title: $title,
        description: $description,
        embedding: $embedding,
        root_cause: $root_cause,
        solution: $solution,
        applicable_versions: $applicable_versions,
        confidence: $confidence
    })

    MERGE (c)-[:HAS_PROBLEM]->(p)

    FOREACH (symptom IN $symptoms |
        MERGE (s:Symptom {name: symptom})
        MERGE (p)-[:HAS_SYMPTOM]->(s)
    )

    RETURN p
    """

    return GraphDB().execute_query(
    query,
    {
        "category_name": category_name,
        "title": request.title,
        "description": request.description,
        "embedding": embedding,
        "root_cause": request.root_cause,
        "solution": request.solution,
        "applicable_versions": request.applicable_versions,
        "confidence": request.confidence,
        "symptoms": request.symptoms,
    }
)