"""
Analytics router for visitor tracking.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import hashlib

from app.config.database import get_db, Visitor
from app.models.schemas import VisitorCreate, VisitorStats

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def hash_ip(ip: str) -> str:
    """Hash IP address for privacy."""
    return hashlib.sha256(ip.encode()).hexdigest()


@router.post("/visit")
async def record_visit(
    visitor_data: VisitorCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Record a visitor page view.
    
    Args:
        visitor_data: Visitor information
        request: FastAPI request object
        db: Database session
        
    Returns:
        Success confirmation
    """
    try:
        # Get client IP and hash it for privacy
        client_ip = request.client.host
        ip_hash = hash_ip(client_ip) if client_ip else None
        
        # Create visitor record
        visitor = Visitor(
            ip_hash=ip_hash or visitor_data.ip_hash,
            user_agent=visitor_data.user_agent,
            page_visited=visitor_data.page_visited
        )
        
        db.add(visitor)
        db.commit()
        
        return {
            "success": True,
            "message": "Visit recorded successfully"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to record visit: {str(e)}"
        )


@router.get("/stats", response_model=VisitorStats)
async def get_visitor_stats(db: Session = Depends(get_db)):
    """
    Get visitor statistics.
    
    Returns:
        VisitorStats with total and recent visitor counts
    """
    try:
        # Total unique visitors (unique IP hashes)
        total_visitors = db.query(func.count(func.distinct(Visitor.ip_hash))).scalar()
        
        # Total visits
        total_visits = db.query(func.count(Visitor.id)).scalar()
        
        # Recent visits (last 24 hours)
        yesterday = datetime.now() - timedelta(days=1)
        recent_visits = db.query(func.count(Visitor.id)).filter(
            Visitor.visit_date >= yesterday
        ).scalar()
        
        return VisitorStats(
            total_visitors=total_visitors or 0,
            total_visits=total_visits or 0,
            recent_visits=recent_visits or 0
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get visitor stats: {str(e)}"
        )


@router.get("/recent")
async def get_recent_visits(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get recent visits (for admin dashboard - Phase 2).
    
    Args:
        limit: Number of recent visits to retrieve
        db: Database session
        
    Returns:
        List of recent visits
    """
    try:
        visits = db.query(Visitor).order_by(
            Visitor.visit_date.desc()
        ).limit(limit).all()
        
        return {
            "visits": [
                {
                    "page": visit.page_visited,
                    "date": visit.visit_date.isoformat(),
                    "user_agent": visit.user_agent[:50] if visit.user_agent else None  # Truncate for privacy
                }
                for visit in visits
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get recent visits: {str(e)}"
        )