'use client';

import { useState } from 'react';
import { API_ENDPOINTS } from '@/lib/config';

export default function SecureDownloadButton() {
    const [isVerified, setIsVerified] = useState(false);
    const [isDownloading, setIsDownloading] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const handleDownload = async () => {
        setErrorMessage(null); // Clear previous errors

        if (!isVerified) {
            alert('Please verify you are a recruiter first');
            return;
        }

        setIsDownloading(true);

        try {
            // Generate time-based token (expires in 1 hour)
            const token = btoa(Date.now().toString());//.slice(0, 12);

            // Use environment-aware URL
            const downloadUrl = `${API_ENDPOINTS.resumeDownload}?token=${encodeURIComponent(token)}`;

            // Call backend API (with token)
            const response = await fetch(
                downloadUrl,
                {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/pdf',
                    }
                }
            );

            if (!response.ok) {
                if (response.status === 403) throw new Error("Session expired. Please refresh the page.");
                if (response.status === 429) throw new Error("Too many downloads. Please wait.");
                throw new Error("Download failed. Please try again.");
            }

            // Get the blob
            const blob = await response.blob();

            // Create download link
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'Howard_Ye_Resume.pdf';
            document.body.appendChild(link);
            link.click();

            // Cleanup
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);

            // Log analytics
            await fetch(API_ENDPOINTS.analyticsDownload, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'resume_download',
                    timestamp: new Date().toISOString()
                })
            }).catch(err => console.error('Analytics failed:', err));

        } catch (error) {
            console.error('Download error:', error);
            setErrorMessage(error.message || 'An unexpected error occurred');
        } finally {
            setIsDownloading(false);
        }
    };

    return (
        <div className="flex flex-col gap-3 items-center">
            {/* Human Verification Checkbox */}
            <label className="flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
                <input
                    type="checkbox"
                    checked={isVerified}
                    onChange={(e) => {
                        setIsVerified(e.target.checked);
                        if (e.target.checked) setErrorMessage(null);
                    }}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                />
                <span>I'm a recruiter or hiring manager</span>
            </label>

            {/* Download Button */}
            <button
                onClick={handleDownload}
                disabled={!isVerified || isDownloading}
                className={`
          px-6 py-3 rounded-lg font-semibold transition-all duration-200 
          flex items-center gap-2 min-w-[200px] justify-center
          ${isVerified
                        ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl cursor-pointer'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }
                `}
                aria-label="Download resume"
            >
                {isDownloading ? (
                    <>
                        <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Downloading...
                    </>
                ) : (
                    <>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Download Resume
                    </>
                )}
            </button>

            {/* OPTIMIZATION: Display Error Message Here */}
            {errorMessage && (
                <p className="text-sm text-red-500 font-medium animate-pulse">
                    {errorMessage}
                </p>
            )}

            {/* Privacy Notice */}
            <p className="text-xs text-slate-500 text-center max-w-sm">
                🔒 Your download is private and only logged anonymously for analytics
            </p>
        </div>
    );
}