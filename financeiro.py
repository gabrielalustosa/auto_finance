import os
import pandas as pd
from datetime import datetime

def calcular_reserva_emergencia(itens, meses=3):
    essenciais = [
        i['valor'] for i in itens
        if i['tipo'] == 'despesa'
        and isinstance(i.get('valor'), (int, float))
        and i.get('categoria', '').lower() in ['moradia', 'alimentação', 'transporte', 'saúde', 'educação']
    ]

    meses_distintos = set()
    for i in itens:
        if 'data' in i and i['data']:
            try:
                dt = datetime.strptime(i['data'], "%Y-%m-%d")
            except ValueError:
                try:
                    dt = datetime.strptime(i['data'], "%d/%m/%Y")
                except ValueError:
                    continue 
            meses_distintos.add(dt.strftime("%m/%Y"))

    custo_mensal = sum(essenciais) / max(1, len(meses_distintos))
    meta_reserva = custo_mensal * meses
    return custo_mensal, meta_reserva

def arredondar_valores(dicionario_de_valores, casas=2):
    valores_arredondados = {}
    for nome_do_campo, valor_original in dicionario_de_valores.items():
        if isinstance(valor_original, (int, float)):
            valores_arredondados[nome_do_campo] = round(valor_original, casas)
        else:
            valores_arredondados[nome_do_campo] = valor_original
    return valores_arredondados

def calcular_descontos_salario(salario):
    try:
        salario = float(salario)
    except (TypeError, ValueError):
        return 0, 0, 0

    if salario <= 1320:
        inss = salario * 0.075
    elif salario <= 2571.29:
        inss = salario * 0.09
    elif salario <= 3856.94:
        inss = salario * 0.12
    elif salario <= 7507.49:
        inss = salario * 0.14
    else:
        inss = 7507.49 * 0.14

    base_irrf = salario - inss

    if base_irrf <= 2112:
        irrf = 0
    elif base_irrf <= 2826.65:
        irrf = base_irrf * 0.075 - 158.40
    elif base_irrf <= 3751.05:
        irrf = base_irrf * 0.15 - 370.40
    elif base_irrf <= 4664.68:
        irrf = base_irrf * 0.225 - 651.73
    else:
        irrf = base_irrf * 0.275 - 884.96

    liquido = salario - inss - irrf
    return inss, irrf, liquido

def ler_csv(caminho:str):
    caminho = caminho.strip('"').strip("'")

    caminho_formatado = os.path.normpath(caminho)

    df = pd.read_csv(caminho_formatado)

    df_filtrado = df[["Data", "Descrição", "Valor"]]

    return df_filtrado.to_dict(orient="records")