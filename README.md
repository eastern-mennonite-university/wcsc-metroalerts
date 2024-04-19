# wcsc-metroalerts
## NOTICE: PORT FORWARD AT YOUR OWN RISK!
This project was never intended to be deployed on an open port. Because of that there are possible issues, like ```DEBUG == True``` in Django settings. You have been warned.

### About:
A live WMATA Metro map that shows where incidents are located, where maintenance is happening, and if there are any service advisories. It uses the email that MetroAlerts sends notifications to. Make sure to use a dedicated email account, or set rules that send WMATA messages to folders called 'alerts' and 'advisories'. The code could pull down random stuff you don't want stored locally. The email protocols this project supports is Gmail and Maildir Imap. Mbox is not in my scope. The Imap implementation has no way of pulling down emails on it's own, you'll need an email client that supports Maildir. I have personally been using Thunderbird.

### Software notes: 

- Python 3.11.2

- Django 5.0.1
  - Right now, I am using mariaDB instead of the SQLite3 database. Might've been me being an idiot, but model tables weren't showing in DBeaver when doing ```python3 manage.py makemigrations``` and ```python3 manage.py migrate``` with SQLite. You'll need to setup a mariaDB database and will need to install the mariadb and mysqlclient Python libraries (Django was picky, and mysqlclient wasn't showing up on Pylance, sorry that there's two). 

- When using Gmail, you need to have a Google API project and Google Python libraries. In order to get your API project setup, look at [ThePythonCode's guide](https://www.thepythoncode.com/article/use-gmail-api-in-python "PythonCode's Gmail API Guide").
  - Google has a quick start guide to using their API things. [Google's API Guide](https://developers.google.com/gmail/api/quickstart/python "Google Gmail API Quickstart")
