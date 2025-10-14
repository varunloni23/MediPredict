from app.database import Base, engine
from app.models import user, device, device_data, prediction

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()