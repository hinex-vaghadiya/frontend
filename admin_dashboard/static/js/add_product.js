// ================= VARIANT LOGIC =================
function addVariant() {
    const container = document.getElementById("variants-container");

    // Generate a unique ID for this variant's images preview
    const variantId = Date.now();

    container.insertAdjacentHTML("beforeend", `
        <div class="variant-block">
            <input type="text" name="variant_name[]" placeholder="Variant Name" required>
            <input type="text" name="price[]" placeholder="Price" required>
            <input type="text" name="compare_at_price[]" placeholder="Compare At Price" required>

            <input type="text" value="0" readonly placeholder="Stock (auto calculated by batch)">

            <label>Variant Images</label>
            <input type="file" name="variant_images[]" multiple accept="image/*" 
                   data-variant-id="variant-${variantId}" class="variant-images-input" required>

            <div class="image-preview" id="variant-preview-${variantId}"></div>

            <button type="button" class="btn btn-gray remove-variant-btn" onclick="removeVariant(this)">
                − Remove Variant
            </button>

            <hr>
        </div>
    `);

    // Attach image preview logic for the newly added variant
    attachVariantImagePreview(variantId);
}

function removeVariant(button) {
    const variants = document.querySelectorAll(".variant-block");
    if (variants.length <= 1) {
        alert("At least one variant is required.");
        return;
    }
    button.closest(".variant-block").remove();
}

// ================= PRODUCT IMAGE PREVIEW =================
const productImagesInput = document.getElementById('product_images');
const imagePreview = document.getElementById('imagePreview');
let productImagesData = [];

productImagesInput.addEventListener('change', (e) => {
    imagePreview.innerHTML = '';
    productImagesData = [];

    Array.from(e.target.files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = () => {
            const div = document.createElement('div');
            div.className = 'image-box';
            div.innerHTML = `<img src="${reader.result}"><div class="primary-badge">Primary</div>`;

            // Select primary image
            div.addEventListener('click', () => {
                document.querySelectorAll('.image-box').forEach(b => b.classList.remove('primary'));
                div.classList.add('primary');
                productImagesData.forEach(img => img.isPrimary = false);
                productImagesData[index].isPrimary = true;
                document.getElementById('primary_image_index').value = index;
            });

            imagePreview.appendChild(div);
            productImagesData.push({ file, isPrimary: index === 0 });

            if (index === 0) {
                div.classList.add('primary');
                document.getElementById('primary_image_index').value = 0;
            }
        };
        reader.readAsDataURL(file);
    });
});

// ================= VARIANT IMAGE PREVIEW (NO PRIMARY) =================
function attachVariantImagePreview(variantId) {
    const input = document.querySelector(`.variant-images-input[data-variant-id="variant-${variantId}"]`);
    const previewContainer = document.getElementById(`variant-preview-${variantId}`);

    input.addEventListener('change', (e) => {
        previewContainer.innerHTML = '';

        Array.from(e.target.files).forEach((file) => {
            const reader = new FileReader();
            reader.onload = () => {
                const div = document.createElement('div');
                div.className = 'image-box';
                div.innerHTML = `<img src="${reader.result}">`; // Only preview, no primary badge
                previewContainer.appendChild(div);
            };
            reader.readAsDataURL(file);
        });
    });
}

// ================= INITIAL VARIANT IMAGE PREVIEW =================
document.addEventListener('DOMContentLoaded', () => {
    const initialVariantInput = document.querySelector('.variant-images-input');
    if (initialVariantInput) {
        const id = Date.now();
        initialVariantInput.setAttribute('data-variant-id', `variant-${id}`);
        const previewDiv = document.createElement('div');
        previewDiv.className = 'image-preview';
        previewDiv.id = `variant-preview-${id}`;
        initialVariantInput.insertAdjacentElement('afterend', previewDiv);

        attachVariantImagePreview(id);
    }
});
