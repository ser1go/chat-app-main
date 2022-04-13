document.addEventListener('DOMContentLoaded', () => {

     // Кнопка мобильного меню
     document.querySelector('#menu_button').onclick = () =>{
        document.querySelector('#nav-menu').classList.toggle('menu-show');
    }

    // Отправка сообщения по Enter
    let msg = document.querySelector('#user_message');
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13){
            document.querySelector('#send_message').click();
        }
    })
})