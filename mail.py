'''
mail
Author: Jacob Hess
 
Reads a maildir folder and will parse messages for information

######################## NOTE ########################
This is written for Linux, and evolution specificaly. Windows User directories don't work this way. I don't even know if you can get Evolution
on Windows anyway.
'''
import mailbox, os
from pathlib import Path

#Setup the maildir path
user = str(Path.home())
path = Path( "" + user + "/.local/share/evolution/mail/local/")
mail = mailbox.Maildir(path)
#folders = mailbox.Maildir.list_folders(mail)

#Alerts
a = mailbox.Maildir.get_folder('folder')
