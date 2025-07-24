from pydantic import BaseModel
from typing import List

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
