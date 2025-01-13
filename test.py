import email
import email.policy

filepath = "/home/jacob/.thunderbird/8k099pv0.default-esr/ImapMail/outlook.office365.com/INBOX/cur/202406051237.8879f18091d44464b3cdb7dc3f5fe043-NVZWS5D4IFBVGRKNIFEUYLKQKJHUILSDGJDDAOJXHE3UKRJSGE2EKQ2CHFCDMNRYGQ3TGMSEGRBDCQ.eml"

with open(filepath, "rb") as f:
    msg = email.message_from_bytes(f.read(), policy=email.policy.default)

body = msg.get_body('html')
print(body)
for part in msg.walk():
    print(part.get_content(), # print part, decoding quotable
    part.is_multipart())