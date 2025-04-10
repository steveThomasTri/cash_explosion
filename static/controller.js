date = localStorage.getItem("date")
player = localStorage.getItem("player#")

if ((date == null) || (player == null) || (date == "") || ( player == 0)){
    window.location.replace("/splash");
}