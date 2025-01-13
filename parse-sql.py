#
# I THINK THIS FILE SUPERCEDED parseimap. USE THIS ONE.
#
import os
import re
import mariadb
import sys
import fnmatch

class StartSQL():
    def __init__(self):
        super().__init__()


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
        cur = conn.cursor()


class FileParser():
    def __init__(self):
        super().__init__()

        alparts = {}
        adparts = {}
        #Lists for alerts
        alsub = []
        aldat = []
        albod = []
        '''
        #Lists for advisories
        adda = []
        adho = []
        adse = []
        adma = []
        adrl = []
        adbl = []
        adol = []
        adsl = []
        adyl = []
        adgl = []
        adet = []
        '''
        # create a dictionary to store the filenames and their file types
        files = []

        # specify the folder containing the files
        folder_path = './emails/'

        # loop through all the files in the folder
        for file_name in os.listdir(folder_path):
            files.append(file_name)

        # Open the file for reading
        for i in files:
            for file_name in os.listdir("./emails/"):
                if fnmatch.fnmatch(file_name, "alerts-*.txt"):
                    with open("./emails/"+file_name, 'r') as f:
                        # Read the contents of the file into a string variable
                        file_contents = f.read()
                    #Get the certain string from the txt file
                    sub = re.search('Subject: (.+?)Date: ',file_contents)
                    date = re.search("Date: (.+?)"+str(r'-0700'), file_contents)
                    body = re.search(str(r'-0700')+" (.+?)OptOut: ", file_contents)
                    if sub:
                        sub = sub.group(1)
                        alsub.append(sub)
                        
                    if date:
                        date = date.group(1)
                        aldat.append(date)

                    if body:
                        body = body.group(1)
                        albod.append(body)
                '''
                else:
                    with open("./emails/"+file_name, 'r') as f:
                        file_contents = f.read()
                    da = re.search('(.+?)' + str(r'\nHours:'),file_contents)
                    ho = re.search(str(r'\nHours:') + '(.+?)' + str(r'\nService:'),file_contents)
                    se = re.search(str(r'\nService:') + '(.+?)' + str(r'\nMaintenance:'),file_contents)
                    ma = re.search(str(r'\nMaintenance:')+'(.+?)' + str(r'\nRed Line'),file_contents)
                    rl = re.search(str(r'\nRed Line') + '(.+?)' + str(r'\nBlue Line'),file_contents)
                    bl = re.search(str(r'\nBlue Line') + '(.+?)' + str(r'\nOrange Line'),file_contents)
                    ol = re.search(str(r'\nOrange Line') + '(.+?)' + str(r'\nSilver Line'),file_contents)
                    sl = re.search(str(r'\nSilver Line') + '(.+?)' + str(r'\nYellow Line'),file_contents)
                    yl = re.search(str(r'\nYellow Line') + '(.+?)' + str(r'\nGreen Line'),file_contents)
                    gl = re.search(str(r'\nGreen Line') + '(.+?)' + str(r'\nFor more information'),file_contents)
                    et = re.search(str(r'\nFor more information') + '(.+?)',file_contents)

                    if da:
                        da = da.group(1)
                        adda.append(da)

                    if ho:
                        ho = ho.group(1)
                        adho.append(ho)

                    if se:
                        se = se.group(1)
                        adse.append(se)

                    if ma:
                        ma = ma.group(1)
                        adma.append(ma)

                    if rl:
                        rl= rl.group(1)
                        adrl.append(rl)

                    if bl:
                        bl = bl.group(1)
                        adbl.append(bl)

                    if ol:
                        ol = ol.group(1)
                        adol.append(ol)

                    if sl:
                        sl = sl.group(1)
                        adsl.append(sl)

                    if yl:
                        yl = yl.group(1)
                        adyl.append(yl)

                    if gl:
                        gl = gl.group(1)
                        adgl.append(gl)

                    if et:
                        et = et.group(1)
                        adet.append(et)
                    '''
        #Alert Dictionary
        #Convert list to tuple
        tasu = tuple(alsub)
        tada = tuple(aldat)
        tabo = tuple(albod)
        #Add tuples to dictionary
        alparts["Subject:"] = tasu
        alparts["Date:"] = tada
        alparts["Body:"] = tabo
        '''
        #Advisory Dictionary
        tadda = tuple(adda)
        print(tadda)
        tadho = tuple(adho)
        tadse = tuple(adse)
        tadma = tuple(adma)
        tadrl = tuple(adrl)
        tadbl = tuple(adbl)
        tadol = tuple(adol)
        tadsl = tuple(adsl)
        tadyl = tuple(adyl)
        tadgl = tuple(adgl)
        tadet = tuple(adet)
        adparts["Date:"] = tadda
        adparts["Hours:"] = tadho
        adparts["Service:"] = tadse
        adparts["Maintenance:"] = tadma
        adparts["Red Line:"] = tadrl
        adparts["Blue Line:"] = tadbl
        adparts["Orange Line:"] = tadol
        adparts["Silver Line:"] = tadsl
        adparts["Yellow Line:"] = tadyl
        adparts["Green Line:"] = tadgl
        adparts["Etcetera:"] = tadet
        '''
if __name__ == "__main__":
    StartSQL()
    FileParser()