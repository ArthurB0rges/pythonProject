# Eventos Acadêmicos — Aulas 9 a 15

## Instalação e execução no Windows

### 1. Crie e ative o ambiente virtual

Abra o PowerShell na pasta `meuProjeto`, onde ficam `app.py` e `requirements.txt`. Se o PowerShell abriu na pasta `Desenvolvimento_WebII`, entre no projeto com `cd .\meuProjeto`. Use o Python 3.14, versão usada nos testes do projeto.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Crie o ambiente na primeira configuração. Em um novo terminal, basta ativar a `.venv` existente.

### 2. Instale as bibliotecas

Com a `.venv` ativa, instale o Flask, o Flask-SQLAlchemy e as demais dependências nas versões registradas em [`requirements.txt`](requirements.txt).

```powershell
python -m pip install -r requirements.txt
```

### 3. Inicie o servidor

```powershell
python app.py
```

Abra [http://127.0.0.1:5000](http://127.0.0.1:5000), clique em **Criar conta** e entre com seu e-mail e sua senha. O SQLite cria o arquivo `instance/banco.db` na primeira execução. Para parar o servidor, pressione **Ctrl+C** no terminal.

Se o PowerShell bloquear a execução de `Activate.ps1`, estes comandos usam o Python da `.venv` diretamente.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### 4. Crie uma conta de coordenação para testar a exclusão

Em um segundo PowerShell na pasta `meuProjeto`, execute o comando abaixo com um e-mail diferente do usado na conta comum. O terminal solicita e confirma a senha. Em seguida, entre no site com essa conta.

```powershell
.\.venv\Scripts\python.exe -m flask --app app criar-admin --email coordenacao@exemplo.com
```

## Aula 9 — CRUD de eventos

- [`controller/evento_controller.py`](controller/evento_controller.py) coordena as rotas HTML. `GET /` lista os eventos e `POST /` cadastra um evento. Em `/editar/<id>`, o GET abre o formulário preenchido e o POST salva as mudanças. A rota `/excluir/<id>` recebe POST. Após uma gravação bem-sucedida, o controller redireciona para a listagem. Esse é o padrão Post/Redirect/Get, que evita reenviar a operação ao atualizar a página.
- [`dao/evento_dao.py`](dao/evento_dao.py) concentra as operações `salvar`, `listar`, `buscar_por_id`, `atualizar` e `excluir`. O DAO confirma as gravações com `db.session.commit()`.
- [`templates/index.html`](templates/index.html) apresenta o cadastro, a lista e as ações de cada evento. [`templates/editar.html`](templates/editar.html) reutiliza [`templates/campos_evento.html`](templates/campos_evento.html) para preencher os campos com os valores que o controller buscou pelo ID.

## Aula 10 — Templates, arquivos estáticos e mensagens

- [`templates/base.html`](templates/base.html) define os blocos Jinja `titulo` e `conteudo`. As páginas os reutilizam com `extends`. O `url_for()` gera os endereços das rotas e dos arquivos estáticos, como [`static/style.css`](static/style.css).
- [`templates/index.html`](templates/index.html) usa uma condição Jinja para mostrar a mensagem de lista vazia. [`controller/evento_controller.py`](controller/evento_controller.py) usa `flash()` para enviar avisos de sucesso e erro. A base mostra e consome esses avisos com `get_flashed_messages()`.

## Aula 11 — Revisão das camadas e da persistência

O guia de revisão acompanha o caminho da requisição. Na edição de um evento, [`evento_controller.py`](controller/evento_controller.py) recebe o ID da URL e pede o registro ao [`EventoDAO`](dao/evento_dao.py). O DAO consulta o modelo [`Evento`](model/evento.py) usando o SQLAlchemy configurado em [`extensions.py`](extensions.py). O controller repassa os dados para [`editar.html`](templates/editar.html). Ao salvar, o caminho volta do formulário ao controller e ao DAO, que confirma a alteração no SQLite.

## Aula 12 — Sessão, cookie e escopos de memória

| Conceito | Onde se aplica |
| --- | --- |
| Sessão | [`auth_controller.py`](controller/auth_controller.py) grava o nome do usuário no login e limpa a sessão na saída. [`evento_controller.py`](controller/evento_controller.py) incrementa `session["visitas"]` em cada GET da página inicial. |
| Escopo da aplicação | [`app.py`](app.py) inicializa o contador compartilhado. [`evento_controller.py`](controller/evento_controller.py) incrementa o total para todos os visitantes até o processo reiniciar. |
| Cookie de preferência | A rota `POST /preferencia` grava `exibicao` por 30 dias. [`index.html`](templates/index.html) usa essa escolha para mostrar ou ocultar local e vagas. |
| Escopo da requisição | Os dados recebidos do formulário em `index()` e `editar()` são variáveis locais, usadas durante o processamento de cada pedido. |

## Aula 13 — Autenticação e autorização

- O [modelo `Usuario`](model/usuario.py) guarda o e-mail único, o hash da senha e o perfil. O [`UsuarioDAO`](dao/usuario_dao.py) busca o usuário pelo e-mail e grava a conta.
- [`auth_controller.py`](controller/auth_controller.py) usa `generate_password_hash()` no cadastro e `check_password_hash()` no login. O [formulário de cadastro](templates/cadastro.html) e o [JavaScript](static/script.js) avisam sobre o comprimento mínimo da senha. O servidor também aplica a validação.
- Em [`evento_controller.py`](controller/evento_controller.py), `before_request` redireciona para `/login` quando a sessão não identifica um usuário. A rota de exclusão exige o perfil `admin`, e a listagem verifica esse mesmo perfil para exibir o botão **Excluir**. O cadastro público cria contas de perfil `comum`. O comando `criar-admin`, implementado no controller de autenticação, cria uma conta de coordenação para testar a permissão.

## Aula 14 — AJAX com Fetch e JSON

- Em [`model/evento.py`](model/evento.py), `para_dicionario()` reúne os campos do evento. [`api_controller.py`](controller/api_controller.py) usa `jsonify()` para enviar esses dados em respostas JSON.
- [`static/script.js`](static/script.js) usa `fetch()` com GET para atualizar a lista. No cadastro, `preventDefault()` intercepta o envio, o script envia um POST com JSON e insere na lista o evento devolvido pelo servidor. [`templates/index.html`](templates/index.html) fornece o formulário, o modelo de item e a área de feedback.
- [`controller/dados_evento.py`](controller/dados_evento.py) valida os campos tanto no fluxo HTML quanto no JSON. Com JavaScript desativado, o formulário continua enviando POST para a rota HTML da Aula 9. No fluxo com `fetch()`, a página distingue uma recusa HTTP de uma falha de comunicação.

## Aula 15 — API REST

[`controller/api_controller.py`](controller/api_controller.py) define os recursos no Blueprint com prefixo `/api`, registrado em [`app.py`](app.py). A API e as rotas HTML compartilham o [`EventoDAO`](dao/evento_dao.py).

| Método | Endereço | Operação | Sucesso | Recusas |
| --- | --- | --- | --- | --- |
| `GET` | `/api/eventos` | Listar eventos | `200` | `401` |
| `GET` | `/api/eventos/<id>` | Consultar um evento | `200` | `401`, `404` |
| `POST` | `/api/eventos` | Criar um evento | `201` | `400`, `401`, `415` |
| `PUT` | `/api/eventos/<id>` | Substituir os campos de um evento | `200` | `400`, `401`, `404`, `415` |
| `DELETE` | `/api/eventos/<id>` | Excluir um evento como coordenação | `204` | `401`, `403`, `404` |

- O `before_request` da API usa a sessão e responde `401` quando falta autenticação. A tentativa de exclusão com perfil comum recebe `403`. O tratamento em [`app.py`](app.py) mantém o status e devolve as recusas em `{"erro": "mensagem"}`. O [JavaScript](static/script.js) verifica `resposta.ok` e apresenta a mensagem recebida.
- POST e PUT recebem um objeto JSON com `nome` e `data` no formato `AAAA-MM-DD`. `local` e `vagas` são opcionais e assumem texto vazio e zero quando omitidos. O POST devolve o endereço do novo evento no cabeçalho `Location`. Repetir o mesmo PUT mantém o mesmo estado. O DELETE bem-sucedido devolve `204` com corpo vazio.
