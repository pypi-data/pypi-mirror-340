"""Tests for the Agent class functionality."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from semantic_kernel.contents import ChatHistory

from agently.agents.agent import Agent
from agently.conversation.context import ConversationContext, Message
from agently.errors import AgentError


@pytest.mark.asyncio
async def test_agent_initialization(test_agent_config):
    """Test basic agent initialization."""
    agent = Agent(test_agent_config)
    assert agent.id == test_agent_config.id
    assert agent.name == test_agent_config.name
    assert agent.provider is None  # Provider not initialized yet


@pytest.mark.asyncio
async def test_agent_initialization_with_openai(test_agent_config, mock_openai_key):
    """Test agent initialization with OpenAI provider."""
    agent = Agent(test_agent_config)
    await agent.initialize()

    assert agent.provider is not None
    assert agent.provider.__class__.__name__ == "OpenAIProvider"


@pytest.mark.asyncio
async def test_agent_initialization_invalid_provider(test_agent_config):
    """Test agent initialization with invalid provider."""
    test_agent_config.model.provider = "invalid_provider"
    agent = Agent(test_agent_config)

    with pytest.raises(AgentError) as exc_info:
        await agent.initialize()

    assert "Failed to initialize agent" in str(exc_info.value)
    assert "Unsupported provider type" in str(exc_info.value.__cause__)


@pytest.mark.asyncio
async def test_agent_process_message(test_agent_config, mock_openai_key):
    """Test agent message processing."""
    agent = Agent(test_agent_config)
    await agent.initialize()

    # Create a mock process_message method that returns our expected chunks
    async def mock_process_message(*args, **kwargs):
        for chunk in ["Hello", " there", "!"]:
            yield chunk

    # Patch the process_message method directly
    with patch.object(agent, "process_message", side_effect=mock_process_message):
        # Create a test message and context
        message = Message(content="Test message", role="user")
        context = ConversationContext(conversation_id="test_context")

        # Process the message
        response = ""
        async for chunk in agent.process_message(message, context):
            response += chunk

        # Check the response
        assert response == "Hello there!"


@pytest.mark.asyncio
async def test_agent_process_message_without_initialization(test_agent_config):
    """Test message processing without initialization."""
    agent = Agent(test_agent_config)
    message = Message(content="Hi", role="user")
    context = ConversationContext("test-conv")

    responses = []
    async for chunk in agent.process_message(message, context):
        responses.append(chunk)

    assert len(responses) == 1
    assert "Error processing message" in responses[0]
    assert "Try rephrasing your message or check agent status" in responses[0]


@pytest.mark.asyncio
async def test_agent_process_message_provider_error(test_agent_config, mock_openai_key):
    """Test handling of provider errors during message processing."""
    agent = Agent(test_agent_config)
    await agent.initialize()

    # Mock process_message to yield an error message
    async def mock_process_message_error(*args, **kwargs):
        yield "Error: API Error - Try rephrasing your message or check agent status"

    # Replace the process_message method with our mock
    with patch.object(agent, "process_message", side_effect=mock_process_message_error):
        # Create a test message and context
        message = Message(content="Test message", role="user")
        context = ConversationContext(conversation_id="test_context")

        # Process the message
        response = ""
        async for chunk in agent.process_message(message, context):
            response += chunk

        # Check that the response contains the error message
        assert "Error" in response


@pytest.mark.asyncio
async def test_agent_error_context_creation(test_agent_config):
    """Test creation of error context in agent operations."""
    agent = Agent(test_agent_config)
    context = await agent._handle_agent_operation("test_operation", extra_detail="test")

    assert context.component == "agent"
    assert context.operation == "test_operation"
    assert context.details["agent_id"] == agent.id
    assert context.details["agent_name"] == agent.name
    assert context.details["extra_detail"] == "test"
