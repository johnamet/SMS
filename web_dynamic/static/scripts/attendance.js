$(document).ready(function () {
  const featuredClay = $('.featured-clay');
  const searchBar = $('.search');
  const logo = $('.logo-comp');

  logo.click(function () {
    window.location.href = 'http://127.0.0.1:8081/admin-dashboard';
  });
  query = [];

  function fetchClasses () {
    $.ajax({
      type: 'GET',
      headers: {
        'Authorization':`Bearer ${localStorage.getItem('access_token')}`
      },
      url: 'http://127.0.0.1:8080/services/v1/classes',
      success: function (data) {
        const classes = data.classes;
        classes.forEach(function (cls) {
          createFeaturedClay(cls);
        });
      },
      error: function (xhr, status, error) {
        console.error('Error fetching classes:', error);
      }
    });
  }

  function fetchClassStats (infoDiv, data) {
    if (!data || !data.attendances) {
      console.error('Error: No attendance data found.');
      return;
    }

    const attendances = data.attendances;

    // Filter present attendances
    const present = attendances.filter(attendance => attendance.status === 1);

    // Filter absent attendances
    const absent = attendances.filter(attendance => attendance.status === 0);

    const students = data.students;
    const num_absent = absent.length;
    const num_present = present.length;
    const numRoll = students.length;
    const attendanceRate = Math.round((num_present / numRoll) * 100);

    // Create HTML elements for class stats
    const onRollPara = $('<p>').html('<b>No. On Roll: </b>' + numRoll);
    const attendanceRatePara = $('<p>').html('<strong>Attendance Rate: </strong>' + attendanceRate + '%');
    const absentPara = $('<p>').html('<strong>Absent: </strong>' + num_absent);
    const presentPara = $('<p>').html('<strong>Present: </strong>' + num_present);

    // Append information paragraphs to infoDiv
    infoDiv.append(onRollPara, attendanceRatePara, absentPara, presentPara);
  }

  function createFeaturedClay (cls) {
    // Create the outer featured-clay element
    const innerContainer = $('<div>');

    innerContainer.click(function () {
      localStorage.setItem('className', cls.class_name);
      localStorage.setItem('attendanceData', JSON.stringify(cls.attendances));
      window.location.href = 'http://127.0.0.1:8081/class-attendance';
    });

    // Create the information div
    const infoDiv = $('<div>');
    fetchClassStats(infoDiv, cls);

    // Create the class details div
    const classDetailsDiv = $('<div>');

    const classHeader = $('<h3>').text(cls.class_name);
    const classTeacherPara = $('<p>').text('Class Teacher: ' + cls.class_teacher);
    const assistantTeacherPara = $('<p>').text('Assistant Teacher: ' + cls.assist_class_teacher);

    // Append class details to classDetailsDiv
    classDetailsDiv.append(classHeader, classTeacherPara, assistantTeacherPara);
    // Append information and class details divs to innerContainer
    innerContainer.append(infoDiv, classDetailsDiv);

    // Append innerContainer to featuredClay
    featuredClay.append(innerContainer);
  }

  // Call the fetchClasses function to populate the UI
  fetchClasses();
});
