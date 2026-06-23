fetch("components/navbar.html")
.then(res => res.text())
.then(data => {
    document.getElementById("navbar").innerHTML = data;
});

function logout() {

    localStorage.removeItem("loggedIn");

    window.location.href = "login.html";
}

if (localStorage.getItem("loggedIn") !== "true") {

    if (
        !window.location.pathname.includes("login.html")
    ) {
        window.location.href = "login.html";
    }
}