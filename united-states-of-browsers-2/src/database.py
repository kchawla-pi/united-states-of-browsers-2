
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.schema import History



db_path = "/home/kshitijchawla/.mozilla/firefox/xac6zxxp.default-release/places (copy).sqlite"
db_engine = create_engine(f"sqlite:///{db_path}", echo=True, future=True)
with Session(bind=db_engine, future=True) as session:
    for history in session.query(History):
        print(history)
