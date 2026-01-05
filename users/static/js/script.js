const userIcon = document.getElementById("userIcon");
const authDrawer = document.getElementById("authDrawer");
const authOverlay = document.getElementById("authOverlay");
const closeAuth = document.getElementById("closeAuth");

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

const openRegister = document.getElementById("openRegister");
const openLogin = document.getElementById("openLogin");

/* Open drawer on user icon click */
if (userIcon) {
userIcon.addEventListener("click", () => {
    authDrawer.classList.add("active");
    authOverlay.classList.add("active");
    loginForm.style.display = "block";
    registerForm.style.display = "none";
});
}

/* Close drawer */
function closeDrawer() {
    authDrawer.classList.remove("active");
    authOverlay.classList.remove("active");
}

closeAuth.addEventListener("click", closeDrawer);
authOverlay.addEventListener("click", closeDrawer);

/* Switch to Register */
openRegister.addEventListener("click", (e) => {
    e.preventDefault();
    loginForm.style.display = "none";
    registerForm.style.display = "block";
});

/* Switch to Login */
openLogin.addEventListener("click", (e) => {
    e.preventDefault();
    registerForm.style.display = "none";
    loginForm.style.display = "block";
});


/* =========================
   AUTO OPEN LOGIN/REGISTER ON ERROR
========================= */
document.addEventListener("DOMContentLoaded", function() {
    // open login after registration..
    const params = new URLSearchParams(window.location.search);
    const auth = params.get("auth");

    if (auth === "login") {
        // Auto open login drawer
        authDrawer.classList.add("active");
        authOverlay.classList.add("active");
        loginForm.style.display = "block";
        registerForm.style.display = "none";
        return;
    }

    // Check if there are any messages inside the login drawer
    const loginMessages = document.querySelectorAll("#loginForm .auth-message");
    const registerMessages = document.querySelectorAll("#registerForm .auth-message");

    if (loginMessages.length > 0) {
        // Open login drawer automatically
        authDrawer.classList.add("active");
        authOverlay.classList.add("active");
        loginForm.style.display = "block";
        registerForm.style.display = "none";
    }

    if (registerMessages.length > 0) {
        // Open register drawer automatically
        authDrawer.classList.add("active");
        authOverlay.classList.add("active");
        loginForm.style.display = "none";
        registerForm.style.display = "block";
    }
});