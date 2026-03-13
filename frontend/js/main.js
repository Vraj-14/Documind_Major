// function displayAnswer(result){

// document.getElementById("answerWindow").innerText = result.answer;

// document.getElementById("company").innerText =
// (result.entities.COMPANY || []).join(",");

// document.getElementById("metric").innerText =
// (result.entities.METRIC || []).join(",");

// document.getElementById("year").innerText =
// (result.entities.YEAR || []).join(",");

// }


// function addHistory(question){

// const history = document.getElementById("history");

// const li = document.createElement("li");

// li.innerText = question;

// history.appendChild(li);

// }




const sendBtn = document.getElementById("sendBtn");
const questionInput = document.getElementById("questionInput");

console.log("JS Loaded");

sendBtn.addEventListener("click", async () => {

    const question = questionInput.value.trim();

    if (!question) {
        alert("Enter a question");
        return;
    }

    console.log("Sending question:", question);

    try {

        const result = await askBackend(question);

        console.log("API response:", result);

        displayAnswer(result);

        addHistory(question);

    } catch (error) {

        console.error("API error:", error);

    }

});


// Enter key triggers the same send action
questionInput.addEventListener("keydown", (e) => {

    if (e.key === "Enter") {

        sendBtn.click();

    }

});


const companies = document.querySelectorAll(".company-card");

companies.forEach(button => {

    button.addEventListener("click", async () => {

        const company = button.innerText;

        const question =
        `What is revenue, net profit and eps of ${company} in 2025`;

        console.log("Company question:", question);

        const result = await askBackend(question);

        displayAnswer(result);

        addHistory(question);

    });

});