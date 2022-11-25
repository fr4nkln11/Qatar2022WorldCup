document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect();
    //receive details from server
    socket.on("fresh_data", function (msg) {
        scores = msg.scores
        let scorelines = document.querySelectorAll("#scoreline")
        for (let i = 0; i < scorelines.length; i++){
            scorelines[i].innerHTML = `${scores[i].home} : ${scores[i].away}`
        }
    });
});