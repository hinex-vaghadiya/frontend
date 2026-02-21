/* =========================
   HAMBURGER MENU TOGGLE
========================= */
const hamburgerBtn = document.getElementById("hamburgerBtn");
const mobileMenu = document.getElementById("mobileMenu");

if (hamburgerBtn && mobileMenu) {
    hamburgerBtn.addEventListener("click", () => {
        hamburgerBtn.classList.toggle("active");
        mobileMenu.classList.toggle("active");
    });

    // Close menu when clicking a nav link on mobile
    mobileMenu.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            hamburgerBtn.classList.remove("active");
            mobileMenu.classList.remove("active");
        });
    });
}

/* =========================
   INLINE SEARCH BAR
========================= */
const searchInput = document.getElementById("siteSearch");
const searchBtn = document.getElementById("searchBtn");
const navSearch = document.getElementById("navSearch");

function filterProducts(query) {
    const cards = document.querySelectorAll(".product-card");
    if (cards.length === 0) return;

    let visible = 0;
    cards.forEach(card => {
        const title = card.querySelector(".product-title");
        const text = title ? title.textContent.toLowerCase() : "";
        const show = !query || text.indexOf(query) > -1;
        card.style.display = show ? "" : "none";
        if (show) visible++;
    });

    let noResult = document.getElementById("noSearchResult");
    if (!noResult) {
        noResult = document.createElement("p");
        noResult.id = "noSearchResult";
        noResult.textContent = "No products match your search";
        noResult.style.cssText = "text-align:center; color:#999; padding:40px 0; grid-column: 1/-1; font-size:16px;";
        const grid = document.querySelector(".product-grid");
        if (grid) grid.appendChild(noResult);
    }
    noResult.style.display = (query && visible === 0) ? "" : "none";
}

function doSearch() {
    const query = searchInput ? searchInput.value.trim() : "";
    if (query) {
        window.location.href = "/shop/?q=" + encodeURIComponent(query);
    }
}

if (searchBtn && navSearch && searchInput) {
    // Click icon: expand or search
    searchBtn.addEventListener("click", () => {
        if (!navSearch.classList.contains("expanded")) {
            navSearch.classList.add("expanded");
            setTimeout(() => searchInput.focus(), 350);
        } else {
            doSearch();
        }
    });

    // Enter key triggers search
    searchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") doSearch();
    });

    // Live filter on pages with product cards
    searchInput.addEventListener("input", () => {
        filterProducts(searchInput.value.toLowerCase().trim());
    });

    // Click outside to collapse
    document.addEventListener("click", (e) => {
        if (!navSearch.contains(e.target) && navSearch.classList.contains("expanded")) {
            if (!searchInput.value.trim()) {
                navSearch.classList.remove("expanded");
            }
        }
    });

    // Auto-apply ?q= param on page load
    const urlParams = new URLSearchParams(window.location.search);
    const initialQuery = urlParams.get("q");
    if (initialQuery) {
        searchInput.value = initialQuery;
        navSearch.classList.add("expanded");
        filterProducts(initialQuery.toLowerCase().trim());
    }
}

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

/* Open login popup when non-authenticated user clicks cart */
const cartLoginTrigger = document.getElementById("cartLoginTrigger");
if (cartLoginTrigger && authDrawer && authOverlay) {
    cartLoginTrigger.addEventListener("click", () => {
        authDrawer.classList.add("active");
        authOverlay.classList.add("active");
        loginForm.style.display = "block";
        registerForm.style.display = "none";
    });
}

/* Open login popup when non-authenticated user clicks any add-to-cart button */
document.addEventListener("click", (e) => {
    const btn = e.target.closest(".login-required-btn");
    if (btn && authDrawer && authOverlay) {
        e.preventDefault();
        authDrawer.classList.add("active");
        authOverlay.classList.add("active");
        loginForm.style.display = "block";
        registerForm.style.display = "none";
    }
});

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

// COMMUNITY SECTION
// Auto play preview videos (5 sec loop)
document.querySelectorAll('.video-card video').forEach(video => {
    const LOOP_END = 5; // seconds

    video.addEventListener('timeupdate', () => {
        if (video.currentTime >= LOOP_END) {
            video.currentTime = 0;
            video.play();
        }
    });

    video.play();
});

// Open modal on click
// Auto play preview videos (5 sec loop)
document.querySelectorAll('.video-card video').forEach(video => {
    const LOOP_END = 5; // seconds

    video.addEventListener('timeupdate', () => {
        if (video.currentTime >= LOOP_END) {
            video.currentTime = 0;
            video.play();
        }
    });

    video.play();
});

// Open modal on click
const modal = document.getElementById('videoModal');
const modalVideo = document.getElementById('modalVideo');
const cards = document.querySelectorAll('.video-card');
let currentVideo = null; // track which card's video is currently open

cards.forEach(card => {
    card.addEventListener('click', () => {
        currentVideo = card.querySelector('video');
        const src = card.getAttribute('data-video');
        modal.style.display = 'flex';
        modalVideo.src = src;
        modalVideo.play();
    });
});

// Close modal
document.querySelector('.close-modal').addEventListener('click', () => {
    modal.style.display = 'none';
    modalVideo.pause();
    modalVideo.src = '';
    currentVideo = null;
});

// Close on outside click
modal.addEventListener('click', e => {
    if (e.target === modal) {
        modal.style.display = 'none';
        modalVideo.pause();
        modalVideo.src = '';
        currentVideo = null;
    }
});

// Helper to get current video index
function getCurrentVideoIndex() {
    return Array.from(cards).findIndex(card => card.querySelector('video') === currentVideo);
}

// Modal next video
document.getElementById('nextVideo').addEventListener('click', e => {
    e.stopPropagation();
    let idx = getCurrentVideoIndex();
    idx = (idx + 1) % cards.length;
    currentVideo = cards[idx].querySelector('video');
    modalVideo.src = cards[idx].getAttribute('data-video');
    modalVideo.play();
});

// Modal previous video
document.getElementById('prevVideo').addEventListener('click', e => {
    e.stopPropagation();
    let idx = getCurrentVideoIndex();
    idx = (idx - 1 + cards.length) % cards.length;
    currentVideo = cards[idx].querySelector('video');
    modalVideo.src = cards[idx].getAttribute('data-video');
    modalVideo.play();
});




// WHY CHOOSE - DYNAMIC CONTENT & IMAGE
const accordionButtons = document.querySelectorAll(".accordion-btn");
const whyImage = document.getElementById("whyImage");
const whyText = document.getElementById("whyText");

accordionButtons.forEach(btn => {
    btn.addEventListener("click", () => {

        // Remove active from all
        document.querySelectorAll(".accordion-item").forEach(item => {
            item.classList.remove("active");
        });

        // Activate current
        btn.parentElement.classList.add("active");

        // Update image & text
        const newImage = btn.getAttribute("data-image");
        const newText = btn.getAttribute("data-text");

        whyImage.src = newImage;
        whyText.textContent = newText;
    });
});



