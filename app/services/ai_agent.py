"""
AI Agent service using Google Gemini API.
"""
from typing import List, Dict, Optional
from google import genai
from google.genai import types
from app.config.settings import settings
from app.services.document_loader import document_loader
from app.models.schemas import ChatMessage
import logging
logger = logging.getLogger(__name__)


class AIAgent:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model  # "gemini-2.0-flash" recommended
        self.knowledge_base = document_loader.get_all_content()
        self.system_instruction = self._build_system_instruction()

    def _build_system_instruction(self) -> str:
        return f"""You are Howard's Portfolio Assistant, an AI helping recruiters and hiring managers learn about Howard (Hao) Ye.

ROLE:
You are professional, helpful, and concise. Your goal is to provide accurate information about Howard's background, skills, projects, and career interests.

GUIDELINES:
1. Be professional and enthusiastic about Howard's capabilities
2. Provide specific details from the knowledge base below
3. If asked about something not in the knowledge base, acknowledge it honestly
4. Highlight relevant experience for the specific question asked
5. Be concise but thorough — recruiters are busy
6. Include links to projects when relevant
7. Emphasize quantifiable results and technical depth

KNOWLEDGE BASE:
{self.knowledge_base}
"""

    async def chat(
        self,
        message: str,
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> Dict[str, any]:
        try:
            # Build conversation contents
            contents = []

            if conversation_history:
                for msg in conversation_history[-5:]:
                    role = "user" if msg.role == "user" else "model"
                    contents.append(types.Content(
                        role=role,
                        parts=[types.Part(text=msg.content)]
                    ))

            # Append current user message
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=message)]
            ))

            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=settings.temperature,
                    max_output_tokens=settings.max_tokens,
                )
            )

            response_text = response.text

            return {
                "response": response_text,
                "tokens_used": len(response_text.split()),
                "success": True
            }

        except Exception as e:
            logger.error(f"Gemini API error: {type(e).__name__}: {str(e)}", exc_info=True)
            return {
                "response": "I'm having trouble right now. Please try again or contact Howard directly.",
                "tokens_used": 0,
                "success": False,
                "error": str(e)
            }

    def get_example_questions(self) -> List[str]:
        return [
            "What is Howard's background and education?",
            "Tell me about Howard's CI/CD pipeline experience",
            "What cloud and DevOps skills does Howard have?",
            "What programming languages does Howard know?",
            "What types of roles is Howard seeking?",
            "What makes Howard's background unique?",
            "Can you describe Howard's MatchingDonors project?",
            "What is the Clinical Data Reconciliation Engine?"
        ]


# Global AI agent instance
ai_agent = AIAgent()