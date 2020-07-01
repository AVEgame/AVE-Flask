function gameRestart() {
    window.location.href = `/play/${filename}`;
}

function gameList() {
    window.location.href = "/play";
}

function loadRoom(info) {
    document.getElementById('roominfo').innerHTML = info.room_desc;
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
    var http = new XMLHttpRequest();
    var url = `/play/${filename}`
    var data = {
        "current_room": current_room,
        "option": option,
        "inventory": inventory,
        "numbers": numbers
    }
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