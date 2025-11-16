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

## Executando localmente (passo a passo)

Estas instruções mostram exatamente o que fazer para rodar o projeto no seu computador Windows (PowerShell). O projeto também está publicado em: https://gabrielalustosa.pythonanywhere.com — você pode acessar essa URL para ver a versão hospedada.

1) Clone o repositório (se ainda não fez):

```powershell
git clone https://github.com/gabrielalustosa/auto_finance.git
cd auto_finance
```

2) Crie e ative um ambiente virtual (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Instale as dependências:

```powershell
pip install -r requirements.txt
```

4) Configurar variáveis de ambiente opcionais (recomendado para comportamento igual ao de produção):

- `SECRET_KEY` — chave secreta do Flask (padrão é usado se não definido, mas é inseguro em produção).
- `DB_PASSWORD` — senha do banco MySQL (se você quiser conectar ao MySQL no PythonAnywhere). Se não definir `DB_PASSWORD`, o projeto usará um banco SQLite local (arquivo `connection/autofinance_local.db`) como fallback para desenvolvimento.

Exemplo (PowerShell):

```powershell
$env:SECRET_KEY = "minha_chave_secreta_local"
# Se tiver senha do MySQL (opcional localmente):
$env:DB_PASSWORD = "SENHA_DO_BANCO"
```

Observações sobre banco de dados:
- Se você pretende usar o MySQL no PythonAnywhere (ou outro servidor MySQL), defina `DB_PASSWORD` com a senha correta antes de iniciar o app. O código criará as tabelas automaticamente com SQLAlchemy (`Base.metadata.create_all(engine)`).
- Se preferir testar localmente sem configurar MySQL, não defina `DB_PASSWORD` — o app criará/usar um arquivo SQLite local automaticamente.

5) Rodar o servidor localmente:

```powershell
python app.py
```

Por padrão o Flask iniciará em http://127.0.0.1:5000 ou http://localhost:5000 — abra essa URL no navegador para acessar a aplicação.

6) Acesso à versão pública hospedada

Se você não quiser rodar localmente, ou para comparar comportamentos, a versão hospedada está disponível em:

```
https://gabrielalustosa.pythonanywhere.com
```

Observação: para que a versão hospedada funcione corretamente com MySQL no PythonAnywhere, você precisa configurar no painel "Web" do PythonAnywhere a variável de ambiente `DB_PASSWORD` e recarregar (Reload) a aplicação.

7) Criar usuário de teste (opção rápida)

- Acesse `http://localhost:5000/cadastro` (ou use o formulário de cadastro disponível na rota `/` que redireciona para `/login`) e crie um usuário para testar login, dashboard e funcionalidades.

Problemas comuns e como depurar

- Internal Server Error (500) ao abrir `/login`:
   - Verifique os logs no PythonAnywhere (Error log) para trace. Localmente, rode `python app.py` e observe o terminal para a stacktrace.
   - Se houver erro de conexão ao banco, confirme que `DB_PASSWORD` está definido quando você espera usar MySQL. Caso contrário, o fallback SQLite evita a falha.
- Erros de templates relacionados a dados: o módulo `connection/collections.py` agora retorna dicionários para `listar_itens` e `buscar_usuario`. Se você editar o código e passar objetos ORM diretamente, mantenha o formato esperado (dict com chaves como `Valor`, `valor`, `Descrição`, `Data`, `categoria`).

Segurança / produção

- Nunca comite senhas no repositório. Use variáveis de ambiente para `SECRET_KEY` e `DB_PASSWORD`.
- Em produção, use um servidor WSGI (gunicorn/uWSGI) e configure logging e variáveis de ambiente no provedor.


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