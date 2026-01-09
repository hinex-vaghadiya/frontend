// ================= PRODUCT IMAGE PREVIEW + PRIMARY SELECTION =================
const productImagesInput = document.getElementById('product_images');
const imagePreview = document.getElementById('imagePreview');
let productImagesData = [];

if (productImagesInput) {
    productImagesInput.addEventListener('change', (e) => {
        imagePreview.innerHTML = '';
        productImagesData = [];

        Array.from(e.target.files).forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = () => {
                const div = document.createElement('div');
                div.className = 'image-box';
                div.innerHTML = `<img src="${reader.result}"><div class="primary-badge">Primary</div>`;

                // Click to select primary image (scoped only inside product preview)
                div.addEventListener('click', () => {
                    imagePreview.querySelectorAll('.image-box').forEach(b => b.classList.remove('primary'));
                    div.classList.add('primary');

                    productImagesData.forEach(img => img.isPrimary = false);
                    productImagesData[index].isPrimary = true;

                    document.getElementById('primary_image_index').value = index;
                });

                imagePreview.appendChild(div);
                productImagesData.push({ file, isPrimary: index === 0 });

                // Set first image as primary by default
                if (index === 0) {
                    div.classList.add('primary');
                    document.getElementById('primary_image_index').value = 0;
                }
            };
            reader.readAsDataURL(file);
        });
    });
}

// ================= VARIANT LOGIC =================
let variantIndex = 1;

function addVariant() {
    const container = document.getElementById("variants-container");

    container.insertAdjacentHTML("beforeend", `
        <div class="variant-block" data-variant-index="${variantIndex}">
            <input type="text" name="variants[${variantIndex}][name]" placeholder="Variant Name" required>
            <input type="text" name="variants[${variantIndex}][price]" placeholder="Price" required>
            <input type="text" name="variants[${variantIndex}][compare_at_price]" placeholder="Compare At Price" required>
            <input type="text" value="0" readonly placeholder="Stock (auto calculated by batch)">
            <label>Variant Images</label>
            <input type="file"
                   name="variants[${variantIndex}][images]"
                   multiple
                   accept="image/*"
                   class="variant-images-input"
                   data-variant-index="${variantIndex}"
                   required>
            <div class="image-preview variant-preview" id="variant-preview-${variantIndex}"></div>
            <button type="button" class="btn btn-gray remove-variant-btn" onclick="removeVariant(this)">
                − Remove Variant
            </button>
            <hr>
        </div>
    `);

    attachVariantImagePreview(variantIndex);
    variantIndex++;
}

function removeVariant(button) {
    const variants = document.querySelectorAll(".variant-block");
    if (variants.length <= 1) {
        alert("At least one variant is required.");
        return;
    }
    button.closest(".variant-block").remove();
}

// ================= VARIANT IMAGE PREVIEW (NO PRIMARY) =================
function attachVariantImagePreview(index) {
    const input = document.querySelector(`.variant-images-input[data-variant-index="${index}"]`);
    const previewContainer = document.getElementById(`variant-preview-${index}`);

    if (!input || !previewContainer) return;

    input.addEventListener("change", (e) => {
        previewContainer.innerHTML = "";

        Array.from(e.target.files).forEach(file => {
            const reader = new FileReader();
            reader.onload = () => {
                const div = document.createElement("div");
                div.className = "image-box"; // Variant images do not have primary
                div.innerHTML = `<img src="${reader.result}">`;
                previewContainer.appendChild(div);
            };
            reader.readAsDataURL(file);
        });
    });
}

// ================= INITIAL VARIANT IMAGE PREVIEW =================
document.addEventListener("DOMContentLoaded", () => {
    attachVariantImagePreview(0);
});
