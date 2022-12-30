$(document).ready(function () {
   var socket = io.connect('http://192.168.0.2:5000')
   socket.on('connect', function () {
        socket.send('User connected!');
   });

   socket.on('message', async function (data) {
       await $('#messages').append($('<p>').text(data));
       await scrollSmoothToBottom('messages')
   });

   $('form#messageForm').on('submit', function (event) {
       let message_input = document.getElementById('message');
       let username = document.getElementById('username')

       socket.send(username.innerText + ': ' + message_input.value);
       socket.emit(username.innerText + ': ' + message_input.value);
       message_input.value = '';
   })

   var messageBox = document.getElementById('messages');
   messageBox.scrollTop = messageBox.scrollHeight;

});

function scrollSmoothToBottom(id) {
  var div = document.getElementById(id);
  $("#" + id).animate(
    {
      scrollTop: div.scrollHeight - div.clientHeight,
    },
    500
  );
}

function getData(form) {
    var formData = new FormData(form);
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
    }
}

document.getElementById('messageForm').addEventListener('submit', function (e) {
    e.preventDefault();
    getData(e.target);
})
