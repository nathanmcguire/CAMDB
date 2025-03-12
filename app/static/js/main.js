// Wait for the DOM to be ready
$(document).ready(function() {
    // Initialize Bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    // Make rows clickable
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarExpanded = document.getElementById('sidebar-expanded');
    const toggleButton = document.querySelector('.navbar-toggler');

    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('d-none');
        sidebarExpanded.classList.toggle('d-none');
    });
});
