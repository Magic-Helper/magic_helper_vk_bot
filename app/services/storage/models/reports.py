from sqlalchemy import BigInteger, Column, DateTime, Integer, Text
from sqlalchemy.sql import func

from app.services.storage.base_class import Base


class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    author_nickname = Column(Text, nullable=False)
    report_steamid = Column(BigInteger, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False, default=func.now())
    server_number = Column(Integer)
