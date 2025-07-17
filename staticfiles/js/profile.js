document.addEventListener('DOMContentLoaded', () => {
  const profileButton = document.getElementById('profileButton');
  const goalsButton = document.getElementById('goalsButton');
  const profileSection = document.getElementById('profile');
  const goalsSection = document.getElementById('goals');

  // Add click event listeners to buttons
  profileButton.addEventListener('click', () => {
    profileButton.classList.add('active');
    goalsButton.classList.remove('active');
    profileSection.scrollIntoView({ behavior: 'smooth' });
  });

  goalsButton.addEventListener('click', () => {
    goalsButton.classList.add('active');
    profileButton.classList.remove('active');
    goalsSection.scrollIntoView({ behavior: 'smooth' });
  });

  // Use IntersectionObserver to detect which section is in view
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        if (entry.target === profileSection) {
          profileButton.classList.add('active');
          goalsButton.classList.remove('active');
        } else if (entry.target === goalsSection) {
          goalsButton.classList.add('active');
          profileButton.classList.remove('active');
        }
      }
    });
  }, { threshold: 0.5 });

  observer.observe(profileSection);
  observer.observe(goalsSection);
});

// Function to preview uploaded image
document.getElementById('uploadInput').addEventListener('change', function(event) {
  const file = event.target.files[0];  // Get the selected file
  console.log(file);  // Debugging: Check if the file is being correctly picked up

  if (file) {
    const formData = new FormData();
    formData.append("profile_picture", file);

    fetch('/upload-profile-pic/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')  // Handle CSRF token
      },
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if (data.message) {
        document.getElementById('profilePic').src = data.message;
      }
    })
    .catch(error => console.error('Error:', error));
  }
});

// CSRF token function for Django security
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function removeProfilePic() {
  fetch('/delete-profile-pic/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.message) {
      // Set the profile image back to the default
      document.getElementById('profilePic').src = 'https://static-00.iconduck.com/assets.00/profile-major-icon-512x512-xosjbbdq.png';
      
      // Optional: if your homepage has a profile icon that should update too
      const homeIcon = document.querySelector('.profile-icon img');
      if (homeIcon) {
        homeIcon.src = 'https://static-00.iconduck.com/assets.00/profile-major-icon-512x512-xosjbbdq.png';
      }
    } else {
      console.error(data.error);
    }
  })
  .catch(error => console.error('Error:', error));
}
