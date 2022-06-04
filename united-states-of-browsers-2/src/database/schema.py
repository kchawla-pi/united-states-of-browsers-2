from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import declarative_base

from value_objects import ProductName

Base = declarative_base()


class HistorySchema(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    visit_count = Column(Integer)

    def __repr__(self):
        return f"History(id={self.id}, url={self.url}, title={self.title})"


class FirefoxHistorySchema(HistorySchema):
    __tablename__ = "moz_places"

    hidden = Column(Integer)
    rev_host = Column(String)
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


class ChromiumHistorySchema(HistorySchema):
    __tablename__ = "urls"
    hidden = Column(Integer)
    last_visit_time = Column(Integer)
    typed_count = Column(Integer)


SchemaOptions = {
    ProductName.FIREFOX: FirefoxHistorySchema,
    ProductName.EDGE: ChromiumHistorySchema,
    ProductName.CHROME: ChromiumHistorySchema
    }


class MergedHistorySchema(HistorySchema):
    __tablename__ = "history"

"""
{
'id': Column('id', INTEGER(), table=<urls>, primary_key=True),
'url': Column('url', TEXT(), table=<urls>),
'title': Column('title', TEXT(), table=<urls>),
'visit_count': Column('visit_count', INTEGER(), table=<urls>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7fe98fa58df0>, for_update=False)),
'typed_count': Column('typed_count', INTEGER(), table=<urls>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7fe98fa5b250>, for_update=False)),
'last_visit_time': Column('last_visit_time', INTEGER(), table=<urls>, nullable=False),
'hidden': Column('hidden', INTEGER(), table=<urls>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7fe98fa58a90>, for_update=False)),
}
"""
