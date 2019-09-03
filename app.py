from flask import Flask, render_template, request, jsonify
from mcstatus import MinecraftServer
from server import getInstanceInfo, startThread, getInitializing
from configuration import Config
from os import urandom


app = Flask(__name__)
app.secret_key = urandom(24)

#Homepage
@app.route("/")
def index():
    return render_template("index.html")

#Handling login POST event 
@app.route("/auth", methods=["POST"])
def auth():
    response = request.get_json()
    password = response["pwd"]
    if password == Config.SERVER_PASSWORD:
        server = startThread()
        if server == 0:
            response = {"status": 0}
        else:
            response = {"status": 1}
    else:
        response = {"status": 2}
    return jsonify(response)

#Handling Server status GET event
@app.route("/status", methods=["GET"])
def status():
    response = {}
    info = getInstanceInfo()
    if info[1] == 16:
        #Lookup Minecraft Server status if the EC2 instance is online
        server = MinecraftServer.lookup("3.1.60.100:25565")
        try:
            #Return minecraft server info if the minecraft server is online
            server_status = server.status()
            online_player = server_status.players.online
            mc_version = server_status.version.name
            response = {
                "status": 1,
                "online_player": online_player,
                "mc_version": mc_version
            }
        except:
            #Otherwise check if it is starting or crashed
            instance = getInitializing()
            if instance:
                response = {
                    "status": 2,
                }
            else:
                response = {
                    "status": 3,
                }
    else:
        #EC2 instance is OFFLINE
        response = {
            "status": 0,
        }
    #Return as a json
    return jsonify(response)

#Add headers for CORS
@app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization")
    return response


if __name__ == "__main__":
    #Change cache to dict to improve performace
    app.jinja_env.cache = {}
    app.run()