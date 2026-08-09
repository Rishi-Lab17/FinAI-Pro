/*
=========================================================
FinAI Pro
Main JavaScript File
Part 1
=========================================================
*/


document.addEventListener("DOMContentLoaded", () => {

    hideLoadingSpinner();

    initializeSidebar();

    updateGreeting();

    updateCurrentDate();

    updateClock();

    highlightActiveMenu();

});


/*
=========================================================
Loading Spinner
=========================================================
*/

function hideLoadingSpinner() {

    const spinner = document.getElementById("loading-spinner");

    if (!spinner) {
        return;
    }

    window.addEventListener("load", () => {

        spinner.style.display = "none";

    });

}


/*
=========================================================
Sidebar
=========================================================
*/

function initializeSidebar() {

    const menuButton = document.getElementById("menu-toggle");

    const sidebar = document.querySelector(".sidebar");

    if (!menuButton || !sidebar) {
        return;
    }

    menuButton.addEventListener("click", () => {

        sidebar.classList.toggle("active");

    });

}


/*
=========================================================
Greeting
=========================================================
*/

function updateGreeting() {

    const greeting = document.getElementById("greeting");

    if (!greeting) {
        return;
    }

    const hour = new Date().getHours();

    let message = "";

    if (hour >= 5 && hour < 12) {

        message = "Good Morning";

    }

    else if (hour >= 12 && hour < 17) {

        message = "Good Afternoon";

    }

    else if (hour >= 17 && hour < 21) {

        message = "Good Evening";

    }

    else {

        message = "Good Night";

    }

    greeting.textContent = message;

}


/*
=========================================================
Current Date
=========================================================
*/

function updateCurrentDate() {

    const currentDate = document.getElementById("current-date");

    if (!currentDate) {
        return;
    }

    const today = new Date();

    currentDate.textContent = today.toLocaleDateString(
        "en-IN",
        {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        }
    );

}


/*
=========================================================
Live Clock
=========================================================
*/

function updateClock() {

    const clock = document.getElementById("live-clock");

    if (!clock) {
        return;
    }

    function refreshClock() {

        const now = new Date();

        clock.textContent = now.toLocaleTimeString(
            "en-IN",
            {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
            }
        );

    }

    refreshClock();

    setInterval(refreshClock, 1000);

}


/*
=========================================================
Active Sidebar Menu
=========================================================
*/

function highlightActiveMenu() {

    const currentPage = window.location.pathname;

    const links = document.querySelectorAll(".sidebar-menu a");

    links.forEach((link) => {

        if (currentPage === link.getAttribute("href")) {

            link.classList.add("active");

        }

    });

}
/*
=========================================================
Password Visibility
=========================================================
*/

function togglePassword(inputId, iconId) {

    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    if (!input || !icon) {
        return;
    }

    if (input.type === "password") {

        input.type = "text";

        icon.classList.remove("bi-eye");

        icon.classList.add("bi-eye-slash");

    } else {

        input.type = "password";

        icon.classList.remove("bi-eye-slash");

        icon.classList.add("bi-eye");

    }

}


/*
=========================================================
Password Strength
=========================================================
*/

function checkPasswordStrength(password) {

    let score = 0;

    if (password.length >= 8) score++;

    if (/[A-Z]/.test(password)) score++;

    if (/[a-z]/.test(password)) score++;

    if (/[0-9]/.test(password)) score++;

    if (/[^A-Za-z0-9]/.test(password)) score++;

    return score;

}


function updatePasswordStrength(inputId, messageId) {

    const input = document.getElementById(inputId);
    const message = document.getElementById(messageId);

    if (!input || !message) {
        return;
    }

    input.addEventListener("input", () => {

        const score = checkPasswordStrength(input.value);

        if (score <= 2) {

            message.textContent = "Weak Password";
            message.style.color = "#dc2626";

        }

        else if (score <= 4) {

            message.textContent = "Medium Password";
            message.style.color = "#f59e0b";

        }

        else {

            message.textContent = "Strong Password";
            message.style.color = "#16a34a";

        }

    });

}


/*
=========================================================
Animated Counter
=========================================================
*/

function animateCounter(elementId, targetValue) {

    const element = document.getElementById(elementId);

    if (!element) {
        return;
    }

    let currentValue = 0;

    const increment = Math.ceil(targetValue / 100);

    const timer = setInterval(() => {

        currentValue += increment;

        if (currentValue >= targetValue) {

            currentValue = targetValue;

            clearInterval(timer);

        }

        element.textContent = currentValue.toLocaleString("en-IN");

    }, 20);

}


/*
=========================================================
Progress Bar Animation
=========================================================
*/

function animateProgressBar(progressId, percentage) {

    const progressBar = document.getElementById(progressId);

    if (!progressBar) {
        return;
    }

    progressBar.style.width = percentage + "%";

    progressBar.setAttribute("aria-valuenow", percentage);

}


/*
=========================================================
Smooth Scroll
=========================================================
*/

function smoothScroll(targetId) {

    const element = document.getElementById(targetId);

    if (!element) {
        return;
    }

    element.scrollIntoView({

        behavior: "smooth"

    });

}


/*
=========================================================
Simple Form Validation
=========================================================
*/

function validateRequiredFields(formId) {

    const form = document.getElementById(formId);

    if (!form) {
        return true;
    }

    const requiredFields = form.querySelectorAll("[required]");

    for (const field of requiredFields) {

        if (field.value.trim() === "") {

            field.focus();

            return false;

        }

    }

    return true;

}


/*
=========================================================
Currency Formatter
=========================================================
*/

function formatCurrency(amount) {

    return new Intl.NumberFormat("en-IN", {

        style: "currency",

        currency: "INR"

    }).format(amount);

}


/*
=========================================================
Confirmation Dialog
=========================================================
*/

function confirmDelete(message = "Are you sure you want to delete this record?") {

    return confirm(message);

}


/*
=========================================================
Scroll To Top
=========================================================
*/

function scrollToTop() {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}


/*
=========================================================
End of File
=========================================================
*/