from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from apps.cliente.models import Cliente
from sqlalchemy.orm import relationship
from datetime import datetime
from utils.db.base_sqlalchemy.base import _Base


class TipoMercadoria(_Base):
    __tablename__ = "tipo_mercadoria"

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(100), nullable=False)

    mercadorias = relationship("Mercadoria", back_populates="tipo_mercadoria")


class Mercadoria(_Base):
    __tablename__ = "mercadoria"

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(100), nullable=False)
    numero_registro = Column(Integer, nullable=False)
    fabricante = Column(String(50), nullable=False)
    tipo = Column(Integer, ForeignKey("tipo_mercadoria.id"), nullable=False)

    tipo_mercadoria = relationship("TipoMercadoria", back_populates="mercadorias")


class EntradaMercadoria(_Base):
    __tablename__ = "entrada_mercadoria"

    id = Column(Integer, primary_key=True)
    mercadoria = Column(Integer, ForeignKey("mercadoria.id"), nullable=False)
    unidade = Column(Integer, ForeignKey("unidade.id"), nullable=False)
    data = Column(DateTime, nullable=False, default=datetime.now())
    quantidade = Column(Integer, nullable=False)
    usuario = Column(Integer, ForeignKey("users.id"), nullable=False)

    usuario_rel = relationship("Users", back_populates="entrada_mercadoria")


class SaidaMercadoria(_Base):
    __tablename__ = "saida_mercadoria"

    id = Column(Integer, primary_key=True)
    mercadoria = Column(Integer, ForeignKey("mercadoria.id"), nullable=False)
    unidade_destino = Column(Integer, ForeignKey("unidade.id"), nullable=False)
    unidade_saida = Column(Integer, ForeignKey("unidade.id"), nullable=False)
    entrega = Column(Integer, nullable=False, default=0)
    data = Column(DateTime, nullable=False, default=datetime.now())
    quantidade = Column(Integer, nullable=False)
    usuario = Column(Integer, ForeignKey("users.id"), nullable=False)


class EstoqueMercadoria(_Base):
    __tablename__ = "estoque_mercadoria"

    id = Column(Integer, primary_key=True)
    mercadoria = Column(Integer, ForeignKey("mercadoria.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
