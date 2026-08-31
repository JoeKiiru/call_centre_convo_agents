"""Agent compositions for conversation analysis and QA scoring.

This module defines a small set of Agents (Pydantic-AI) used by the
application: an analysis agent, a QA scoring agent, and a lightweight
chat assistant. Prompts and tool composition are intentionally small so
this code is easy to read and reuse in portfolio contexts.
"""

import os
from pydantic_ai import Agent
from src.models import Conversation, ConversationAnalysis, QualityScore
from src.agent.tools import hf_sentiment_tool

# Select model via environment, with a sensible default for local runs
model_name = os.getenv("LLM_MODEL", "google-gla:gemini-2.5-flash")


# Agent 1: Conversation analyzer producing structured `ConversationAnalysis`.
analysis_agent = Agent(
    model_name,
    output_type=ConversationAnalysis,
    system_prompt=(
        "You are an expert Customer Support Analyst. "
        "Analyze the provided conversation transcript and return a structured "
        "summary including sentiment, key topics, resolution status, and a short summary."
    ),
    tools=[hf_sentiment_tool],
)


# Agent 2: QA scorer that evaluates agent performance on a fixed rubric.
qa_agent = Agent(
    model_name,
    output_type=QualityScore,
    system_prompt=(
        "You are a Quality Assurance Specialist. "
        "Evaluate the agent's performance on Greeting, Understanding, Solution, and Clarity. "
        "Return numeric scores (0-10) and a concise justification for the overall score."
    ),
)


# Agent 3: General assistant for conversational queries. Accepts a Conversation
# object as dependency to enable context-aware responses.
chat_agent = Agent(
    model_name,
    system_prompt=(
        "You are a helpful assistant for conversation analysis. "
        "Answer user questions about provided conversations and reference evidence when available."
    ),
    deps_type=Conversation,
)
