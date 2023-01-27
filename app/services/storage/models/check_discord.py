from sqlalchemy import BigInteger, Column, ForeignKey, Integer, UniqueConstraint

from app.services.storage.base_class import Base


class CheckDiscord(Base):
    id = Column(Integer, primary_key=True, index=True)
    check_id = Column(Integer, ForeignKey('checks.id'), nullable=False)
    discord_id = Column(BigInteger, nullable=False)
    __table_args__ = (UniqueConstraint('check_id', 'discord_id', name='check_discord_uc'),)
