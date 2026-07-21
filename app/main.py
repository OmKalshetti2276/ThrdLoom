from fastapi import FastAPI
from app.services.search_service import search_issue
from app.services.add_issue_service import add_new_issue
from app.models.requests import (
    SearchIssueRequest,
    AddIssueRequest
)
from app.graph.repository import get_category_names



app = FastAPI(
    title="ThrdLoom: Your Organizational Memory",
    description="Helps to fix bugs",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "service": "ThrdLoom",
        "status": "online",
        "version": "1.0.0"
    }


@app.post("/search-issue")

def search_issue_route(request: SearchIssueRequest):

    knowledge = search_issue(
        request.category,
        request.issue
    )

    if knowledge is None:
        return {
            "found": False,
            "knowledge":[]
        }

    return {
        "found": True,
        "knowledge": knowledge
    }


@app.get("/get-categories")

def get_categories():
    return get_category_names()



@app.post("/add-issue")

def add_issue_route(request:AddIssueRequest):

    result = add_new_issue(request)

    return result














# @app.post("/sample")

# def run_sample():

#     print("Calling search_issue...")

#     sample = search_issue("FastAPI cannot connect to the database.")

#     print("Returned:", sample)

#     return sample
