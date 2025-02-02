from .database import SessionLocal

class DBSessionManager:
    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # An exception occurred, roll back
            self.db.rollback()
        else:
            # Everything was okay, commit
            self.db.commit()
        self.db.close()

# Alternatively, a generator style:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
