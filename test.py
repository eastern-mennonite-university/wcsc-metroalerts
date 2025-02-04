import re
import quopri
import os, sys
import json
import mariadb
import datetime
from bs4 import BeautifulSoup

#Global values
curdate = datetime.date.today()
j=0
ingest = True

with open("Secrets/filepath.json") as se:
    secrets=json.loads(se.read())
    maildir = secrets['maildir']
    username = secrets["dbuser"]
    password = secrets["dbpass"]
se.close()

# Open temp file for the formatted email
for filename in os.listdir(maildir):

    ingest = True
    
    if os.path.exists("emails/temp-format") | os.path.exists("emails/temp-html"):
        os.remove("emails/temp-format")
        os.remove("emails/temp-html")
    
    with open("emails/temp-format", "w+b") as tempf:
        with open(maildir + filename, "rb") as f:
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
    line = line.split('.')[0]
    print(f"Line color: {line}")
    # Need to add station parsing code
    stations = ["Glenmont", "Wheaton", "Forest Glen", "Silver Spring", "Takona", "Fort Totten", "Brookland-CUA",
                "Rhode Island Ave", "NoMa-Galludet U", "Union Station", "Judiciary Square", "Gallery Place", "Metro Center", "Farragut North",
                "Dupont Circle", "Woodley Park", "Cleveland Park", "Van Ness-UDC", "Tenleytown-AU", "Friendship Heights", "Bethesda", "Medical Center",
                "Grosvenor-Strathmore", "North Bethesda", "Twinbrook", "Rockville", "Shady Grove", "Greenbelt", "College Park-U of Md", "Hyattsville Crossing",
                "West Hyattsville", "Georgia Ave-Penworth", "Colombia Heights", "U st", "Shaw-Howard U", "Mt Vernon Sq", "Archives", "L'Efant Plaza", "Waterfront", "Navy Yard-Ballpark",
                "Anacostia", "Congress Heights", "Southern Ave", "Naylor Rd", "Suitland", "Branch Ave", "New Carrollton", "Landover", "Cheverly",
                "Deanwood", "Minnesota Ave", "Stadium-Armory", "Potomac Ave", "Eastern Market", "Capitol South", "Federal Center SW", "Smithsonian",
                "Federal Triangle", "Metro Center", "McPherson Sq", "Farragut West", "Foggy Bottom-GWU", "Rosslyn", "Court House", "Clarendon", "Virginia Sq-GMU",
                "Ballston-MU", "East Falls Church", "West Falls Church", "Dunn Loring", "Vienna", "Downtown Largo", "Morgan Blvd", "Addison Rd", "Capitol Heights",
                "Benning Rd", "Arlington Cemetary", "Van Dorn St", "Franconia-Springfield", "McLean", "Tysons", "Greensboro", "Spring Hill", "Wielhe-Reston East", 
                "Reston Town Center", "Herndon", "Innovation Center", "Washington Dules International Airport", "Loudon Gateway", "Ashburn", "Pentagon", "Pentagon City", 
                "Crystal City", "Ronald Regan Washington National Airport", "Potomac Yard", "Braddock Rd", "King St-Old Town", "Eisenhower Ave", "Huntington"]
    for i in stations:
        if re.search(i, alert):
            print(i)
            station = i
    print(f"Metro station: {station}")
    # Setup the cursor for sending data to a SQL DB
    try:
        conn = mariadb.connect(
            host="localhost",
            user=username,
            password=password,
            database="wcscmetro"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)
    conn.autocommit = False
    cur = conn.cursor()

    # Sending line, station, alert, and date data to the database
    cur.execute("SELECT Alert, Date FROM Alerts")
    for Alert, Date in cur:
        if re.search(alert, Alert):
            if re.search(str(curdate), str(Date)):
                ingest = False
            else:
                ingest = True
    if ingest == True:
        cur.execute("INSERT INTO Alerts(Color, Station, Alert, Date) VALUES (%s, %s, %s, %s)", (line, station, alert, curdate))
        conn.commit()

    cur.execute("SELECT ID, date FROM Alerts")
    for (ID, date) in cur:
        print(f"ID: {ID}, date: {date}")

def Clean():
    try:
        conn = mariadb.connect(
            host="localhost",
            user=username,
            password=password,
            database="wcscmetro"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)
    conn.autocommit = False
    cur = conn.cursor()

    value = cur.execute("SELECT ID, date FROM Alerts")
    print(value)
    timediff = curdate - date
    if(timediff > datetime.timedelta(7)):
            try:
                cur.execute("DELETE FROM Alerts WHERE name=%s")
                conn.commit()
                #This will tell Thunderbird, or any other Imap client, that this
                # message should be deleted.
                #message.set_flags('D')
            except Exception as error:
                print(error)
                conn.rollback()
                return