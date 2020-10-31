var socket = new WebSocket('ws://192.168.1.129:5000/ws');

socket.onopen = function(event) {
    console.log("Connection established");
    // Display user friendly messages for the successful establishment of connection
    var label = document.getElementById("status");
    label.innerHTML = "Connection established";
 }

 socket.onmessage = function(message) {
    console.log("Message Received" + message);
 }


 document.getElementById('capture_frame').onsubmit = function() { 
   socket.send("CLICKED!");
    return false;
};

function capture_frame() {
    socket.send("Capture Frame")
    return
  }