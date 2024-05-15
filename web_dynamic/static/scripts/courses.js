$(document).ready(function () {
    const featuredClay = $('.featured-clay')
    const searchBar = $('.search')
    const logo = $('.logo-comp')

    const totalSubjs = $('.large-banner #subjects')


    logo.click(function () {
        window.location.href = 'http://127.0.0.1:8081/admin-dashboard';
    })

    fetchSubjects()

    function fetchSubjects() {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8080/services/v1/courses',
            success: function (data) {
                const courses = data.courses;
                totalSubjs.text("Total Number of Subjects: " + courses.length)
                courses.forEach(function (course) {
                    createFeaturedClay(course);
                })
            }
        })
    }

    function fetchCourseStats(infoDiv, data) {

        const classes = data.classes;

        const created = new Date(data.created_at).toLocaleDateString()
        const modified = new Date(data.updated_at).toLocaleDateString()

        // Create HTML elements for class stats
        const deptPara = $('<p>').html('<b style="color: seagreen;"> Dept: </b>' + data.department );
        const classesPara = $('<p>').html('<b style="color: seagreen;"> Classes: </b>' + classes.length);
        const createdPara = $('<p>').html('<b style="color: seagreen;"> Created at: </b>' + created);
        const modifiedPara = $('<p>').html('<b style="color: seagreen;"> Modified: </b>' + modified);


        infoDiv.append(classesPara, deptPara, createdPara, modifiedPara)
    }


    function createFeaturedClay(course) {
        const innerContainer = $('<div>');

        innerContainer.click(function () {
            //todo
        })

        const infoDiv = $('<div>')
        fetchCourseStats(infoDiv, course)

        // Create the class details div
        const classDetailsDiv = $('<div>');

        const header = $('<h3>').text(course.course_name)
        const teacherPara = $('<p>').text('Teacher: ' + course.teacher)
        const numClass = $('<p>').text('Description: ' + course.course_description)

        classDetailsDiv.append(header, teacherPara, numClass)

        innerContainer.append(infoDiv, classDetailsDiv)

        featuredClay.append(innerContainer)
    }

    fetchSubjects();
})