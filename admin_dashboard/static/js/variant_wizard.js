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
  const name = step1.querySelector('input[name="name"]').value.trim();
  const price = step1.querySelector('input[name="price"]').value.trim();
  const comparePrice = step1.querySelector('input[name="compare_at_price"]').value.trim();
  const productId = step1.querySelector('select[name="product_id"]').value;

  if (!name) {
    alert("Please enter the Variant Name");
    return;
  }
  if (!price) {
    alert("Please enter the Price");
    return;
  }
  if (!comparePrice) {
    alert("Please enter the Compare At Price");
    return;
  }
  if (!productId) {
    alert("Please select a Product");
    return;
  }

  // ✅ All fields valid, move to next step
  nextStep();
}

// Image Preview Logic (without primary functionality)
const variantImagesInput = document.getElementById('variant_images');
const imagePreview = document.getElementById('imagePreview');
let imagesData = [];

variantImagesInput.addEventListener('change', (e) => {
  imagePreview.innerHTML = '';
  imagesData = [];

  Array.from(e.target.files).forEach((file) => {
    const reader = new FileReader();
    reader.onload = () => {
      const div = document.createElement('div');
      div.className = 'image-box';
      div.innerHTML = `<img src="${reader.result}">`;
      imagePreview.appendChild(div);
      imagesData.push(file); // store file for submission if needed
    };
    reader.readAsDataURL(file);
  });
});
