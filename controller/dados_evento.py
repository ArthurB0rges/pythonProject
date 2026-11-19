from datetime import date
import re


# Aulas 9, 14 e 15 — A validação no servidor atende tanto o formulário HTML quanto o corpo JSON.
def validar_evento(dados, *, formulario=False):
    nome = dados.get("nome")
    data = dados.get("data")
    local = dados.get("local", "")
    vagas = dados.get("vagas", "" if formulario else 0)

    if not isinstance(nome, str) or not nome.strip() or len(nome.strip()) > 120:
        raise ValueError("Informe um nome com até 120 caracteres.")

    if not isinstance(data, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", data):
        raise ValueError("Informe uma data válida no formato AAAA-MM-DD.")
    try:
        date.fromisoformat(data)
    except ValueError:
        raise ValueError("Informe uma data válida.") from None

    if not isinstance(local, str) or len(local.strip()) > 120:
        raise ValueError("O local deve ser um texto de até 120 caracteres.")
    if formulario and not local.strip():
        raise ValueError("Informe o local do evento.")

    # Aula 14 — O formulário envia texto. No JSON, vagas deve chegar como número inteiro.
    if formulario and isinstance(vagas, str) and re.fullmatch(r"[0-9]{1,19}", vagas):
        vagas = int(vagas)
    if type(vagas) is not int or not 0 <= vagas <= 2**63 - 1:
        raise ValueError("Informe uma quantidade válida de vagas (inteiro a partir de zero).")

    return {"nome": nome.strip(), "data": data, "local": local.strip(), "vagas": vagas}
