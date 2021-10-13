from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.util.concurrency import asynccontextmanager

engine = create_async_engine(
    "sqlite+aiosqlite:///db.sqlite3",
    future=True,
)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine, class_=AsyncSession)


@asynccontextmanager
async def get_session():
    async with Session() as session:
        yield session
