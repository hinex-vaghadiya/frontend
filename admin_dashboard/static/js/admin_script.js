/* =========================
   ADMIN SIDEBAR TOGGLE (MOBILE)
========================= */
document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.getElementById('adminHamburger');
    const sidebar = document.getElementById('adminSidebar');
    const overlay = document.getElementById('sidebarOverlay');

    /* --- Active link highlighting --- */
    const navLinks = document.querySelectorAll('.sidebar nav a');
    const currentPath = window.location.pathname;

    navLinks.forEach(function (link) {
        const href = link.getAttribute('href');
        if (!href || href === '#') return;

        // Exact match for Dashboard (/admin/), prefix match for others
        if (href === '/admin/' || href === '/admin') {
            if (currentPath === '/admin/' || currentPath === '/admin') {
                link.classList.add('active');
            }
        } else if (currentPath.startsWith(href)) {
            link.classList.add('active');
        }
    });

    /* --- Mobile sidebar toggle --- */
    if (!hamburger || !sidebar || !overlay) return;

    hamburger.addEventListener('click', function () {
        hamburger.classList.toggle('active');
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    overlay.addEventListener('click', function () {
        hamburger.classList.remove('active');
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    sidebar.querySelectorAll('nav a').forEach(function (link) {
        link.addEventListener('click', function () {
            if (window.innerWidth <= 768) {
                hamburger.classList.remove('active');
                sidebar.classList.remove('active');
                overlay.classList.remove('active');
            }
        });
    });
});

/* =========================
   CLIENT-SIDE TABLE PAGINATION
   Auto-paginates all .admin-table elements
   10 rows per page
========================= */
document.addEventListener('DOMContentLoaded', function () {
    var ROWS_PER_PAGE = 10;

    document.querySelectorAll('.admin-table').forEach(function (table) {
        var tbody = table.querySelector('tbody');
        if (!tbody) return;

        var allRows = Array.from(tbody.querySelectorAll('tr'));
        // Skip if there's an empty-state row or ≤10 rows
        if (allRows.length <= ROWS_PER_PAGE) return;
        if (allRows.length === 1 && allRows[0].querySelector('.empty')) return;

        var totalPages = Math.ceil(allRows.length / ROWS_PER_PAGE);
        var currentPage = 1;

        // Create pagination container
        var paginationDiv = document.createElement('div');
        paginationDiv.className = 'pagination-controls';
        // Insert after the table-wrapper
        var wrapper = table.closest('.table-wrapper') || table.parentElement;
        wrapper.parentElement.appendChild(paginationDiv);

        function showPage(page) {
            currentPage = page;
            allRows.forEach(function (row, i) {
                var start = (page - 1) * ROWS_PER_PAGE;
                var end = start + ROWS_PER_PAGE;
                row.style.display = (i >= start && i < end) ? '' : 'none';
            });
            renderControls();
        }

        function renderControls() {
            paginationDiv.innerHTML = '';

            // Info text
            var info = document.createElement('span');
            info.className = 'page-info';
            var start = (currentPage - 1) * ROWS_PER_PAGE + 1;
            var end = Math.min(currentPage * ROWS_PER_PAGE, allRows.length);
            info.textContent = 'Showing ' + start + '–' + end + ' of ' + allRows.length;
            paginationDiv.appendChild(info);

            var btnsWrap = document.createElement('div');
            btnsWrap.className = 'page-buttons';

            // Prev
            var prev = document.createElement('button');
            prev.textContent = '‹';
            prev.className = 'page-btn';
            prev.disabled = currentPage === 1;
            prev.addEventListener('click', function () { showPage(currentPage - 1); });
            btnsWrap.appendChild(prev);

            // Page numbers
            for (var p = 1; p <= totalPages; p++) {
                (function (pageNum) {
                    var btn = document.createElement('button');
                    btn.textContent = pageNum;
                    btn.className = 'page-btn' + (pageNum === currentPage ? ' active' : '');
                    btn.addEventListener('click', function () { showPage(pageNum); });
                    btnsWrap.appendChild(btn);
                })(p);
            }

            // Next
            var next = document.createElement('button');
            next.textContent = '›';
            next.className = 'page-btn';
            next.disabled = currentPage === totalPages;
            next.addEventListener('click', function () { showPage(currentPage + 1); });
            btnsWrap.appendChild(next);

            paginationDiv.appendChild(btnsWrap);
        }

        showPage(1);
    });
});
