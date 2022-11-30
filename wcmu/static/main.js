document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect();
    //receive details from server
    socket.on("fresh_data", function (msg) {
        let scores = msg.scores
        let status = JSON.parse(msg.status)
        let status_board = document.querySelectorAll("#match_status")
        let scorelines = document.querySelectorAll("#scoreline")
        for (let i = 0; i < scorelines.length; i++){
            scorelines[i].innerHTML = `${scores[i].home} : ${scores[i].away}`
        }
        for (let i = 0; i < status_board.length; i++){
            status_board[i].innerHTML = status[i]
        }
        console.log("success");
    });
});

    window.addEventListener('load',() => {
        mod = new bootstrap.Modal(document.querySelector("#splashModal"), {backdrop: false});
        mod.show();
        setTimeout(() => {           
            document.querySelector(".splash").style.transform = "translate(0, -20%)";
            document.querySelector(".splash").style.opacity = '0'
            document.querySelector(".splash").addEventListener('transitionend', () => {mod.hide()});
            document.querySelector(".container").style.display = 'block';
        }, 3500);
    });
