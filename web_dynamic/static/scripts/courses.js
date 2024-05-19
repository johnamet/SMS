$(document).ready(function () {
  const featuredClay = $('.featured-clay');
  const searchBar = $('#search'); // Corrected selector for search bar
  const logo = $('.logo-comp');

  const totalSubjs = $('.large-banner #subjects');

  let courses; // Variable to hold fetched courses

  logo.click(function () {
    window.location.href = 'http://127.0.0.1:8081/admin-dashboard';
  });

  function fetchSubjects () {
    $.ajax({
      type: 'GET',
            headers: {
        'Authorization':`Bearer ${localStorage.getItem('access_token')}`
      },
      url: 'http://127.0.0.1:8080/services/v1/courses',
      success: function (data) {
        courses = data.courses; // Store fetched courses
        totalSubjs.text('Total Number of Subjects: ' + courses.length);
        $('.large-banner #primary').text(`Primary Dept: 
        ${courses.filter(course => course.department.toLowerCase() === "primary department").length}`);
        $('.large-banner #secondary').text(`Secondary Dept: ${courses.filter(course => course.department.toLowerCase() === 'secondary department').length}`);
        courses.forEach(function (course) {
          createFeaturedClay(course);
        });
      }
    });
  }

  function fetchCourseStats (infoDiv, data) {
    const classes = data.classes;

    const created = new Date(data.created_at).toLocaleDateString();
    const modified = new Date(data.updated_at).toLocaleDateString();

    // Create HTML elements for class stats
    const deptPara = $('<p>').html('<b style="color: seagreen;"> Dept: </b>' + data.department);
    const classesPara = $('<p>').html('<b style="color: seagreen;"> Classes: </b>' + classes.length);
    const createdPara = $('<p>').html('<b style="color: seagreen;"> Created at: </b>' + created);
    const modifiedPara = $('<p>').html('<b style="color: seagreen;"> Modified: </b>' + modified);

    infoDiv.append(classesPara, deptPara, createdPara, modifiedPara);
  }

  function createFeaturedClay (course) {
    const innerContainer = $('<div>');

    innerContainer.click(function () {
      localStorage.setItem('course_id', course.id);
      window.location.href = 'http://127.0.0.1:8081/courses/' + course.course_name.trim().replaceAll(' ', '_').toLowerCase();
    });

    const infoDiv = $('<div>');
    fetchCourseStats(infoDiv, course);

    // Create the class details div
    const classDetailsDiv = $('<div>');

    const header = $('<h3>').text(course.course_name);
    const teacherPara = $('<p>').text('Teacher: ' + course.teacher);
    const numClass = $('<p>').text('Description: ' + course.course_description);

    classDetailsDiv.append(header, teacherPara, numClass);

    innerContainer.append(infoDiv, classDetailsDiv);

    featuredClay.append(innerContainer);
  }

  function searchCourses(query) {
    if (query.startsWith('@class')) {
      const className = query.substring(6).trim().toLowerCase();
      featuredClay.empty(); // Clear previous results
      courses.forEach(function (course) {
        course.classes.filter(cls => cls.class_name.toLowerCase().includes(className)).forEach(function (cls) {
          createFeaturedClay(course); // Display course containing the class
        });
      });
    } else if (query.startsWith('@course')) {
      const courseName = query.substring(7).trim().toLowerCase();
      featuredClay.empty(); // Clear previous results
      courses.filter(course => course.course_name.toLowerCase().includes(courseName)).forEach(function (course) {
        createFeaturedClay(course);
      });
    }
  }

  searchBar.on('input', function () {
    const query = $(this).val();
    if (query.startsWith('@class') || query.startsWith('@course')) {
      searchCourses(query);
    }
  });

  fetchSubjects();
});
