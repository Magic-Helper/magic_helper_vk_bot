from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer

from app.services.storage.base_class import Base

TIMEZONE = 'Europe/Moscow'


class Check(Base):
    id = Column(Integer, primary_key=True, index=True)
    steamid = Column(BigInteger, nullable=False)
    moder_vk = Column(BigInteger, nullable=False)
    start_time = Column(DateTime(TIMEZONE), nullable=False)
    end_time = Column(DateTime(TIMEZONE), nullable=True)
    server_number = Column(Integer, nullable=True)
    is_ban = Column(Boolean, nullable=False, default=False)
