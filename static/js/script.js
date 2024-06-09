
const resultBox = document.querySelector(".result-box");
const buttonContainer = document.querySelector(".button-container");
const profile = document.querySelector(".profile");

const URL = "http://localhost:2129";

async function getData(){
    try{
        const response = await fetch(`${URL}/groups`);
        
        if (!response.ok) {
            
            throw new Error(`HTTP error! status: ${response.status}`);
            
        }
        const data = await response.json();
        return data;
    }
    catch(error){
        alert("Can't connect to database");
        console.error(error);
        return null;
    }
}

async function submitGroup(group_data){
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(group_data)
    };
    try{
        const response = await fetch(`${URL}/group`, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    }
    catch(error){
        alert("Couldn't add Group");
        console.error(error);
    }
}
async function deleteGroup(id){
    const options = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: id})
    };
    try{
        const response = await fetch(`${URL}/group/`, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    }
    catch(error){
        alert("Couldn't delete Group");
        console.error(error);
    }
}

async function getGroups(){
    resultado = await getData();
    if(!resultado){
        return;
    }
    buttonContainer.innerHTML = "";
    if(resultado){
        resultado.forEach(createGroupButtons);
    }
    const button = document.createElement("button");
    button.innerHTML = '＋';
    button.classList.add("group-btn");
    button.addEventListener("click", addGroup);
    buttonContainer.append(button);
}

function addGroup(){
    profile.innerHTML = "";
    resultBox.innerHTML = "";
    const form = document.createElement("div");
    form.classList.add("group-form");

    //Add Group
    const fieldsetGroup = document.createElement("fieldset");
    fieldsetGroup.classList.add("fieldset-group-input");
    const legendGroup = document.createElement("legend");
    legendGroup.textContent = "Group";
    fieldsetGroup.appendChild(legendGroup);

    //group name label
    const labelGroupName = document.createElement("label");
    labelGroupName.setAttribute("for", "group-name");
    labelGroupName.textContent = "Name: ";
    const inputGroupName = document.createElement("input");
    inputGroupName.setAttribute("id", "group-name");
    inputGroupName.setAttribute("type", "text");
    inputGroupName.setAttribute("required", true);

    labelGroupName.appendChild(inputGroupName);
    
    //company name label
    const labelCompanyName = document.createElement("label");
    labelCompanyName.setAttribute("for", "company-name");
    labelCompanyName.textContent = "Company: ";
    const inputCompanyName = document.createElement("input");
    inputCompanyName.setAttribute("id", "company-name");
    inputCompanyName.setAttribute("type", "text");
    inputCompanyName.setAttribute("required", true);

    labelCompanyName.appendChild(inputCompanyName);
    
    const labelNameAndCompany = document.createElement("label");
    labelNameAndCompany.classList.add("label-name-and-company");
    labelNameAndCompany.appendChild(labelGroupName);
    labelNameAndCompany.appendChild(labelCompanyName);
    
    fieldsetGroup.appendChild(labelNameAndCompany);
        

    //Add Idols
    const fieldsetIdols = document.createElement("fieldset");
    fieldsetIdols.classList.add("fieldset-idols-input");
    const legendIdols = document.createElement("legend");
    legendIdols.textContent = "Idols";
    fieldsetIdols.appendChild(legendIdols);

    const addIdolButton = document.createElement("button");
    addIdolButton.classList.add("add-idol-btn");
    addIdolButton.textContent = "Add Idol";
    addIdolButton.addEventListener("click", () => {
        
        const labelIdolStageName = document.createElement("label");
        labelIdolStageName.setAttribute("for", "idol-stage-name");
        labelIdolStageName.textContent = "Stage Name: ";
        const inputIdolStageName = document.createElement("input");
        inputIdolStageName.setAttribute("id", "idol-stage-name");
        inputIdolStageName.setAttribute("type", "text");
        inputIdolStageName.setAttribute("required", true);
        
        labelIdolStageName.appendChild(inputIdolStageName);
        
        const labelIdolRealName = document.createElement("label");
        labelIdolRealName.setAttribute("for", "idol-real-name");
        labelIdolRealName.textContent = "Real Name: ";
        const inputIdolRealName = document.createElement("input");
        inputIdolRealName.setAttribute("id", "idol-real-name");
        inputIdolRealName.setAttribute("type", "text");
        inputIdolRealName.setAttribute("required", true);
        
        labelIdolRealName.appendChild(inputIdolRealName);
        
        const labelStageNameAndRealName = document.createElement("label");
        labelStageNameAndRealName.classList.add("label-stagename-and-realname");
        labelStageNameAndRealName.appendChild(labelIdolStageName);
        labelStageNameAndRealName.appendChild(labelIdolRealName);
    
        fieldsetIdols.appendChild(labelStageNameAndRealName);
    })
    fieldsetIdols.appendChild(addIdolButton);


    //Adding to form
    form.appendChild(fieldsetGroup);
    form.appendChild(fieldsetIdols);

    const submitButton = document.createElement("button");
    submitButton.classList.add("submit-group-button");
    submitButton.textContent = "Submit Group";
    submitButton.addEventListener("click", (event) => {
        event.preventDefault();
        const grupo = new Object();
        grupo.name = document.querySelector("#group-name").value;
        grupo.company = document.querySelector("#company-name").value;
        grupo.idols = []
        
        const idolsName = document.querySelectorAll(".label-stagename-and-realname");

        idolsName.forEach(idol => {
            idolsStageAndRealName = new Object();
            idolsStageAndRealName.stage_name = idol.querySelector("#idol-stage-name").value;
            idolsStageAndRealName.real_name = idol.querySelector("#idol-real-name").value;
            if(idolsStageAndRealName.stage_name && idolsStageAndRealName.real_name){
                grupo.idols.push(idolsStageAndRealName);
            }
        });
        if(grupo.name && grupo.company){
            if(grupo.idols.length){
                submitGroup(grupo);
                getGroups();

            }
            else{
                alert("Insert at least one idol");
            }
        }
        else{
            alert("Name and Company can't be empty");
        }

    });

    form.appendChild(fieldsetIdols);
    form.appendChild(submitButton);
    profile.appendChild(form);

}

function createGroupButtons(grupo){
    const button = document.createElement("button");
    button.textContent = grupo.name;
    button.classList.add("group-btn");

    button.addEventListener("click", () => {
        resultBox.innerHTML = '';
        profile.innerHTML = "";
        grupo.idols.forEach(createIdolButtons);
        const deleteGroupButton = document.createElement("button");
        deleteGroupButton.classList.add("delete-button")
        deleteGroupButton.textContent = "Delete Group";
        deleteGroupButton.addEventListener("click", () => {
            if (confirm(`Delete ${grupo.name}?`)){
                deleteGroup(grupo.id)
            }
        });
        resultBox.appendChild(deleteGroupButton);
    });
    buttonContainer.appendChild(button);
}

function createIdolButtons(idol){
    const idolBotao = document.createElement("button");
    idolBotao.classList.add("idol-button")
    idolBotao.textContent = idol.stage_name;
    idolBotao.addEventListener("click", () => {
        profile.innerHTML = "";
        const titleName = document.createElement("h2");
        titleName.textContent = idol.real_name;
        profile.append(titleName);
        });
    resultBox.append(idolBotao);
}

getGroups();