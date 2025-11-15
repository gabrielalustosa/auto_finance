import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, session
from financeiro import calcular_reserva_emergencia, arredondar_valores, calcular_descontos_salario, ler_csv
from connection.collections import (
    buscar_usuario,
    listar_itens,
    adicionar_item,
    retirar_item,
    salvar_salario,
    buscar_salario,
    criar_usuario
)
from new_user import senha_forte, email_valido
from functools import wraps

from graficos import grafico_pizza_despesas, grafico_despesas_mensais
from settings import CATEGORIAS

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "chave_insegura_dev")

@app.route('/')
def index():
    """Redireciona para a página de login ao acessar a raiz do site."""
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/cadastro', methods=['POST'])
def cadastro():
    username = request.form.get('usuario')
    senha = request.form.get('senha')
    email = request.form.get('email')

    if not username or not senha or not email:
        erro = "Todos os campos são obrigatórios."
    elif not email_valido(email):
        erro = "E-mail inválido."
    elif not senha_forte(senha):
        erro = "Senha fraca. Use pelo menos 8 caracteres, incluindo maiúsculas, minúsculas, números e símbolos."
    elif buscar_usuario(username):
        erro = "Usuário já existe."
    else:
        criar_usuario(username, senha, email)
        return redirect(url_for('login'))

    return render_template('login.html', erro_cadastro=erro)

