from sqlalchemy import Column, Integer, String
from utils.db.base_sqlalchemy.base import _Base


class Unidade(_Base):
    __tablename__ = "unidade"

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    uf = Column(String(2), nullable=False)
    endereco = Column(String(50), nullable=False)
