window.addEventListener("load", ()=> {
    let addIngredientBtn = document.querySelector("#add-ingredient-btn");
    let ingredientEmptyForm = document.querySelector("#ingredient-form-empty");
    let ingredientCount = document.getElementById("id_ingredient-TOTAL_FORMS");
    addIngredientBtn.addEventListener('click', (e) => {
        if (parseInt(ingredientCount.value) < parseInt(document.getElementById("id_ingredient-MAX_NUM_FORMS").value)){

            ingredientCount.value = parseInt(ingredientCount.value) + 1;
            let newForm = ingredientEmptyForm.cloneNode(true);
            newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, ingredientCount.value);
            newForm.id = "ingredient-form-" + (parseInt(ingredientCount.value) - 1)
            ingredientEmptyForm.before(newForm);
            if (parseInt(ingredientCount.value) == parseInt(document.getElementById("id_ingredient-MAX_NUM_FORMS").value)){
                addIngredientBtn.classList.add("btn-disabled")
            }
        }
    })
})