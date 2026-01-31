window.addEventListener("load", ()=> {

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
    
})

{
    function getDataFromPopup(window, add_change, id, text) {
        if (add_change == "add") {
            let newOption = new Option(text, parseInt(id), false, true);
            $("#" + window.name).append(newOption).trigger("change");
        }
        window.close();
    }
}
