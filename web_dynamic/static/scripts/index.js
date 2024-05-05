$(document).ready(function() {
    const loginButton = $('.home-buttons .home-login')

    loginButton.click(function () {
        window.location.host = "127.0.0.1"
        window.location.port = 5000
        window.location.pathname = "/login"
    });
})