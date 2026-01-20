// ===============================
// FUNÇÕES DE VALIDAÇÃO
// ===============================

// Exibir erro ACIMA do input
function mostrarErro(input, mensagem) {
  removerErro(input);
  const span = document.createElement("span");
  span.classList.add("erro-input");
  span.textContent = mensagem;
  input.insertAdjacentElement("beforebegin", span);
}

// Remover erro ao corrigir
function removerErro(input) {
  if (input.previousElementSibling && input.previousElementSibling.classList.contains("erro-input")) {
    input.previousElementSibling.remove();
  }
}

// Validar email
function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// Validar senha (maiúscula, minúscula, número, caractere especial)
function validarSenha(senha) {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{6,}$/;
  return regex.test(senha);
}

// Validar CPF real
function validarCPF(cpf) {
  cpf = cpf.replace(/\D/g, "");
  if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

  let soma = 0, resto;

  for (let i = 1; i <= 9; i++)
    soma += parseInt(cpf[i - 1]) * (11 - i);
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf[9])) return false;

  soma = 0;
  for (let i = 1; i <= 10; i++)
    soma += parseInt(cpf[i - 1]) * (12 - i);
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;

  return resto === parseInt(cpf[10]);
}

// Validar telefone
function validarTelefone(tel) {
  tel = tel.replace(/\D/g, "");
  return tel.length === 11;
}

// Validar CEP
function validarCEP(cep) {
  cep = cep.replace(/\D/g, "");
  return cep.length === 8;
}

// ===============================
// CONTROLE DO FORM STEPS
// ===============================
$(function () {

  // ---- BOTÃO NEXT COM VALIDAÇÕES ---- //
  $(".next").off("click").on("click", function () {

    let current_fs = $(this).closest("fieldset");
    let valid = true;

    // Todos inputs deste step
    current_fs.find("input, select, textarea").each(function () {
      removerErro(this);

      // Campo vazio
      if (this.value.trim() === "") {
        mostrarErro(this, "Este campo é obrigatório.");
        valid = false;
      }

      // Email
      if (this.name === "email" && this.value !== "" && !validarEmail(this.value)) {
        mostrarErro(this, "Email inválido.");
        valid = false;
      }

      // Senha (regras)
      if (this.name === "pass") {
        if (!validarSenha(this.value)) {
          mostrarErro(this,
            "A senha deve ter: letra maiúscula, minúscula, número e caractere especial."
          );
          valid = false;
        }
      }

      // Confirmar senha
      if (this.name === "cpass") {
        let senha = current_fs.find("input[name='pass']").val();
        if (this.value !== senha) {
          mostrarErro(this, "As senhas não coincidem.");
          valid = false;
        }
      }

      // CPF
      if (this.name === "cpf" && this.value !== "" && !validarCPF(this.value)) {
        mostrarErro(this, "CPF inválido.");
        valid = false;
      }

      // Telefone
      if (this.name === "phone" && this.value !== "" && !validarTelefone(this.value)) {
        mostrarErro(this, "Telefone inválido.");
        valid = false;
      }

      // CEP
      if (this.name === "cep" && this.value !== "" && !validarCEP(this.value)) {
        mostrarErro(this, "CEP inválido.");
        valid = false;
      }

    });

    if (!valid) return; // impede avanço

    // ---- AVANÇAR SE TUDO OK ---- //
    let next_fs = current_fs.next("fieldset");
    current_fs.hide();
    next_fs.show();

    $("#progressbar li").removeClass("active");
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
  });


  // ---- BOTÃO PREVIOUS ---- //
  $(".previous").off("click").on("click", function () {
    var current_fs = $(this).closest("fieldset");
    var prev_fs = current_fs.prev("fieldset");

    current_fs.hide();
    prev_fs.show();

    $("#progressbar li").removeClass("active");
    $("#progressbar li").eq($("fieldset").index(prev_fs)).addClass("active");
  });


  // Máscara CPF
  document.getElementById("cpf").addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, "");
    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    e.target.value = value;
  });

});

// ===============================
// MÁSCARAS (Telefone e CEP)
// ===============================
function mascaraTelefone(campo) {
  let v = campo.value.replace(/\D/g, "");
  if (v.length > 11) v = v.slice(0, 11);

  let formatted = "";
  if (v.length > 0) formatted = "(" + v.substring(0, 2);
  if (v.length >= 3) formatted += ")" + v.substring(2, 7);
  if (v.length >= 8) formatted += "-" + v.substring(7, 11);

  campo.value = formatted;
}

function mascaraCEP(campo) {
  let v = campo.value.replace(/\D/g, "");
  if (v.length > 8) v = v.slice(0, 8);

  campo.value = v.length > 5 ? v.slice(0, 5) + "-" + v.slice(5) : v;
}

// ===============================
// VOLTAR DO PRIMEIRO PASSO → HOME
// ===============================
$(document).on("click", ".btn-voltar-home", function () {
  window.location.href = "../index.html";
});

// ===============================
// ENVIO DO FORMULÁRIO (SEM REDIRECIONAR)
// ===============================
$("#msform").on("submit", function () {
  // NÃO usa preventDefault!
  // A página recarrega e os dados aparecem via GET
});

// ===============================
// MENSAGEM DE SUCESSO AO ENVIAR
// ===============================
$("#msform").on("submit", function () {
  alert("Cadastro realizado com sucesso!");
});

// ===============================
// SALVAR USUÁRIO NO LOCALSTORAGE
// ===============================
$("#msform").on("submit", function (event) {
    
    // pega todos os valores do form
    const usuario = {
        username: $("input[name='user']").val(),
        email: $("input[name='email']").val(),
        senha: $("input[name='pass']").val(),
        estado: $("#UF").val(),
        cidade: $("input[name='cidade']").val(),
        cep: $("input[name='cep']").val(),
        endereco: $("textarea[name='endereco']").val(),
        cpf: $("input[name='cpf']").val(),
        nomeCompleto: $("input[name='Nome_C']").val(),
        telefone: $("input[name='phone']").val()
    };

    // salva no LocalStorage
    localStorage.setItem("usuario", JSON.stringify(usuario));

    // o seu alert atual
    alert("Cadastro realizado com sucesso!");

    // deixa o redirecionamento do HTML funcionar normalmente
});


