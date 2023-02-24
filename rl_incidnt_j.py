# This folder is for the "JSON - Rail Incidents" moduel in the WMATA API
import http.client, urllib.request, urllib.parse, urllib.error, json, base64
from pathlib import Path

def RlIncidents():
    global dataInc
    global errorInc

    #Grab your API key from the JSON file. Should work on Windows and Linux
    folder = Path("API_keys")
    file = folder / "key.json"
    key = json.load(open(file))

    # Request headers { 'api_key':'{subscription key}' }
    headers = key
        
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Incidents.svc/json/Incidents?%s" % params, "{body}", headers)
        response = conn.getresponse()
        dataInc = response.read()
        print(dataInc)
        conn.close()
    except Exception as e:
        errorInc = "[Errno {0}] {1}".format(e.errno, e.strerror)
        print(errorInc)