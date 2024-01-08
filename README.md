# wcsc-metroalerts
## NOTICE: PORT FORWARD AT YOUR OWN RISK!
This project was never intended to be deployed on an open port. Because of that there are possible issues, like ```DEBUG == True``` in Django settings. You have been warned.

### About:
A live WMATA Metro map that shows where incidents are located, where maintenance is happening, and if there are any service advisories.

### Software notes: 

- 3.11.2

- Django 5.0.1
  - Right now, I am using mariaDB instead of the SQLite3 database. Might've been me being an idiot, but model tables weren't showing in DBeaver when doing ```python3 manage.py makemigrations``` and ```python3 manage.py migrate``` with SQLite. You'll need to setup a mariaDB database and will need to install the mariadb and mysqlclient Python libraries (Django was picky, and mysqlclient wasn't showing up on Pylance, sorry that there's two). 

- When using Gmail, you need to have a Google API project and Google Python libraries. In order to get your API project setup, look at [ThePythonCode's guide](https://www.thepythoncode.com/article/use-gmail-api-in-python "PythonCode's Gmail API Guide").
  - Google has a quick start guid to using their API things with Google. Might be helpful if you are new to this. [Google's Guide](https://developers.google.com/gmail/api/quickstart/python "Google Gmail API Quickstart")
  - I personally reccomend imap at this time, it's just simpler to use. If you have a Microsoft account, you can use your @Outlook.com email. You have one even if you have never used or purchased Office.
