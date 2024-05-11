from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN, DOUBLE, DATETIME
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///BD.db')
Base = declarative_base()
class clsPozos_PP(Base):
    __tablename__ = 'tblPozos_PP'
    id = Column(Integer, primary_key=True)
    Baja = Column(BOOLEAN)
    Pozo = Column(String)
    Pozo_Tipo = Column(String)
    Fecha_Fin = Column(DATETIME)
    Equipo = Column(String)
    Estado = Column(String)
    Cert_Op = Column(DOUBLE)


class clsPozos_TE(Base):
    __tablename__ = 'tblPozos_TE'
    id = Column(Integer, primary_key=True)
    Baja = Column(BOOLEAN)
    Pozo = Column(String)
    Pozo_Tipo = Column(String)
    Fecha_Fin = Column(DATETIME)
    Equipo = Column(String)
    Estado = Column(String)
    Cert_Op = Column(DOUBLE)

Base.metadata.create_all(engine)

