import email
import email.policy
import quopri
import os
import json
from bs4 import BeautifulSoup

with open("Secrets/filepath.json") as se:
    secrets=json.loads(se.read())
    maildir = secrets['maildir']
se.close()

for file_name in os.listdir(maildir):
    with open(maildir + file_name, "rb") as f:
        if os.path.exists("emails/"+file_name) == False:
            with open("emails/"+file_name, "xb") as w:
                quopri.decode(f, w)
            w.close()
        else:
            pass
    f.close()

# Save for future reference. Still need to write the clean up part
#os.remove(fname)

for file_name in os.listdir("emails/"):
    with open("emails/"+file_name, "rb") as w:
        msg = email.message_from_bytes(w.read(), policy=email.policy.default)
        print(msg['date'])
        print(msg['content'])
        print(msg['body'])

        body = msg.get_body(preferencelist=('html', 'plain'))
        print(body)
        soup = BeautifulSoup(str(body), "html.parser")

        if soup.find("metrorail/RD.png") == True:
            print("Red")
        elif soup.find("metrorail/GR.png") == True:
            print("Green")
        elif soup.find("metrorail/YL.png") == True:
            print("Yellow")
        elif soup.find("metrorail/BL.png") == True:
            print("Blue")
        elif soup.find("metrorail/OR.png") == True:
            print("Orange")
        elif soup.find("metrorail/SV.png") == True:
            print("Silver")
        
    w.close() 

#for part in msg.walk():
#    if part.get_content_type() == "text/html":
#        html_content = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
#else:
#    print("No text/html part found.")
'''
print(body)
for part in msg.walk():
    print(part.get_content_type(), # print part, decoding quotable
    part.is_multipart())
'''