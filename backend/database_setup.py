from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base  # imports all your models

# Replace with your actual database URL
# Example for PostgreSQL: "postgresql://user:password@localhost:5432/mydb"
DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for simplicity

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables defined in your models
Base.metadata.create_all(bind=engine)

# Optional: create a session factory for interacting with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Simple test to check everything works
if __name__ == "__main__":
    print("All tables are created successfully!")
