"""
{'id': Column('id', INTEGER(), table=<urls>, primary_key=True), 'url': Column('url', TEXT(), table=<urls>), 'title': Column('title', TEXT(), table=<urls>), 'visit_count': Column('visit_count', INTEGER(), table=<urls>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7fe98fa58df0>, for_update=False)), 'typed_count': Column('typed_count', INTEGER(), table=<urls>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7fe98fa5b250>, for_update=False)), 'last_visit_time': Column('last_visit_time', INTEGER(), table=<urls>, nullable=False), 'hidden': Column('hidden', INTEGER(), table=<urls>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7fe98fa58a90>, for_update=False))}

"""
import sqlalchemy


def get_table(db_path, table_name: str) -> sqlalchemy.Table:
    db_engine = sqlalchemy.create_engine(f"sqlite:///{db_path}", echo=True, future=True)
    with db_engine.connect() as connection:
        metadata = sqlalchemy.MetaData()
        return sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=db_engine)


if __name__ == "__main__":
    # db_paths = (
    # "/home/kshitijchawla/.mozilla/firefox/xac6zxxp.default-release/places (copy).sqlite",
    # "/home/kshitijchawla/.var/app/com.microsoft.Edge/config/microsoft-edge/Default/History",
    # )
    # [get_table(db_path_) for db_path_ in db_paths]

    table = get_table(
        db_path="/home/kshitijchawla/.var/app/com.microsoft.Edge/config/microsoft-edge/Default/History",
        table_name="urls",
        )
