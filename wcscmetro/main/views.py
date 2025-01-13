import os
import re
import mariadb
import sys
import fnmatch

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Alerts, Advisories

# Create your views here.
class Home:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def sqlStart(self):
        try:
            conn = mariadb.connect(
                host="localhost",
                user="pythonma",
                password="password",
                database="metroalerts"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            sys.exit(1)
        conn.autocommit = False
        self.cur = conn.cursor()

    def parser(self,request):
        self.alparts = {}
        #adparts = {}
        #Lists for alerts
        self.alsub = []
        self.aldat = []
        self.albod = []

        self.files = []

        # specify the folder containing the files
        self.folder_path = './emails/'

        # loop through all the files in the folder
        for file_name in os.listdir(self.folder_path):
            self.files.append(file_name)

        # Open the file for reading
        for i in self.files:
            for file_name in os.listdir("./emails/"):
                if fnmatch.fnmatch(file_name, "alerts-*.txt"):
                    with open("./emails/"+file_name, 'r') as f:
                        # Read the contents of the file into a string variable
                        self.file_contents = f.read()
                    #Get the certain string from the txt file
                    self.sub = re.search('Subject: (.+?)Date: ',self.file_contents)
                    self.date = re.search("Date: (.+?)"+str(r'-0700'), self.file_contents)
                    self.body = re.search(str(r'-0700')+" (.+?)OptOut: ", self.file_contents)
                    if self.sub:
                        self.sub = self.sub.group(1)
                        self.alsub.append(self.sub)
                        
                    if self.date:
                        self.date = self.date.group(1)
                        self.aldat.append(self.date)

                    if self.body:
                        self.body = self.body.group(1)
                        self.albod.append(self.body)

        #Alert Dictionary
        #Convert list to tuple
        self.tasu = tuple(self.alsub)
        self.tada = tuple(self.aldat)
        self.tabo = tuple(self.albod)
        #Add tuples to dictionary
        self.alparts["Subject:"] = self.tasu
        self.alparts["Date:"] = self.tada
        self.alparts["Body:"] = self.tabo
def main(request):
    return render(request, 'index.html', {
        "alerts_list": Alerts.objects.all(),
        "advisories_list": Advisories.objects.all()
    })
'''
def check_database_updates(request):
    #Retrieve data from the database
    new_items = Alerts.objects.filter(is_processed=False)

    #Process new items if needed
    for item in new_items:
        item.is_processed = True
        item.save()
'''