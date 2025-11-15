import pandas as pd
import plotly.express as px

def grafico_pizza_despesas(itens):
    dados = [
        {
            "categoria": i.get("categoria", "Não especificada"),
            "valor": i.get("valor", 0)
        }
        for i in itens
        if i.get("tipo") == "despesa" and isinstance(i.get("valor"), (int, float))
    ]

    df = pd.DataFrame(dados)

    if df.empty:
        return "<p>Nenhuma despesa registrada.</p>"

    fig = px.pie(
        df,
        names="categoria",
        values="valor",
        title="Distribuição das Despesas por Categoria"
    )
    return fig.to_html(full_html=False)

def grafico_despesas_mensais(itens):
    dados = [
        {
            "data": i.get("data"),
            "valor": i.get("valor")
        }
        for i in itens
        if i.get("tipo") == "despesa"
        and isinstance(i.get("valor"), (int, float))
        and isinstance(i.get("data"), str)
    ]

    df = pd.DataFrame(dados)

    if df.empty:
        return "<p>Nenhuma despesa registrada para gerar gráfico mensal.</p>"

    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
    df.loc[df["data"].isna(), "data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    df = df.dropna(subset=["data"])

    df["mes"] = df["data"].dt.to_period("M").dt.to_timestamp()
    df_mensal = df.groupby("mes")["valor"].sum().reset_index()
    df_mensal["mes_formatado"] = df_mensal["mes"].dt.strftime("%b/%Y")

    fig = px.bar(
        df_mensal,
        x="mes_formatado",
        y="valor",
        title="Despesas Mensais",
        labels={"mes_formatado": "Mês", "valor": "Total de Despesas"},
        text_auto=True,
        color_discrete_sequence=["#dc3545"]
    )

    return fig.to_html(full_html=False)