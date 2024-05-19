$(document).ready(function () {
  const user_id = sessionStorage.getItem('user_id');
  const access_token = sessionStorage.getItem('access_token');
  const adminName = $('.page-display h1');

  if(!access_token){
    //redirect to the login page
    portal('/login');
  }

  let user;

  setUsername();

  const attendanceCard = $('.attendance-card');
  const staffCard = $('.staff-card');
  const coursesCard = $('.courses-card');
  const announcementCard = $('.announcement-card');
  const studentCard = $('.student-card');
  const classesCard = $('.classes-card');

  attendanceCard.click(function () {
    portal('attendance');
  });

  staffCard.click(function () {
    portal('staff');
  });

  coursesCard.click(function () {
    portal('courses');
  });

  studentCard.click(function () {
    portal('student');
  });

  announcementCard.click(function () {
    portal('announcement');
  });

  classesCard.click(function () {
    portal('classes');
  });

  function setUsername () {
    $.ajax({
      type: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`
      },
      url: 'http://127.0.0.1:8080/services/v1/users/' + user_id,
      success: function (data) {
        console.log(data);
        adminName.text('Hi, ' + data[user_id].first_name);
      }
    });
  }

  function portal (path) {
    window.location.host = '127.0.0.1';
    window.location.port = 8081;
    window.location.pathname = '/' + path;
  }
});
