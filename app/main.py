from fastapi import FastAPI
from pydantic import BaseModel
from app.services.search_service import search_issue
# from app.graph.repository import create_category, get_category


class SearchIssueRequest(BaseModel):
    issue:str

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






# @app.post("/sample")

# def run_sample():

#     print("Calling search_issue...")

#     sample = search_issue("FastAPI cannot connect to the database.")

#     print("Returned:", sample)

#     return sample
