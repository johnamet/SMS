$(document).ready(function (){
    const loginButton = $('.button')
    const emailField = $('.login__field .login__input input[type="text"]')
    const passwordField = $('.login__field .login__input input[type="password"]')

    loginButton.click(function (){
        console.log("Clicked");
        login()
    })


    function login(){
        $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8080/services/v1/login',
        data: JSON.stringify({"email": emailField.textContent,
            "password": passwordField.textContent}),
        contentType: 'application/json',
        success: function (data) {
            const access_token = data["access_token"]
            console.log(access_token)
        },

    })}

});