export interface Project {
    id: string;
    title: string;
    description: string;
    problem: string;
    metrics: string[];
    techStack: string[];
    github: string;
    liveDemo?: string;
    diagramPath?: string;
}

export const projects: Project[] = [
    {
        id: 'matchingdonors-platform',
        title: 'MatchingDonors AI Platform',
        description: 'Full-stack healthcare platform for organ donor matching featuring an AI-powered assistant suite for profile creation, content discovery, and advertiser engagement.',
        problem: 'Patient profile creation was manual and slow, and healthcare news content lacked structured metadata, making topic-based filtering difficult.',
        metrics: [
            'Integrated Gemini API for automated news content categorization',
            'Built real-time advertiser chat using Socket.IO',
            'Designed enterprise CI/CD pipelines with Jenkins and GitHub Actions',
            'Implemented strict RBAC and JWT authentication schemas'
        ],
        techStack: ['React', 'TypeScript', 'Node.js', 'SQLite', 'Google Gemini API', 'Socket.IO', 'Jenkins', 'GitHub Actions'],
        github: 'https://github.com/yehao622/demo/tree/feature/admin',
        liveDemo: 'https://matchingdonors-haosdemo.vercel.app',
        diagramPath: `graph TD
            User([Platform Users / Donors]) <-->|HTTPS / WebSockets| Frontend[React Frontend UI]
            Frontend <-->|REST API| Backend[Node.js / Express Backend]
            Frontend <-->|Socket.IO| Chat[Real-Time Chat Service]
            
            subgraph Backend Infrastructure
                Backend --> Auth[JWT & RBAC Security Layer]
                Auth --> Controllers[Business Logic Controllers]
                Controllers <--> DB[(SQLite Database)]
                Controllers --> Notifications[Resend API Integration]
            end
            
            subgraph AI & Automation
                Controllers <-->|Prompts & Context| Gemini[Google Gemini API]
                Crawler[Content Crawler] --> Gemini
                Gemini -->|Auto-labels| DB
            end

            subgraph CI/CD Pipeline
                Dev([Developer]) -->|Push| GitHub[GitHub Repo]
                GitHub -->|Trigger| GHActions[GitHub Actions: Unit Tests]
                GitHub -->|Trigger| Jenkins[Jenkins Pipeline: QA & Integration Tests]
            end`
    },
    {
        id: 'clinical-data-engine',
        title: 'Clinical Data Reconciliation Engine',
        description: 'AI-powered REST API that resolves conflicting medical records from disparate healthcare systems using LLM-driven confidence scoring and quality validation.',
        problem: 'Healthcare providers deal with conflicting patient data across EHRs, pharmacies, and portals, requiring manual reconciliation to ensure patient safety.',
        metrics: [
            'Reduced LLM costs by ~60% through intelligent response caching',
            'Automated data validation across 4 clinical dimensions',
            'Achieved high availability via Render deployment with Docker',
            'Secured endpoints with 30 req/15min rate limiting and API key auth'
        ],
        techStack: ['Node.js', 'TypeScript', 'React', 'Docker', 'Google Gemini 2.5 Flash', 'Jest', 'SQLite', 'Render'],
        github: 'https://github.com/yehao622/interview',
        liveDemo: 'https://engine-demo.onrender.com',
        diagramPath: `graph TD
            Clients([Healthcare Portals / Clients]) -->|HTTPS| API_Gateway[Render.com Load Balancer]
            API_Gateway --> RateLimiter[Rate Limiter: 30req/15min]
            RateLimiter --> Auth[API Key Authentication]
            
            subgraph Docker Container
                Auth --> NodeApp[Node.js/TypeScript Engine]
                NodeApp --> Validator[Clinical Dimension Validator]
                NodeApp <--> Cache[LLM Response Cache]
                NodeApp <--> DB[(SQLite Audit Trail)]
            end
            
            subgraph External Systems
                Validator -->|Fetch Records| EHR[(EHR Systems)]
                Validator -->|Fetch Records| Pharmacy[(Pharmacy Systems)]
                NodeApp <-->|Reconciliation Tasks| Gemini[Google Gemini 2.5 Flash]
            end`
    },
    {
        id: 'hpc-cloud-platform',
        title: 'Cloud-Native HPC Simulation Platform',
        description: '4-service microservices platform orchestrated with Docker Compose and deployed on AWS EC2, integrating a core C++/OMNeT++ simulation engine for large-scale HPC storage networks.',
        problem: 'Large-scale distributed systems need performance modeling for HPC clusters (like Lustre) alongside a modern, cloud-accessible API gateway and caching layer.',
        metrics: [
            'Simulated complex Fattree topologies and parallel file systems',
            'Deployed production-ready application on AWS EC2 with security groups',
            'Built RESTful API gateway with JWT auth and Redis caching',
            'Engineered automated benchmarking tools and data analysis pipelines'
        ],
        techStack: ['Docker', 'Node.js/TypeScript', 'PostgreSQL', 'Redis', 'AWS EC2', 'C/C++', 'OMNeT++'],
        github: 'https://github.com/yehao622/hpc-simulation-platform',
        diagramPath: `graph TD
            Client([Web Dashboard]) -->|HTTPS| AWS_EC2[AWS EC2 Instance]
            
            subgraph Docker Compose Environment
                AWS_EC2 --> API_Gateway[Node.js API Gateway]
                API_Gateway <--> Redis[(Redis Cache)]
                API_Gateway <--> AuthLayer[JWT Auth Layer]
                
                AuthLayer --> SimService[Simulation Microservice]
                AuthLayer --> DataService[Data Processor Service]
                
                SimService <--> C_Engine[C++/OMNeT++ HPC Core]
                DataService <--> Postgres[(PostgreSQL DB)]
            end
            
            subgraph Simulation Core
                C_Engine --> Fattree[Fattree Topology Models]
                C_Engine --> Lustre[Lustre File System Models]
            end`
    },
    {
        id: 'smart-home-energy',
        title: 'Smart Home Energy Management System',
        description: 'Event-driven microservices platform for real-time energy management and optimization using reinforcement learning (PPO) with a Vue.js dashboard.',
        problem: 'Residential energy consumption lacks intelligent optimization. Home energy systems need smart scheduling considering IoT telemetry and time-of-use pricing.',
        metrics: [
            'Built 4 containerized services processing data from 11+ IoT devices',
            'Integrated reinforcement learning service for automated scheduling',
            'Implemented local Docker dev and Vercel production deployment',
            'Real-time bi-directional communication via Socket.IO'
        ],
        techStack: ['Docker', 'Vue.js', 'TypeScript', 'Node.js', 'Python', 'PPO (Reinforcement Learning)', 'Socket.IO'],
        github: 'https://github.com/yehao622/SmartHomeSimulator',
        liveDemo: 'https://smart-home-energy-demo.vercel.app/',
        diagramPath: `graph TD
            IoT([11+ Smart IoT Devices]) -->|Real-time Telemetry| EventBus[Socket.IO Event Bus]
            VueUI[Vue.js Dashboard on Vercel] <-->|WebSockets| EventBus
            
            subgraph Containerized Microservices
                EventBus <--> NodeBackend[Node.js Core Service]
                NodeBackend <--> Scheduler[Device Scheduling Service]
                
                Scheduler <--> RLEngine[Python Reinforcement Learning Engine]
            end
            
            subgraph AI Engine
                RLEngine --> PPO[PPO Optimization Model]
                PPO -->|Optimal Policy| RLEngine
            end`
    }
];