// ================================
// MOSTRAR / OCULTAR SENHA
// ================================
const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

togglePassword.addEventListener("click", () => {
  const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
  passwordInput.setAttribute("type", type);

  togglePassword.classList.toggle("fa-eye");
  togglePassword.classList.toggle("fa-eye-slash");
});


// ================================
// VALIDAÇÃO DO FORMULÁRIO
// ================================
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");

  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");

  const emailError = document.getElementById("emailError");
  const passwordError = document.getElementById("passwordError");

  form.addEventListener("submit", function (event) {
    let valido = true;

    // Limpa mensagens
    emailError.textContent = "";
    passwordError.textContent = "";

    // ==========================
    // VALIDAÇÃO DO EMAIL
    // ==========================
    if (emailInput.value.trim() === "") {
      emailError.textContent = "Informe o e-mail.";
      valido = false;
    } else if (!emailValido(emailInput.value)) {
      emailError.textContent = "E-mail inválido.";
      valido = false;
    }

    // ==========================
    // VALIDAÇÃO DA SENHA
    // ==========================
    if (passwordInput.value.trim() === "") {
      passwordError.textContent = "Informe a senha.";
      valido = false;
    }

    // ==========================
    // BLOQUEIA ENVIO SE ERRO
    // ==========================
    if (!valido) {
      event.preventDefault();
    }
  });
});


// ================================
// FUNÇÃO AUXILIAR
// ================================
function emailValido(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
