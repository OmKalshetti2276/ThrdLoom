from pydantic import BaseModel,Field

class SearchIssueRequest(BaseModel):
    category:str
    issue: str

class AddIssueRequest(BaseModel):
    category: str
    title: str
    description: str
    symptoms: list[str]
    root_cause: str
    solution: str
    applicable_versions: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    