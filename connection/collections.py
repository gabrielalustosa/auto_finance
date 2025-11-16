import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração de conexão: tenta MySQL (PythonAnywhere) quando DB_PASSWORD estiver presente,
# caso contrário usa um SQLite local como fallback para desenvolvimento.
usuario = "gabrielalustosa"
senha = os.environ.get("DB_PASSWORD")
host = f"{usuario}.mysql.pythonanywhere-services.com"
banco = f"{usuario}$autofinance"

if senha:
    DATABASE_URL = f"mysql+pymysql://{usuario}:{senha}@{host}/{banco}"
    engine = create_engine(DATABASE_URL, echo=False)
else:
    # Fallback para sqlite local para evitar falha na importação quando a variável de ambiente
    # DB_PASSWORD não estiver definida (útil ao rodar localmente ou em ambientes sem DB configurado).
    sqlite_path = os.path.join(os.path.dirname(__file__), "autofinance_local.db")
    DATABASE_URL = f"sqlite:///{sqlite_path}"
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

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

def _user_to_dict(user):
    if not user:
        return None
    return {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "email": user.email,
        "salario": user.salario
    }


def buscar_usuario(username):
    """Busca um usuário pelo nome de usuário e retorna um dicionário (ou None).

    Retornar um dict facilita o uso em templates e funções que esperam acesso via .get().
    """
    user = session.query(User).filter_by(username=username).first()
    return _user_to_dict(user)

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
    return float(user.salario) if user and user.salario is not None else None

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

def _lancamento_to_dict(item):
    if not item:
        return None
    # formata data como string dd/mm/YYYY se for datetime
    data_val = item.data
    if isinstance(data_val, datetime):
        data_str = data_val.strftime("%d/%m/%Y")
    else:
        data_str = str(data_val) if data_val is not None else datetime.now().strftime("%d/%m/%Y")

    return {
        "id": item.id,
        "Descrição": item.descricao,
        "descricao": item.descricao,
        "valor": float(item.valor) if item.valor is not None else 0.0,
        "Valor": f"{item.valor:.2f}" if isinstance(item.valor, (int, float)) else str(item.valor),
        "tipo": item.tipo,
        "categoria": item.categoria,
        "Categoria": item.categoria,
        "data": data_str,
        "Data": data_str,
        "usuario": item.usuario
    }


def listar_itens(usuario):
    """Retorna uma lista de dicionários representando lançamentos do usuário.

    Isso mantém compatibilidade com as funções que esperam iteráveis de dicts (como `graficos.py`).
    """
    rows = session.query(Lancamento).filter_by(usuario=usuario).all()
    return [_lancamento_to_dict(r) for r in rows]

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
