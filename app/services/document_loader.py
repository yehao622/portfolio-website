"""
Document loader service for loading resume and project documentation.
This provides the knowledge base for the AI agent.
"""
from typing import List, Dict


class DocumentLoader:
    """Loads and manages documents for AI agent knowledge base."""
    
    def __init__(self):
        """Initialize document loader with Howard's information."""
        self.documents = self._load_documents()
    
    def _load_documents(self) -> List[Dict[str, str]]:
        """Load all documents for the knowledge base."""
        
        # Resume and background information
        resume_doc = {
            "type": "resume",
            "content": """
Howard (Hao) Ye - DevOps & Full Stack & Cloud Engineer

EDUCATION:
- MS in Computer Engineering, University of Tennessee Knoxville (Graduating May 2025)
- MS in Industrial Engineering (Previous degree with focus on optimization and mathematical modeling)

ABOUT:
Computer Engineering graduate student passionate about building scalable cloud infrastructure, 
DevOps automation, and AI-powered systems. Experience spans Python backend development, 
microservices architecture, AWS cloud services, and high-performance computing simulation.

CORE COMPETENCIES:
- Cloud Infrastructure: AWS, Docker, PostgreSQL
- Full Stack Development: Python, Node.js, React, TypeScript
- AI/ML Integration: LangChain, OpenAI, RAG, PyTorch
- DevOps & CI/CD Automation
- High-Performance Computing (HPC)
- System Performance Optimization
- Mathematical Optimization (IBM CPLEX)

SEEKING:
Junior to mid-level positions in:
- DevOps Engineering
- Full Stack Engineering  
- Cloud Engineering
- Site Reliability Engineering
- Backend Engineering
- System Performance Engineering

LOCATION: Worcester, MA (Open to remote/hybrid)
STATUS: Open to full-time, part-time, and contract opportunities
GRADUATION: May 2025

GITHUB: https://github.com/yehao622
LINKEDIN: https://www.linkedin.com/in/ye-hao-256168121/
"""
        }
        
        # Project 1: HPC Simulation & SmartOps AI Platform
        project1_doc = {
            "type": "project",
            "title": "HPC Simulation & SmartOps AI Platform",
            "content": """
HPC Simulation & SmartOps AI Platform

DESCRIPTION:
Enterprise-grade AI-powered platform combining HPC simulations (C++ OMNeT++) with LangChain AI agents, 
multi-language microservices, and production monitoring.

PROBLEM SOLVED:
Large-scale distributed systems need both performance modeling for HPC clusters and intelligent 
automation with real-time analytics across microservices architecture.

KEY RESULTS:
✓ Simulated 1000+ node HPC clusters with Lustre file system
✓ Sub-100ms API response times across microservices
✓ 80% deployment time reduction with Docker containerization
✓ Real-time AI-powered system analysis with RAG
✓ Production monitoring with Prometheus/Grafana

TECHNOLOGY STACK:
- HPC Simulation: C++ with OMNeT++ framework
- Backend Services: Python FastAPI, Java Spring Boot, Node.js
- AI Integration: LangChain, Claude API, RAG architecture
- Databases: PostgreSQL, ChromaDB (vector store)
- Infrastructure: Docker, AWS
- Monitoring: Prometheus, Grafana
- File Systems: Lustre, PVFS, GPFS

TECHNICAL HIGHLIGHTS:
- Microservices architecture with multiple languages (C++, Python, Java, Node.js)
- HPC cluster performance modeling and simulation
- AI-powered operational insights using RAG
- Real-time metrics collection and visualization
- Containerized deployment for rapid iteration

GITHUB: https://github.com/yehao622/hpc-simulation-platform
"""
        }
        
        # Project 2: Smart Home Energy Management System
        project2_doc = {
            "type": "project",
            "title": "Smart Home Energy Management System",
            "content": """
Smart Home Energy Management System

DESCRIPTION:
Web-based microservices platform for real-time energy management and optimization using 
reinforcement learning (PPO algorithm) with Vue.js dashboard.

PROBLEM SOLVED:
Residential energy consumption lacks intelligent optimization, leading to waste and higher costs. 
Home energy systems need smart scheduling considering solar generation, battery storage, 
grid electricity, and time-of-use pricing.

KEY RESULTS:
✓ 25% reduction in energy costs through RL optimization
✓ Real-time monitoring of 11 different appliances
✓ Smart scheduling based on electricity pricing
✓ Thermal modeling for HVAC and water heater optimization
✓ Live demo deployed on Vercel

TECHNOLOGY STACK:
- Machine Learning: Python, PyTorch, PPO (Proximal Policy Optimization)
- Backend: REST APIs, Node.js
- Frontend: Vue.js dashboard
- Infrastructure: Docker, Kubernetes, Terraform
- Real-time Communication: Socket.IO
- Deployment: Vercel (frontend), containerized backend

TECHNICAL HIGHLIGHTS:
- Reinforcement learning for energy optimization
- Real-time appliance monitoring and control
- Time-of-use pricing integration
- Thermal modeling for heating/cooling systems
- Microservices architecture with event-driven design
- Live production deployment with monitoring

GITHUB: https://github.com/yehao622/SmartHomeSimulator
LIVE DEMO: https://smart-home-energy-demo.vercel.app/
"""
        }
        
        # Additional context and FAQs
        faq_doc = {
            "type": "faq",
            "content": """
FREQUENTLY ASKED QUESTIONS:

Q: What is Howard's graduation date?
A: May 2025 from University of Tennessee Knoxville (MS in Computer Engineering)

Q: What types of roles is Howard seeking?
A: Junior to mid-level positions in DevOps, Full Stack, Cloud, Backend, Site Reliability, 
   and System Performance Engineering. Particularly interested in roles combining cloud infrastructure,
   performance optimization, and AI/ML integration.

Q: What is Howard's experience level?
A: Equivalent to 2-4 years of experience through graduate research, projects, and technical work.
   Strong foundation in HPC simulation, cloud infrastructure, and full-stack development.

Q: What makes Howard's background unique?
A: Combination of HPC simulation expertise, mathematical optimization background, and modern 
   cloud-native development. Experience bridging C++ legacy systems with Python/Node.js microservices.

Q: Is Howard open to relocation?
A: Yes, currently located in Worcester, MA but open to remote, hybrid, or relocation opportunities.

Q: What industries is Howard interested in?
A: Climate tech, healthcare, scientific computing, and mission-driven companies focused on 
   sustainability and social impact.

Q: What are Howard's technical strengths?
A: Performance optimization, system architecture design, AI/ML integration (LangChain, RAG),
   cloud infrastructure (AWS, Docker), full-stack development (Python, Node.js, React),
   and mathematical modeling.

Q: Can Howard work with legacy systems?
A: Yes! Experience integrating C++ OMNeT++ simulations with modern Python/Node.js services.
   Comfortable working across technology generations.

Q: What development practices does Howard follow?
A: Microservices architecture, containerization (Docker/Kubernetes), CI/CD automation,
   monitoring/observability (Prometheus/Grafana), infrastructure as code.
"""
        }
        
        return [resume_doc, project1_doc, project2_doc, faq_doc]
    
    def get_all_content(self) -> str:
        """Get all documents concatenated as a single knowledge base."""
        return "\n\n---\n\n".join([doc["content"] for doc in self.documents])
    
    def search_documents(self, query: str) -> List[Dict[str, str]]:
        """Simple keyword-based search (Phase 1 MVP - no vector store yet)."""
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in self.documents:
            if any(keyword in doc["content"].lower() for keyword in query_lower.split()):
                relevant_docs.append(doc)
        
        return relevant_docs if relevant_docs else self.documents


# Global document loader instance
document_loader = DocumentLoader()