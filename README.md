# Simple on-demand Minecraft server
The idea is to minimize the server uptime with no player to save computer resources and cost. It uses Python Flask as the backend to communicate with Amazon AWS for instance operation. Once the instance is online, start an SSH channel to run the preloaded shell script to start the actual Minecraft server. While the front-end provides a simple login interface for the user to start the server by inputting the correct password.

Inspired by this Github: https://github.com/trevor-laher/OnDemandMinecraft

# Target User
- Small-Medium Minecraft community.
- Usually, play on the server in a specific timeslot.
- Want to minimize the server renting cost.

# Requirement
Some knowledge of python and shell script.

Shell Scripts:
- A script to start the tmux terminal and start the Minecraft server
- A script to stop the Minecraft server and shutoff the EC2 instance

EC2 details:
- ACCESS_KEY of the account
- SECRET_KEY of the account
- INSTANCE_ID of the Minecraft server instance
- EC2_REGION of the hosted region
- The access key file (.pem) of the instance

An online platform to host the app:
- Heroku (Free tier is enough)
