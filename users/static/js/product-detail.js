 document.addEventListener("DOMContentLoaded", function () {
            const mainImage = document.getElementById("mainProductImage");
            const thumbs = document.querySelectorAll(".thumb-image");

            thumbs.forEach(thumb => {
                thumb.addEventListener("click", () => {
                    mainImage.src = thumb.dataset.image;
                });
            });
        });

 document.addEventListener("DOMContentLoaded", function () {
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
  });