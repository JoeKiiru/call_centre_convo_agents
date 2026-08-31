"""Pytest configuration and fixtures for the conversation agents demo."""

import json
import pytest
from pathlib import Path


@pytest.fixture
def sample_conversations():
    """Load sample conversation data for testing."""
    data_path = Path(__file__).parent.parent / "data" / "sample_conversations.json"
    with open(data_path) as f:
        return json.load(f)["conversations"]


@pytest.fixture
def single_conversation(sample_conversations):
    """Get a single conversation for simple tests."""
    return sample_conversations[0]


@pytest.fixture
def good_conversation(sample_conversations):
    """Get a conversation with positive outcome (billing resolution)."""
    return sample_conversations[0]  # conv_001


@pytest.fixture
def poor_conversation(sample_conversations):
    """Get a conversation with negative outcome (technical issue - escalated)."""
    return sample_conversations[1]  # conv_002


@pytest.fixture
def upgrade_conversation(sample_conversations):
    """Get a successful upgrade conversation."""
    return sample_conversations[2]  # conv_003


@pytest.fixture
def retention_conversation(sample_conversations):
    """Get a retention/cancellation conversation."""
    return sample_conversations[3]  # conv_004


@pytest.fixture
def feedback_conversation(sample_conversations):
    """Get a feature request/feedback conversation."""
    return sample_conversations[4]  # conv_005


@pytest.fixture
def empty_conversation():
    """Create an empty conversation for edge case testing."""
    return {
        "id": "conv_empty",
        "customer_id": "cust_test",
        "channel": "chat",
        "started_at": "2025-01-20T00:00:00Z",
        "ended_at": "2025-01-20T00:01:00Z",
        "agent_id": "agent_test",
        "agent_name": "Test Agent",
        "customer_name": "Test Customer",
        "tags": [],
        "messages": [],
        "metadata": {}
    }


@pytest.fixture
def minimal_conversation():
    """Create a minimal valid conversation."""
    return {
        "id": "conv_minimal",
        "customer_id": "cust_test",
        "channel": "chat",
        "started_at": "2025-01-20T00:00:00Z",
        "ended_at": "2025-01-20T00:05:00Z",
        "agent_id": "agent_test",
        "agent_name": "Test Agent",
        "customer_name": "Test Customer",
        "tags": ["test"],
        "messages": [
            {
                "id": "msg_001",
                "role": "customer",
                "content": "Hello, I need help",
                "timestamp": "2025-01-20T00:00:00Z"
            },
            {
                "id": "msg_002",
                "role": "agent",
                "content": "Hi! How can I assist you today?",
                "timestamp": "2025-01-20T00:00:30Z"
            }
        ],
        "metadata": {
            "handle_time_seconds": 300
        }
    }


# Mock LLM response fixtures
@pytest.fixture
def mock_analysis_response():
    """Mock structured response for conversation analysis."""
    return {
        "sentiment": {
            "overall": "positive",
            "confidence": 0.85,
            "trajectory": "stable"
        },
        "topics": ["billing", "refund", "subscription"],
        "intent": "complaint_resolution",
        "resolution_status": "resolved",
        "summary": "Customer reported a duplicate charge. Agent verified the issue and processed a refund. Customer was satisfied with the quick resolution."
    }


@pytest.fixture
def mock_qa_score_response():
    """Mock structured response for QA scoring."""
    return {
        "greeting_professionalism": 9,
        "problem_understanding": 8,
        "solution_effectiveness": 9,
        "communication_clarity": 8,
        "overall_score": 8.5,
        "justification": "Agent demonstrated excellent professionalism and effectively resolved the customer's billing issue.",
        "improvement_areas": ["Could have proactively offered additional assistance sooner"]
    }
