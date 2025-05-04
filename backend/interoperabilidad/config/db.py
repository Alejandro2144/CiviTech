# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///acf.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={ 'check_same_thread': False}, pool_size=20, max_overflow=30)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         return db
#     finally:
#         db.close()

''' Use whatever may be needed from this code to connect to the database.'''