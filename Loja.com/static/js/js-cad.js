// ===============================
// FUNÇÕES DE ERRO
// ===============================
function mostrarErro(input, mensagem) {
  removerErro(input);
  const span = document.createElement("span");
  span.classList.add("erro-input");
  span.textContent = mensagem;
  input.insertAdjacentElement("beforebegin", span);
}

function removerErro(input) {
  if (
    input.previousElementSibling &&
    input.previousElementSibling.classList.contains("erro-input")
  ) {
    input.previousElementSibling.remove();
  }
}

// ===============================
// FUNÇÕES DE VALIDAÇÃO
// ===============================
function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function validarSenha(senha) {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{6,}$/;
  return regex.test(senha);
}

function validarCPF(cpf) {
  cpf = cpf.replace(/\D/g, "");
  if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

  let soma = 0;
  for (let i = 1; i <= 9; i++) soma += cpf[i - 1] * (11 - i);
  let resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== Number(cpf[9])) return false;

  soma = 0;
  for (let i = 1; i <= 10; i++) soma += cpf[i - 1] * (12 - i);
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;

  return resto === Number(cpf[10]);
}

function validarTelefone(tel) {
  tel = tel.replace(/\D/g, "");
  return tel.length === 11;
}

function validarCEP(cep) {
  if (!cep) return false;
  const numeros = cep.replace(/\D/g, "");
  return numeros.length === 8;
}

// ===============================
// CONTROLE DOS STEPS
// ===============================
$(document).ready(function () {

  // Aplica máscaras em tempo real
  $("#cep").on("input", function () {
    let v = this.value.replace(/\D/g, "").slice(0, 8);
    if (v.length > 5) {
      this.value = v.substring(0, 5) + "-" + v.substring(5);
    } else {
      this.value = v;
    }
  });

  $("#phone").on("input", function () {
    let v = this.value.replace(/\D/g, "").slice(0, 11);
    if (v.length > 10) {
      this.value = v.replace(/^(\d{2})(\d{5})(\d{4})$/, "($1)$2-$3");
    } else if (v.length > 5) {
      this.value = v.replace(/^(\d{2})(\d{4,5})/, "($1)$2-");
    } else if (v.length > 2) {
      this.value = v.replace(/^(\d{2})/, "($1)");
    }
  });

  // -------- NEXT --------
  $(".next").on("click", function () {
    let current_fs = $(this).closest("fieldset");
    let valid = true;

    current_fs.find("input, select, textarea").each(function () {
      removerErro(this);

      if (this.value.trim() === "") {
        mostrarErro(this, "Este campo é obrigatório.");
        valid = false;
      }

      if (this.name === "email" && !validarEmail(this.value)) {
        mostrarErro(this, "Email inválido.");
        valid = false;
      }

      if (this.name === "pass" && !validarSenha(this.value)) {
        mostrarErro(
          this,
          "Senha deve ter maiúscula, minúscula, número e caractere especial."
        );
        valid = false;
      }

      if (this.name === "cpass") {
        let senha = current_fs.find("input[name='pass']").val();
        if (this.value !== senha) {
          mostrarErro(this, "As senhas não coincidem.");
          valid = false;
        }
      }

      if (this.name === "cpf" && !validarCPF(this.value)) {
        mostrarErro(this, "CPF inválido.");
        valid = false;
      }

      if (this.name === "phone" && !validarTelefone(this.value)) {
        mostrarErro(this, "Telefone inválido.");
        valid = false;
      }

      if (this.name === "cep" && !validarCEP(this.value)) {
        mostrarErro(this, "CEP inválido.");
        valid = false;
      }
    });

    if (!valid) return;

    let next_fs = current_fs.next("fieldset");
    current_fs.hide();
    next_fs.show();

    $("#progressbar li").removeClass("active");
    $("#progressbar li")
      .eq($("fieldset").index(next_fs))
      .addClass("active");
  });

  // -------- PREVIOUS --------
  $(".previous").on("click", function () {
    let current_fs = $(this).closest("fieldset");
    let prev_fs = current_fs.prev("fieldset");

    current_fs.hide();
    prev_fs.show();

    $("#progressbar li").removeClass("active");
    $("#progressbar li")
      .eq($("fieldset").index(prev_fs))
      .addClass("active");
  });

  // -------- VOLTAR HOME --------
  $(".btn-voltar-home").on("click", function () {
    window.location.href = "../index.html";
  });

  // -------- SUBMIT FINAL --------
  $("#msform").on("submit", function (event) {

    let valid = true;

    $("#msform").find("input, select, textarea").each(function () {
      removerErro(this);
      if (this.value.trim() === "") {
        mostrarErro(this, "Este campo é obrigatório.");
        valid = false;
      }
    });

    if (!valid) {
      event.preventDefault();
      return;
    }

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

    localStorage.setItem("usuario", JSON.stringify(usuario));

    alert("Cadastro realizado com sucesso!");
    // formulário segue para login.html
  });


});



