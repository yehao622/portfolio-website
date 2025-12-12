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
        id: 'hpc-smartops-platform',
        title: 'HPC Simulation & SmartOps AI Platform',
        description: 'Enterprise-grade AI-powered platform combining HPC simulations (C++ OMNeT++) with LangChain AI agents, multi-language microservices, and production monitoring.',
        problem: 'Large-scale distributed systems need both performance modeling for HPC clusters and intelligent automation with real-time analytics across microservices architecture.',
        metrics: [
            'Simulated 1000+ node HPC clusters with Lustre file system',
            'Sub-100ms API response times across microservices',
            '80% deployment time reduction with Docker containerization',
            'Real-time AI-powered system analysis with RAG',
            'Production monitoring with Prometheus/Grafana'
        ],
        techStack: [
            'C++',
            'OMNeT++',
            'Python',
            'FastAPI',
            'LangChain',
            'Java Spring Boot',
            'Node.js',
            'PostgreSQL',
            'ChromaDB',
            'Docker',
            'AWS',
            'Prometheus',
            'Grafana',
            'HPC',
            'Parallel File Systems(Lustre, PVFS, GPFS)'
        ],
        github: 'https://github.com/yehao622/hpc-simulation-platform',
        diagramPath: '/diagrams/hpc-smartops-architecture.jpg?v=2'
    },
    {
        id: 'smart-home-energy',
        title: 'Smart Home Energy Management System',
        description: 'Web-based microservices platform for real-time energy management and optimization using reinforcement learning (PPO) with Vue.js dashboard.',
        problem: 'Residential energy consumption lacks intelligent optimization, leading to waste and higher costs. Home energy systems need smart scheduling considering solar, battery, grid, and time-of-use pricing.',
        metrics: [
            '25% reduction in energy costs through RL optimization',
            'Real-time monitoring of 11 different appliances',
            'Smart scheduling based on electricity pricing',
            'Thermal modeling for HVAC and water heater',
            'Live demo deployed on Vercel'
        ],
        techStack: [
            'Python',
            'PyTorch',
            'PPO (Reinforcement Learning)',
            'REST APIs',
            'Node.js',
            'Vue.js',
            'Go',
            'Docker',
            'Socket.IO',
            'Kubernetes',
            'Terraform'
        ],
        github: 'https://github.com/yehao622/SmartHomeSimulator',
        liveDemo: 'https://smart-home-energy-demo.vercel.app/',
        diagramPath: '/diagrams/smart-home-architecture.jpg?v=2'
    }
];