from app.services.category_service import validate_category
from app.services.embedding_service import generate_embedding
from app.graph.repository import (get_all_categories,
                                  find_top_k_similar_problems)

TOP_PROBLEMS =5


def search_issue(category:str,issue:str):

    embedding=generate_embedding(issue)

    categories=get_all_categories()
    
    category_names = [c["name"] for c in categories]

    if category not in category_names:
        category=validate_category(category,categories)


    matched_problems=find_top_k_similar_problems(category, embedding, TOP_PROBLEMS)


    if not matched_problems:
        return None
    
    return matched_problems



    