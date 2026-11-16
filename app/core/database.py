import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

# Fallback SQLite URL if PostgreSQL is unavailable or not configured
SQLITE_FALLBACK_URL = "sqlite:///./agritech.db"

def get_engine_and_session(database_url: str):
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    
    _engine = create_engine(
        database_url,
        connect_args=connect_args
    )
    _session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine, _session_local

# Determine initial database URL
target_db_url = settings.DATABASE_URL or SQLITE_FALLBACK_URL

try:
    engine, SessionLocal = get_engine_and_session(target_db_url)
    # Quick probe if not sqlite to fail fast and fallback
    if not target_db_url.startswith("sqlite"):
        with engine.connect() as conn:
            pass
        print(f"✅ Connected to primary database: {target_db_url.split('@')[-1] if '@' in target_db_url else target_db_url}")
except Exception as e:
    print(f"⚠️ Primary database connection failed ({e}). Falling back to SQLite ({SQLITE_FALLBACK_URL}).")
    target_db_url = SQLITE_FALLBACK_URL
    engine, SessionLocal = get_engine_and_session(target_db_url)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables with automatic SQLite fallback"""
    global engine, SessionLocal
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables verified/initialized")
    except Exception as e:
        print(f"⚠️ Failed to initialize tables on current database ({e}). Switching to SQLite fallback...")
        engine, SessionLocal = get_engine_and_session(SQLITE_FALLBACK_URL)
        Base.metadata.create_all(bind=engine)
        print("✅ Fallback SQLite database initialized successfully at ./agritech.db")

