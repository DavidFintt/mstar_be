from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import UUIDType
from utils.db.base_sqlalchemy.base import _Base
from sqlalchemy.orm import relationship
import uuid


class Users(_Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    primeiro_nome = Column(String(20), nullable=False)
    ultimo_nome = Column(String(20), nullable=False)
    is_admin = Column(Integer, nullable=False, default=0)
    is_active = Column(Integer, nullable=False, default=1)

    entrada_mercadoria = relationship("EntradaMercadoria", back_populates="usuario_rel")
