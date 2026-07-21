from app.services.embedding_service import generate_embedding
from app.services.helper import cosine_similarity


def validate_category(category, categories):
    category_embedding = generate_embedding(category)

    best_match = max(
        categories,
        key=lambda c: cosine_similarity(c["embedding"], category_embedding)
    )

    return best_match["name"]