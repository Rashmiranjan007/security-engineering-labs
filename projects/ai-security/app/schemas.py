from pydantic import BaseModel, Field, ConfigDict


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str
    citations: list[str]
    security_status: str
