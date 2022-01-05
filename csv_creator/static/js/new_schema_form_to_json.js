

function convert_form_to_json(event) {
    event.preventDefault()
    let form_dict = {};
    for (i = 0; i < event.target.length; i++) {
        console.log(event.target[i])
        form_dict[event.target[i].id] = event.target[i].value
    }
    console.log("-----------------------------------------------")
    console.log(form_dict)
}