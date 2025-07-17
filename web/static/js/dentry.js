document.addEventListener("DOMContentLoaded", function () {
    loadDiaryEntry(); // Load entry when page loads (if date is set)
  });
  
  // Function to fetch and load diary entry
  // function loadDiaryEntry() {
  //   let selectedDate = document.getElementById("entry-date").value;
  //   if (!selectedDate) return;
  
  //   fetch('/get_diary_entry/?date=${selectedDate}')
  //       .then(response => response.json())
  //       .then(data => {
  //           if (data.status === "success") {
  //               document.getElementById("diary-content").value = data.content || "";
  //           } else {
  //               document.getElementById("diary-content").value = "no data fount"; // Clear if no entry
  //           }
  //       })
  //       .catch(error => console.error("Error loading diary entry:", error));
  // }

  function loadDiaryEntry() {
    let selectedDate = document.getElementById("entry-date").value;
    if (!selectedDate) return;

    fetch(`/get_entry_by_date/?date=${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            const diaryContent = document.getElementById("diary-content");
            if (diaryContent) {
                diaryContent.value = data.status === "success" ? (data.content || "") : "no data found";
            } else {
                console.error("Element with ID 'diary-content' not found.");
            }
        })
        .catch(error => console.error("Error loading diary entry:", error));
}

  
  // Function to save diary entry
  function saveEntry() {
    const content = document.querySelector('.lined-textarea').value;
    const date = document.getElementById('entry-date').value;
  
    if (!date) {
      alert("Please select a date.");
      return;
    }
  
    fetch('/save-entry/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify({ content: content, date: date })
    })
    .then(response => {
      if (response.ok) {
        Toastify({
          text: "Message saved successfully!",
          duration: 3000,
          gravity: "top",
          position: "right",
          backgroundColor: "#4CAF50",
          close: true
        }).showToast();
      } else {
        Toastify({
          text: "Failed to save message.",
          duration: 3000,
          gravity: "top",
          position: "right",
          backgroundColor: "#FF4C4C",
          close: true
        }).showToast();
      }
    });
  }
  
  function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return '';
  }  
  
  
  // new
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  
  function saveEntry() {
    const content = document.querySelector('.lined-textarea').value;
    const date = document.getElementById('entry-date').value;
  
    fetch(`/entry/${date}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `content=${encodeURIComponent(content)}`
    })
    .then(response => {
        if (response.ok) {
            Toastify({
                text: "Saved!",
                duration: 3000,
                gravity: "top",
                position: "center",
                backgroundColor: "#4CAF50"
            }).showToast();
        } else {
            alert("Failed to save entry.");
        }
    });
  }


  function loadDiaryEntry() {
    const selectedDate = document.getElementById('entry-date').value;
  
    if (!selectedDate) return;
  
    fetch(`/api/entry/?date=${selectedDate}`)
      .then(response => response.json())
      .then(data => {
        document.querySelector('.lined-textarea').value = data.content || '';
      })
      .catch(error => {
        console.error("Error loading diary entry:", error);
      });
  }
  
  function insertEmoji(emoji) {
    const textarea = document.querySelector('.lined-textarea');
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;

    // Insert the emoji
    textarea.value = text.slice(0, start) + emoji + text.slice(end);

    // Move cursor after emoji
    textarea.selectionStart = textarea.selectionEnd = start + emoji.length;

    // Refocus on the textarea
    textarea.focus();
  }