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