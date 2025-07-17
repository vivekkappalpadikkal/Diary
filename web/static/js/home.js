/*function checkWidth() {
    if (window.innerWidth <= 768) {
      document.querySelector('.container').style.display = 'none';
      document.querySelector('.mobile-content').style.display = 'flex';
    } else {
      document.querySelector('.container').style.display = 'flex';
      document.querySelector('.mobile-content').style.display = 'none';
    }
  }


  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  let currentDate = new Date();

  function renderCalendar() {
    const monthYear = document.getElementById("month-year");
    const calendarBody = document.getElementById("calendar-body");
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    monthYear.textContent = `${monthNames[month]} ${year}`;
    calendarBody.innerHTML = "";

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    let row = document.createElement("tr");
    for (let i = 0; i < firstDay; i++) {
      row.appendChild(document.createElement("td"));
    }

    for (let day = 1; day <= daysInMonth; day++) {
      if (row.children.length === 7) {
        calendarBody.appendChild(row);
        row = document.createElement("tr");
      }
      const cell = document.createElement("td");
      cell.textContent = day;
      if (day === currentDate.getDate() && month === new Date().getMonth() && year === new Date().getFullYear()) {
        cell.style.color = "blue";
        cell.style.fontWeight = "bold";
      }
      row.appendChild(cell);
    }

    if (row.children.length > 0) {
      calendarBody.appendChild(row);
    }
  }

  function changeMonth(offset) {
    currentDate.setMonth(currentDate.getMonth() + offset);
    renderCalendar();
  }

  document.addEventListener("DOMContentLoaded", renderCalendar);
  window.addEventListener('resize', checkWidth);
  window.addEventListener('load', checkWidth); */

  function checkWidth() {
    if (window.innerWidth <= 768) {
      document.querySelector('.container').style.display = 'flex';
      document.querySelector('.mobile-content').style.display = 'flex';
    } else {
      document.querySelector('.container').style.display = 'flex';
      document.querySelector('.mobile-content').style.display = 'flex';
    }
  }
  
  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  
  let currentDate = new Date();
  
  function renderCalendar() {
    const monthYear = document.getElementById("month-year");
    const calendarBody = document.getElementById("calendar-body");
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
  
    monthYear.textContent = `${monthNames[month]} ${year}`;
    calendarBody.innerHTML = "";
  
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
  
    let row = document.createElement("tr");
  
    // Empty cells before the first day
    for (let i = 0; i < firstDay; i++) {
      row.appendChild(document.createElement("td"));
    }
  
    for (let day = 1; day <= daysInMonth; day++) {
      if (row.children.length === 7) {
        calendarBody.appendChild(row);
        row = document.createElement("tr");
      }
  
      const cell = document.createElement("td");
      cell.textContent = day;
      cell.style.cursor = "pointer";
  
      // Highlight today's date
      if (
        day === new Date().getDate() &&
        month === new Date().getMonth() &&
        year === new Date().getFullYear()
      ) {
        cell.style.color = "rgb(166,159,19)";
        cell.style.fontWeight = "bold";
        cell.style.fontSize = "1.2em";
      }
  
      // Make date clickable
      cell.onclick = () => {
        const selectedDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        window.location.href = `/entry/${selectedDate}/`;
      };
  
      row.appendChild(cell);
    }
  
    if (row.children.length > 0) {
      calendarBody.appendChild(row);
    }
  }
  
  function changeMonth(offset) {
    currentDate.setMonth(currentDate.getMonth() + offset);
    renderCalendar();
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    renderCalendar();
    checkWidth();
  });
  

  
 
  document.addEventListener("DOMContentLoaded", function () {
  fetch('/api/recent-diaries/')
    .then(response => response.json())
    .then(data => {
      const listBox = document.querySelector('.right-panel .list-box ul');
      listBox.innerHTML = ''; // Clear old entries

      data.forEach(entry => {
        const li = document.createElement('li');
        const dateDiv = document.createElement('div');
        const contentDiv = document.createElement('div');

        dateDiv.textContent = entry.date;
        contentDiv.textContent = entry.content;

        li.appendChild(dateDiv);
        li.appendChild(contentDiv);
        listBox.appendChild(li);
      });
    })
    .catch(error => {
      console.error('Error fetching recent diaries:', error);
    });
});



document.addEventListener("DOMContentLoaded", function () {
  fetch('/api/recent-diaries/')
    .then(response => response.json())
    .then(data => {
      const listBox = document.querySelector('.right-panel .list-box ul');
      listBox.innerHTML = ''; // Clear old entries

      data.forEach(entry => {
        const li = document.createElement('li');
        const dateDiv = document.createElement('div');
        const contentDiv = document.createElement('div');

        dateDiv.textContent = entry.date;
        contentDiv.textContent = entry.content;

        li.appendChild(dateDiv);
        li.appendChild(contentDiv);

        // ✅ Make li clickable
        li.style.cursor = "pointer";
        li.onclick = function () {
          window.location.href = `/entry/${entry.date}/`;
        };

        listBox.appendChild(li);
      });
    })
    .catch(error => {
      console.error('Error fetching recent diaries:', error);
    });



    loadTasks();

    const addBtn = document.getElementById('add-task-btn');
    if (addBtn) addBtn.addEventListener('click', () => addTodo());
});


// ========== ✅ To-Do List ==========
function addTodo(value = '') {
  const ul = document.getElementById('todo-list');
  const li = document.createElement('li');

  li.innerHTML = `
    <input type="text" value="${value}" oninput="autoSave(this)" />
    <button onclick="deleteTodo(this)">🗑</button>
  `;
  ul.appendChild(li);
}

function deleteTodo(button) {
  button.parentElement.remove();
  saveToServer();
}

function autoSave(input) {
  saveToServer();
}

function saveToServer() {
  const tasks = [];
  document.querySelectorAll('#todo-list input').forEach(input => {
    if (input.value.trim() !== "") {
      tasks.push(input.value.trim());
    }
  });

  fetch('/save-todos/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ tasks })
  });
}

function loadTasks() {
  fetch('/get-todos/')
    .then(response => response.json())
    .then(data => {
      const ul = document.getElementById('todo-list');
      ul.innerHTML = '';
      data.tasks.forEach(task => addTodo(task));
    });
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", renderCalendar);
window.addEventListener('resize', checkWidth);
window.addEventListener('load', checkWidth);


// Open the modal and display the full profile picture
function openModal(imageSrc) {
  const modal = document.getElementById("profileModal");
  const modalImg = document.getElementById("fullProfilePic");
  modal.style.display = "block";
  modalImg.src = imageSrc;
}

// Close the modal
function closeModal() {
  const modal = document.getElementById("profileModal");
  modal.style.display = "none";
}