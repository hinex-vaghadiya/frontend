let formVisible = false;

  function toggleCategoryForm() {
    const formCard = document.getElementById('category-form-card');
    const toggleBtn = document.getElementById('toggle-category-btn');
    const form = document.getElementById('category-form');
    const submitBtn = document.getElementById('submit-btn');

    if (formVisible) {
      // Hide form
      formCard.style.display = 'none';
      toggleBtn.innerText = '+ Add Category';

      // Reset form fields
      document.getElementById('category_name').value = '';
      document.getElementById('category_id').value = '';
      submitBtn.innerText = 'Save';

      // Reset form action to add
      form.action = "/admin/add-category/";

      formVisible = false;
    } else {
      // Show form
      formCard.style.display = 'block';
      toggleBtn.innerText = 'Cancel';
      formVisible = true;
    }
  }

  function editCategory(id, name) {
    const formCard = document.getElementById('category-form-card');
    const toggleBtn = document.getElementById('toggle-category-btn');
    const form = document.getElementById('category-form');
    const submitBtn = document.getElementById('submit-btn');

    // Show form
    formCard.style.display = 'block';
    toggleBtn.innerText = 'Cancel';
    formVisible = true;

    // Fill in the values
    document.getElementById('category_name').value = name;
    document.getElementById('category_id').value = id;

    // Change form action to edit URL with category ID
    form.action = `/admin/edit-category/${id}/`;

    // Change button text
    submitBtn.innerText = 'Update';
  }