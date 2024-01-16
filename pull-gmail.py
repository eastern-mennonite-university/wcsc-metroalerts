"""
Project: WCSC Metro Alerts
Author: BitUniverse
About Script: This part is supposed to download emails
Code Used: 
    Google API examples, 
    https://thepythoncode.com/article/use-gmail-api-in-python, 
    and ChatGPT because I can't even, I don't even care about learning how to get gmail into
    Python. This has been such bs. Just let the AI do it for me.
"""
import os
from bs4 import BeautifulSoup
import base64
from base64 import urlsafe_b64decode
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

#This is to make sure your email isn't in the file permanently
#Make a json file called email, and put your email in it like this:
'''
}
    'emails':'you@wherevere.com'
}
'''
email_fp = "email.json"
with open(email_fp) as ef:
    email=json.loads(ef.read())

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
# Give you full access to your email
SCOPES = ["https://mail.google.com/"]
our_email = email["emails"]

# The file token.json stores the user"s access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
# ie: Name the json you downloaded from Google 'credentials.json' and the script
# will make the 'token.json'
creds = None
if os.path.exists("./Secrets/token.json"):
    creds = Credentials.from_authorized_user_file("./Secrets/token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "./Secrets/credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("./Secrets/token.json", "w") as token:
        token.write(creds.to_json())
service = build("gmail", "v1", credentials=creds)

#Search for specific emails you want to download
def SearchMessages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

# This will take the messages list (or array depending on your religion) and convert it to 'parts', 
# which is how this script (possibly maildir as a whole) organizes data. Parts are what got me so frustrated.
def ReadMessage(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    msgraw = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
    #print(msg)
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    info = []
    if headers:
        # this section prints email basic info & creates a folder for the email
        # It also makes an array for the bad choices WMATA made with just sending really simple emails for service updates.
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
                f = "From: "+value
                info.append(f)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
                t = "To: "+value
                info.append(t)
            if name.lower() == "subject":
                print("Subject:", value)
                s = "Subject: "+value
                info.append(s)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
                d = "Date: "+value
                info.append(d)

    #This joins the array into one big string          
    info=' '.join(info)
    ParseParts(service, parts, message, msg, info)
    print("="*50)

def ParseParts(service, parts, message, msg, info):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part has parts inside
                parse_parts(service, part.get("parts"), message)
            if mimeType == "text/plain":
                # if the email part is text plain
                # Incidentally, it also saves html files as plain text
                filename = message['id'] + ".txt"
                data = part["body"]["data"]
                text_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
                # Existing file check
                if os.path.exists("./emails/" + filename) == True:
                    pass
                elif os.path.exists("./emails/" + filename) == False:
                    with open("./emails/" + filename, "w") as f:
                        f.write(text_data.decode("utf-8"))
            ''' #If you want to have html files be their own file
            elif mimeType == "text/html":
                # if the email part is an HTML content
                # save the HTML file and optionally open it in the browser
                filename = message['id'] + ".html"
                data = part["body"]["data"]
                html_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
                soup = BeautifulSoup(html_data, "html.parser")
                if os.path.exists("./emails/" + filename) == True:
                    pass
                elif os.path.exists("./emails/" + filename) == False:
                    with open("./emails/" + filename, "w") as f:
                        f.write(soup.prettify())
            '''
    # This helps fix the bad choices WMATA made.
    # For some reason, the smaller update emails have no 'parts', so going through a 'if parts:' was giving me everything else.
    # As you can see, it checks to see if there are parts and then will grab my Jerry-rigged array strings and give you a nice .txt file.
    elif parts == None:
        filename = message['id'] + ".txt"
        data = msg["snippet"]
        #print(data)
        if os.path.exists("./emails/alerts-" + filename) == True:
            pass
        elif os.path.exists("./emails/alerts-" + filename) == False:
            with open("./emails/alerts-" + filename, "w") as f:
                f.write(info + " " + data)

def DeleteMessages(service, query):
    messages_to_delete = SearchMessages(service, query)
    # it's possible to delete a single message with the delete API, like this:
    # service.users().messages().delete(userId='me', id=msg['id'])
    # but it's also possible to delete all the selected messages with one query, batchDelete
    return service.users().messages().batchDelete(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_delete]
      }
    ).execute()

# get emails that match the query you specify from the command lines
results = SearchMessages(service, "MetroAlerts")
print(f"Found {len(results)} results.")
# for each email matched, read it (output plain/text to console & save HTML and attachments)
for msg in results:
    ReadMessage(service, msg)