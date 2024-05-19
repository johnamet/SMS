
$(document).ready(function () {
  const loginButton = $('.home-buttons .home-login');

  loginButton.click(function () {
    window.location.host = '127.0.0.1';
    window.location.port = 8081;
    window.location.pathname = '/login';
  });
});
