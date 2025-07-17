
    function navigateBack() {
      const referrer = document.referrer;
      if (referrer.includes('home2.html')) {
        window.location.href = 'home2.html';
      } else if (referrer.includes('login.html')) {
        window.location.href = 'login.html';
      } else if (referrer.includes('signup.html')) {
        window.location.href = 'signup.html';
      } else {
        window.history.back();
      }
    }
