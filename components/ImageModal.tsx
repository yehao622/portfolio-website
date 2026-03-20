import { useEffect, useRef } from "react";
import Image from "next/image";
import mermaid from "mermaid";

// 1. Safe Client-Side Mermaid Renderer specifically for the Modal
const MermaidModalDiagram = ({ chart }: { chart: string }) => {
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (ref.current) {
            mermaid.contentLoaded();
            mermaid.render(`mermaid-modal-${Math.random().toString(36).substr(2, 9)}`, chart).then((result) => {
                if (ref.current) {
                    ref.current.innerHTML = result.svg;
                    // Let the SVG scale up beautifully inside the modal
                    const svg = ref.current.querySelector('svg');
                    if (svg) {
                        svg.style.maxWidth = '100%';
                        svg.style.height = 'auto';
                    }
                }
            });
        }
    }, [chart]);

    // Added a white background and padding so the diagram is easy to read
    return <div ref={ref} className="flex justify-center items-center w-full h-full bg-white rounded-xl p-4 md:p-8 overflow-auto" />;
};

interface ImageModalProps {
    isOpen: boolean;
    onClose: () => void;
    imageSrc: string;
    imageAlt: string;
}

export default function ImageModal({ isOpen, onClose, imageSrc, imageAlt }: ImageModalProps) {
    if (!isOpen) return null;

    // 2. Detect if the incoming "imageSrc" is actually Mermaid code
    const isMermaid = imageSrc && imageSrc.startsWith('graph');

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 p-6 md:p-12"
            onClick={onClose}
        >
            <div className="relative max-w-6xl max-h-[90vh] w-full h-full flex flex-col items-center justify-center">
                
                {/* Close button - Moved slightly outside the box for better UX */}
                <button
                    onClick={onClose}
                    className="absolute -top-4 -right-4 z-10 bg-white text-slate-900 rounded-full p-2 hover:bg-gray-200 transition shadow-xl"
                    aria-label="Close modal"
                >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>

                {/* Content Area */}
                <div className="relative w-full h-full flex items-center justify-center" onClick={(e) => e.stopPropagation()}>
                    {isMermaid ? (
                        <MermaidModalDiagram chart={imageSrc} />
                    ) : (
                        <Image
                            src={imageSrc}
                            alt={imageAlt}
                            fill
                            className="object-contain"
                            sizes="90vw"
                        />
                    )}
                </div>

                {/* Instructions */}
                <p className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-white text-sm bg-black bg-opacity-50 px-4 py-1.5 rounded-full pointer-events-none">
                    Click outside to close
                </p>
            </div>
        </div>
    );
}