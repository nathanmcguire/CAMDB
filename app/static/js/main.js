// Wait for the DOM to be ready
$(document).ready(function() {
    // Initialize Bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    // Make rows clickable
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});
