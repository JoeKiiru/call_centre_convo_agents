"""FastAPI routes exposing the conversation agent functionality.

The routes are intentionally small and focused so they are easy to
include in a portfolio demo. They perform validation via Pydantic
models and call into the agent and ML services.
"""

from fastapi import APIRouter, HTTPException

from src.models import (
    Conversation,
    ConversationAnalysis,
    QualityScore,
    HFInferenceResult,
)
from src.agent.core import analysis_agent, qa_agent, chat_agent
from src.services import ml_service

router = APIRouter()


@router.post("/conversations/analyze", response_model=ConversationAnalysis)
async def analyze_conversation(conversation: Conversation):
    transcript = conversation.get_text_transcript()

    try:
        result = await analysis_agent.run(transcript)
        return result.output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations/qa-score", response_model=QualityScore)
async def score_conversation(conversation: Conversation):
    transcript = conversation.get_text_transcript()
    try:
        result = await qa_agent.run(transcript)
        return result.output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations/ml-analyze", response_model=HFInferenceResult)
async def ml_analyze(text_input: str):
    try:
        return await ml_service.predict_sentiment(text_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML Inference failed: {e}")


@router.post("/agent/chat")
async def agent_chat(user_query: str, conversation_context: Conversation = None):
    try:
        prompt = user_query
        if conversation_context:
            prompt = f"Context: {conversation_context.get_text_transcript()}\n\nUser Question: {user_query}"

        # Run the chat assistant; agent.run may return a structured object
        # depending on the agent configuration. Return a stable JSON shape.
        result = await chat_agent.run(prompt)
        return {"response": getattr(result, "output", result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
