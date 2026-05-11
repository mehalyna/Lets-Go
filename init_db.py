"""
Initialize database script
Run this script to set up Neo4j constraints and indexes
"""
from app import create_app
from app.database import init_db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        print("Initializing database...")
        init_db()
        print("Database initialized successfully!")
