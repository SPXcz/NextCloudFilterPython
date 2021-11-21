import xml.etree.ElementTree as ET
import requests

#with open("requestTest.xml", "r") as fr:
#    run(["curl", "-u", "nextCloudUser:nextCloudPassword", ""])
def execute():
    with open("login.txt", "r") as fr:
        USER = fr.readline().split("\n")[0]
        PASSWORD = fr.readline().split("\n")[0]

    header = {"content-Type": "text/xml"}

    with open("requestTest.xml", "r") as fr:
        r = requests.api.request("SEARCH",
        'http://localhost:8080/remote.php/dav/', 
        data=fr.read(), 
        headers=header, 
        auth=requests.auth.HTTPBasicAuth(USER, PASSWORD))

    print(r.status_code)
    print(r.text)
    tree = ET.fromstring(r.content)
    for ele in tree:
        print(ele)
        for att, name in zip(ele.findall("{DAV:}href"), ele.findall("{DAV:}name")):
            print(att.text.split("/")[-1])

execute()