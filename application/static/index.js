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