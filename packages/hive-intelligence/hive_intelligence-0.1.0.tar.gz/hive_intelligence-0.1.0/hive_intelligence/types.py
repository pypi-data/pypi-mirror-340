
from typing import Optional, List, Any
from pydantic import BaseModel, Field

class HiveSearchMessage(BaseModel):
    role: str  # 'user' | 'assistant'
    content: str

class HiveSearchRequest(BaseModel):
    prompt: Optional[str] = Field(default=None)
    messages: Optional[List[HiveSearchMessage]] = Field(default=None)
    temperature: Optional[float] = Field(default=0.7)
    top_k: Optional[int] = Field(default=None)
    top_p: Optional[float] = Field(default=None)
    include_data_sources: Optional[bool] = Field(default=True)

class HiveSearchResponse(BaseModel):
    response: dict[str, Any]
    isAdditionalDataRequired: Optional[list] = None
    data_sources: Optional[List[str]] = None

