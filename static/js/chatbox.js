            base_url =  document.location.origin;
            const roomName = JSON.parse(document.getElementById('room-name').textContent);
            const userName = JSON.parse(document.getElementById('user_username').textContent);

            const chatSocket = new WebSocket(
                'ws://'
                + window.location.host
                + '/ws/appchat/'
                + roomName
                + '/'
            );

            chatSocket.onmessage = async function (e) {
                const data = JSON.parse(e.data);
                suffix = data.from === 'room' ? '' : ' написал тебе';
                document.querySelector('#chat-text').value += data.username.toUpperCase() + suffix + ' : '
                    + data.message  + '\n';
                scrollToBottom();
                await usersOfRoom(data.usernames);
            };

            chatSocket.onclose = function(e) {
                console.error('Сокет чата неожиданно закрылся с ошибкой:', e);
            };

            document.addEventListener('submit', function (e) {
                e.preventDefault();
                document.querySelector('#chat-message-submit').click();
            });

            document.querySelector('#chat-message-submit').addEventListener('click', function (e) {
                const messageInputDom = document.querySelector('#chat-message-input');
                const message = messageInputDom.value;
                chatSocket.send(JSON.stringify({
                    'type': 'text_message',
                    'message': message,
                    'username': userName,
                    'whom': 'room',
                }));
                messageInputDom.value = '';
                return false;
            });

            document.querySelector('#leave-room-submit').addEventListener('click', function (e) {
                document.location.replace(`${base_url}/appchat/`);
            });

            function scrollToBottom() {
                let objDiv = document.querySelector('#chat-text');
                objDiv.scrollTop = objDiv.scrollHeight;
            };

            function sendToUser(channelName) {
                tagS = `${channelName.split('!')[1]}-input`;
                const messageInputDom = document.getElementById(tagS);
                const message = messageInputDom.value;
                chatSocket.send(JSON.stringify({
                    'type': 'text_message',
                    'message': message,
                    'username': userName,
                    'whom': channelName,
                }));
                messageInputDom.value = '';
                return false;
            };

            function closeToUser(tagClose) {
                removed = document.getElementById(tagClose);
                document.getElementById('connections').removeChild(removed);
            };

            function writeToUser (channelName, userName) {
                tagP = `p-${channelName.split('!')[1]}`;
                tagS = `${channelName.split('!')[1]}`;
                userMessageInput = `<div id="` + tagS + `-close"><div class="form-group">`
                    + `<input class="form-control" placeholder="Сообщение для ` + userName + ` напишите тут" id="` + tagS
                    + `-input" type="text"/></div>`
                    + `<div style="display: flex;"><input class="btn btn-primary" id="` + tagS + `-submit" type="button" `
                    + `onClick="sendToUser('` + channelName + `')" style="width: 50%;" value="Написать ` + userName
                    + `"/>&nbsp;<input class="btn btn-primary" type="button" `
                    + `onClick="closeToUser('` + tagS + `-close')" style="width: 50%;" value="Закрыть"/></div><br></div>`;
                document.getElementById('connections').innerHTML += userMessageInput;
            };

            function usersOfRoom (userDict) {
                if (userDict != 0) {
                    document.querySelector('#users-in-room').innerHTML = '';
                }
                for (let u in userDict) {
                    tagU = u.split('!')[1];
                    roomUser = `<p id="p-` + tagU + `"><button input class="btn btn-primary type="button" id="` + tagU + `" onClick="writeToUser('`
                        + u + `', '` + userDict[u] + `')">` + userDict[u] + `</button></p>`;
                    document.querySelector('#users-in-room').insertAdjacentHTML('beforeend', roomUser);
                }
            };