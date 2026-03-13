function displayAnswer(result){

document.getElementById("answerWindow").innerText = result.answer;

document.getElementById("company").innerText =
(result.entities.COMPANY || []).join(",");

document.getElementById("metric").innerText =
(result.entities.METRIC || []).join(",");

document.getElementById("year").innerText =
(result.entities.YEAR || []).join(",");

}


function addHistory(question){

const history = document.getElementById("history");

const li = document.createElement("li");

li.innerText = question;

history.appendChild(li);

}