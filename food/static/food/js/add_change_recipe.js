window.addEventListener("load", ()=> {

    let foodFormDiv = document.querySelector("#food-form-div");
    let saveFoodBtn = document.querySelector("#save-new-food-btn");
    let foodForm = document.querySelector("#food-form");


    let newFoodBtns = document.querySelectorAll(".add-new-btn");
    Array.from(newFoodBtns).forEach((btn) => {
        btn.addEventListener("click", (e) => {
            createNewFood(e.target)
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
                    createNewFood(e.target)
                }
                )

                ingredientEmptyForm.before(newForm);
                
                // disable button if necessary
                if (parseInt(ingredientCount.value) == parseInt(document.getElementById("id_ingredient-MAX_NUM_FORMS").value)){
                    addIngredientBtn.classList.add("btn-disabled")
                }
            }
        })
    }
    

    function createNewFood(btn) {
        foodFormDiv.classList.remove("display-none")
        saveFoodBtn.dataset.toId = btn.dataset.toId
        saveFoodBtn.addEventListener('click', async () => {
            let formData = new FormData(foodForm);
            let response = await fetch("/food/food/add", {
                method: "POST",
                body: formData,
            });
            let data = await response.json();
            if (data["errors"]) {
                console.log(data["errors"])
                Array.from(document.querySelectorAll("#food-form .errorlist")).forEach((el)=>{
                    el.classList.add("display-none");
                })
                for (const [key, value] of Object.entries(data["errors"])) {
                    value.forEach((el) => {
                        const li = document.createElement("li");
                        li.innerText = el;
                        if (key == "__all__") {
                            document.querySelector(`#add-food-form-error`).appendChild(li);
                            document.querySelector(`#add-food-form-error`).classList.remove("display-none");

                        } else {
                            document.querySelector(`#add-food-${key}-error`).appendChild(li);
                            document.querySelector(`#add-food-${key}-error`).classList.remove("display-none");

                        }
                    })
                }
            }
            else {
                let newOption = new Option(data["text"], parseInt(data["id"]), false, true);
                $("#" + saveFoodBtn.dataset.toId).append(newOption).trigger("change");
                foodFormDiv.classList.add("display-none");
            }
            
        })
    }

})

