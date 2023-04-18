document.querySelector('#room-name-input').focus();
document.querySelector('#room-name-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.querySelector('#room-name-submit').click();
    }
};

document.querySelector('#room-name-submit').onclick = function(e) {
    var roomName = document.querySelector('#room-name-input').value;
    if (/^[a-z0-9\s]+$/i.test(roomName)) {
        window.location.pathname = '/appchat/' + roomName + '/';

    } else { alert('Название комнаты только из латинских букв, цифр и пробелов'); }
};

function roomsList(rooms) {
    if (rooms.length != 0) {
        roomsOpened = '';
        for (let r of rooms) {
            roomsOpened += `<p><a href="` + r + `/">` + r + `</a></p>`;
        }
    } else {
        roomsOpened = `На данный момент нет созданных комнат. Вы можете создать свою нажав кнопку выше!`
    };
    document.getElementById("rooms-list").innerHTML = roomsOpened;
}

async function roomsLoader(callback) {
    const roomsUpload = await fetch('./roomsupdate/')
            .then(response => response.json());
    callback(roomsUpload);
};

rooms = JSON.parse(document.getElementById('rooms').textContent);
roomsList(rooms);
setTimeout(roomsLoader, 1000, roomsList);
setInterval(roomsLoader, 30000, roomsList);

// focus 'roomInput' when user opens the page
document.querySelector("#roomInput").focus();

// submit if the user presses the enter key
document.querySelector("#roomInput").onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        document.querySelector("#roomConnect").click();
    }
};

// redirect to '/room/<roomInput>/'
document.querySelector("#roomConnect").onclick = function() {
    let roomName = document.querySelector("#roomInput").value;
    window.location.pathname = "/appchat/" + roomName + "/";
}

// redirect to '/room/<roomSelect>/'
document.querySelector("#roomSelect").onchange = function() {
    let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
    window.location.pathname = "/appchat/" + roomName + "/";
}