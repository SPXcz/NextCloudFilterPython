import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timezone
from sys import argv, exit
from urllib.parse import unquote

def filterName(name, username, path="/"):
    with open("files/templateUser.xml", "r") as fr:
        request = fr.read().format(xmlUsername = username, xmlName = name, xmlPath = path)
    print(request)
    return request


def filterSuffix(suffix, username, path="/"):
    with open("files/templateSuffix.xml", "r") as fr:
        request = fr.read().format(xmlUsername = username, xmlSuffix = suffix, xmlPath = path)
    return request

def filterLastEdited(username, after, before=datetime.now(timezone.utc).astimezone(), path="/"):
    with open("files/templateEdit.xml", "r") as fr:
        request = fr.read().format(xmlUsername = username, xmlPath = path, xmlFrom = after.astimezone().isoformat(), xmlTo = before.astimezone().isoformat())
    return request

def filterPermissions(username, permissionString, path="/"):
    with open("files/templatePrivilege.xml", "r") as fr:
        request = fr.read().format(xmlUsername = username, xmlPath = path, xmlPermissions = permissionString)
    print(request)
    return request

#In bytes, max. 10 000 petabytes
def filterSize(username, minSize, maxSize, path="/"):
    with open("files/templateSize.xml", "r") as fr:
        request = fr.read().format(xmlUsername = username, xmlPath = path, xmlFrom = minSize, xmlTo = maxSize)
    print(request)
    return request

def createRequestFromQuery():
    pass

def convertor(input):
    number = int(input[:-2])
    unit = input[-2:]
    try:
        match unit:
            case "B":
                return number
            case "KB":
                return number * 1000
            case "MB":
                return number * 1000000
            case "GB":
                return number * 1000000000
            case "TB":
                return number * 1000000000000
            case _:
                exit("Unsupported unit. See -h for correct usage")
    except:
        return number


def execute(xmlRequest, USER, PASSWORD, URL):

    header = {"content-Type": "text/xml"}

    r = requests.api.request("SEARCH",
    URL,
    data=xmlRequest, 
    headers=header, 
    auth=requests.auth.HTTPBasicAuth(USER, PASSWORD))
    if r.status_code >= 400:
        exit("Finished with code", r.status_code)

    tree = ET.fromstring(r.content)
    for ele in tree:
        for id, att, contenttype, permissions, lastmodified in zip(
        ele.find("{DAV:}propstat/{DAV:}prop").findall("{http://owncloud.org/ns}fileid"), ele.findall("{DAV:}href"), 
        ele.find("{DAV:}propstat/{DAV:}prop").findall("{DAV:}getcontenttype"), ele.find("{DAV:}propstat/{DAV:}prop").findall("{http://owncloud.org/ns}permissions"),
        ele.find("{DAV:}propstat/{DAV:}prop").findall("{DAV:}getlastmodified")):
            print(id.text, unquote(att.text.split("/")[-1]), unquote(contenttype.text), permissions.text, "", lastmodified.text, sep="\t")


#Main begins here

with open("files/login.txt", "r") as fr:
    USER = fr.readline().split("\n")[0]
    PASSWORD = fr.readline().split("\n")[0]
    URL = fr.readline()

PATH = argv[1]
if PATH != "-h":
    match argv[2]:
        case "-type":
            try:
                query = filterSuffix(argv[3], USER, PATH)
            except:
                exit("Bad argument for type. See -h for correct usage")
        case "-edit":
            try:
                query = filterLastEdited(USER, convertor(argv[3]), convertor(argv[4]), PATH)
            except:
                exit("Bad argument for edit. See -h for correct usage")
        case "-size":
            try:
                query = filterSize(USER, argv[3], argv[4], PATH)
            except:
                exit("Bad argument for edit. See -h for correct usage")
        case _:
            exit("Non existing filtering mode. View -h for correct usage")
    print("ID", "FILE NAME", "CONTENT TYPE", "PERMISSIONS", "LAST MODIFIED", sep="\t")
    print("---------------------------------------------------------------------")
    execute(query, USER, PASSWORD, URL)
else:
    print("SIMPLE PYTHON NEXTCLOUD WEBDAV CLIENT")
    print("-------------------------------------")
    print("USAGE:")
    print(" python3.10 clientCustomRequest.py [PATH or -h] [MODE] [MODE ARGUMENTS]")
    print(" ")
    print("OPTIONS:")
    print(" [PATH] - Should begin with '/'. Path in your NextCloud storage from your root folder.")
    print(" [-h] - Help information")
    print(" [MODE] - Choices:")
    print("     [-type] - Filter by type of file. For example 'image' or 'text'. List of file types is defined on NextCloud server.")
    print("         This option requires additional argument [SUBJECT]")
    print("     [-edit] - Filter by last date of editation of files in a folder.")
    print("         This option requires two additional arguments [FROM] [TO] of a type 'date'")
    print("     [-size] - Filter by the size of files in a folder.")
    print("         This option requires two additional arguments [FROM] [TO] of a type 'data size'. No unit means the size is in bytes. You can also write the with a unit - eg. '10GB'")

#query = filterName(USER, "nextCloudUser", "/testFolder")
#query = filterSuffix("image", USER, "/testFolder")
#query = filterLastEdited(USER, datetime(2021, 11, 19), datetime(2021, 11, 21), "/testFolder")
#query = filterPermissions(USER, "G", "/testFolder")
#query = filterSize(USER, 600, 10000000000, "/testFolder")