const sampleHistory = [

    {
        news: "Government launches new project for economic development.",
        verdict: "REAL",
        confidence: "96%"
    },

    {
        news: "Aliens landed in Dhaka and met local politicians.",
        verdict: "FAKE",
        confidence: "99%"
    }
];

const table = document.getElementById("historyTable");

sampleHistory.forEach((item, index) => {

    table.innerHTML += `

        <tr>

            <td>${index + 1}</td>

            <td>
                ${item.news.substring(0, 50)}...
            </td>

            <td>${item.verdict}</td>

            <td>

                <button
                    class="view-btn"
                    onclick="openModal(${index})"
                >

                    <i class="fa-solid fa-eye"></i>

                </button>

            </td>

        </tr>
    `;
});

/* ================= MODAL ================= */

const modal = document.getElementById("newsModal");

const closeModalBtn = document.getElementById("closeModal");

function openModal(index) {

    const item = sampleHistory[index];

    document.getElementById("modalNews").innerText =
        item.news;

    document.getElementById("modalVerdict").innerText =
        item.verdict;

    document.getElementById("modalConfidence").innerText =
        item.confidence;

    modal.style.display = "block";
}

closeModalBtn.onclick = function () {

    modal.style.display = "none";
}

window.onclick = function(event) {

    if (event.target === modal) {

        modal.style.display = "none";
    }
}