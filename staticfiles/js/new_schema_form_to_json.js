

function convert_form_to_json(event) {
    event.preventDefault()
    let form_dict = {'columns': []}
    let column = {}
    let re_column_order = /\d+/
    let re_column_name = /[a-zA-Z]+/g
    let current_order = 0;
    for (i = 0; i < event.target.length; i++) {
        if (event.target[i].id.startsWith("column")) {
            let order = re_column_order.exec(event.target[i].id)[0]
            let name = event.target[i].id.match(re_column_name).join("")
            if (current_order == order) {
                if (name == 'columnTypeFrom' ) {
                    if (column['columnType'] != "integer") {
                        continue
                    } else {
                        column['from'] = event.target[i].value 
                    } 
                } else if (name == "columnTypeTo") {
                    if (column['columnType'] != "integer") {
                        continue
                    } else {
                        column['to'] = event.target[i].value 
                    } 
                } else {
                    column[name] = event.target[i].value
                }
            } else {
                form_dict['columns'].push(column)
                column = {}
                column[name] = event.target[i].value
                current_order += 1
            }
        } else {
            form_dict[event.target[i].id] = event.target[i].value
        }
    }
    form_dict['columns'].push(column)

    var oReq = new XMLHttpRequest();
    oReq.onreadystatechange = function(data) {
        if (this.readyState !== 4) {
            return
        }
        if (this.status === 200 ) {
            location.href = this.responseURL
          } 
        if (this.status === 403) {
            console.log(data)
            let data_json = JSON.parse(oReq.responseText)
            alert(data_json['error'])
        }
      };
    oReq.open("POST",  document.getElementById('schema_creation').getAttribute("action"))
    oReq.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
    oReq.setRequestHeader('Content-Type', 'application/json;charset=UTF-8')
    oReq.send(JSON.stringify(form_dict));
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}