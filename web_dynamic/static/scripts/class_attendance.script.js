$(document).ready(function () {
  const pageSize = 10; // Number of rows per page
  const attendanceData = JSON.parse(localStorage.getItem('attendanceData')); // Array of attendance objects
  const pagination = $('#pagination');
  const header = $('.header .page-display h1');
  const logoComp = $('.logo-comp');
  const className = localStorage.getItem('className');
  header.text(className);

  logoComp.click(function () {
    window.location.href = 'http://127.0.0.1:8081/admin-dashboard';
  });
  pagination.on('click', 'button', function () {
    const pageNumber = parseInt($(this).text(), 10);
    generateTable(pageNumber);
  });
  function generateTable (page) {
    const startIndex = (page - 1) * pageSize;
    const endIndex = Math.min(startIndex + pageSize, attendanceData.length);

    let tableHtml = `
            <table>
                <tr>
                    <th>Name of Student</th>
                    ${getUniqueDatesHtml()}
                </tr>
        `;

    for (let i = startIndex; i < endIndex; i++) {
      const attendance = attendanceData[i];
      const studentName = attendance.student_name;

      const rowHtml = `
                <tr>
                    <td>${studentName}</td>
                    ${getAttendanceStatusHtml(attendance)}
                </tr>
            `;
      tableHtml += rowHtml;
    }

    tableHtml += '</table>';
    $('#attendanceTable').html(tableHtml);

    generatePagination(Math.ceil(attendanceData.length / pageSize), page);
  }

  function getUniqueDatesHtml () {
    const uniqueDates = [...new Set(attendanceData.map(item => item.date))];
    uniqueDates.sort((a, b) => new Date(a) - new Date(b)); // Sort dates in ascending order
    return uniqueDates.map(date => `<th>${new Date(date).toLocaleDateString()}</th>`).join('');
  }

  function getAttendanceStatusHtml (attendance) {
    const uniqueDates = [...new Set(attendanceData.map(item => item.date))];
    return uniqueDates.map(date => {
      const matchingAttendance = attendanceData.find(item => item.date === date && item.student_id === attendance.student_id);
      return `<td>${matchingAttendance ? matchingAttendance.status : '-'}</td>`;
    }).join('');
  }

  function generatePagination (totalPages, currentPage) {
    let paginationHtml = '';

    for (let i = 1; i <= totalPages; i++) {
      paginationHtml += `<button ${currentPage === i ? 'disabled' : ''}>${i}</button>`;
    }
    pagination.html(paginationHtml);
  }

  async function getStudentName (studentId) {
    const url = `http://127.0.0.1:8080/services/v1/students/${studentId}`;
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Error fetching student data: ${response.status}`);
      }
      const data = await response.json();
      return `${data.first_name} ${data.last_name}`;
    } catch (error) {
      console.error('Error getting student name:', error);
      // Handle error appropriately (e.g., return a default value or throw a specific error)
      return null; // Or throw a custom error
    }
  }

  // Initialize table with first page
  generateTable(1);
});
