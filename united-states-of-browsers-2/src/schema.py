from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class History(Base):
    __tablename__ = "moz_places"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    rev_host = Column(String)
    visit_count = Column(Integer)
    hidden = Column(Integer)
    typed = Column(Integer)
    frecency = Column(Integer)
    last_visit_date = Column(Integer)
    guid = Column(Integer)
    foreign_count = Column(Integer)
    url_hash = Column(Integer)
    description = Column(Text)
    preview_image_url = Column(Text)
    site_name = Column(Text)
    origin_id = Column(Integer)

    def __repr__(self):
        return f"History(id={self.id}, url={self.url}, title={self.title})"
