date = localStorage.getItem("date")
player = localStorage.getItem("player#")
page = window.location.pathname


if ((date == null) || (player == null) || (date == "") || ( player == 0)){
    //
    if (page != "/splash"){
        window.location.replace("/splash");
    }
}

if ((date != "") && ((player > 0) && (player <= 8))){
    if (page != "/"){
        window.location.replace("/");
    }
}

if ((date != "") && (player == 9)){
    if (page != "/endgame"){
        window.location.replace("/endgame");
    }
}