import numpy as np
from app.services.helper import cosine_similarity
from app.services.embedding_service import generate_embedding
from app.graph.repository import (get_all_categories, get_problems_by_category)

CATEGORY_THRESHOLD = 0.60
TOP_CATEGORIES = 3
TOP_PROBLEMS =5
PROBLEM_THRESHOLD=0.70





def search_issue(issue:str):

    

    embedding=generate_embedding(issue)

    categories=get_all_categories()

    matched_categories = [] #list

    for category in categories:
        score=cosine_similarity(embedding,category["embedding"])

        if score>CATEGORY_THRESHOLD :
            matched_categories.append({
                "name":category["name"],
                "score":score
            })
    # return matched_categories

    matched_categories.sort(
    key=lambda x: x["score"],
    reverse=True
    )

    matched_categories = matched_categories[:TOP_CATEGORIES]

    if not matched_categories :
        return None
    
    matched_problems = []
    
    for category in matched_categories:
        problems=get_problems_by_category(category["name"])

        for problem in problems:
            score=cosine_similarity(embedding,problem["embedding"])

            if score> PROBLEM_THRESHOLD:
                matched_problems.append({
                    
                    "id": problem["id"],
                    "title": problem["title"],
                    "description": problem["description"],
                    "symptoms": problem["symptoms"],
                    "root_cause": problem["root_cause"],
                    "solution": problem["solution"],
                    "score": score

})
        

    if not matched_problems:
        return None


        # Now take top 5 problems acc to simailarity and add to result and return



    matched_problems.sort(
    key=lambda x: x["score"],
    reverse=True
    )

    return matched_problems[:TOP_PROBLEMS]


        



    

    # def find_best_category(query: str):


    