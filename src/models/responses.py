"""API response models used by the chat agent endpoints.

Keep response shapes simple for demo and documentation purposes.
"""

from typing import List, Optional
from pydantic import BaseModel


class AgentResponse(BaseModel):
    response: str
    citations: Optional[List[str]] = None
    structured_data: Optional[dict] = None