@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    """
    Adiciona um novo lançamento financeiro (receita ou despesa) para o usuário logado.

    O lançamento é salvo no banco de dados."""

    tipo = request.form.get('tipo')
    descricao = request.form.get('descricao', 'Salário')
    valor = round(float(request.form.get('valor')), 2)
    categoria = request.form.get('categoria', 'Salário')
    data = request.form.get('data', datetime.now().strftime("%d/%m/%Y"))

    adicionar_item(descricao, valor, tipo, categoria, data=data, usuario=session['usuario'])
    print("Dados recebidos:", descricao, valor, tipo, categoria, data, session['usuario'])
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Exibe o formulário de login e autentica o usuário com base nas credenciais fornecidas."""
    erro = None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        usuario_encontrado = buscar_usuario(usuario)

        if usuario_encontrado and senha == usuario_encontrado.get("password"):
            session['usuario'] = usuario_encontrado["username"]
            return redirect(url_for('dashboard'))
        else:
            erro = 'Usuário ou senha inválidos.'

    return render_template('login.html', erro=erro)

@app.route('/salvar_salario', methods=['POST'])
@login_required
def salvar_salario_route():
    """Salva ou atualiza o salário bruto do usuário logado."""
    salario = request.form.get('salario')
    if not salario:
        return redirect(url_for('dashboard'))

    try:
        salario = float(salario)
    except ValueError:
        return redirect(url_for('dashboard'))

    salvar_salario(session['usuario'], salario)
    return redirect(url_for('dashboard'))

def inserir_salario_automatico(username):
    """
    Insere automaticamente o salário do usuário no dia 10 de cada mês,
    caso ainda não tenha sido registrado para o mês atual.

    - Busca o salário bruto do usuário.
    - Verifica se já existe um lançamento de salário no mês.
    - Se não existir e for dia 10, adiciona o lançamento como receita.
    """

    salario = buscar_salario(username)
    if not salario:
        return

    hoje = datetime.now()
    data_str = hoje.strftime("%d/%m/%Y")

    existe = any(
        item for item in listar_itens(username)
        if item["tipo"] == "receita"
        and item["categoria"].lower() == "salário"
        and item["data"].endswith(hoje.strftime("%m/%Y"))
    )

    if not existe and hoje.day == 10:
        adicionar_item("Salário", salario, "receita", "salário", data=data_str, usuario=username)
    

@app.route('/dashboard')
@login_required
def dashboard():
    usuario = session['usuario']
    inserir_salario_automatico(usuario)
    itens = listar_itens(usuario)

    receitas = sum(item['valor'] for item in itens if item['tipo'] == 'receita' and item['categoria'].lower() != "salário")
    despesas = sum(item['valor'] for item in itens if item['tipo'] == 'despesa')

    salario_bruto = buscar_salario(usuario)

    if salario_bruto is not None:
        inss, irrf, salario_liquido = calcular_descontos_salario(salario_bruto)
        receitas += salario_liquido
    else:
        inss = irrf = salario_liquido = 0

    saldo = receitas - despesas
    custo_mensal, meta_reserva = calcular_reserva_emergencia(itens, meses=6)

    dados = {
        "receitas": receitas,
        "despesas": despesas,
        "saldo": saldo,
        "custo_mensal": custo_mensal,
        "meta_reserva": meta_reserva,
        "salario_bruto": salario_bruto,
        "salario_liquido": salario_liquido,
        "inss": inss,
        "irrf": irrf
    }

    dados = arredondar_valores(dados)

    return render_template('home.html', itens=itens, categorias=CATEGORIAS, **dados)

@app.route('/guardar_reserva', methods=['POST'])
@login_required
def guardar_reserva():
    """Registra um valor como despesa na categoria 'Reserva de Emergência'."""
    valor = round(float(request.form['valor']), 2)
    data = datetime.now().strftime("%d/%m/%Y")

    adicionar_item(
        descricao="Reserva de Emergência",
        valor=valor,
        tipo="despesa",
        categoria="Reserva de Emergência",
        data=data,
        usuario=session['usuario']
    )

    return redirect(url_for('dashboard'))

@app.route('/graficos')
@login_required
def graficos():
    """Gera e exibe gráficos financeiros do usuário: despesas por categoria, evolução mensal e composição salarial."""
    usuario = session['usuario']
    itens = listar_itens(usuario)
    grafico_pizza = grafico_pizza_despesas(itens)
    grafico_mensal = grafico_despesas_mensais(itens)

    salario = buscar_salario(usuario)

    if salario is not None:
        inss, irrf, liquido = calcular_descontos_salario(salario)
    else:
        salario = 0
        inss = irrf = liquido = 0

    fig = go.Figure(data=[
        go.Pie(
            labels=["INSS", "IRRF", "Salário Líquido"],
            values=[inss, irrf, liquido],
            textinfo="label+value",
            hoverinfo="label+value"
        )
    ])
    fig.update_layout(title=f"Composição do Salário Bruto (R$ {salario:.2f})")
    grafico_salario = fig.to_html(full_html=False)

    return render_template(
        'graficos.html',
        grafico_pizza=grafico_pizza,
        grafico_salario=grafico_salario,
        grafico_mensal=grafico_mensal,
        salario=salario,
        inss=inss,
        irrf=irrf,
        liquido=liquido
    )

@app.route('/remover/<item_id>', methods=['POST'])
@login_required
def remover(item_id):
    """
    Remove um lançamento financeiro do banco de dados.

    - Recebe o ID do item a ser removido.
    - Chama a função retirar_item para excluir do banco.
    """
    retirar_item(item_id)
    return redirect(url_for('dashboard'))

@app.route("/extrair_csv", methods=["POST"])
@login_required
def rota_extrair_csv():
    """
    Lê um arquivo CSV informado pelo usuário e exibe os dados para categorização.

    - Recebe o caminho do arquivo CSV via formulário.
    - Lê o arquivo usando a função ler_csv.
    - Armazena os dados na sessão para uso posterior.
    - Renderiza a página de categorização com os dados e lista de categorias.
    """
    caminho = request.form.get("caminho_csv")
    try:
        dados = ler_csv(caminho)
        session["dados_csv"] = dados
        return render_template("categorizar.html", dados=dados, categorias=CATEGORIAS)
    except Exception as e:
        return render_template("erro.html", mensagem=str(e))

@app.route("/definir_categorias", methods=["POST"])
@login_required
def salvar_categorias():
    """
    Salva os lançamentos categorizados pelo usuário a partir do CSV importado.

    - Recupera os dados armazenados na sessão.
    - Para cada linha:
        - Permite edição da descrição.
        - Identifica se é receita (valor positivo) ou despesa (valor negativo).
        - Associa a categoria escolhida (somente para despesas).
    - Insere os lançamentos no banco de dados.
    """
    dados = session.get("dados_csv", [])

    for i, linha in enumerate(dados, start=1):
        descricao = request.form.get(f"descricao_{i}", linha["Descrição"])
        
        valor = float(str(linha["Valor"]).replace(",", "."))
        
        if valor >= 0:
            tipo = "receita"
            categoria = "Receita"
        else:
            tipo = "despesa"
            valor = abs(valor)
            categoria = request.form.get(f"categoria_{i}", "Outros")

        adicionar_item(
            descricao=descricao,
            valor=valor,
            tipo=tipo,
            categoria=categoria,
            data=linha["Data"],
            usuario=session['usuario']
        )

    return redirect(url_for("dashboard"))

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Finaliza a sessão do usuário e redireciona para a página de login."""
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

