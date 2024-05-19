$(document).ready(function () {
  const courseId = localStorage.getItem('course_id');
  const mainContainer = $('.main-container');

  fetchCourses();

  function fetchCourses () {
    $.ajax({
      type: 'GET',
      url: `http://127.0.0.1:8080/services/v1/courses/${courseId}`,
      success: function (data) {
        const grades = data.course.gradebooks;
        console.log(calcPercentage(grades));
        const grouped = groupByAcademicYear(calcPercentage(grades));
        const byTerm = groupByTerm(grouped);
        for (const key in byTerm) {
          mainContainer.append(createFeaturedContainer(key, byTerm));
        }
      },
      error: function (e) {
        console.log('Error fetching course. Reason: ', e);
      }
    });
  }

  function calcPercentage (grades) {
    const n_grades = [];
    for (const grade in grades) {
      const gr = grades[grade];
      const g = gr.grade;
      const of = gr.out_of;
      const percent = (g / of) * 100;

      gr.percentage = percent;

      n_grades.push(gr);
    }

    return n_grades;
  }

  // Function to group grades by grade_desc
  function groupGradesByDesc (grades) {
    const groupedGrades = {};
    grades.forEach(grade => {
      const desc = grade.grade_desc;
      if (!groupedGrades[desc]) {
        groupedGrades[desc] = [];
      }
      groupedGrades[desc].push(grade);
    });
    return groupedGrades;
  }

  function groupByAcademicYear (data) {
    const groupedGrades = {};
    const uniqueAcademicYears = [...new Set(data.map(item => item.academic_year))].sort();

    uniqueAcademicYears.forEach(year => {
      groupedGrades[year] = data.filter(grade => grade.academic_year === year);
    });

    return groupedGrades;
  }

  function groupByTerm (dataByAcYear) {
    const groupedGrades = {};

    for (const year in dataByAcYear) {
      groupedGrades[year] = {};
      const grades = dataByAcYear[year];
      const uniqueTerms = [...new Set(grades.map(item => item.term))].sort();

      uniqueTerms.forEach(term => {
        groupedGrades[year][term] = grades.filter(grade => grade.term === term);
      });
    }
    return groupedGrades;
  }

  function createFeaturedContainer (acYear, data) {
    const featuredContainer = $('<div>').addClass('featured-container');
    const title = $('<h1>').text(acYear);
    featuredContainer.append(title);

    function createAssessmentBlock (term, termData) {
      const featuredClayDiv = $('<div>').addClass('featured-clay');
      const content = $('<div>');

      function createAssessmentStats (descData) {
        const outerDiv = $('<div>');
        const innerDiv = $('<div>');
        const header = $('<h2>').text('Assessment Statistics');
        innerDiv.append(header);

        for (const key in descData) {
          const para = $('<p>').text(`${key.toUpperCase()}: ${descData[key].length}`);
          innerDiv.append(para);
        }
        outerDiv.append(innerDiv);
        return outerDiv;
      }

      function rightContent () {
        const rC = $('<div>');
        const termHeader = $('<h3>').text(term);
        const Para = $('<h4>').text('End of Term Statistics');
        const abovePara = $('<p>').text(termData.filter(grade => grade.percentage >= 60).length + ' above 60%');
        const belowPara = $('<p>').text(termData.filter(grade => grade.percentage < 60).length + ' below 60%');

        rC.append(termHeader, Para, abovePara, belowPara);
        return rC;
      }

      content.append(createAssessmentStats(groupGradesByDesc(termData)), rightContent());
      featuredClayDiv.append(content);
      return featuredClayDiv;
    }

    for (const term in data[acYear]) {
      featuredContainer.append(createAssessmentBlock(term, data[acYear][term]));
    }

    return featuredContainer;
  }
});
