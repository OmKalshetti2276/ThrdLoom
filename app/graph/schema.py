from src.graph.connection import db
from src.config import config


def setup_indexes():
    dim = config.embedding_dim

    queries = [
        "CREATE CONSTRAINT issue_id IF NOT EXISTS FOR (n:Issue) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT symptom_id IF NOT EXISTS FOR (n:Symptom) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT root_cause_id IF NOT EXISTS FOR (n:RootCause) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT resolution_id IF NOT EXISTS FOR (n:Resolution) REQUIRE n.id IS UNIQUE",

        f"CREATE VECTOR INDEX issue_vector IF NOT EXISTS FOR (n:Issue) ON (n.embedding) OPTIONS {{indexConfig: {{vector_dimensions: {dim}, vector_similarity_function: 'cosine'}}}}",
        f"CREATE VECTOR INDEX symptom_vector IF NOT EXISTS FOR (n:Symptom) ON (n.embedding) OPTIONS {{indexConfig: {{vector_dimensions: {dim}, vector_similarity_function: 'cosine'}}}}",
        f"CREATE VECTOR INDEX root_cause_vector IF NOT EXISTS FOR (n:RootCause) ON (n.embedding) OPTIONS {{indexConfig: {{vector_dimensions: {dim}, vector_similarity_function: 'cosine'}}}}",
        f"CREATE VECTOR INDEX resolution_vector IF NOT EXISTS FOR (n:Resolution) ON (n.embedding) OPTIONS {{indexConfig: {{vector_dimensions: {dim}, vector_similarity_function: 'cosine'}}}}",

        "CREATE FULLTEXT INDEX issue_ft IF NOT EXISTS FOR (n:Issue) ON EACH [n.title, n.description]",
        "CREATE FULLTEXT INDEX symptom_ft IF NOT EXISTS FOR (n:Symptom) ON EACH [n.name, n.description]",
        "CREATE FULLTEXT INDEX root_cause_ft IF NOT EXISTS FOR (n:RootCause) ON EACH [n.description]",
        "CREATE FULLTEXT INDEX resolution_ft IF NOT EXISTS FOR (n:Resolution) ON EACH [n.summary, n.steps]",
    ]

    with db.session() as session:
        for q in queries:
            try:
                session.run(q)
            except Exception as e:
                print(f"Index setup note: {e}")
    print("Graph indexes verified.")
