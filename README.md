# cucmBackupChecker
#
#I'm not a big fan of Cisco RTMT. To me it's clunky and confusing. But a big part of managing a Cisco Collaboration environment is making sure the nodes are getting backed up.
#
#To solve this problem, I decided to create my own Python script that I could Dockerize and schedule to run as a cron job.
#
#This script looks at a CSV file of collab nodes, logs into the CLI, and looks for the keyword "success" in the line with today's timestamp.
#
#I think there's a way to do this with threading, but that's a little advanced for me right now.
#
#Since it runs as a scheduled task anyway, it really doesn't matter to me that it's running one node as a time as long as I get the information I need.
#
#Results are sent to a Google Chat space webhook. Obviously this can be changed to anything.
#
#The error reporting is a little unrefined right now and will get cleaned up in later versions of this script.
#
#-MS
