// Redirect to the home page after 10 seconds
setTimeout(function() {
    window.location.href = "{{ url_for('select') }}"; // Replace with actual home page URL
}, 3000);
