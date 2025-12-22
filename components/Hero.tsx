'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Button from './Button';
import SecureDownloadButton from './SecureDownloadButton';

export default function Hero() {
    const [visitorCount, setVisitorCount] = useState<number | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Define API URL
        const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

        const initVisit = async () => {
            try {
                // 1. Record the visit
                // We use a simple POST request. You can expand the body if needed.
                await fetch(`${API_URL}/api/analytics/visit`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        page_visited: window.location.pathname,
                        user_agent: navigator.userAgent
                    }),
                });

                // 2. Fetch the updated stats
                const response = await fetch(`${API_URL}/api/analytics/stats`);
                if (response.ok) {
                    const data = await response.json();
                    setVisitorCount(data.total_visits);
                }
            } catch (error) {
                console.error('Error fetching visitor count:', error);
            } finally {
                setLoading(false);
            }
        };

        initVisit();
    }, []);

    return (
        <section className="max-w-6xl mx-auto px-4 py-20">
            <div className="text-center">
                {/* Profile Photo */}
                <div className="mb-8">
                    <Image
                        src="/photo.jpeg"
                        alt="Howard Ye"
                        width={128}
                        height={128}
                        className="rounded-full mx-auto shadow-lg"
                        priority
                    />
                </div>

                {/* Title */}
                <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
                    DevOps & Full Stack & Cloud Engineer
                </h2>

                {/* Subtitle */}
                <p className="text-lg md:text-xl text-slate-600 mb-2 max-w-2xl mx-auto">
                    MS in Computer Engineering @ University of Tennessee Knoxville
                </p>
                <p className="text-base md:text-lg text-slate-500 mb-8 max-w-2xl mx-auto">
                    Building scalable cloud systems, AI-powered platforms, and high-performance computing solutions
                </p>

                {/* Social Links */}
                <div className="flex gap-4 justify-center mb-8">
                    <a
                        href="https://github.com/yehao622"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-slate-600 hover:text-slate-900 transition"
                        aria-label="GitHub"
                    >
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                        </svg>
                    </a>
                    <a
                        href="https://www.linkedin.com/in/ye-hao-256168121/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-slate-600 hover:text-slate-900 transition"
                        aria-label="LinkedIn"
                    >
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                        </svg>
                    </a>
                    <a
                        href="mailto:hyedailyuse@gmail.com"
                        className="text-slate-600 hover:text-slate-900 transition"
                        aria-label="Email"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                    </a>
                </div>

                <div className="mb-8">
                    <SecureDownloadButton />
                </div>

                {/* Visitor Counter */}
                {/* <div className="text-sm text-slate-500">
                    👁️ Visitors: <span className="font-semibold">0 (To be deployed)</span>
                </div> */}
                <div className="text-sm text-slate-500 flex items-center justify-center gap-2">
                    <span>👁️ Visitors:</span>
                    <span className="font-semibold min-w-[20px] text-center">
                        {loading ? (
                            <span className="animate-pulse">...</span>
                        ) : (
                            visitorCount !== null ? visitorCount.toLocaleString() : 'N/A'
                        )}
                    </span>
                </div>
            </div>
        </section>
    );
}