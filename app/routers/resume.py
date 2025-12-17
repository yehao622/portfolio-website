"""
Resume download router with anti-crawler protection.
"""
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import os
from datetime import datetime
import hashlib
import base64

router = APIRouter(prefix="/api/resume", tags=["resume"])

# Rate limiter: 3 downloads per hour per IP
limiter = Limiter(key_func=get_remote_address)

# Path to resume PDF
RESUME_PATH = "resumes/Howard_Ye_Resume.pdf"


def validate_token(token: str) -> bool:
    """
    Validate time-based token (must be within 1 hour).
    Token format: base64(timestamp)
    """
    try:
        # Decode token to get timestamp
        decoded = base64.b64decode(token + '==')  # Add padding
        token_time = int(decoded.decode('utf-8'))
        
        # Check if token is within 1 hour (3600000 ms)
        current_time = int(datetime.now().timestamp() * 1000)
        time_diff = current_time - token_time
        
        # Token valid if less than 1 hour old
        return 0 <= time_diff <= 3600000
        
    except Exception:
        return False


@router.get("/download")
@limiter.limit("3/hour")  # Max 3 downloads per hour per IP
async def download_resume(
    token: str,
    request: Request
):
    """
    Download resume with anti-crawler protection.
    
    Protection layers:
    1. Token validation (time-based, 1-hour expiry)
    2. Rate limiting (3 per hour per IP)
    3. User agent checking (block obvious bots)
    """
    
    # Check 1: Validate token
    if not validate_token(token):
        raise HTTPException(
            status_code=403,
            detail="Invalid or expired token. Please refresh the page and try again."
        )
    
    # Check 2: Basic user agent validation
    user_agent = request.headers.get('user-agent', '').lower()
    bot_keywords = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
    if any(keyword in user_agent for keyword in bot_keywords):
        raise HTTPException(
            status_code=403,
            detail="Automated access not allowed. Please use a web browser."
        )
    
    # Check 3: Verify file exists
    if not os.path.exists(RESUME_PATH):
        raise HTTPException(
            status_code=404,
            detail="Resume not found. Please contact me directly."
        )
    
    # Log download (hash IP for privacy)
    ip_hash = hashlib.sha256(
        request.client.host.encode()
    ).hexdigest()[:16]
    
    print(f"📥 Resume download - IP: {ip_hash}, UA: {user_agent[:50]}")
    
    # Return file
    return FileResponse(
        path=RESUME_PATH,
        filename="Howard_Ye_Resume.pdf",
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Howard_Ye_Resume.pdf",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


@router.get("/preview")
async def preview_resume():
    """
    Return resume info without downloading (for SEO/preview).
    """
    return {
        "available": True,
        "filename": "Howard_Ye_Resume.pdf",
        "description": "Computer Engineering graduate student (MS) seeking DevOps, Full Stack, Cloud, and System Performance Engineering roles",
        "updated": "December 2025",
        "download_info": "Click 'Download Resume' button on the homepage to access"
    }