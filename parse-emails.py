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

#Settings up variables
email_fp = "email.json"
with open(email_fp) as ef:
    email=json.loads(ef.read())

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ["https://mail.google.com/"]
our_email = email["emails"]

creds = None
# The file token.json stores the user"s access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time
if os.path.exists("./API_keys/token.json"):
    creds = Credentials.from_authorized_user_file("./API_keys/token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "./API_keys/credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("./API_keys/token.json", "w") as token:
        token.write(creds.to_json())
service = build("gmail", "v1", credentials=creds)

'''
def get_email_id(service):
    global email_id
    try:
        results = service.users().messages().list(userId="me", maxResults=1).execute()
        messages = results.get("messages", [])
        if messages:
            email_id = messages[0]["id"]

    except HttpError as error:
        print(f"An error occurred: {error}")
        email_id = None

    return email_id
'''

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def search_messages(service, query):
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

def read_message(service, message):
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
        info=' '.join(info)
    if parts == None:
        print("It's none")
        # if the email part is text plain
        filename = message['id'] + ".txt"
        data = msg["snippet"]
        print(data)
        if os.path.exists("./emails/" + filename) == True:
            pass
        elif os.path.exists("./emails/" + filename) == False:
            with open("./emails/" + filename, "w") as f:
                f.write(info + data)

    else:
        parse_parts(service, parts, message, headers)
    print("="*50)

def parse_parts(service, parts, message, headers):
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
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), message)
            if mimeType == "text/plain":
                # if the email part is text plain
                filename = message['id'] + ".txt"
                data = part["body"]["data"]
                text_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
                if os.path.exists("./emails/" + filename) == True:
                    pass
                elif os.path.exists("./emails/" + filename) == False:
                    with open("./emails/" + filename, "w") as f:
                        f.write(text_data.decode("utf-8"))
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

# get emails that match the query you specify from the command lines
results = search_messages(service, "MetroAlerts")
print(f"Found {len(results)} results.")
# for each email matched, read it (output plain/text to console & save HTML and attachments)
for msg in results:
    read_message(service, msg)

'''
def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
    parse_parts(service, parts, message)

def parse_parts(service, parts, message):
    """
    Utility function that parses the content of an email partition
    """
    for part in parts:
        if part["filename"]:
            part_headers = part["headers"]
            filename = message['id']+ "-" + part["filename"]
            body = part["body"]
            data = body["data"]
            file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
            if os.path.exists("./emails/" + filename) == True:
                pass
            elif os.path.exists("./emails/" + filename) == False:
                with open("./emails/" + filename, "wb") as f:
                    f.write(file_data)

        if part["mimeType"] == "text/plain":
            part_headers = part["headers"]
            filename = message['id'] + ".txt"
            data = part["body"]["data"]
            text_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
            if os.path.exists("./emails/" + filename) == True:
                pass
            elif os.path.exists("./emails/" + filename) == False:
                with open("./emails/" + filename, "w") as f:
                    f.write(text_data.decode("utf-8"))

        if part["mimeType"] == "text/html":
            part_headers = part["headers"]
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
