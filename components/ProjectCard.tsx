'use client';

import { useState, useEffect, useRef } from 'react';
import { Project } from '@/lib/projects';
import ImageModal from './ImageModal';
import mermaid from 'mermaid';

// Initialize mermaid with a clean theme
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
});

// Safe Client-Side Mermaid Renderer
const MermaidDiagram = ({ chart }: { chart: string }) => {
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (ref.current) {
            mermaid.contentLoaded();
            mermaid.render(`mermaid-${Math.random().toString(36).substr(2, 9)}`, chart).then((result) => {
                if (ref.current) {
                    ref.current.innerHTML = result.svg;

                    // Force the SVG to shrink and fit inside the project card beautifully
                    const svg = ref.current.querySelector('svg');
                    if (svg) {
                        svg.style.maxWidth = '100%';
                        svg.style.maxHeight = '100%';
                        svg.style.height = 'auto';
                    }
                }
            });
        }
    }, [chart]);

    return <div ref={ref} className="mermaid flex justify-center items-center w-full h-full p-4" />;
};

interface ProjectCardProps {
    project: Project;
}

export default function ProjectCard({ project }: ProjectCardProps) {
    const [isModalOpen, setIsModalOpen] = useState(false);

    return (
        <>
            <div className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow flex flex-col">
                {/* Project Diagram Area */}
                <div 
                    className="h-64 bg-slate-50 border-b border-slate-100 flex items-center justify-center cursor-pointer group relative overflow-hidden"
                    onClick={() => project.diagramPath && setIsModalOpen(true)}
                >
                    {project.diagramPath ? (
                         // If diagramPath contains mermaid code (starts with 'graph'), render it natively
                        project.diagramPath.startsWith('graph') ? (
                            <MermaidDiagram chart={project.diagramPath} />
                        ) : (
                            // Fallback to image if it's a standard URL/path
                            <img src={project.diagramPath} alt={`${project.title} Architecture`} className="w-full h-full object-contain p-4" />
                        )
                    ) : (
                        <div className="flex flex-col items-center justify-center h-full text-slate-400">
                            <svg className="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                            </svg>
                            <span className="text-sm">Architecture Diagram Coming Soon</span>
                        </div>
                    )}

                    {/* Hover Enlarge Badge */}
                    {project.diagramPath && (
                        <div className="absolute top-4 right-4 bg-blue-600 text-white px-3 py-1.5 rounded-full text-xs font-medium shadow-md opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" /></svg>
                            Enlarge
                        </div>
                    )}
                </div>

                {/* Text Content Area */}
                <div className="p-6 flex-grow flex flex-col">
                    <h3 className="text-2xl font-bold text-slate-900 mb-3">{project.title}</h3>
                    <p className="text-slate-600 mb-4 text-sm">{project.description}</p>

                    <div className="mb-4">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Problem Solved</h4>
                        <p className="text-slate-700 text-sm bg-slate-50 p-3 rounded-md border border-slate-100">{project.problem}</p>
                    </div>

                    <div className="mb-6 flex-grow">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Key Results</h4>
                        <ul className="space-y-1.5">
                            {project.metrics.map((metric, index) => (
                                <li key={index} className="text-slate-600 text-sm flex items-start">
                                    <span className="text-green-500 mr-2 mt-0.5 font-bold">✓</span>
                                    <span>{metric}</span>
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="mb-6">
                        <div className="flex flex-wrap gap-1.5">
                            {project.techStack.map((tech, index) => (
                                <span key={index} className="bg-blue-50 text-blue-700 border border-blue-100 text-xs px-2.5 py-1 rounded-md font-medium">
                                    {tech}
                                </span>
                            ))}
                        </div>
                    </div>

                    <div className="flex gap-4 pt-4 border-t border-slate-100 mt-auto">
                        <a href={project.github} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1.5 text-slate-600 hover:text-slate-900 transition font-medium text-sm">
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" /></svg>
                            GitHub Repo
                        </a>
                        {project.liveDemo && (
                            <a href={project.liveDemo} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1.5 text-blue-600 hover:text-blue-800 transition font-medium text-sm">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                                Live Demo
                            </a>
                        )}
                    </div>
                </div>
            </div>

            {/* Image Modal for the Enlarge Feature */}
            {project.diagramPath && (
                <ImageModal
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    imageSrc={project.diagramPath}
                    imageAlt={`${project.title} Architecture Diagram`}
                />
            )}
        </>
    );
}