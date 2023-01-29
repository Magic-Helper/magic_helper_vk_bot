from sqlalchemy import BigInteger, Column, DateTime, Integer, Text, UniqueConstraint
from sqlalchemy.sql import func

from app.services.storage.base_class import Base


class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    author_nickname = Column(Text, nullable=False)
    report_steamid = Column(BigInteger, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False, default=func.now())
    server_number = Column(Integer)
    __table_args__ = (UniqueConstraint('author_nickname', 'report_steamid', name='author_nickname_report_steamid_uc'),)
