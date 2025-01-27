import re
import quopri
import os, sys
import json
import mariadb
from bs4 import BeautifulSoup
from tempfile import TemporaryFile
from email.iterators import _structure

j=0

if os.path.exists("emails/temp-format") | os.path.exists("emails/temp-html"):
    os.remove("emails/temp-format")
    os.remove("emails/temp-html")

with open("Secrets/filepath.json") as se:
    secrets=json.loads(se.read())
    maildir = secrets['maildir']
    username = secrets["dbuser"]
    password = secrets["dbpass"]
se.close()

# Open temp file for the formatted email
with open("emails/temp-format", "w+b") as tempf:
    with open(maildir + "202406052347.1eb89e6d95214abf8ba9c2907ffaa3bc-NVZWS5D4IFBVGRKNIFEUYLKQKJHUILSDGJDDAOJXHE3UKRJSGE2EKQ2CHFCDMNRYGQ3TGMSEGRBDCQ.eml", "rb") as f:
        # Format the weird stuff Outlook is doing
        quopri.decode(f, tempf)
    f.close()
    tempf.seek(0)
    array = tempf.readlines()
    # Find the line number of a unique string in a consistant spot
    for index, value in enumerate(array):
        if re.search("MIME-Version: 1.0", str(value)):
            j = index
    print(j)
tempf.close()
# Delete everything other than the HTML
del array[0:j + 2]
# Open a temp file to store the HTML only part of the email 
with open("emails/temp-html", "w+b") as temph:
    for k in array:
        temph.write(k)

    temph.seek(0)
    soup = BeautifulSoup(temph.read(), "lxml")

    # Note: Almost verbatum from ChatGPT. It worked right away.
    # Extract the image name from the link
    image = soup.find('img', {'src': lambda x: x and 'https://metroalerts.wmata.com/i/metrorail/' in x})
    line = None
    if image and 'src' in image.attrs:
        line = image['src'].split('/')[-1]

    # Extract the paragraph contents in the <table class="main">
    content = soup.find('table', {'class': 'main'})
    alert = None
    if content:
        paragraph = content.find('p')
        if paragraph:
            alert = paragraph.text.strip()

    # Print the results
    print(f"Image Name: {line}")
    print(f"Paragraph Content: {alert}")
temph.close()

# Need to add station parsing code

# Setup the cursor for sending data to a SQL DB
try:
    conn = mariadb.connect(
        host="localhost",
        user=username,
        password=password,
        database="metroalerts"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)
conn.autocommit = False
cur = conn.cursor()

# Sending line, station, alert, and date data to the database