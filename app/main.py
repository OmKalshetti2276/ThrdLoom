from fastapi import FastAPI
from pydantic import BaseModel


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

def search_issue(request: SearchIssueRequest):

    embedding=use_embedding(request.issue)
    matches=query_db(embedding)
    # we will use this to as a parent function to all orchestration functions. It will take the issue and pass it to the model to get the 
    # embedding and then pass the embedding to the model to get the response.
    return matches

def use_embedding(issue):
    # use this to pass the embedding to the model
    # and get the vector

    return {
        }

# @app.post("/query-db")

def query_db(   ):
    # pass the vector embedding as query and then get a matches list with highest
    # confidence than threshold 

    return
  