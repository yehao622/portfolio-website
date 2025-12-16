"""
Chat router for AI agent endpoints.
"""
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.services.ai_agent import ai_agent
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI agent about Howard's background and projects.
    
    Args:
        request: ChatRequest with user message and optional conversation history
        
    Returns:
        ChatResponse with AI-generated answer
    """
    try:
        # Generate or use existing session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get AI response
        result = await ai_agent.chat(
            message=request.message,
            conversation_history=request.conversation_history
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI service error: {result.get('error', 'Unknown error')}"
            )
        
        return ChatResponse(
            response=result["response"],
            session_id=session_id,
            timestamp=datetime.now(),
            tokens_used=result.get("tokens_used")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.get("/examples")
async def get_example_questions():
    """
    Get example questions that recruiters can ask.
    
    Returns:
        List of example questions
    """
    return {
        "examples": ai_agent.get_example_questions()
    }