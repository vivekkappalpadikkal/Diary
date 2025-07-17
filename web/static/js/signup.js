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
      cell.style.color = "#195b75";
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


//Quiz logic

    const questions = [
      { question: "Who is the current Secretary-General of the United Nations?", options: ["António Guterres", "Ban Ki-moon", "Kofi Annan", "Joe Biden"], answer: "António Guterres" },
      { question: "Which is the longest river in the world?", options: ["Amazon", "Nile", "Yangtze", "Mississippi"], answer: "Nile" },
      { question: "What does HTTP stand for?", options: ["Hyper Text Transfer Protocol", "High Tech Transfer Protocol", "Hyper Text Translation Program", "Host Transfer Text Protocol"], answer: "Hyper Text Transfer Protocol" },
      { question: "Which country recently exited the European Union (Brexit)?", options: ["France", "Germany", "United Kingdom", "Italy"], answer: "United Kingdom" },
      { question: "What is the capital of Canada?", options: ["Toronto", "Vancouver", "Ottawa", "Montreal"], answer: "Ottawa" },
      { question: "Who is known as the 'Father of the Indian Constitution'?", options: ["Mahatma Gandhi", "Jawaharlal Nehru", "Dr. B.R. Ambedkar", "Sardar Patel"], answer: "Dr. B.R. Ambedkar" },
      { question: "What is the currency of Japan?", options: ["Yen", "Won", "Dollar", "Peso"], answer: "Yen" },
      { question: "Which element has the chemical symbol ‘O’?", options: ["Oxygen", "Osmium", "Ozone", "Oxide"], answer: "Oxygen" },
      { question: "Which company owns Instagram?", options: ["Google", "Apple", "Meta", "Microsoft"], answer: "Meta" },
      { question: "In which year did India gain independence?", options: ["1947", "1950", "1945", "1930"], answer: "1947" },
      { question: "Which planet is closest to the sun?", options: ["Earth", "Mars", "Mercury", "Venus"], answer: "Mercury" },
      { question: "Who wrote the novel '1984'?", options: ["George Orwell", "J.K. Rowling", "Ernest Hemingway", "Mark Twain"], answer: "George Orwell" },
      { question: "Which is the smallest continent in the world?", options: ["Australia", "Europe", "Antarctica", "South America"], answer: "Australia" },
      { question: "What is the national sport of India?", options: ["Hockey", "Cricket", "Football", "Kabaddi"], answer: "Hockey" },
      { question: "Which Indian won the Nobel Peace Prize in 2014?", options: ["Malala Yousafzai", "Kailash Satyarthi", "Mother Teresa", "Ratan Tata"], answer: "Kailash Satyarthi" }
    ];

    let score = 0;
    let currentQuestionIndex = 0;

    function renderQuestion() {
      const q = questions[currentQuestionIndex];
      document.getElementById("question").textContent = `Q${currentQuestionIndex + 1}: ${q.question}`;

      const optionsContainer = document.getElementById("options-container");
      const feedback = document.getElementById("feedback");
      feedback.textContent = "";
      optionsContainer.innerHTML = "";

      q.options.forEach(option => {
        const button = document.createElement("button");
        button.textContent = option;
        button.onclick = () => checkAnswer(option);
        optionsContainer.appendChild(button);
      });

      document.getElementById("score").textContent = `Score: ${score}`;
    }

    function checkAnswer(selectedOption) {
      const correct = questions[currentQuestionIndex].answer;
      const feedback = document.getElementById("feedback");

      if (selectedOption === correct) {
        score += 5;
        feedback.style.color = "green";
        feedback.textContent = "✅ Correct!";
      } else {
        feedback.style.color = "red";
        feedback.textContent = `❌ Wrong! Correct: ${correct}`;
      }

      currentQuestionIndex++;

      setTimeout(() => {
        if (currentQuestionIndex < questions.length) {
          renderQuestion();
        } else {
          document.getElementById("question").textContent = "🎉 Quiz completed!";
          document.getElementById("options-container").innerHTML = "";
          feedback.style.color = "black";
          feedback.textContent = `Final Score: ${score} / ${questions.length * 5}`;
          document.getElementById("score").textContent = `Total Score: ${score}`;
        }
      }, 1000);
    }

    document.addEventListener("DOMContentLoaded", renderQuestion);


    document.addEventListener("DOMContentLoaded", function () {
      const usernameInput = document.getElementById("username");
      const lastNameInput = document.getElementById("last_name");
    
      usernameInput.addEventListener("input", function () {
        const parts = this.value.trim().split(" ");
        if (parts.length >= 2) {
          lastNameInput.value = parts[parts.length - 1];  // Get last word
        } else {
          lastNameInput.value = "";
        }
      });
    });
    