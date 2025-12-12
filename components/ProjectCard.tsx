'use client';

import { useState } from 'react';
import { Project } from '@/lib/projects';
import ImageModal from './ImageModal';

interface ProjectCardProps {
    project: Project;
}

export default function ProjectCard({ project }: ProjectCardProps) {
    const [isModalOpen, setIsModalOpen] = useState(false);

    return (
        <>
            <div className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                {/* Project Diagram - Using simple img tag for debugging */}
                <div
                    className="h-64 bg-gradient-to-br from-blue-50 to-slate-100 flex items-center justify-center cursor-pointer group overflow-hidden"
                    onClick={() => project.diagramPath && setIsModalOpen(true)}
                >
                    {project.diagramPath ? (
                        <div className="relative w-full h-full p-4">
                            {/* Simple img tag - no Next.js optimization */}
                            <img
                                src={project.diagramPath}
                                alt={`${project.title} Architecture`}
                                className="w-full h-full object-contain"
                                style={{ maxWidth: '100%', maxHeight: '100%' }}
                                onError={(e) => {
                                    console.error('Image failed to load:', project.diagramPath);
                                    e.currentTarget.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><text x="50%" y="50%" text-anchor="middle" fill="gray">Image Error</text></svg>';
                                }}
                                onLoad={(e) => {
                                    console.log('Image loaded successfully:', project.diagramPath);
                                }}
                            />

                            {/* Animated "Click to Enlarge" Badge */}
                            <div className="absolute top-4 right-4 bg-blue-600 text-white px-3 py-1.5 rounded-full text-xs font-medium shadow-lg animate-pulse group-hover:animate-none">
                                🔍 Click to Enlarge
                            </div>

                            {/* Hover overlay with zoom icon */}
                            <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                <div className="bg-white rounded-full p-2 shadow-lg">
                                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="flex items-center justify-center h-full text-slate-500 text-center p-4">
                            <div>
                                <svg className="w-16 h-16 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                </svg>
                                <p className="text-sm">Architecture Diagram Coming Soon</p>
                            </div>
                        </div>
                    )}
                </div>

                {/* Rest of the component */}
                <div className="p-6">
                    <h3 className="text-2xl font-bold text-slate-900 mb-3">
                        {project.title}
                    </h3>

                    <p className="text-slate-600 mb-4">
                        {project.description}
                    </p>

                    <div className="mb-4">
                        <h4 className="text-sm font-semibold text-slate-700 mb-2">Problem Solved:</h4>
                        <p className="text-slate-600 text-sm">
                            {project.problem}
                        </p>
                    </div>

                    <div className="mb-4">
                        <h4 className="text-sm font-semibold text-slate-700 mb-2">Key Results:</h4>
                        <ul className="space-y-1">
                            {project.metrics.map((metric, index) => (
                                <li key={index} className="text-slate-600 text-sm flex items-start">
                                    <span className="text-green-600 mr-2">✓</span>
                                    {metric}
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="mb-4">
                        <h4 className="text-sm font-semibold text-slate-700 mb-2">Tech Stack:</h4>
                        <div className="flex flex-wrap gap-2">
                            {project.techStack.map((tech, index) => (
                                <span
                                    key={index}
                                    className="bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full"
                                >
                                    {tech}
                                </span>
                            ))}
                        </div>
                    </div>

                    <div className="flex gap-3 pt-4 border-t border-slate-200">
                        <a
                            href={project.github}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-2 text-slate-700 hover:text-slate-900 transition"
                        >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                            </svg>
                            <span className="text-sm font-medium">GitHub</span>
                        </a>

                        {project.liveDemo && (
                            <a
                                href={project.liveDemo}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 text-blue-600 hover:text-blue-700 transition"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                </svg>
                                <span className="text-sm font-medium">Live Demo</span>
                            </a>
                        )}
                    </div>
                </div>
            </div>

            {/* Image Modal */}
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