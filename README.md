# AUTOFINANCE

## Objetivo

Este sistema de gestão financeira pessoal tem como principal objetivo facilitar a compreensão do seu dinheiro de forma visual e intuitiva. Ao registrar suas receitas e despesas, você consegue enxergar com mais clareza para onde está indo cada centavo e de onde ele vem, o que torna muito mais fácil tomar decisões conscientes sobre seus gastos. Além disso, ele ajuda a construir uma reserva de emergência baseada na sua realidade: com os dados que você inscreve na plataforma, o sistema calcula quanto seria necessário para você sobreviver por até três meses cobrindo apenas os gastos essenciais. Os gráficos gerados pelo app tornam tudo mais didático, revelando padrões de consumo, comparando meses e destacando categorias que mais pesam no seu orçamento. Com essa organização, você deixa de apenas reagir aos imprevistos e passa a se planejar com segurança e autonomia.

## Requisitos

- Python < 3.12 (ver `runtime.txt` para versão alvo de runtime).
- Recomenda-se criar um ambiente virtual.

## Instalação rápida

1. Crie e ative um ambiente virtual:

   Windows (PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

2. Instale dependências:

   ```powershell
   pip install -r requirements.txt
   ```

3. Execute a aplicação/script de entrada desejado (exemplo):

   ```powershell
   python app.py
   ```

## Estrutura do projeto (resumida)

- `auto_finance/` — pacote principal
# auto_finance

Projeto: auto_finance — automação financeira, processamento de dados e geração de gráficos

Visão geral
------------
`auto_finance` é um conjunto de scripts e um pacote Python desenvolvidos para automatizar tarefas financeiras rotineiras, transformar dados em relatórios e visualizações e oferecer interfaces simples para revisão e categorização de gastos. O projeto centraliza utilitários, componentes e fluxos de trabalho que ajudam a organizar finanças pessoais e a entender melhor hábitos de consumo.

Motivação pessoal
------------------
Hoje eu trabalho como desenvolvedora no Sicredi. No passado eu não tinha noção do quão importante é ter uma vida financeira organizada: eu costumava parcelar tudo no máximo de vezes possível, não investia e não mantinha uma reserva de emergência. Durante este semestre, quando precisei finalizar meu TCC, fiquei sem notebook — foi a reserva financeira que me salvou naquele momento. Além disso, a vida traz imprevistos (doenças, emergências, despesas inesperadas) e ter uma estrutura financeira minimamente organizada ajuda a lidar com essas situações.

Como pessoa neurodivergente, percebi que visualizar dados em gráficos facilita muito o entendimento para mim. Por isso, decidi incorporar visualizações no projeto: gráficos tornam padrões (gastos por categoria, evolução de saldo, proporção de despesas) mais fáceis de interpretar do que listas brutas de números. Essa é a motivação que guiou o desenho das funcionalidades deste repositório — torná-lo útil para quem precisa de ferramentas práticas e visuais para cuidar do próprio dinheiro.

Principais funcionalidades
------------------------
- Importação e processamento de dados financeiros (planilhas, CSVs ou entradas manuais).
- Categorização de transações (página de revisão/categorização com interface simples em HTML).
- Geração de gráficos/visualizações para monitoramento (módulo `graficos.py`).
- Scripts utilitários para operações recorrentes (`financeiro.py`, `new_user.py`).
- Pacote modular em `auto_finance/` com componentes, contexts e helpers para reutilização.

Conteúdo do repositório (resumido)
----------------------------------
- `app.py` — ponto de entrada (quando o sistema é executado como aplicação/web).
- `financeiro.py` — rotinas para processamento de transações e regras de negócio.
- `graficos.py` — funções para gerar gráficos (matplotlib/plotly/etc., conforme dependências).
- `new_user.py` — utilitários para criação e validação de usuários/contas.
- `auto_finance/` — pacote principal com:
   - `core/` — constantes e regras centrais
   - `components/` — componentes reutilizáveis
   - `contexts/` — controladores de fluxo
   - `models/` — modelos de dados e steps
   - `tools/` — utilitários e exceções
- `connection/` — coleções e validações auxiliares
- `templates/`, `static/` — páginas HTML e ativos estáticos (UI básica)
- `requirements.txt` — dependências do projeto
- `Procfile`, `runtime.txt` — indicativos para deploy em plataformas compatíveis

Requisitos
----------
- Python 3.10+ (ver `runtime.txt` para a versão alvo).
- Recomenda-se criar um ambiente virtual antes de instalar dependências.

Instalação
---------
1. Crie e ative um ambiente virtual (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale dependências:

```powershell
pip install -r requirements.txt
```

3. Execute o script ou app desejado (ex.: abrir a interface de categorização):

```powershell
python app.py
```

Uso e exemplos rápidos
----------------------
- Categorização: abra a rota que apresenta `templates/categorizar.html` para revisar e atribuir categorias às transações. A interface permite editar descrições e selecionar categorias antes de salvar.
- Gráficos: rode `graficos.py` (ou invoque as funções correspondentes) para gerar visualizações como:
   - Gastos por categoria (pizza/barras)
   - Evolução de saldo por período (linha)
   - Distribuição de despesas (histograma)

Arquitetura e fluxo
-------------------
1. Entrada de dados: arquivos CSV, planilhas, ou inputs manuais são normalizados pelas rotinas em `financeiro.py`.
2. Processamento: regras de negócio em `auto_finance/core` e `models` transformam os dados e preparam para exibição.
3. Revisão/Categorização: templates em `templates/` (p.ex. `categorizar.html`) apresentam uma UI leve para revisar transações e atribuir categorias.
4. Visualização: `graficos.py` consome os dados processados e gera imagens/arquivos que podem ser salvos em `static/` ou exibidos via templates.

Agradecimentos e nota pessoal
----------------------------
Este projeto nasceu da vontade de transformar uma necessidade real em ferramenta prática e visual. Minha experiência pessoal — aprender a importância da reserva de emergência, usar a própria reserva para honrar compromissos acadêmicos e reconhecer como visualizações ajudam no entendimento — foi o que motivou o desenvolvimento. Se você também prefere ver números representados graficamente, este projeto tenta facilitar exatamente isso: tornar o cuidado financeiro mais acessível, previsível e visualmente compreensível.