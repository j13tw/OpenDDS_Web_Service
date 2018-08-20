// var wsUrl = 'ws://127.0.0.1:3000';
// var websocket = new WebSocket(wsUrl);
// websocket.onopen = function(evt) {
//     console.log('Connected');
//     // websocket.send('Hello Server!');
// };
// websocket.onclose = function(evt) {
//     console.log('DisConnected');
// };
// websocket.onmessage = function(evt) {
//     console.log('Got Message');
//     console.log(evt.data);
//     // var msg = $('<div>').append(evt.data);
//     // $('#messages').append(msg);
// };
// websocket.onerror = function(evt) {
//     console.log('Something\'s wrong');
// };

$(function() {
    var ul_A = document.getElementById("listA");
    var ul_B = document.getElementById("listB");
    $('#sendA').on('click', function() {
        // websocket.send($('#msgA').val());
        //send message from a to b
        var li_A = document.createElement("li");
        li_A.innerHTML = "<div class = 'message-a-to-a-sty' ><div>" + $('#msgA').val() + "</div></div>";
        ul_A.appendChild(li_A);

        var li_B = document.createElement("li");
        // li.appendChild(document.createTextNode("Four"));
        li_B.innerHTML = "<div class = 'message-a-to-b-sty' ><img src='/static/img/A.jpg' alt='A' width='31px' height='31px'><div>" + $('#msgA').val() + "</div></div>";
        ul_B.appendChild(li_B);
        let listA = document.getElementById("listA");
        listA.scrollTop = listA.scrollHeight;
        let listB = document.getElementById("listB");
        listB.scrollTop = listB.scrollHeight;
        $('#msgA').val('');
    });

    $('#sendB').on('click', function() {
        // websocket.send($('#msgB').val());
        //send message from b to a
        let li_A = document.createElement("li");
        li_A.innerHTML = "<div class = 'message-b-to-a-sty' ><img src='/static/img/B.jpg' alt='B' width='31px' height='31px'><div>" + $('#msgB').val() + "</div></div>"
        ul_A.appendChild(li_A);
        //send message from b to b
        let li_B = document.createElement("li");
        li_B.innerHTML = "<div class = 'message-b-to-b-sty' ><div>" + $('#msgB').val() + "</div></div>";
        ul_B.appendChild(li_B);

        let listA = document.getElementById("listA");
        listA.scrollTop = listA.scrollHeight;
        let listB = document.getElementById("listB");
        listB.scrollTop = listB.scrollHeight;
        $('#msgB').val('');
    });
});