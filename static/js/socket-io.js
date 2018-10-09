// const socket = io.connect('http://10.21.20.162:9806');
const socket = io.connect('http://10.21.20.52:9806');
// const socket = io.connect('http://127.0.0.1:3000');

const ul_A = document.getElementById("listA");
const ul_B = document.getElementById("listB");

let userSendMsg = "";

socket.on('publishReturn', function (evt) {
    console.log('publishReturn');
    console.log(evt);
    try {
        let data = evt.data;
        if (data == userSendMsg) {
            console.log(data);
            //send message from a to b
            var li_A = document.createElement("li");
            li_A.innerHTML = "<div class = 'message-a-to-a-sty' ><div>" + data + "</div></div>";
            ul_A.appendChild(li_A);

            //     var li_B = document.createElement("li");
            //     li_B.innerHTML = "<div class = 'message-a-to-b-sty' ><img src='/static/img/A.jpg' alt='A' width='31px' height='31px'><div>" + data.message + "</div></div>";
            //     ul_B.appendChild(li_B);

            let listA = document.getElementById("listA");
            listA.scrollTop = listA.scrollHeight;
            userSendMsg = "";
            //     let listB = document.getElementById("listB");
            //     listB.scrollTop = listB.scrollHeight;
        } else {
            if (data == 'create' || data == 'exist' || data == 'exit' || data == 'kill') {
                //send message from b to a
                let li_A = document.createElement("li");
                li_A.innerHTML = "<div class = 'message-b-to-a-sty' ><img src='/static/img/B.jpg' alt='B' class='message-img' width='31px' class='message-img' height='31px'><div>" + 'publish狀態：' + data + "</div></div>"
                ul_A.appendChild(li_A);
                let listA = document.getElementById("listA");
                listA.scrollTop = listA.scrollHeight;
                userSendMsg = "";
            } else {
                console.log(data)
                //send message from b to a
                let li_A = document.createElement("li");
                li_A.innerHTML = "<div class = 'message-b-to-a-sty' ><img src='/static/img/B.jpg' alt='B' class='message-img' width='31px' height='31px'><div>" + data + "</div></div>"
                ul_A.appendChild(li_A);
                let listA = document.getElementById("listA");
                listA.scrollTop = listA.scrollHeight;
                userSendMsg = "";
            }
            //     //send message from b to b
            //     let li_B = document.createElement("li");
            //     li_B.innerHTML = "<div class = 'message-b-to-b-sty' ><div>" + data.message + "</div></div>";
            //     ul_B.appendChild(li_B);

            //     let listB = document.getElementById("listB");
            //     listB.scrollTop = listB.scrollHeight;
        }
    } catch (error) {
        console.log("json error");
    }
    // var msg = $('<div>').append(evt.data);
    // $('#messages').append(msg);
});

socket.on('subscriberReturn', function (evt) {
    console.log('subscriberReturn');
    console.log(evt);
    let data = evt.data;
    try {
        //send message from b to a
        let li_A = document.createElement("li");
        li_A.innerHTML = "<div class = 'message-b-to-a-sty' ><img src='/static/img/B.jpg' alt='B' class='message-img' width='31px' height='31px'><div>" + 'subscriber狀態：' + data + "</div></div>"
        ul_A.appendChild(li_A);
        let listA = document.getElementById("listA");
        listA.scrollTop = listA.scrollHeight;
        userSendMsg = "";
    } catch (error) {
        console.log("a json error");
    }
});

socket.on('subscriberRecevie', function (evt) {
    console.log('subscriberRecevie');
    console.log(evt);
    let data = evt.data;
    try {
        //send message from b to a
        let li_A = document.createElement("li");
        li_A.innerHTML = "<div class = 'message-b-to-a-sty' ><img src='/static/img/B.jpg' alt='B' class='message-img' width='31px' height='31px'><div>" + 'subscriber狀態：' + data + "</div></div>"
        ul_A.appendChild(li_A);
        let listA = document.getElementById("listA");
        listA.scrollTop = listA.scrollHeight;
        userSendMsg = "";
    } catch (error) {
        console.log("b json error");
    }
});

$(function () {
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

    $('#publishCreate').on('click', function () {
        // {"active":"create","cmd":"./publisher -DCPSConfigFile rtps.ini","topic":"A"}
        let ini = $('#publishIni').val();
        let topic = $('#publishTopic').val();
        socket.emit('publishSend', {
            "active": "create",
            "cmd": "./publisher -DCPSConfigFile " + ini,
            "topic": topic
        });
        $('#publishTopic').val('');
    });

    $('#publishStatus').on('click', function () {
        socket.emit('publishSend', {
            "active": "status"
        });
    });

    $('#publishExit').on('click', function () {
        socket.emit('publishSend', {
            "active": "exit"
        });
    });

    $('#publishKill').on('click', function () {
        socket.emit('publishSend', {
            "active": "kill"
        });
    });

    $('#subscriberCreate').on('click', function () {
        let ini = $('#subscriberIni').val();
        let topic = $('#subscriberTopic').val();
        console.log(ini, topic);
        socket.emit('subscriberSend', {
            "active": "create",
            "cmd": "./subscriber -DCPSConfigFile " + ini,
            "topic": topic
        });
        $('#subscriberTopic').val('');
    });

    $('#subscriberStart').on('click', function () {
        socket.emit('subscriberRecevieStart', 'start');
    });

    $('#subscriberStatus').on('click', function () {
        socket.emit('subscriberSend', {
            "active": "status"
        });
    });

    $('#subscriberExit').on('click', function () {
        socket.emit('subscriberSend', {
            "active": "exit"
        });
    });

    $('#subscriberKill').on('click', function () {
        socket.emit('subscriberSend', {
            "active": "kill"
        });
    });

    $('#sendA').on('click', function () {
        let message = $('#msgA').val();
        userSendMsg = message;
        socket.emit('publishSend', {
            "send": message
        });
    });
});