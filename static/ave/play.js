function gameRestart() {
    window.location.href = `/play/${filename}`;
}

function gameList() {
    window.location.href = "/play";
}

function loadRoom(info) {
    document.getElementById('roominfo').innerHTML = info.roominfo;
    var inventory = "INVENTORY";
    info.inventory.forEach( item => inventory += `</br>${item}`);
    document.getElementById('inventory').innerHTML = inventory;
    menu = document.getElementById('menu');
    menu.innerHTML = "";
    for (var i = 0; i < info.options.length; i++) {
        div = document.createElement('div');
        div.innerHTML = info.options[i].desc;
        div.classList.add("menuitem");
        div.onclick = function() {

        }
    }
    info.options.forEach( function(option) {
        div = document.createElement('div');
        div.innerHTML = option.desc;
        div.classList.add("menuitem");
        div.onclick = function() {
            menuHandler(this)
        }
        menu.appendChild(div);
    }
    )
}

function resetScreen() {
    document.getElementById('roominfo').innerHTML = "";
    document.getElementById('inventory').innerHTML = "";
    document.getElementById('menu').innerHTML = "";
}

function menuHandler(e) {
    i = Array.from(e.parentNode.children).indexOf(e);
    resetScreen();
    getNextRoom(current_room, i);
}

function getNextRoom(current_room, option) {
    var http = new XMLHttpRequest();
    var url = `/play/${filename}`
    var data = {
        "current_room": current_room,
        "option": option,
        "inventory": inventory
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
            loadRoom(returnData.info);
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