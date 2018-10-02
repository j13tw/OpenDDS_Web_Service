const socket = io.connect('http://10.21.20.52:9806');
// const socket = io.connect('http://127.0.0.1:3000');

const ul_A = document.getElementById("listA");
const ul_B = document.getElementById("listB");

socket.on('publishReturn', function (evt) {
    console.log('Got Message');
    console.log(evt);
    try {
        let data = JSON.parse(evt.data);
        console.log(data);
        if (data.from == 'A') {
            console.log(data.message);
            //send message from a to b
            var li_A = document.createElement("li");
            li_A.innerHTML = "<div class = 'message-a-to-a-sty' ><div>" + data.message + "</div></div>";
            ul_A.appendChild(li_A);

            var li_B = document.createElement("li");
            li_B.innerHTML = "<div class = 'message-a-to-b-sty' ><img src='/static/img/A.jpg' alt='A' width='31px' height='31px'><div>" + data.message + "</div></div>";
            ul_B.appendChild(li_B);

            let listA = document.getElementById("listA");
            listA.scrollTop = listA.scrollHeight;
            let listB = document.getElementById("listB");
            listB.scrollTop = listB.scrollHeight;
        } else if (data.from == 'B') {
            //send message from b to a
            let li_A = document.createElement("li");
            li_A.innerHTML = "<div class = 'message-b-to-a-sty' ><img src='/static/img/B.jpg' alt='B' width='31px' height='31px'><div>" + data.message + "</div></div>"
            ul_A.appendChild(li_A);
            //send message from b to b
            let li_B = document.createElement("li");
            li_B.innerHTML = "<div class = 'message-b-to-b-sty' ><div>" + data.message + "</div></div>";
            ul_B.appendChild(li_B);

            let listA = document.getElementById("listA");
            listA.scrollTop = listA.scrollHeight;
            let listB = document.getElementById("listB");
            listB.scrollTop = listB.scrollHeight;
        }
    } catch (error) {
        console.log("json error");
    }
    // var msg = $('<div>').append(evt.data);
    // $('#messages').append(msg);
});

$(function () {
    socket.emit('publishSend', { "active": "create", "cmd": "./publisher -DCPSConfigFile rtps.ini", "topic": "A" });
    $('#sendA').on('click', function () {
        let message = JSON.stringify({ 'from': 'A', 'message': $('#msgA').val() });
        console.log($('#msgA').val() != 'status' && $('#msgA').val() != 'exit' ? message : $('#msgA').val());
        socket.emit('publishSend', {
            'send': $('#msgA').val() != 'status' && $('#msgA').val() != 'exit' ? message : $('#msgA').val()
        });
        $('#msgA').val('');
    });

    $('#sendB').on('click', function () {
        let message = JSON.stringify({ 'from': 'B', 'message': $('#msgB').val() });
        console.log($('#msgB').val() != 'status' && $('#msgB').val() != 'exit' ? message : $('#msgB').val());
        socket.emit('publishSend', {
            'send': $('#msgB').val() != 'status' && $('#msgB').val() != 'exit' ? message : $('#msgB').val()
        });
        $('#msgB').val('');
    });
});