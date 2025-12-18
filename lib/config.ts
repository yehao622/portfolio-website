/**
 * Application configuration
 * Automatically uses correct API URL based on environment
 */

// Detect if we're in development or production
const isDevelopment = process.env.NODE_ENV === 'development';

// API Base URL
export const API_BASE_URL = isDevelopment
    ? 'http://localhost:8000'  // Local development
    : 'https://howardye.up.railway.app';  // Production (Railway)

// Helper function to build API URLs
export function getApiUrl(endpoint: string): string {
    // Remove leading slash if present
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
    return `${API_BASE_URL}/${cleanEndpoint}`;
}

// Export individual endpoints for convenience
export const API_ENDPOINTS = {
    health: getApiUrl('health'),
    chat: getApiUrl('api/chat'),
    chatExamples: getApiUrl('api/chat/examples'),
    resumeDownload: getApiUrl('api/resume/download'),
    resumePreview: getApiUrl('api/resume/preview'),
    analyticsDownload: getApiUrl('api/analytics/download'),
    analyticsVisitor: getApiUrl('api/analytics/visitor'),
};

// Log current environment (helpful for debugging)
if (typeof window !== 'undefined') {
    console.log(`🌍 Environment: ${process.env.NODE_ENV}`);
    console.log(`🔗 API URL: ${API_BASE_URL}`);
}