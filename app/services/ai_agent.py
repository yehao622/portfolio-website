"""
AI Agent service using Google Gemini API.
"""
from typing import List, Dict, Optional
from google import genai
from google.genai import types
from pdfminer.high_level import extract_text

from app.config.settings import settings
from app.services.document_loader import document_loader
from app.models.schemas import ChatMessage
import logging, os

logger = logging.getLogger(__name__)

def get_dynamic_portfolio_context() -> str:
    """Reads the live TypeScript project file to dynamically inject into the AI context."""
    projects_file_path = os.path.join(os.getcwd(), "lib", "projects.ts")
    
    try:
        with open(projects_file_path, "r", encoding="utf-8") as file:
            projects_content = file.read()
    except FileNotFoundError:
        projects_content = "Projects data currently unavailable."

    return f"""
    CURRENT PORTFOLIO PROJECTS (from lib/projects.ts):
    The following is the live TypeScript data driving my portfolio website right now. 
    Use this to understand my exact, current projects, tech stacks, and metrics:
    
    {projects_content}
    """

def get_resume_context() -> str:
    """Extracts raw text from the latest PDF resume."""
    resume_path = os.path.join(os.getcwd(), "public", "Howard_Ye_Resume.pdf")
    
    if not os.path.exists(resume_path):
        resume_path = os.path.join(os.getcwd(), "resumes", "Howard_Ye_Resume.pdf")
        
    try:
        if os.path.exists(resume_path):
            raw_text = extract_text(resume_path)
            cleaned_text = " ".join(raw_text.split())
            return f"""
            HOWARD YE'S CURRENT RESUME:
            The following is the raw text extracted from my latest PDF resume. 
            Use this to answer questions about my work history, education, skills, and certifications:
            
            {cleaned_text}
            """
        else:
            return "Resume PDF not found on the server."
    except Exception as e:
        logger.error(f"PDF Parsing Error: {e}")
        return "Resume data currently unavailable."

class AIAgent:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model  # "gemini-2.0-flash" recommended
        self.base_knowledge = document_loader.get_all_content()
        self.system_instruction = self._build_system_instruction()

    def _build_system_instruction(self) -> str:
        # Dynamically fetch latest frontend and resume data
        live_projects = get_dynamic_portfolio_context()
        live_resume = get_resume_context()
        
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
8. Use the LIVE RESUME DATA and LIVE PORTFOLIO PROJECTS provided below to answer questions about projects and work history.

BASE KNOWLEDGE:
{self.base_knowledge}

{live_resume}

{live_projects}
"""

    async def chat(
        self, 
        message: str, 
        history: Optional[List[ChatMessage]] = None
    ) -> Dict:
        """Process a chat message using Gemini API."""
        try:
            contents = []
            
            # Format history for Gemini
            if history:
                for msg in history:
                    contents.append(
                        types.Content(
                            role="user" if msg.role == "user" else "model",
                            parts=[types.Part.from_text(text=msg.content)]
                        )
                    )
            
            # Add current message
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=message)]
                )
            )

            # Generate response
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