function _(x) {
  return document.getElementById(x);
}

const form = _("loginForm");
const user = _("user-name");
const pass = _("user-pass");
const mainContent = _("main");
const loggedIn = _("logged-in");

form.addEventListener("submit", login);

function login(event) {

  event.preventDefault();

  let userValue = user.value.trim();
  let passValue = pass.value.trim();

  // TEMPORARY LOGIN CREDENTIALS
  const correctUsername = "tanmoy";
  const correctPassword = "12345";

  if (
    userValue === correctUsername &&
    passValue === correctPassword
  ) {

    // SAVE LOGIN STATUS
    localStorage.setItem("loggedIn", "true");

    // hide login UI
    mainContent.classList.add("login-true");

    // show welcome screen
    loggedIn.style.display = "block";

    loggedIn.innerHTML = `
      <h2>Welcome, ${userValue}</h2>
      <p>Redirecting to dashboard...</p>
    `;

    // redirect to dashboard
    setTimeout(() => {

      window.location.href = "dashboard.html";

    }, 1000);

  } else {

    alert("Invalid username or password.");

  }
}