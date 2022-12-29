$(document).ready(function () {
   var socket = io.connect('http://127.0.0.1:5000')
   socket.on('connect', function () {
        socket.send('User connected!');
   });

   socket.on('message', function (data) {
       $('#messages').append($('<p>').text(data));
       scrollSmoothToBottom('messages')
   });

   $('#sendBtn').on('click', function () {
       socket.send($('#username').val() + ': ' + $('#message').val());
       $('#message').val('');
   });
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