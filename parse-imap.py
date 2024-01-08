import os
import json
import mariadb
import mailbox
import email
from datetime import datetime, timedelta

#Get secrets
with open("./Secrets/filepath.json") as j:
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

#Global time value
curdate = datetime.now()

def get_body(message: email.message.Message, encoding: str = "utf-8") -> str:
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

def ImapAlertParser():
        #Open mailbox folder for alerts
        for message in mailbox.Maildir(alpath):
                alsub = message['subject']
                aldat = message['date']
                albod = get_body(message)
                connection = mariadb.connect(**db_config)
                cursor = connection.cursor()
                setup = "INSERT INTO main_alerts"
                cursor.execute(setup)
                add = "VALUES ("+message+", "+alsub+", "+aldat+", "+albod+")"


def ImapAdvisoryParser():
        print("Hi")

def Clean():
        for message in mailbox.Maildir(alpath):
                aldat = message['date']

                timediff = curdate - aldat
                if(timediff > timedelta(7)):
                        message.set_flags('D')
                        try:
                                connection = mariadb.connect(**db_config)
                                cursor = connection.cursor()
                                query = "DELETE FROM main_alerts WHERE id='"+message+"';"
                                cursor.execute(query)
                                connection.commit()
                        except Exception as error:
                                print("Error: "+ error)
                                connection.rollback()
                        i = i - 1
ImapAlertParser()