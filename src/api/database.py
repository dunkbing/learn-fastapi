import math
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, Query
from sqlalchemy_searchable import make_searchable, search
from sqlalchemy_filters import apply_pagination, apply_sort, apply_filters
from .config import settings

# DATABASE_URL = "sqlite:///./sql_app.db"
# DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/admin"
DATABASE_URL = f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_class_by_tablename(table_fullname: str):
    for c in Base._decl_class_registry.values():
        if hasattr(c, "__table__"):
            if c.__table__.fullname.lower() == table_fullname.lower():
                return c

    raise Exception(f"Incorrect tablename {table_fullname}")


def create_filter_spec(model, fields, ops, values):
    if fields and ops and values:
        return [{"model": model, "field": field, "op": op, "value": value} for field, op, value in zip(fields, ops, values)]

    return []


def create_sort_spec(model, sort_by, descending):
    if sort_by and descending:
        return [{"model": model, "field": field, "direction": "desc" if direction else "asc"} for field, direction in zip(sort_by, descending)]

    return []


def join_required_attrs(query: Query, model, join_attrs) -> Query:
    if not join_attrs:
        return query

    for attr in join_attrs:
        query = query.join(getattr(model, attr))

    return query


def find_items(
    db_session: Session,
    model: str,
    query_str: str = None,
    page: int = 1,
    items_per_page: int = 10,
    sort_by: list[str] = None,
    descending: list[bool] = None,
    fields: list[str] = None,
    ops: list[str] = None,
    values: list[str] = None,
    join_attrs: list[str] = None,
):
    model_cls = get_class_by_tablename(model)

    query = db_session.query(model_cls)

    if query_str:
        query = search(query, query_str)

    query = join_required_attrs(query, model_cls, join_attrs)

    filter_spec = create_filter_spec(model, fields, ops, values)
    query = apply_filters(query, filter_spec)

    sort_spec = create_sort_spec(model, sort_by, descending)
    query = apply_sort(query, sort_spec)

    query, pagination = apply_pagination(
        query, page_number=page, page_size=items_per_page
    )

    page_size, page_number, num_pages, total_results = pagination

    total_page = 1
    if items_per_page:
        total_page = math.ceil(total_results / items_per_page)
    next_page = -1
    if page:
        next_page = page + 1 if page < total_page else -1
    has_more = False if next_page == -1 else True

    return {
        "object": model,
        "total_item": pagination.total_results,
        "total_page": total_page,
        "has_more": has_more,
        "next_page": next_page,
        "data": query.all(),
    }
