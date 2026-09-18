from Dal.database import engine, SessionLocal
import Dal.DTOs
from Dal.DTOs.Base import Base
from sqlalchemy import text
from Core.Seed import role_seed, admin_seed

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

    with SessionLocal() as session:
        role_seed(session)
        admin_seed(session)