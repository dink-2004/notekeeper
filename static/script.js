// ===============================
// Notes Keeper - Frontend JS
// ===============================

// 1. Auto logout countdown (works with backend session timeout)
// let sessionTimeoutSeconds = 300; // must match your Flask SESSION_TIMEOUT
// let warningSeconds = 60; // show warning 1 min before logout
// let countdownInterval;
// let logoutTimer;

// function startSessionTimer() {
//     clearTimers();
//     let remaining = sessionTimeoutSeconds;

//     countdownInterval = setInterval(() => {
//         remaining--;

//         const el = document.getElementById("session-countdown");
//         if (el) {
//             let mins = Math.floor(remaining / 60);
//             let secs = remaining % 60;
//             el.innerText = `${mins}:${secs.toString().padStart(2, "0")}`;
//         }

//         if (remaining === warningSeconds) {
//             alert("⚠ You will be logged out soon due to inactivity!");
//         }

//         if (remaining <= 0) {
//             clearTimers();
//             alert("Session expired! Redirecting to login...");
//             window.location.href = "/login";
//         }
//     }, 1000);

//     logoutTimer = setTimeout(() => {
//         clearTimers();
//         window.location.href = "/login";
//     }, sessionTimeoutSeconds * 1000);
// }

// function clearTimers() {
//     if (countdownInterval) clearInterval(countdownInterval);
//     if (logoutTimer) clearTimeout(logoutTimer);
// }

// ["click", "keypress", "mousemove"].forEach(evt => {
//     window.addEventListener(evt, () => {
//         startSessionTimer();
//     });
// });

// window.addEventListener("load", startSessionTimer);


// ===============================
// 2. Character counter for note textarea
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("note-content");
    const counter = document.getElementById("char-counter");
    const maxChars = 500;

    if (textarea && counter) {
        textarea.addEventListener("input", () => {
            let remaining = maxChars - textarea.value.length;
            counter.innerText = `${remaining} characters left`;

            if (remaining < 0) {
                counter.style.color = "red";
            } else {
                counter.style.color = "green";
            }
        });
    }
});


// ===============================
// 3. Auto-save draft (localStorage)
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("note-content");

    if (textarea) {
        const savedDraft = localStorage.getItem("note-draft");
        if (savedDraft) {
            textarea.value = savedDraft;
        }

        textarea.addEventListener("input", () => {
            localStorage.setItem("note-draft", textarea.value);
        });

        const form = textarea.closest("form");
        if (form) {
            form.addEventListener("submit", () => {
                localStorage.removeItem("note-draft");
            });
        }
    }
});


// ===============================
// 4. Auto-dismiss alerts after 5 seconds
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(() => {
            alert.classList.remove('show');  
            setTimeout(() => alert.remove(), 500); 
        }, 5000); 
    });
});


// ===============================
// 5. Dark Mode Toggle (use navbar button)
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("dark-mode-toggle");

  if (toggle) {
    // Load saved theme
    if (localStorage.getItem("theme") === "dark") {
      document.body.classList.add("dark-mode");
      toggle.innerHTML = "☀️"; // change icon
    }

    // Toggle theme on click
    toggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");

      if (document.body.classList.contains("dark-mode")) {
        toggle.innerHTML = "☀️";
        localStorage.setItem("theme", "dark");
      } else {
        toggle.innerHTML = "🌙";
        localStorage.setItem("theme", "light");
      }
    });
  }
document.addEventListener("DOMContentLoaded", () => {
  // Expand on "Read more..."
  document.querySelectorAll(".note-card .read-more-link").forEach(link => {
    link.addEventListener("click", () => {
      const card = link.closest(".note-card");
      card.classList.add("expanded");
      link.style.display = "none"; // hide after expand
    });
  });

  // Expand/collapse with View button
  document.querySelectorAll(".note-card .view-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault(); // stop navigation
      const card = btn.closest(".note-card");
      card.classList.toggle("expanded");

      btn.innerHTML = card.classList.contains("expanded")
        ? '<i class="bi bi-x-circle"></i> Close'
        : '<i class="bi bi-eye"></i> View';
    });
  });
});

});

