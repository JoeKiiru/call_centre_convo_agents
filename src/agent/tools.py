"""Agent tools that wrap lightweight ML service calls.

Tools are small async adapters that the Pydantic-AI agents can call to
augment LLM outputs with model-based signals (for example, a HF
sentiment pipeline).
"""

from pydantic_ai import RunContext
from src.services import ml_service
from src.models import HFInferenceResult


async def hf_sentiment_tool(ctx: RunContext, text: str) -> HFInferenceResult:
    """
    A tool that uses a specialized local Machine Learning model to detect
    sentiment with high precision. Use this when you need a second opinion
    or a numerical confidence score for sentiment.

    Args:
        text: The specific text segment to analyze.
    """
    try:
        result = await ml_service.predict_sentiment(text)
        return result
    except Exception as e:
        raise RuntimeError(f"Error running ML inference: {str(e)}")
