$(document).ready(function (){
    const loginButton = $('.button');
    const emailField = $('#email');
    const passwordField = $('#password');

    loginButton.click(function (){
        console.log("Clicked");
        login();
    });

    function login(){
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8080/services/v1/login',
            data: JSON.stringify({
                "email": emailField.val(),
                "password": passwordField.val()
            }),
            contentType: 'application/json',
            success: function (data) {
                if (data && data.access_token && data.user_id) {
                    // Store user ID in sessionStorage
                    sessionStorage.setItem('user_id', data.user_id);
                    sessionStorage.setItem('access_token', data.access_token)
                    window.location.href = "http://127.0.0.1:8081/admin-dashboard";
                } else {
                    alert("Failed to login");
                }
            },
            error: function (error){
                alert("Failed to login");
            }
        });
    }
});
