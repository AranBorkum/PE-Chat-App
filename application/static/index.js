$(document).ready(function () {
   var socket = io.connect('http://127.0.0.1:5000')
   socket.on('connect', function () {
        socket.send('User connected!');
   });

   socket.on('message', async function (data) {
       await $('#messages').append($('<p>').text(data));
       await scrollSmoothToBottom('messages')
   });

   $('#sendBtn').on('click', function () {
       if ($('#message').val() !== '') {
           socket.send($('#username').text() + ': ' + $('#message').val());
           socket.emit($('#username').text() + ': ' + $('#message').val());
           $('#message').val('');
       }
   });

   $('#message').on('keypress', function (event) {
       if (event.key === 'Enter') {
            if ($('#message').val() !== '') {
                socket.send($('#username').text() + ': ' + $('#message').val());
                socket.emit($('#username').text() + ': ' + $('#message').val());
                $('#message').val('');
            }
       }
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