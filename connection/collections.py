import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

usuario = "gabrielalustosa"
senha = os.environ.get("DB_PASSWORD")
host = f"{usuario}.mysql.pythonanywhere-services.com"
banco = f"{usuario}$autofinance"

engine = create_engine(f"mysql+pymysql://{usuario}:{senha}@{host}/{banco}", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(200))
    email = Column(String(200))
    salario = Column(Float)
    criado_em = Column(DateTime, default=datetime.now)


class Lancamento(Base):
    __tablename__ = 'lancamentos'
    id = Column(Integer, primary_key=True)
    descricao = Column(String(200))
    valor = Column(Float)
    tipo = Column(String(50))
    categoria = Column(String(100))
    data = Column(DateTime)
    usuario = Column(String(100))


Base.metadata.create_all(engine)

def buscar_usuario(username):
    return session.query(User).filter_by(username=username).first()

def salvar_salario(username, valor):
    user = session.query(User).filter_by(username=username).first()
    if user:
        user.salario = float(valor)
        session.commit()
    else:
        novo_user = User(username=username, salario=float(valor))
        session.add(novo_user)
        session.commit()

def buscar_salario(username):
    user = session.query(User).filter_by(username=username).first()
    return user.salario if user else None

def adicionar_item(descricao, valor, tipo, categoria, data, usuario):
    if isinstance(data, str):
        try:
            data = datetime.strptime(data, "%d/%m/%Y")
        except Exception:
            data = datetime.now()

    novo_item = Lancamento(
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        categoria=categoria,
        data=data,
        usuario=usuario
    )
    session.add(novo_item)
    session.commit()
    return novo_item

def listar_itens(usuario):
    return session.query(Lancamento).filter_by(usuario=usuario).all()

def buscar_item(item_id):
    return session.query(Lancamento).filter_by(id=item_id).first()

def atualizar_item(item_id, novos_dados):
    item = session.query(Lancamento).filter_by(id=item_id).first()
    if item:
        for chave, valor in novos_dados.items():
            setattr(item, chave, valor)
        session.commit()
    return item

def retirar_item(item_id):
    item = session.query(Lancamento).filter_by(id=item_id).first()
    if item:
        session.delete(item)
        session.commit()
        return True
    return False

def criar_usuario(username, senha, email):
    novo_usuario = User(
        username=username,
        password=senha,
        email=email,
        criado_em=datetime.now()
    )
    session.add(novo_usuario)
    session.commit()
    return novo_usuario
