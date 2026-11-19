// Aula 13 — Valida o comprimento da senha no navegador antes de enviar o formulário.
const formCadastro = document.getElementById("form-cadastro");
if (formCadastro) {
    const senha = formCadastro.elements.senha;
    senha.addEventListener("input", function () {
        const curta = senha.value.length > 0 && senha.value.length < 6;
        senha.setCustomValidity(curta ? "Use pelo menos 6 caracteres." : "");
    });
}

// Aula 14 — Localiza o formulário e a lista que serão atualizados sem recarregar a página.
const formEvento = document.getElementById("form-evento");
if (formEvento) {
    const atualizar = document.getElementById("atualizar-lista");
    const cadastrar = formEvento.querySelector("button");
    const lista = document.getElementById("lista-eventos");
    const listaVazia = document.getElementById("lista-vazia");
    const modelo = document.getElementById("item-evento");
    const feedback = document.getElementById("feedback-eventos");

    function mostrarFeedback(mensagem, erro = false) {
        feedback.className = erro ? "mensagem erro" : "mensagem sucesso";
        feedback.textContent = mensagem;
    }

    // Aula 14 — Clona o item definido no template e insere o conteúdo recebido como texto.
    function criarItem(evento) {
        const item = modelo.content.firstElementChild.cloneNode(true);
        item.querySelector('[data-campo="nome"]').textContent = evento.nome;
        const data = item.querySelector("time");
        data.dateTime = evento.data;
        data.textContent = evento.data;

        const local = item.querySelector('[data-campo="local"]');
        if (local) {
            local.textContent = evento.local || "Local a definir";
            item.querySelector('[data-campo="vagas"]').textContent = evento.vagas + " vagas";
        }

        // Aulas 9 e 14 — Substitui o ID provisório pelos dados recebidos da API.
        const editar = item.querySelector("a");
        editar.href = editar.getAttribute("href").replace(/0$/, evento.id);
        const excluir = item.querySelector("form");
        if (excluir) {
            excluir.action = excluir.getAttribute("action").replace(/0$/, evento.id);
        }
        return item;
    }

    // Aulas 14 e 15 — Faz a requisição e trata separadamente problemas de comunicação e respostas de erro.
    async function pedirEventos(opcoes, aoReceber) {
        atualizar.disabled = cadastrar.disabled = true;
        feedback.className = "meta";
        feedback.textContent = "Aguarde…";
        try {
            const resposta = await fetch(formEvento.dataset.api, opcoes);
            const dados = await resposta.json().catch(() => null);
            // Aula 15 — A API responde com status HTTP e uma mensagem JSON, inclusive quando falta login.
            if (!resposta.ok) {
                mostrarFeedback(dados?.erro || "O servidor recusou o pedido (" + resposta.status + ").", true);
                return;
            }
            if (dados === null) {
                mostrarFeedback("O servidor retornou uma resposta inválida.", true);
                return;
            }
            aoReceber(dados);
            listaVazia.hidden = lista.childElementCount !== 0;
        } catch {
            mostrarFeedback("Não foi possível concluir a operação. Atualize a lista para conferir os eventos.", true);
        } finally {
            atualizar.disabled = cadastrar.disabled = false;
        }
    }

    // Aula 14 — O botão aparece com JavaScript e usa GET para redesenhar a lista.
    atualizar.hidden = false;
    atualizar.addEventListener("click", function () {
        pedirEventos({}, function (eventos) {
            lista.replaceChildren(...eventos.map(criarItem));
            mostrarFeedback("Lista atualizada.");
        });
    });

    // Aula 14 — Intercepta o POST HTML, envia JSON à API e inclui o novo evento na lista.
    formEvento.addEventListener("submit", function (evento) {
        evento.preventDefault();
        const campos = formEvento.elements;
        const dados = {
            nome: campos.nome.value,
            data: campos.data.value,
            local: campos.local.value,
            vagas: campos.vagas.valueAsNumber,
        };
        pedirEventos({
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(dados),
        }, function (criado) {
            lista.append(criarItem(criado));
            formEvento.reset();
            mostrarFeedback("Evento cadastrado.");
        });
    });
}
