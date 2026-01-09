let formVisible = false;

  function toggleBatchForm() {
    const card = document.getElementById('batch-form-card');
    const btn = document.getElementById('toggle-batch-btn');
    const form = document.getElementById('batch-form');

    if (formVisible) {
      card.style.display = 'none';
      btn.innerText = '+ Add Batch';
      form.reset();
      document.getElementById('batch_id').value = '';
      form.action = '/admin/add-batch/';
      document.getElementById('submit-btn').innerText = 'Save';
      formVisible = false;
    } else {
      card.style.display = 'block';
      btn.innerText = 'Cancel';
      formVisible = true;
    }
  }

  function editBatch(id, variantId, qty, mfg, exp) {
    if (!formVisible) toggleBatchForm();

    document.getElementById('batch_id').value = id;
    document.getElementById('variant_id').value = variantId;
    document.getElementById('qty').value = qty;
    document.getElementById('mfg_date').value = mfg;
    document.getElementById('exp_date').value = exp;

    document.getElementById('batch-form').action =
      `/admin/edit-batch/${id}/`;

    document.getElementById('submit-btn').innerText = 'Update';
  }