# wcsc-metroalerts

## NOTICE: PORT FORWARD AT YOUR OWN RISK!
This project was never intended to be deployed on an open port. Because of that there are possible issues, like ```DEBUG == True``` in Django settings. You have been warned.

### About:
A live WMATA Metro map that shows where incidents are located, where maintenance is happening, and if there are any service advisories. It uses the email that MetroAlerts sends notifications to. Make sure to use a dedicated email account and set rules that send WMATA messages to two folders called 'alerts' and 'advisories'. If you don't the code could pull down random stuff you don't want and then store it locally. The email protocols this project supports are ```Gmail``` and ```Maildir IMAP```. ```Mbox``` is not in my scope. The ```IMAP``` implementation in this project has no way of pulling down emails on it's own. You'll need an email client that supports ```Maildir```. I have personally been using Thunderbird.

### Software notes: 

- Python 3.11 \<
  - I started this on 3.11.2, and my current environment is 3.12.x

- Django
  - As of updating the README, I'm using 5.1.4
  - Right now, I am using mariaDB instead of the SQLite3 database. You'll need to setup a mariaDB database. Run `sudo apt install mariadb-server libmariadb-dev`. Inside of your Python virtual environment for this project, run `pip install mariadb`.
    - You will need to run `python3 manage.py makemigrations` and `python3 manage.py migrate` to transfer from SQLite to mariaDB.
  - If command line isn't your vibe, there's a visual manager for databases called DBeaver Community Edition that I have been using to manage mariaDB. Note: You will still need to use the command line to setup the mariaDB database.

- Notes for using a Gmail based account
  - I'm not focusing on this part of the project. I recommend finding a email service that lets you directly access IMAP.
  - When using Gmail, you need to have a Google API project and Google Python libraries. In order to get your API project setup, look at [ThePythonCode's guide](https://www.thepythoncode.com/article/use-gmail-api-in-python "PythonCode's Gmail API Guide").
  - Google has a quick start guide to using their API things. [Google's API Guide](https://developers.google.com/gmail/api/quickstart/python "Google Gmail API Quickstart")

### A Note on Advisories
Before MetroAlerts went down in Feburary of 2024, there would be longer form emails that would announce scheduling changes and on going cunstruction delays. After the relaunch of MetroAlerts, it seems like they don't do this anymore. However, I am keeping the code around in case they bring back advisories in some way.