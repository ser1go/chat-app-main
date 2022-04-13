document.addEventListener('DOMContentLoaded', () =>{
    var socket = io();

    let room = "Общение"
    joinRoom("Общение");

    // Отображение сообщений
    socket.on('message',data => {
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')
            // Отображение собственных сообщений
            if (data.username == username) {
                    p.setAttribute("class", "my-msg");

                    // Имя пользователя
                    span_username.setAttribute("class", "my-username");
                    span_username.innerText = data.username;

                    // Модуль со временем сообщения
                    span_timestamp.setAttribute("class", "timestamp");
                    span_timestamp.innerText = data.time_stamp;

                    // HTML для внесения
                    p.innerHTML += span_username.outerHTML + span_timestamp.outerHTML + br.outerHTML + data.msg;

                    //Внесение
                    document.querySelector('#message_window').append(p);
            }
            // Отображение сообщений других пользователей
            else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");

                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML для внесения
                p.innerHTML += span_username.outerHTML + span_timestamp.outerHTML + br.outerHTML + data.msg;

                //Внесение
                document.querySelector('#message_window').append(p);
            }
            // Отображение системного сообщения
            else {
                printSysMsg(data.msg);
            }


        }
        scrollDownChatWindow();
    });

    // Отправка сообщения на сервер
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 'username': username, 'room':room});
        // Очищение инпута после отправки
        document.querySelector('#user_message').value='';
    }

    // Выбор чата
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room){
                msg=`Вы уже находитесь в чате ${room}.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room=newRoom;
            }
        }
    })
    // Кнопка выхода
    document.querySelector('#logout_button').onclick = () => {
        leaveRoom(room)
    }

    // Покинуть чат
    function leaveRoom(room){
        socket.emit('leave', {'username': username, 'room': room});
        document.querySelectorAll('.select-room').forEach(p => {
            p.style.backgroundColor = "#189AB4";
        });
    }
    // Присоединиться к чату
    function joinRoom(room){
        socket.emit('join', {'username':username, 'room':room});
        document.querySelector('#message_window').innerHTML = '';
        // Автофокус на поле ввода
        document.querySelector('#user_message').focus();
        // Подстветка, в каком чате в данный момент пользователь
        document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "aqua";
    }
    // Скролл чата
    function scrollDownChatWindow(){
        const chatWindow = document.querySelector("#message_window");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
    //вывод системных сообщений
    function printSysMsg(msg){
        const p = document.createElement('p');
        p.setAttribute("class", "sys-msg");
        p.innerHTML = msg;
        document.querySelector('#message_window').append(p);
    }
})