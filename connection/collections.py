from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["autofinance"] 
users_collection = db["users"]
materiais_collection = db["lancamentos"]

def buscar_usuario(username):

    """Busca um usuário pelo nome de usuário."""

    return users_collection.find_one({"username": username})

def salvar_salario(username, valor):

    """Salva ou atualiza o salário fixo do usuário"""

    users_collection.update_one(
        {"username": username},
        {"$set": {"salario": float(valor)}},
        upsert=True
    )

def buscar_salario(username):

    """Retorna o salário fixo do usuário, se existir"""

    user = users_collection.find_one({"username": username})
    return user.get("salario") if user else None

def adicionar_item(descricao, valor, tipo, categoria, data, usuario):

    """Adiciona um novo lançamento financeiro (Despesas e receitas) vinculado a um usuário."""

    novo_item = {
        "descricao": descricao,
        "valor": valor,
        "tipo": tipo,
        "categoria": categoria,
        "data": data,
        "usuario": usuario
    }

    materiais_collection.insert_one(novo_item)
    return novo_item

def listar_itens(usuario):

    """Lista todos os lançamentos financeiros de um usuário."""

    return list(materiais_collection.find({"usuario": usuario}))

def buscar_item(item_id):

    """Busca um lançamento financeiro pelo seu ID do MongoDB"""

    return materiais_collection.find_one({"_id": ObjectId(item_id)})

def atualizar_item(item_id, novos_dados):

    """Atualiza os dados de um lançamento financeiro existente."""

    return materiais_collection.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": novos_dados},
        return_document=True
    )

def retirar_item(item_id):

    """Remove um lançamento financeiro pelo seu ID."""

    return materiais_collection.delete_one({"_id": ObjectId(item_id)})

def criar_usuario(username, senha, email):

    """Cria um novo usuário no banco de dados."""

    novo_usuario = {
        "username": username,
        "password": senha,
        "email": email,
        "criado_em": datetime.now()
    }
    users_collection.insert_one(novo_usuario)
    return novo_usuario