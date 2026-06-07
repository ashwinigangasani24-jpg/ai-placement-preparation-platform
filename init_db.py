#!/usr/bin/env python3
"""
Database initialization script for AI Internship & Placement Intelligence Platform
"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.db.session import engine, SessionLocal
from app.db.models import Base, User, UserRole
from app.core.security import get_password_hash


def init_db():
    """Initialize database with schema and sample data"""
    
    print("🔄 Initializing database...")
    
    # Create all tables
    print("📋 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")
    
    # Create sample admin user
    print("👤 Creating sample admin user...")
    db = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@placement.local").first()
        
        if not admin:
            admin_user = User(
                name="Admin User",
                email="admin@placement.local",
                password_hash=get_password_hash("admin123"),
                role=UserRole.admin,
            )
            db.add(admin_user)
            print("✅ Admin user created")
            print("   Email: admin@placement.local")
            print("   Password: admin123")
        else:
            print("⚠️  Admin user already exists")
        
        # Create sample student user
        student = db.query(User).filter(User.email == "student@placement.local").first()
        
        if not student:
            student_user = User(
                name="Sample Student",
                email="student@placement.local",
                password_hash=get_password_hash("student123"),
                role=UserRole.student,
            )
            db.add(student_user)
            print("✅ Sample student user created")
            print("   Email: student@placement.local")
            print("   Password: student123")
        else:
            print("⚠️  Sample student already exists")
        
        db.commit()
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n✨ Database initialization complete!")
    print("\nYou can now:")
    print("1. Start the backend: uvicorn app.main:app --reload")
    print("2. Start the frontend: npm run dev")
    print("3. Login at http://localhost:3000/login")
    print("\nSample credentials:")
    print("  Admin: admin@placement.local / admin123")
    print("  Student: student@placement.local / student123")


if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
