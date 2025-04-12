import os
from sqlmodel import create_engine, SQLModel, Session

def get_database_url():
    # Option 1: Use a pre-built DATABASE_URL, recommended for simplicity.
    url = os.environ.get("DATABASE_URL")
    if url:
        return url

    # Option 2: Build the URL from individual components.
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")         # e.g. "35.223.217.207" for public IP connection.
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME")         # e.g. "timesheet-db"
    connection_name = os.environ.get("DB_CONNECTION_NAME")  # e.g. "hopkinstimesheetproj:us-central1:timesheet-db"

    # If a connection name is provided, assume you're using Cloud SQL with Unix sockets.
    if connection_name:
        return f"postgresql+psycopg2://{db_user}:{db_password}@/{db_name}?host=/cloudsql/{connection_name}"
    else:
        # Otherwise, use the host, port, and other components for a direct connection.
        return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create the engine using the database URL from the environment.
engine = create_engine(get_database_url(), echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
