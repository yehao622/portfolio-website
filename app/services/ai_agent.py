"""
AI Agent service using Google Gemini API.
Provides conversational interface for recruiters to learn about Howard.
"""
from typing import List, Dict, Optional
import google.generativeai as genai
from app.config.settings import settings
from app.services.document_loader import document_loader
from app.models.schemas import ChatMessage


class AIAgent:
    """AI agent for answering questions about Howard's background and projects."""
    
    def __init__(self):
        """Initialize AI agent with Gemini client."""
        # Configure Gemini
        genai.configure(api_key=settings.gemini_api_key)
        
        # Create model
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config={
                "temperature": settings.temperature,
                "max_output_tokens": settings.max_tokens,
            }
        )
        
        self.knowledge_base = document_loader.get_all_content()
        self.system_instruction = self._build_system_instruction()
    
    def _build_system_instruction(self) -> str:
        """Build system instruction with knowledge base."""
        return f"""You are Howard's Portfolio Assistant, an AI helping recruiters and hiring managers learn about Howard (Hao) Ye.

ROLE:
You are professional, helpful, and concise. Your goal is to provide accurate information about Howard's background, skills, projects, and career interests to help recruiters evaluate his fit for engineering roles.

GUIDELINES:
1. Be professional and enthusiastic about Howard's capabilities
2. Provide specific details from the knowledge base below
3. If asked about something not in the knowledge base, acknowledge that honestly
4. Highlight relevant experience for the specific question asked
5. Be concise but thorough - recruiters are busy
6. Include links to projects (GitHub, live demos) when relevant
7. Emphasize quantifiable results and technical depth

KNOWLEDGE BASE:
{self.knowledge_base}

EXAMPLE QUESTIONS YOU MIGHT GET:
- "What is Howard's experience with cloud infrastructure?"
- "Tell me about Howard's HPC simulation project"
- "What programming languages does Howard know?"
- "When does Howard graduate?"
- "What types of roles is Howard seeking?"
- "Can Howard work with legacy C++ systems?"
- "What makes Howard's background unique?"

Remember: Be helpful, accurate, and professional. You're representing Howard to potential employers!
"""
    
    async def chat(
        self, 
        message: str, 
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> Dict[str, any]:
        """
        Process a chat message and return AI response.
        
        Args:
            message: User's question
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dict with response text and metadata
        """
        try:
            # Build conversation history for Gemini
            history = []
            
            if conversation_history:
                for msg in conversation_history[-5:]:  # Keep last 5 messages
                    history.append({
                        "role": "user" if msg.role == "user" else "model",  # Gemini uses "model" not "assistant"
                        "parts": [msg.content]
                    })
            
            # Start chat session with history
            chat = self.model.start_chat(history=history)
            
            # Create prompt with system instruction
            full_prompt = f"{self.system_instruction}\n\nUser Question: {message}"
            
            # Send message
            response = chat.send_message(full_prompt)
            
            # Extract response text
            response_text = response.text
            
            # Gemini doesn't directly provide token counts in the same way
            # We'll estimate based on response length
            tokens_used = len(response_text.split()) * 1.3  # Rough estimate
            
            return {
                "response": response_text,
                "tokens_used": int(tokens_used),
                "success": True
            }
            
        except Exception as e:
            return {
                "response": "I apologize, but I'm having trouble processing your question right now. Please try again or contact Howard directly via email or LinkedIn.",
                "tokens_used": 0,
                "success": False,
                "error": str(e)
            }
    
    def get_example_questions(self) -> List[str]:
        """Get example questions for the UI."""
        return [
            "What is Howard's background and education?",
            "Tell me about Howard's HPC simulation project",
            "What experience does Howard have with cloud infrastructure?",
            "What programming languages and technologies does Howard know?",
            "What types of roles is Howard seeking?",
            "When does Howard graduate and what is his availability?",
            "What makes Howard's background unique?",
            "Can you describe Howard's Smart Home Energy project?"
        ]


# Global AI agent instance
ai_agent = AIAgent()