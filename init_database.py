"""
Database initialization script.
Run this to create all necessary tables.
"""
import sys
from app.config.database import init_db, engine
from sqlalchemy import text


def main():
    """Initialize database with all tables."""
    print("Initializing database...")
    
    try:
        # Test connection first
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful")
        
        # Create tables
        init_db()
        print("✓ Database tables created successfully")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            print(f"✓ Created tables: {', '.join(tables)}")
        
        print("\n✅ Database initialization complete!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())