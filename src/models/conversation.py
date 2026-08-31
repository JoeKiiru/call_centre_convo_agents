"""Pydantic domain models for conversations and messages.

These models represent the minimal structures used by the agents and API
endpoints. Validators enforce basic correctness for portfolio demos.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Role(str, Enum):
    CUSTOMER = "customer"
    AGENT = "agent"


class Message(BaseModel):
    id: str = Field(
        ...,
        description="Unique message id, incorporated as part of the Conversation BaseModel",
    )
    role: Role
    content: str = Field(..., min_length=1)
    timestamp: datetime


class ConversationMetadata(BaseModel):
    queue_time_seconds: Optional[int] = Field(None, ge=0)
    handle_time_seconds: Optional[int] = Field(None, ge=0)
    customer_satisfaction_score: Optional[int] = Field(None, ge=1, le=5)
    first_contact_resolution: bool = False


class Conversation(BaseModel):
    id: str
    customer_id: str
    channel: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    customer_name: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    messages: List[Message]
    metadata: ConversationMetadata

    @field_validator("messages")
    def must_have_messages(cls, v):
        if len(v) == 0:
            raise ValueError("Conversation must have at least one message")
        return v

    def get_text_transcript(self) -> str:
        """Return a simple text transcript suitable for LLM prompts.

        The transcript is a newline-separated sequence of role: content
        pairs. This is intentionally simple so prompts are easier to
        reason about in portfolio examples.
        """
        return "\n".join([f"{m.role.upper()}: {m.content}" for m in self.messages])
