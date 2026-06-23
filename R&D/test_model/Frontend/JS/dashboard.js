const analyzeBtn = document.getElementById("analyzeBtn");

analyzeBtn.addEventListener("click", analyzeNews);

function analyzeNews() {

    let newsText = document
        .getElementById("newsInput")
        .value
        .trim();

    if (newsText === "") {

        alert("Please enter news text.");

        return;
    }

    // TEMP MOCK RESULT
    let result = Math.random() > 0.5
        ? "REAL NEWS"
        : "FAKE NEWS";

    document.getElementById("resultBox").innerHTML =
        `Prediction Result: ${result}`;
}