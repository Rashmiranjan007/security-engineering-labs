from pydantic import BaseModel, Field, ConfigDict

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tenant_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    user_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    message: str = Field(min_length=1, max_length=4000)

class ChatResponse(BaseModel):
    answer: str
    citations: list[str]
    security_status: str
