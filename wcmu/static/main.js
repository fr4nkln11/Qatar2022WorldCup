let auto_reload = async () => {
    let scores
    await fetch('/reload_scores').then((response) => {
                return response.json();
            }).then((array) => {
                scores = array
            });
    let scorelines = document.querySelectorAll("#scoreline")
    for (let i = 0; i < scorelines.length; i++){
        scorelines[i].innerHTML = `${scores[i].home} : ${scores[i].away}`
    }
    setTimeout(auto_reload, 10000);
}

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