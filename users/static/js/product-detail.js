document.addEventListener("DOMContentLoaded", function () {
    // ----- MAIN IMAGE & THUMBS -----
    const mainImage = document.getElementById("mainProductImage");
    const thumbsContainer = document.querySelector(".thumbs");

    function updateThumbs(images) {
        thumbsContainer.innerHTML = "";
        images.forEach(img => {
            const thumb = document.createElement("img");
            thumb.src = `https://res.cloudinary.com/diipo18tm/${img.image}`;
            thumb.dataset.image = `https://res.cloudinary.com/diipo18tm/${img.image}`;
            thumb.classList.add("thumb-image");
            thumb.addEventListener("click", () => {
                mainImage.src = thumb.dataset.image;
            });
            thumbsContainer.appendChild(thumb);
        });
        // Set main image to first variant image
        if (images.length > 0) {
            mainImage.src = `https://res.cloudinary.com/diipo18tm/${images[0].image}`;
        }
    }

    // ----- QUANTITY -----
    const qtySpan = document.querySelector(".quantity span");
    const btnMinus = document.querySelector(".quantity button:first-child");
    const btnPlus = document.querySelector(".quantity button:last-child");

    btnPlus.addEventListener("click", () => {
        let currentQty = parseInt(qtySpan.textContent);
        qtySpan.textContent = currentQty + 1;
    });

    btnMinus.addEventListener("click", () => {
        let currentQty = parseInt(qtySpan.textContent);
        if (currentQty > 1) {
            qtySpan.textContent = currentQty - 1;
        }
    });

    // ----- VARIANTS -----
    // ----- AMAZON STYLE VARIANTS -----
const variantCards = document.querySelectorAll(".variant-card");

variantCards.forEach(card => {
    card.addEventListener("click", () => {

        variantCards.forEach(v => v.classList.remove("active"));
        card.classList.add("active");

        const variant = JSON.parse(card.dataset.variant);

        // Update price
        document.getElementById("price").textContent = `₹${variant.price}`;

        const compare = document.getElementById("compareAtPrice");
        const badge = document.getElementById("discountBadge");

        if (variant.compare_at_price) {
            compare.textContent = `₹${variant.compare_at_price}`;
            compare.style.display = "inline-block";
        } else {
            compare.style.display = "none";
        }

        if (variant.discount_percent) {
            badge.textContent = `${variant.discount_percent}% OFF`;
            badge.style.display = "inline-block";
        } else {
            badge.style.display = "none";
        }

        document.querySelector("#stockInfo strong").textContent = variant.stock;

        // Update images
        updateThumbs(variant.images);
    });
});

});
