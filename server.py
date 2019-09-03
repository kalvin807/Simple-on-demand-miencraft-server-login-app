import boto3
from botocore.exceptions import ClientError
from configuration import Config
import time
import paramiko
import os
from threading import Thread, Event

#Create a ec2 object
def initInstance():
    ec2 = boto3.client("ec2",
                       aws_access_key_id=Config.ACCESS_KEY,
                       aws_secret_access_key=Config.SECRET_KEY,
                       region_name=Config.EC2_REGION)
    return ec2

#Get instnace's publicIP & status from aws 
def instanceStatus(ec2):
    response = ec2.describe_instances(InstanceIds=[Config.INSTANCE_ID])
    instance = response["Reservations"][0]["Instances"][0]
    publicIP = instance["PublicIpAddress"]
    statusCode = instance["State"]["Code"]
    return [publicIP, statusCode]

#Get instnace's server checkup status from aws 
def instanceState(ec2):
    response = ec2.describe_instance_status(
        InstanceIds=[Config.INSTANCE_ID])["InstanceStatuses"][0]
    instanceStateCode = response["InstanceState"]["Code"]
    instanceStatus = response["InstanceStatus"]["Status"]
    systemStatus = response["SystemStatus"]["Status"]
    return [instanceStateCode, instanceStatus, systemStatus]

#Start the instance
def startInstance(ec2):
    if (instanceStatus(ec2)[1] == 16):
        #Safe check to ensure server is OFFLINE
        return 1
    else:
        print("Starting Instance")
        try:
            ec2.start_instances(InstanceIds=[Config.INSTANCE_ID], DryRun=True)
        except ClientError as e:
            if "DryRunOperation" not in str(e):
                raise
        try:
            response = ec2.start_instances(InstanceIds=[Config.INSTANCE_ID],
                                           DryRun=False)
        except ClientError as e:
            print(e)
        print("Instance Started", response)
        return 0

#Start the minecraft server by SSH into ec2
def startServer(ec2):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, Config.SSH_KEY_FILE_NAME)
    key = paramiko.RSAKey.from_private_key_file(filename)
    instanceIp = instanceStatus(ec2)[0]
    try:
        print("Creating SSH Channel")
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Edit username accordingly
        sshClient.connect(hostname=instanceIp, username="ubuntu", pkey=key)
        print("Starting Minecraft Server")
        stdin, stdout, stderr = sshClient.exec_command(
            #Preloaded shell script to start the server in tmux
            "/home/ubuntu/mcserver/scripts/tmux.sh")
        sshClient.close()
        print(stdin, stdout, stderr)
        print("Started Minecraft Server")
        return 0
    except:
        print("Error - Failed to run server commands")
        return 1

#Create a sperate thread to handle the server start
def startThread():
    info = getInstanceInfo()
    if (info[1] == 16):
        #Skip the operation if server already online
        return 1
    else:
        thread = Thread(target=startSequence)
        thread.start()
        return 0

#Main seqence to start the server
def startSequence():
    ec2 = initInstance()
    instance = startInstance(ec2)
    if instance == 0:
        time.sleep(5)
        status = instanceState(ec2)
        while (status != [16, "ok", "ok"]):
            print("Waiting Instance Ready")
            print(status)
            time.sleep(5)
            status = instanceState(ec2)
        startServer(ec2)
        return 0
    else:
        print("Server already running!")
        return 1

#Getter for instance general info
def getInstanceInfo():
    ec2 = initInstance()
    return instanceStatus(ec2)

#Getter for instance startup info
def getInitializing():
    ec2 = initInstance()
    init = instanceState(ec2)
    if init[1] == 'initializing' or init[2] == 'initializing':
        return True
    else:
        return False
