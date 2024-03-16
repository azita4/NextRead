document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuButton = document.getElementById('mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    mobileMenuButton.addEventListener('click', function () {
        navLinks.classList.toggle('show');
        mobileMenuButton.classList.toggle('active');
    });
});