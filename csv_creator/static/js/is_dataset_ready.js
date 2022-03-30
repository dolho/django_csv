const MessageTypes = {
   IS_CSV_READY: "is_csv_ready",
};

const StatusCSV = {
   PROCESSING: "processing",
   READY: "ready",
   FAILED: "failed"
};

class AppMessage {
   constructor(type = "undefined", payload = null) {
       this.type = type;
       this.payload = payload;
   }
}

// window.addEventListener("load", onLoad, false);

const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsLocation = `${protocol}//${location.host}/ws`;
const websocket = new WebSocket(wsLocation);
websocket.onopen = function(evt) { onOpen(evt) };
websocket.onclose = function(evt) { onClose(evt) };
websocket.onmessage = function(evt) { onMessage(evt) };
websocket.onerror = function(evt) { onError(evt) };


      
 function onOpen(evt) {
    console.log("Opened a websocket")
    addMessage()
 }
      
 function onClose(evt) {
    console.log("Closed a websocket")
 }
      
 function onMessage(evt) {
    const jsonText = evt.data
    console.log(jsonText)
    const messageObject = JSON.parse(jsonText)
    Object.setPrototypeOf(messageObject, AppMessage)
    let type = messageObject.type
      if (type === MessageTypes.IS_CSV_READY) {
          const payload = messageObject.payload
          onIsCSVReady(payload)
      } else {
         throw new Error("Not supported message type:" + messageObject.type);
    }
 }
      
 function onError(evt) {
    console.log("error")
 }
      
 function addMessage() {
   let schema_id = document.getElementById("schema_id").innerText
   let status_of_csvs = document.querySelectorAll('[id^=status]')
   for(let i = 0; i < status_of_csvs.length; i++){
      console.log(status_of_csvs['i'])
      let message = new AppMessage(MessageTypes.IS_CSV_READY, 
                                  {"data_set_id": status_of_csvs[i].id.replace(/^(status)/, ''), 
                                   "schema_id": schema_id})
      // {"type": MessageTypes.IS_CSV_READY,
      //                "payload": status_of_csvs[i].id.replace(/^(status)/, '') }
      websocket.send(JSON.stringify(message));
   }
 }

 function onIsCSVReady(payload) {
   if (payload["status"] == StatusCSV.PROCESSING) {
      setStatusProcessing("status" + payload["id"])
      hide_action(payload["id"])
   } else if (payload["status"] == StatusCSV.READY) {
      setStatusReady("status" + payload["id"])
      unhide_action(payload["id"])
      set_time(payload["id"], payload["time"])
      set_download_path(payload["id"], payload["path"])
   }
 }

 function setStatusReady(status_id) {
    let element_to_replace = document.getElementById(status_id)
    if (!element_to_replace) {
       throw Error("No element with such id " + status_id)
    }
    let ready_button = document.createElement("div")
    ready_button.id = status_id
    ready_button.innerText = "Ready"
    ready_button.classList.add("btn", "btn-success", "full-opacity", "disabled" )
    ready_button.style.opacity = 1
    element_to_replace.replaceWith(ready_button)
    
 }

 function setStatusProcessing(status_id) {
   let element_to_replace = document.getElementById(status_id)
   if (!element_to_replace) {
      throw Error("No element with such id " + status_id)
   }
   let ready_button = document.createElement("div")
   ready_button.id = status_id
   ready_button.innerText = "Processing"
   ready_button.classList.add("btn", "btn-secondary", "full-opacity", "disabled")
   ready_button.style.opacity = 1
   element_to_replace.replaceWith(ready_button)
 }

 function hide_action(uuid) {
   let element_to_hide = document.getElementById("action" + uuid)
   element_to_hide.style.visibility = "hidden"
 }

 function unhide_action(uuid) {
   let element_to_unhide = document.getElementById("action" + uuid)
   element_to_unhide.style.visibility = "visible"
 }

 function set_time(uuid, time) {
   document.getElementById("time" + uuid).innerText = time
 }

 function set_download_path(uuid, path) {
   document.getElementById("download" + uuid).action = path
 }