from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    query: str
    top_k: Optional[int] = 6

class SearchResult(BaseModel):
    id: str
    question: str
    subject: str
    year: int
    score: float

class AskResponse(BaseModel):
    answer: str
    sources: List[SearchResult]
