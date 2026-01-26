document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.getElementById("mainProductImage");
    const thumbsContainer = document.querySelector(".thumbs");
    const variantCards = document.querySelectorAll(".variant-card");
    const variantInput = document.getElementById("variantInput"); // hidden input
    const productImages = Array.from(
        document.querySelectorAll(".thumb-image")
    ).map(img => img.dataset.image);

    function updateThumbs(productImgs, variantImgs) {
        thumbsContainer.innerHTML = "";
        [...productImgs, ...variantImgs].forEach((img, index) => {
            const thumb = document.createElement("img");
            thumb.src = img;
            thumb.dataset.image = img;
            thumb.className = "thumb-image";
            thumbsContainer.appendChild(thumb);

            if (index === 0) mainImage.src = img;
        });
    }

    function applyVariant(variant) {
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

        const variantImages = variant.images.map(
            img => `https://res.cloudinary.com/diipo18tm/${img.image}`
        );
        updateThumbs(productImages, variantImages);

        // Update hidden input for form
        variantInput.value = variant.id;
    }

    // Initial variant on load
    if (variantCards.length > 0) {
        variantCards[0].classList.add("active");
        applyVariant(JSON.parse(variantCards[0].dataset.variant));
    }

    // Variant click event
    variantCards.forEach(card => {
        card.addEventListener("click", function () {
            variantCards.forEach(v => v.classList.remove("active"));
            this.classList.add("active");

            const variantData = JSON.parse(this.dataset.variant);
            applyVariant(variantData);
        });
    });

    // Thumbnail click
    thumbsContainer.addEventListener("click", function (e) {
        if (e.target.classList.contains("thumb-image")) {
            mainImage.src = e.target.dataset.image;
        }
    });

    /* Quantity buttons (unchanged) */
    const qtySpan = document.querySelector(".quantity span");
    const btnMinus = document.querySelector(".quantity button:first-child");
    const btnPlus = document.querySelector(".quantity button:last-child");

    btnPlus.addEventListener("click", () => {
        let currentQty = parseInt(qtySpan.textContent);
        qtySpan.textContent = currentQty + 1;
    });

    btnMinus.addEventListener("click", () => {
        let currentQty = parseInt(qtySpan.textContent);
        if (currentQty > 1) qtySpan.textContent = currentQty - 1;
    });
});
