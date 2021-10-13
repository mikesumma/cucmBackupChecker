import paramiko
from paramiko_expect import SSHClientInteraction
import datetime
from httplib2 import Http
from json import dumps
import csv
import os

todaysDate = datetime.date.today()
currentDay = todaysDate.strftime("%b %d")

#Fill in the Google Chat webhook URL
chatURL = ''

#Credentials porition is prepped for Dockerization. This can be changed for testing purposes.
username = os.environ.get('USER')
password = os.environ.get('PASS')

listofErrors = []
failedBackups = []

#Opens the list of nodes from CSV, hostname and IP
with open('uc-nodes.csv') as f:
    reader = csv.DictReader(f)
    ucNodes = list(reader)

#Iterate over the CSV, log in, look for succeeded or failed text in the line with today's date.
for line in ucNodes:
    hostname = line['hostname']
    ip = line['ip']
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        interact = SSHClientInteraction(ssh, timeout=60, display=False)  # Set to "display=True" for debugging
        interact.expect('admin:')
        interact.send('utils disaster_recovery history backup')
        interact.expect('admin:')
        output = interact.current_output_clean
        if currentDay in output and "SUCCESS" in output:
            print(f"{hostname} backup succeded.")
        else:
            print(f"{hostname} backup failed.")
            failedBackups.append(hostname)
        ssh.close()
    except:
        listofErrors.append(hostname)

#Status checking
if len(failedBackups) == 0 and len(listofErrors) == 0:
    sendMessage = f"All collboration nodes were backed up successfully today."
elif len(listofErrors) > 0:
    listofErrors = (' '.join(listofErrors))
    sentMessage = f"CUCM Backup Checker was not able to connect to call CUCM nodes. Failed: {listofErrors}"
elif len(failedBackups) > 0:
    failedBackups = (' '.join(failedBackups))
    sendMessage = f"The following CUCM nodes were not backed up today: {failedBackups}"

#Output results to Google Chat
url = chatURL
bot_message = {
    'text' : sendMessage}
message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
http_obj = Http()
response = http_obj.request(
    uri=url,
    method='POST',
    headers=message_headers,
    body=dumps(bot_message),
)