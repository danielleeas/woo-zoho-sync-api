from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
from typing import AsyncGenerator
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": ssl_context
    }
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
        