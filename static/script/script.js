function printRangeValue(value, id) {
    const options = document.getElementsByName(document.getElementById(id).dataset.questionId + "-radio");
    let temp = 0;
    for (const f of options) {
        if (f.checked) {
            temp = f.value;
        }
    }
    document.getElementsByName(id + "-label")[0].textContent = "Ваша градация: " + (parseFloat(temp) + parseFloat(value));
    document.getElementById(id).value = value;
}

function printRadioValue(value, id) {
    const data = document.getElementById(id).dataset.questionId + "-range";
    document.getElementsByName(data + "-label")[0].textContent = "Ваша градация: " + (parseFloat(value) + parseFloat(document.getElementsByName(data)[0].value));
}

function addComment(id) {
    const quest = document.getElementById(id).dataset.questionId;
    const container = document.getElementById(quest + "-comment-container");
    const addButton = document.getElementById(quest + "-add-button");
    const deleteButton = document.getElementById(quest + "-delete-button");
    addButton.style.display = 'none'
    deleteButton.style.display = null
    container.innerHTML = `<textarea class="form-control" data-question-id="${quest}" id="${quest}-textarea" name="${quest}-textarea" rows="4" required></textarea>`
}

function deleteComment(id) {
    const quest = document.getElementById(id).dataset.questionId
    const container = document.getElementById(quest + "-comment-container");
    const addButton = document.getElementById(quest + "-add-button");
    const deleteButton = document.getElementById(quest + "-delete-button");
    addButton.style.display = null
    deleteButton.style.display = "none";
    container.innerHTML = ""
}

async function getIogvList() {
    let response = await fetch( "/api/v1/get_iogv");

    if (response.ok) {
        return await response.json()
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

// getIogvList()