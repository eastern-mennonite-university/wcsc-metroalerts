import linecache
import email
import email.policy
import re
import quopri
import os
import json
from tempfile import TemporaryFile
from email.iterators import _structure

j=0

if os.path.exists("emails/temp-format") | os.path.exists("emails/temp-html"):
    os.remove("emails/temp-format")
    os.remove("emails/temp-html")

with open("Secrets/filepath.json") as se:
    secrets=json.loads(se.read())
    maildir = secrets['maildir']
se.close()

with open("emails/temp-format", "w+b") as temp:
    with open(maildir + "202406052347.1eb89e6d95214abf8ba9c2907ffaa3bc-NVZWS5D4IFBVGRKNIFEUYLKQKJHUILSDGJDDAOJXHE3UKRJSGE2EKQ2CHFCDMNRYGQ3TGMSEGRBDCQ.eml", "rb") as f:
        quopri.decode(f, temp)
    f.close()

    temp.seek(0)

    array = temp.readlines()

    for index, value in enumerate(array):
        if re.search("MIME-Version: 1.0", str(value)):
            j = index
            print(value)
            print(index)
    print(j)
temp.close()

del array[0:j + 2]

with open("emails/temp-html", "w+b") as temp:
    for k in array:
        print(k)
        temp.write(k)
temp.close()