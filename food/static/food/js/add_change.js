window.addEventListener("load", ()=> {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    let newFoodBtns = document.querySelectorAll(".add-new-btn");
    Array.from(newFoodBtns).forEach((btn) => {
        btn.addEventListener("click", (e) => {
            createNewPopup(e.target)
        })
    })

    // add a new ingredient form 
    let addIngredientBtn = document.querySelector("#add-ingredient-btn");
    let ingredientEmptyForm = document.querySelector("#ingredient-form-empty");
    let ingredientCount = document.getElementById("id_ingredient-TOTAL_FORMS");
    if (addIngredientBtn) {
        addIngredientBtn.addEventListener('click', (e) => {
            if (parseInt(ingredientCount.value) < parseInt(document.getElementById("id_ingredient-MAX_NUM_FORMS").value)) {
                // increase TOTAL_FORMS input value
                ingredientCount.value = parseInt(ingredientCount.value) + 1;
                // clone empty form and replace prefix with id
                let newForm = ingredientEmptyForm.cloneNode(true);
                newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, (ingredientCount.value -1));
                newForm.id = "ingredient-form-" + (parseInt(ingredientCount.value) - 1)
                // add eventlistener to NEW button
                newForm.querySelector(".add-new-btn").addEventListener("click", (e) => {
                    createNewPopup(e.target)
                })

                ingredientEmptyForm.before(newForm);
                
                // disable button if necessary
                if (parseInt(ingredientCount.value) == parseInt(document.getElementById("id_ingredient-MAX_NUM_FORMS").value)){
                    addIngredientBtn.classList.add("btn-disabled")
                }
            }
        })
    }

    function createNewPopup(btn) {
        window.open(btn.dataset.addUrl, btn.dataset.toId, 'height=500,width=800,resizable=yes,scrollbars=yes');
    }

    // change portions
    let decreasePortionsBtn = document.querySelector(".update-portions-icon#decrease-portions");
    let portions = document.querySelector("#id_recipe-portions");
    if (decreasePortionsBtn && (parseInt(portions.innerHTML) == 1)) {
        decreasePortionsBtn.classList.add("display-disabled")
    }
    let updatePortionsBtns = document.querySelectorAll(".update-portions-icon:not(.display-disabled)");
    Array.from(updatePortionsBtns).forEach((btn) => {
        btn.addEventListener("click", (e) => {
            updatePortions(e.target);
        })
    })

    async function updatePortions(button) {
        
        let url = window.location.href;
        let urlParts = url.split("?");
        let urlPost = urlParts[0] + "updateportions";
        let response = await fetch(urlPost, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                "button": button.id
            })
        })
        let data = await response.json()
        if (data["status"] = "success") {
            window.location.reload();
            }
    }
    
})

// append and select new option that was created via popup
{
    function getDataFromPopup(window, add_change, id, text) {
        if (add_change == "add") {
            let newOption = new Option(text, parseInt(id), false, true);
            $("#" + window.name).append(newOption).trigger("change");
        }
        window.close();
    }
}
