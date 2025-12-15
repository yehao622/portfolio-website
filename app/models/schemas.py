"""
Pydantic models for request/response schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==================== Chat Models ====================

class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation history")
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=[], 
        description="Previous messages in conversation"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="AI assistant's response")
    session_id: str = Field(..., description="Session ID for tracking conversation")
    timestamp: datetime = Field(default_factory=datetime.now)
    tokens_used: Optional[int] = Field(None, description="Number of tokens used in response")


# ==================== Analytics Models ====================

class VisitorCreate(BaseModel):
    """Model for recording a visitor."""
    ip_hash: Optional[str] = Field(None, description="Hashed IP address for privacy")
    user_agent: Optional[str] = Field(None, description="Browser user agent")
    page_visited: str = Field(..., description="Page path visited")


class VisitorStats(BaseModel):
    """Model for visitor statistics."""
    total_visitors: int = Field(..., description="Total number of unique visitors")
    total_visits: int = Field(..., description="Total page visits")
    recent_visits: int = Field(..., description="Visits in last 24 hours")


# ==================== Health Check Models ====================

class HealthStatus(str, Enum):
    """Health check status enum."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheck(BaseModel):
    """Health check response model."""
    status: HealthStatus
    timestamp: datetime = Field(default_factory=datetime.now)
    database: bool = Field(..., description="Database connection status")
    ai_service: bool = Field(..., description="AI service status")
    version: str = Field(..., description="API version")


# ==================== Error Models ====================

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now)