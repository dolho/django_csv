var order = 0


function add_column() {
    

    var inputs = document.getElementById("columnCreator").querySelectorAll("input,select,label");  
    // console.log(inputs);
    // console.log(order)

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].id.startsWith('order')) {
            inputs[i].value = order
            inputs[i].id += order
        } 
        else if (inputs[i].id.startsWith('customSelectAFrom')) {
            inputs[i].id = "customSelectA" + order + "From"
        }
        else if (inputs[i].id.startsWith('customSelectATo')) {
            inputs[i].id = "customSelectA" + order + "To"
        } else {
            inputs[i].id += order
        }
        inputs[i].setAttribute("name", inputs[i].id)
    }
    let original_element = document.getElementById("userCreatedColumn")
    let element = original_element.cloneNode(true)
    element.id += order
    document.getElementById('listOfColumns').append(element)

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].id.startsWith('customSelectA')) {
            if (inputs[i].id.endsWith('From')) {
                inputs[i].id = 'customSelectA' + 'From'
            }
            else if (inputs[i].id.endsWith('To')) {
                inputs[i].id = 'customSelectA' + 'To'
            }
            else {
                inputs[i].id = inputs[i].id.substring(0, inputs[i].id.indexOf(order.toString()))
            }
        } else {
            inputs[i].id = inputs[i].id.substring(0, inputs[i].id.indexOf(order.toString()))
        }
        inputs[i].removeAttribute("name")
    }
    order++

}


function update_select(val){
    Array.from(val.options).forEach(option => option.removeAttribute('selected'))
    val.options[val.selectedIndex].setAttribute("selected","");
    console.log(val.id)
    if (val.options[val.selectedIndex].innerText == "Integer") {
        document.getElementById(val.id + "From").parentElement.classList.remove('hidden')
        document.getElementById(val.id + "To").parentElement.classList.remove('hidden')
    } else {
        document.getElementById(val.id + "From").parentElement.classList.add('hidden')
        document.getElementById(val.id + "To").parentElement.classList.add('hidden')
    }
  }