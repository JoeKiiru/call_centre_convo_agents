"""Structured model result types used by the ML service.

These lightweight models are intentionally small and typed so they
are easy to use in examples and tests.
"""

from typing import Literal
from pydantic import BaseModel, Field


class SentimentResult(BaseModel):
    overall: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    explanation: str


class TopicExtraction(BaseModel):
    topics: list[str]
    primary_topic: str


class ConversationAnalysis(BaseModel):
    sentiment: SentimentResult
    topics: TopicExtraction
    summary: str = Field(max_length=500)
    resolution_status: Literal["resolved", "unresolved", "escalated"]


class QualityScore(BaseModel):
    greeting_score: int = Field(ge=0, le=10)
    understanding_score: int = Field(ge=0, le=10)
    solution_effectiveness: int = Field(ge=0, le=10)
    communication_clarity: int = Field(ge=0, le=10)
    overall_score: float = Field(ge=0, le=10)
    justification: str


class HFInferenceResult(BaseModel):
    label: str
    score: float
    model_name: str
