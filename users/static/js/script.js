const userIcon = document.getElementById("userIcon");
const dropdown = document.getElementById("dropdownMenu");

userIcon.addEventListener("click", () => {
    dropdown.style.display =
        dropdown.style.display === "flex" ? "none" : "flex";
});

document.addEventListener("click", (e) => {
    if (!userIcon.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = "none";
    }
});
