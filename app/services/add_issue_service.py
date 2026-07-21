from app.models.requests import AddIssueRequest
from app.services.embedding_service import generate_embedding
from app.graph.repository import (
    get_all_categories,find_top_k_similar_problems,
    create_problem
    )
from app.services.category_service import validate_category
from app.models.status import AddIssueStatus


DUPLICATE_THRESHOLD=0.85


def validate_duplication(category_name: str,
    problem_embedding: list[float]
    ):


    top_K_problems=find_top_k_similar_problems(
    category_name,
    embedding=problem_embedding,
    k=5
    )

    if not top_K_problems:
        return False

    return top_K_problems[0]["score"] >= DUPLICATE_THRESHOLD




def add_new_issue(request: AddIssueRequest):

    embedding_text = f"""
        Title: {request.title}

        Description: {request.description}

        Symptoms:
        {" ".join(request.symptoms)}

        Root Cause:
        {request.root_cause}

        Solution:
        {request.solution}
        """
    
    
    categories=get_all_categories()
    
    category_names = [c["name"] for c in categories]

    category_name=request.category

    if request.category not in category_names:
        category_name=validate_category(request.category,categories)


    problem_embedding=generate_embedding(embedding_text)


    duplicate_status=validate_duplication(
        category_name,problem_embedding
        )

    if duplicate_status:
        return {
            "status": AddIssueStatus.DUPLICATE,
            "message": "A similar issue already exists."
        }
    
    create_problem(
        category_name,
        request,
        problem_embedding)
    
    return {
        "status": AddIssueStatus.SUCCESS,
        "message": "Issue added successfully."
    }

    
        







    

