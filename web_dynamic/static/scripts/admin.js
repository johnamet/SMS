$(document).ready(function() {

    const user_id = sessionStorage.getItem('user_id')
    const access_token = sessionStorage.getItem('access_token')
    const adminName = $('.page-display h1')

    let user;

    setUsername()

    const attendanceCard = $('.attendance-card')

    attendanceCard.click(function () {
        window.location.host = "127.0.0.1"
        window.location.port = 8081
        window.location.pathname = "/attendance"
    });


    function setUsername(){
        $.ajax({
            type: 'GET',
            url:'http://127.0.0.1:8080/services/v1/users/'+user_id,
            success: function (data) {
                console.log(data)
                adminName.text("Hi, "+data[user_id].first_name)
            }
    })
    }

})