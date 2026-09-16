from sqlalchemy import text
from src.StudentsTrackingSystem.Dal import engine
from src.StudentsTrackingSystem.Dal.DTOs import Base

with engine.connect() as conn:
    row = conn.execute(
        text("select current_database(), current_user, version()")
    ).one()
    print(row)

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы.")


def reset_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Таблицы пересозданы.")


if __name__ == "__main__":
    create_tables()