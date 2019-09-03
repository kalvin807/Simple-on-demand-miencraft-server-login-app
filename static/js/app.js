$("document").ready(function () {
    wallpaper()
    serverStatus()
    $("#start").click(function () {
        auth()
    });
    $("#status").on("click", function () {
        serverStatus()
    });
});

//Wallpaper change according to the client time
function wallpaper() {
    var d = new Date();
    var n = d.getHours();
    if (n > 18 || n < 6)
        
        document.body.className = "night";
    else

        document.body.className = "day";
}

//Function to send a POST ajax to authorise the server start up
function auth() {
    var pwd = $("#pwd").val();
    $.ajax({
        url: $SCRIPT_ROOT + '/auth',
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "pwd": pwd })
    }).done(function (data) {
        //UI Response according to the result
        if (data.status == 0) {
            $('#msg').html('<div class="alert alert-success msg-box" id="ok" role="alert"><strong>Ok!</strong> Server is starting!<br>(Wait ~5 mins)</div>');
        }
        if (data.status == 1) {
            $('#msg').html('<div class="alert alert-warning msg-box" id="warn" role="alert"><strong>Oops...</strong> Server already running!</div>');
        }
        if (data.status == 2) {
            $('#msg').html('<div class="alert alert-danger msg-box" id="err" role="alert"><strong>Nope.</strong> Wrong magic word!</div>');
        }
    });
}

//Function to send a GET request to get server current status
function serverStatus() {
    $('#status').html('Server is <span class="badge badge-pill badge-secondary">Loading</span> <i class="fa fa-refresh refresh" id="status-refresh"></i>');
    $.ajax({
        url: $SCRIPT_ROOT + '/status',
        type: 'GET',
        success: function (data) {
            //The server status change according to the data returned
            switch (data.status) {
                case 0:
                    $('#status').html('Server is <span class="badge badge-pill badge-danger">Offline</span> <i class="fa fa-refresh refresh" id="status-refresh"aria-hidden="true"></i>');
                    break;
                case 1:
                    $('#status').html('Server is <span class="badge badge-pill badge-success">Online</span> | Minecraft Version is <span class="badge badge-pill badge-info">' + data.mc_version + '</span> | Online Player is <span class="badge badge-pill badge-info">' + data.online_player + '</span> <i class="fa fa-refresh refresh" id="status-refresh" aria-hidden="true"></i>')
                    break;
                case 2:
                    $('#status').html('Server is <span class="badge badge-pill badge-warning">Starting</span> <i class="fa fa-refresh refresh" id="status-refresh" aria-hidden="true"></i>')
                    break;
                case 3:
                    $('#status').html('Server is <span class="badge badge-pill badge-danger">Crashed</span> <i class="fa fa-refresh refresh" id="status-refresh" aria-hidden="true"></i>')
                    break;
                default:
                    $('#status').html('<span class="badge badge-pill badge-danger">Error</span> Find admin for help <i class="fa fa-refresh refresh" id="status-refresh" aria-hidden="true"></i>')
                    break;
            }

        },
        error: function () {
            $('#status').html('<span class="badge badge-pill badge-danger">Error</span> Find admin for help <i class="fa fa-refresh refresh" id="status-refresh"></i>')
        }
    });
}
