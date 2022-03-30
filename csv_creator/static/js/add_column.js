
var order = 0

function set_current_order() {
    console.log("set current order worked")
    let new_order = document.getElementById("currentOrder").innerText
    console.log("New order ", new_order)
    if (new_order) {
        order = parseInt(new_order) + 1
        console.log("Global order", order)
        return order
    } else {
        order = 0
        return 0 
    }
    
    
}
set_current_order()

// function increment_order() {
//     let order = current_order()
//     order += 1
//     document.getElementById("currentOrder").value = order
//     return order
// }

function add_column() {
    
    

    var inputs = document.getElementById("columnCreator").querySelectorAll("input,select,label");  
    // console.log(inputs);
    console.log(order)

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].id.startsWith('columnOrder')) {
            inputs[i].value = order
            inputs[i].id += order
        } 
        else if (inputs[i].id.startsWith('columnTypeFrom')) {
            inputs[i].id = "columnType" + order + "From"
        }
        else if (inputs[i].id.startsWith('columnTypeTo')) {
            inputs[i].id = "columnType" + order + "To"
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
        if (inputs[i].id.startsWith('columnType')) {
            if (inputs[i].id.endsWith('From')) {
                inputs[i].id = 'columnType' + 'From'
            }
            else if (inputs[i].id.endsWith('To')) {
                inputs[i].id = 'columnType' + 'To'
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