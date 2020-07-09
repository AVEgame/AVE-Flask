function gameRestart() {
    window.location.href = `/play/${filename}`;
}

function gameList() {
    window.location.href = "/play";
}

function poplulateRoomInfo(roomDesc) {
    var roominfo = document.getElementById('roominfo');
    roominfo.innerHTML = "";
    var roomStyle = window.getComputedStyle(roominfo, null);
    var roomWidth = parseFloat(roomStyle.width);
    roomDescLineList = roomDesc.split("\n");
    for (var key in roomDescLineList) {
        var line = roomDescLineList[key];
        if (line == "") {
            roominfo.appendChild(document.createElement('br'));
        }
        else {
            var count = 0;
            lineWords = line.split(" ");
            while (count < lineWords.length) {
                var lineDiv = document.createElement('div');
                lineDiv.style.display = 'inline-block';
                lineDiv.style.whiteSpace = 'nowrap';
                roominfo.appendChild(lineDiv);
                while (lineDiv.offsetWidth < roomWidth && count < lineWords.length) {
                    lineDiv.innerText += " " + lineWords[count];
                    count += 1
                    alert(lineDiv.offsetWidth);
                    alert(roomWidth);
                }
                alert(lineDiv.offsetWidth)
                if (lineDiv.offsetWidth >= roomWidth) {
                    count -= 1
                    var lineDivText = lineDiv.innerText.trim()
                    lineDiv.innerText = lineDivText.substring(0, lineDivText.length - lineWords[count].length).trim()   
                }
                roominfo.appendChild(document.createElement('br'));
            }
        }
        var children = roominfo.childNodes;
        for (var i = 0; i < children.length; i++) {
            var child = children[i];
            if (child.tagName == "DIV") {
                child.classList.add("typewriter");
            }
        }
    }
}

function loadRoom(info) {
    poplulateRoomInfo(info.room_desc);
    var inventory = "INVENTORY";
    info.inventory_text.forEach( item => inventory += `</br>${item}`);
    document.getElementById('inventory').innerHTML = inventory;
    menu = document.getElementById('menu');
    menu.innerHTML = "";
    for (var i = 0; i < info.options.length; i++) {
        div = document.createElement('div');
        div.innerHTML = info.options[i][1];
        div.classList.add("menuitem");
        div.setAttribute("data-key", info.options[i][0])
        div.onclick = function() {
            menuHandler(this);
        }
        menu.appendChild(div);
    }
}

function resetScreen() {
    document.getElementById('roominfo').innerHTML = "";
    document.getElementById('inventory').innerHTML = "";
    document.getElementById('menu').innerHTML = "";
}

function menuHandler(e) {
    resetScreen();
    getNextRoom(e.getAttribute("data-key"));
}

function getNextRoom(option) {
    var data = {
        "current_room": current_room,
        "option": option,
        "inventory": inventory,
        "numbers": numbers
    }
    requestRoom(data);
}

function requestRoom(data) {
    var http = new XMLHttpRequest();
    var url = `/play/${filename}`
    http.open('POST', url, true);
    http.setRequestHeader( "Content-Type", "application/json" );
    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            var returnData = JSON.parse(http.responseText);
            current_room = returnData.room;
            if (current_room == "__GAMEOVER__") {
                document.getElementById("gameendtext").innerHTML="GAME OVER";
                document.getElementById("gameend").style.display="block";
                return;
            }
            if (current_room == "__WINNER__") {
                document.getElementById("gameendtext").innerHTML="You Win!";
                document.getElementById("gameend").style.display="block";
                return;
            }
            inventory = returnData.inventory;
            numbers = returnData.numbers;
            loadRoom(returnData);
        }
        else if (http.readyState == 4 && http.status != 200) {
            var gameDiv = document.getElementById('game');
            var parent = gameDiv.parentNode;
            parent.removeChild(gameDiv);
            var errorDiv = document.createElement('div');
            errorDiv.classList.add("error");
            errorDiv.innerHTML = http.responseText;
            parent.appendChild(errorDiv);
        }
    }
    http.send(JSON.stringify(data));
}

function endGame() {
    menuItems = document.getElementsByClassName('menuitem');
    menuItems.forEach( function(e) {
        e.classList.remove('menuitem');
        e.classList.add('dummymenuitem');
        e.onclick = function() {
            return false;
        }
    })
}
