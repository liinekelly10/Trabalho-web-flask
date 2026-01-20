// Mostrar / ocultar senha
const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

togglePassword.addEventListener("click", () => {
    const type = passwordInput.getAttribute("type");
    passwordInput.setAttribute("type", type === "password" ? "text" : "password");

    togglePassword.classList.toggle("fa-eye");
    togglePassword.classList.toggle("fa-eye-slash");
});

document.addEventListener("DOMContentLoaded", () => {
  const btnLogin = document.getElementById("btnLogin");

  if (btnLogin) {
    btnLogin.addEventListener("click", function (event) {
      event.preventDefault();

      const email = document.getElementById("emailLogin").value;
      const senha = document.getElementById("senhaLogin").value;

      const usuarioSalvo = JSON.parse(localStorage.getItem("usuario"));

      if (!usuarioSalvo) {
        alert("Nenhum usuário cadastrado!");
        return;
      }

      if (email === usuarioSalvo.email && senha === usuarioSalvo.senha) {
        alert("Login realizado com sucesso!");
        window.location.href = "../index.html";
      } else {
        alert("E-mail ou senha incorretos!");
      }
    });
  }
});

