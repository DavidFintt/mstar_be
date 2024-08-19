from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.db.base_sqlalchemy.base import _Base


class Cliente(_Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    primeiro_nome = Column(String(20), nullable=False)
    ultimo_nome = Column(String(20), nullable=False)
    cpf = Column(String(11), nullable=False)
    telefone = Column(String(11), nullable=False)
    email = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    uf = Column(String(2), nullable=False)
    endereco = Column(String(50), nullable=False)
    cep = Column(String(8), nullable=False)
