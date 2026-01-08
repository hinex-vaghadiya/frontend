// Wizard Logic
function goToStep(stepNumber) {
  document.querySelectorAll('.step-content').forEach(c => c.classList.remove('active'));
  document.querySelector(`.step-content[data-step="${stepNumber}"]`).classList.add('active');

  document.querySelectorAll('.wizard-steps .step').forEach((s, i) => {
    s.classList.toggle('active', i === stepNumber - 1);
  });
}

function nextStep() { goToStep(2); }
function prevStep() { goToStep(1); }

// ✅ Step 1 validation before moving to step 2
function validateStep1() {
  const step1 = document.querySelector('.step-content[data-step="1"]');
  const productName = step1.querySelector('input[name="product_name"]').value.trim();
  const description = step1.querySelector('textarea[name="description"]').value.trim();
  const category = step1.querySelector('select[name="category_id"]').value;

  if (!productName) {
    alert("Please enter the Product Name");
    return;
  }
  if (!description) {
    alert("Please enter the Description");
    return;
  }
  if (!category) {
    alert("Please select a Category");
    return;
  }

  // ✅ All fields valid, move to next step
  nextStep();
}

// Image Preview Logic
const productImagesInput = document.getElementById('product_images');
const imagePreview = document.getElementById('imagePreview');
let imagesData = [];

productImagesInput.addEventListener('change', (e) => {
  imagePreview.innerHTML = '';
  imagesData = [];

  Array.from(e.target.files).forEach((file, index) => {
    const reader = new FileReader();
    reader.onload = () => {
      const div = document.createElement('div');
      div.className = 'image-box';
      div.innerHTML = `<img src="${reader.result}">
                       <div class="primary-badge">Primary</div>`;

      div.addEventListener('click', () => {
        document.querySelectorAll('.image-box').forEach(b => b.classList.remove('primary'));
        div.classList.add('primary');
        imagesData.forEach(img => img.isPrimary = false);
        imagesData[index].isPrimary = true;
        // ✅ Update the hidden input so Django knows which image is primary
        document.getElementById('primary_image_index').value = index;
      });

      imagePreview.appendChild(div);
      imagesData.push({ file, isPrimary: index === 0 }); // default first as primary
      if (index === 0) div.classList.add('primary');
      // ✅ Set hidden input value for first image
      if (index === 0) document.getElementById('primary_image_index').value = 0;
    };
    reader.readAsDataURL(file);
  });
});
