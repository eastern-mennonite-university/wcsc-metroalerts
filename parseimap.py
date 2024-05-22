import re
import json
import mariadb
import mailbox
import email
from datetime import datetime, timedelta
from time import sleep

#Global time value
curdate = datetime.now().date()

#Get secrets
with open("Secrets/filepath.json") as j:
        secrets=json.loads(j.read())
        user = secrets["dbusername"]
        passw = secrets["dbpassword"]
        alpath = secrets["imapalerts"]
        adpath = secrets["imapadvisories"]

        #Initialize Database access
        database = "wcscmetro"
        db_config = {
              'host': 'localhost',
              'user': str(user),
              'password': str(passw),
              'database': database
        }

#Code to get the contents of an email from the file. https://stackoverflow.com/questions/74084430/extract-body-from-email-message-objects-in-python
def GetBody(message: email.message.Message, encoding: str = "utf-8") -> str:
    body_in_bytes = ""
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # skip any text/plain (txt) attachments
            if ctype == "text/plain" and "attachment" not in cdispo:
                body_in_bytes = part.get_payload(decode=True)  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body_in_bytes = message.get_payload(decode=True)

    body = body_in_bytes.decode(encoding)

    return body

#The filename of the email appears in a slightly different format in
# both Alerts and Advisories. This code makes it into the filename.
def NameFormatter(name):
        if type(name) == str:
                name = name.replace("<", "").replace(">","")+".eml"
                print(name)
                return name
        else:
                name = str(name)
                name = name.replace("<", "").replace(">","")+".eml"
                return name

#Pulls relavent alerts data from the imap file.
def ImapAlertParser():
        #Setup SQL things
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor()
        #Open alert mailbox folder

        key = {
               "Red": "Red",
               "Green": "Green",
               "Yellow": "Yellow",
               "Blue": "Blue",
               "Orange": "Orange",
               "Silver": "Silver",
        }

        lines = {
               "Orange/Silver/Blue": r"\bOrange/Silver/Blue\b",
               "Orange/Silver": r"\bOrange/Silver\b",
               "Silver/Blue": r"\bSilver/Blue\b",
               "Blue/Yellow": r"\bBlue/Yellow\b",
               "Yellow/Green": r"\bYellow/Green\b",
               "Red": r"\bRed\b",
               "Green": r"\bGreen\b",
               "Yellow": r"\bYellow\b",
               "Blue": r"\bBlue\b",
               "Orange": r"\bOrange\b",
               "Silver": r"\bSilver\b"
        }

        for message in mailbox.Maildir(alpath):
                name = str(message.get("Message-Id"))
                alrail = None
                alna = NameFormatter(name)
                alsub = message['subject']
                aldat = message['date']
                albod = GetBody(message)
                albod = albod.replace('\n\nOptOut: http://w.v12.net/u?upvuvrs\n','')
                for key, line in lines.items():
                       if re.search(line, alsub):
                              alrail = key
                              break
                        
                add = """INSERT INTO main_alerts (rail, name, subject, date, content) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(add, (str(alrail), str(alna), str(alsub), str(aldat), str(albod)))
                connection.commit()
        
        cursor.close()
        connection.close()

#Pulls relavent advisory data from the imap file
def ImapAdvisoryParser():
        #Open advisory mailbox folder
        for message in mailbox.Maildir(adpath):
               adsub = message['subject']
               addat = message['date']
'''        
If the emails are left unchecked, the SQL database will quickly become super huge for what this project is. 
        (In about half a year I have just about 3000 emails of alerts, for example)
This function will delete SQL entries, and Imap file, after a certain period. Alerts will be 3 days and Advisories will hopefully be deleted 5 days after their stated
        end, though we'll see.
The length until deletion can be changed by you.
'''
def Clean():
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor()
        for message in mailbox.Maildir(alpath):
                name = str(message.get("Message-Id"))
                alna = NameFormatter(name)
                aldat = message['date']
                sdate = aldat.split(' ')
                if isinstance(sdate[2], str):
                        if sdate[2] == "Jan":
                                sdate[2] = "01"
                        elif sdate[2] == "Feb":
                                sdate[2] = "02"
                        elif sdate[2] == "Mar":
                                sdate[2] = "03"
                        elif sdate[2] == "Apr":
                                sdate[2] = "04"
                        elif sdate[2] == "May":
                                sdate[2] = "05"
                        elif sdate[2] == "Jun":
                                sdate[2] = "06"
                        elif sdate[2] == "Jul":
                                sdate[2] = "07"
                        elif sdate[2] == "Aug":
                                sdate[2] = "08"
                        elif sdate[2] == "Sep":
                                sdate[2] = "09"
                        elif sdate[2] == "Oct":
                                sdate[2] = "10"
                        elif sdate[2] == "Nov":
                                sdate[2] = "11"
                        elif sdate[2] == "Dec":
                                sdate[2] = "12"
                ndate = ""+sdate[3]+"-"+sdate[2]+"-"+sdate[1]+""
                date = datetime.strptime(ndate, '%Y-%m-%d').date()
                timediff = curdate - date
                if(timediff > timedelta(7)):
                        try:
                                delete = "DELETE FROM main_alerts WHERE name=%s"
                                cursor.execute(delete, (str(alna),))
                                connection.commit()
                                #This will tell Thunderbird, or any other Imap client, that this
                                # message should be deleted.
                                #message.set_flags('D')
                        except Exception as error:
                                print(error)
                                connection.rollback()
                                return
        cursor.close
        connection.close


ImapAlertParser()
#ImapAdvisoryParser()
#Clean()
print("Done")