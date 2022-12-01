document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect();
    //receive details from server
    socket.on("live_data", function (msg) {
        let match_data = msg.payload
        for (let i = 0; i < match_data.length; i++){
            document.querySelector(`.current_match[id='${match_data[i].id}'] #scoreline`).innerHTML = `${match_data[i].home} : ${match_data[i].away}`;
            document.querySelector(`.current_match[id='${match_data[i].id}'] #status`).innerHTML = match_data[i].status;
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
            document.querySelector(".navbar").style.display = 'block';
        }, 2500);
    });
