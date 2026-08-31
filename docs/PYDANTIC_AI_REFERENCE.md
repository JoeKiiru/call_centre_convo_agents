# Pydantic AI Quick Reference

This document provides quick reference examples for Pydantic AI patterns you might find useful.

> **Note:** This is supplementary reference material. You're encouraged to consult the official Pydantic AI documentation at https://ai.pydantic.dev/

## Basic Agent Setup

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ResponseModel(BaseModel):
    answer: str
    confidence: float

agent = Agent(
    'openai:gpt-4o-mini',  # Model identifier
    result_type=ResponseModel,  # Structured output
    system_prompt='You are a helpful assistant.'
)

# Synchronous usage
result = agent.run_sync('What is the capital of France?')
print(result.data)  # ResponseModel instance

# Asynchronous usage
async def main():
    result = await agent.run('What is the capital of France?')
    return result.data
```

## Defining Tools

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

class Dependencies(BaseModel):
    """Dependencies available to tools."""
    user_id: str
    database_url: str

agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=Dependencies
)

@agent.tool
def get_user_name(ctx: RunContext[Dependencies]) -> str:
    """Get the current user's name."""
    # Access dependencies via ctx.deps
    user_id = ctx.deps.user_id
    # ... fetch from database
    return f"User {user_id}"

@agent.tool
def search_conversations(
    ctx: RunContext[Dependencies],
    query: str,
    limit: int = 10
) -> list[dict]:
    """Search conversations by keyword."""
    # Tool implementation
    return [{"id": "conv_1", "summary": "..."}]
```

## Structured Outputs with Nested Models

```python
from pydantic import BaseModel, Field
from typing import Literal
from pydantic_ai import Agent

class SentimentResult(BaseModel):
    """Structured sentiment analysis result."""
    overall: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    explanation: str

class TopicExtraction(BaseModel):
    """Extracted topics from conversation."""
    topics: list[str]
    primary_topic: str

class ConversationAnalysis(BaseModel):
    """Complete conversation analysis."""
    sentiment: SentimentResult
    topics: TopicExtraction
    summary: str = Field(max_length=500)
    resolution_status: Literal["resolved", "unresolved", "escalated"]

# Agent with complex structured output
analysis_agent = Agent(
    'openai:gpt-4o-mini',
    result_type=ConversationAnalysis,
    system_prompt='''You are a conversation analyst. 
    Analyze customer support conversations and provide structured insights.'''
)
```

## Dynamic System Prompts

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

class AnalysisContext(BaseModel):
    company_name: str
    scoring_criteria: dict[str, str]

agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=AnalysisContext
)

@agent.system_prompt
def build_system_prompt(ctx: RunContext[AnalysisContext]) -> str:
    criteria_text = "\n".join(
        f"- {k}: {v}" for k, v in ctx.deps.scoring_criteria.items()
    )
    return f'''You are a QA analyst for {ctx.deps.company_name}.
    
Score conversations based on these criteria:
{criteria_text}
'''
```

## Error Handling

```python
from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelRetry, UnexpectedModelBehavior

agent = Agent('openai:gpt-4o-mini')

@agent.tool
def risky_operation(ctx, data: str) -> str:
    """A tool that might fail."""
    if not data:
        # Signal that model should retry with different input
        raise ModelRetry("Data cannot be empty, please provide valid input")
    return f"Processed: {data}"

# Handle errors at the call site
try:
    result = await agent.run("Process this data")
except UnexpectedModelBehavior as e:
    print(f"Model behaved unexpectedly: {e}")
```

## Message History for Multi-turn

```python
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage

agent = Agent('openai:gpt-4o-mini')

# First turn
result1 = await agent.run("Analyze this conversation: ...")
history: list[ModelMessage] = result1.all_messages()

# Second turn - maintains context
result2 = await agent.run(
    "What was the main issue?",
    message_history=history
)
```

## Streaming Responses

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o-mini')

async def stream_response(prompt: str):
    async with agent.run_stream(prompt) as response:
        async for text in response.stream_text():
            yield text
```

## Integration with FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_ai import Agent

app = FastAPI()

class AnalysisRequest(BaseModel):
    conversation: dict

class AnalysisResponse(BaseModel):
    sentiment: str
    summary: str

agent = Agent(
    'openai:gpt-4o-mini',
    result_type=AnalysisResponse
)

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_conversation(request: AnalysisRequest):
    try:
        result = await agent.run(
            f"Analyze this conversation: {request.conversation}"
        )
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Testing Patterns

```python
import pytest
from unittest.mock import patch, AsyncMock
from pydantic_ai import Agent

@pytest.fixture
def mock_agent_response():
    """Create a mock for agent responses."""
    mock_result = AsyncMock()
    mock_result.data = {"sentiment": "positive", "confidence": 0.9}
    return mock_result

@pytest.mark.asyncio
async def test_agent_analysis(mock_agent_response):
    with patch.object(Agent, 'run', return_value=mock_agent_response):
        # Your test code here
        pass
```

---

## Useful Links

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
