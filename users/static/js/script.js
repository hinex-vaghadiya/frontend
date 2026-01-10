/* =========================
   AUTH DRAWER LOGIC (UNCHANGED)
========================= */

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

if (closeAuth) closeAuth.addEventListener("click", closeDrawer);
if (authOverlay) authOverlay.addEventListener("click", closeDrawer);

/* Switch to Register */
if (openRegister) {
    openRegister.addEventListener("click", (e) => {
        e.preventDefault();
        loginForm.style.display = "none";
        registerForm.style.display = "block";
    });
}

/* Switch to Login */
if (openLogin) {
    openLogin.addEventListener("click", (e) => {
        e.preventDefault();
        registerForm.style.display = "none";
        loginForm.style.display = "block";
    });
}

/* =========================
   AUTO OPEN LOGIN/REGISTER ON ERROR
========================= */

document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const auth = params.get("auth");

    if (auth === "login") {
        authDrawer.classList.add("active");
        authOverlay.classList.add("active");
        loginForm.style.display = "block";
        registerForm.style.display = "none";
        return;
    }

    const loginMessages = document.querySelectorAll("#loginForm .auth-message");
    const registerMessages = document.querySelectorAll("#registerForm .auth-message");

    if (loginMessages.length > 0) {
        authDrawer.classList.add("active");
        authOverlay.classList.add("active");
        loginForm.style.display = "block";
        registerForm.style.display = "none";
    }

    if (registerMessages.length > 0) {
        authDrawer.classList.add("active");
        authOverlay.classList.add("active");
        loginForm.style.display = "none";
        registerForm.style.display = "block";
    }
});


/* =========================
   EDIT PROFILE TOGGLE (NEW)
========================= */

document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.getElementById("editProfileBtn");
    const profileForm = document.getElementById("profileForm");

    if (!editBtn || !profileForm) return;

    // Ensure form is hidden initially
    profileForm.style.display = "none";

    editBtn.addEventListener("click", function (e) {
        e.preventDefault();

        const isHidden =
            profileForm.style.display === "none" ||
            profileForm.style.display === "";

        if (isHidden) {
            profileForm.style.display = "block";
            editBtn.textContent = "CANCEL";
            editBtn.classList.add("cancel");
        } else {
            profileForm.style.display = "none";
            editBtn.textContent = "EDIT";
            editBtn.classList.remove("cancel");
        }
    });
});



/* =========================
   HERO IMAGE SLIDER (NEW)
========================= */

document.addEventListener("DOMContentLoaded", function () {
    const slides = document.querySelectorAll(".hero-slide");
    const prevBtn = document.getElementById("prevSlide");
    const nextBtn = document.getElementById("nextSlide");

    if (!slides.length) return;

    let currentIndex = 0;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove("active"));
        slides[index].classList.add("active");
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            currentIndex = (currentIndex + 1) % slides.length;
            showSlide(currentIndex);
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            showSlide(currentIndex);
        });
    }

    // Auto slide like Spiru
    setInterval(() => {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }, 5000);
});




/* =========================
   BESTSELLER SLIDER (CLEAN LOOP)
========================= */

const track = document.querySelector(".bestseller-track");
const prevBtn = document.getElementById("bestPrev");
const nextBtn = document.getElementById("bestNext");

const items = document.querySelectorAll(".bestseller-track .product-card");
const itemsPerView = 4;
const totalSlides = Math.ceil(items.length / itemsPerView);

let currentIndex = 0;

function updateSlider() {
    const slider = document.querySelector(".bestseller-slider");
    const slideWidth = slider.offsetWidth;

    track.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
}

// NEXT (LOOP)
nextBtn.addEventListener("click", () => {
    currentIndex++;
    if (currentIndex >= totalSlides) {
        currentIndex = 0;
    }
    updateSlider();
});

// PREV (LOOP)
prevBtn.addEventListener("click", () => {
    currentIndex--;
    if (currentIndex < 0) {
        currentIndex = totalSlides - 1;
    }
    updateSlider();
});

// Resize safety
window.addEventListener("resize", updateSlider);

// Init
updateSlider();


