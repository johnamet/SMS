$(document).ready(function () {

    const courseId = localStorage.getItem("course_id","53e5cb4e-b063-4277-bbfb-9f484c5fe180")

    fetchCourses()
    function fetchCourses(){
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8080/services/v1/courses/'+"53e5cb4e-b063-4277-bbfb-9f484c5fe180",
            success: function (data){
                const course = data

            },
            error: function (e) {
                console.log("Error fetching course. Reason: ", e)
            }
        })
    }


    // Function to group grades by grade_desc
    function groupGradesByDesc(grades) {
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

    function groupbyPass(grades) {
        const groupedGrades = {};
        grades.forEach(grade => {
            if (grade.percentage >= 50){
                if(!groupedGrades["Above"]){
                    groupedGrades["Above"]= [];
                }

                groupedGrades["Above"].push(grade)
            }else
            {
                if (!groupedGrades["Below"]){
                    groupedGrades["Below"] = []
                }
                groupedGrades["Below"].push(grade)
            }

        });
        return groupedGrades
    }


    function groupByAcademicYear(data) {
        const groupedGrades = {}
        const uniqueAcademicYears = [...new Set(data.map(item => item.academic_year))]
        uniqueAcademicYears.sort()

        for(const year in uniqueAcademicYears){
            data.forEach(grade => {
                if(grade.academic_year === year){
                    if(!groupedGrades[year]){
                        groupedGrades[year] = []
                    }

                    groupedGrades[year].push(grade)
                }
            })
        }
    }




    function groupByTerm(data) {
        const groupedGrades = {}
        const uniqueTerms = [...new Set(data.map(item => item.term))]
        uniqueTerms.sort()

        for(const term in uniqueTerms){
            data.forEach(grade => {
                if (grade.term === term){
                    if(!groupedGrades[term]){
                        groupedGrades[term].push(grade)
                        innerContainer = $('')
                    }
                }
            })
        }

        return groupedGrades

    }



    function createLeftDiv(infoDiv, data){
        const num_students = data.students.length
        const groupedGradeByDesc = groupGradesByDesc(data.gradebooks)

        const numStudentsPara = $('<p>').html('<b>Number of students</b>'+num_students)
        infoDiv.append(numStudentsPara)

        infoDiv.append($('<h3>').html('Assessment Statistics'))

        for (const key in groupedGradeByDesc){
            if (groupedGradeByDesc.hasOwnProperty(key)){
                const gradesLength = groupedGradeByDesc[key].length
                const para = $('<p>').html('<b>'+key+'</b>:'+gradesLength)
                infoDiv.append(para)
            }
        }
    }


    function createRightDiv(infoDiv, data){
        const groupedGrade = groupGradesByDesc(data.gradebooks)
        for (const key in groupedGrade){
            if (groupedGrade.hasOwnProperty(key)){
                groupedGrade[key].forEach( grade => {
                    grade.percentage = (grade.grade/grade.out_of) * 100
                })
            }
        }

        const avg = groupbyPass(groupedGrade)
        const aboveAvg = (avg["Above"].reduce((accum, current) => accum+current, 0))/avg["Above"].length
        const belowAvg = (avg["Below"].reduce((accum, current) => accum+current, 0))/avg["Below"].length

        const rightHeadDiv = $('div')

        const header = $('h3').text(data.term)
        const abovePara = $('<p>').html('<b>Above Average</b>'+aboveAvg)
        const belowPara = $('<p>').html('<b>below Average</b>'+belowAvg)
        rightHeadDiv.append(header, abovePara, belowPara)
        infoDiv.append(rightHeadDiv)
    }

    function createFeaturedClay(leftDiv, rightDiv, data){
        const grouped = groupByTerm(data)
        for(key in grouped){
            if(grouped.hasOwnProperty(key)){

            }
        }
    }
    function createContainer(data){

    }
});
