document.getElementById('theme-toggle').addEventListener('click', function() {
    const html = document.documentElement;
    if (html.getAttribute('data-theme') === 'dark') {
        html.setAttribute('data-theme', 'light');
        this.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        html.setAttribute('data-theme', 'dark');
        this.innerHTML = '<i class="fas fa-moon"></i>';
    }
});
