from pyzotero import zotero as pyzotero
import os
import subprocess
from yaml import safe_load

LIBRARY_TYPE = 'user'

# user config variables. set these in a .env
config = safe_load(open("config.ini"))
API_KEY = config['API_KEY']
LIBRARY_ID = config['LIBRARY_ID']
COLLECTION_NAME = config['COLLECTION_NAME']  # in Zotero
FOLDER_NAME = config['FOLDER_NAME']  # on the Remarkable device, this must exist!
STORAGE_BASE_PATH = config['STORAGE_BASE_PATH']  # on local computer
RMAPI = config['RMAPI']

RMAPI_LS = f"{RMAPI} ls /{FOLDER_NAME}"

zotero = pyzotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)


def getCollectionId(zotero, collection_name):
    collections = zotero.collections(limit=200)
    for collection in collections:
        if collection['data']['name'] == collection_name:
            return collection['data']['key']


def getPapersTitleAndPathsFromZoteroCollection(zotero, collection_id, STORAGE_BASE_PATH):
    papers = []
    collection_items = zotero.collection_items(collection_id)
    for item in collection_items:
        data = item['data']
        if (data.get('contentType') == 'application/pdf'):
            item_pdf_path = os.path.join(STORAGE_BASE_PATH, data['key'], data['filename'])
            item_title = data['filename'][:-4]
            if (item_pdf_path and item_title):
                papers.append({'title': item_title, 'path': item_pdf_path})
    return papers


def getPapersFromRemarkable(RMAPI_LS):
    remarkable_files = []
    for f in subprocess.check_output(RMAPI_LS, shell=True).decode("utf-8").split('\n')[1:-1]:
        if '[d]\t' not in f:
            remarkable_files.append(f.strip('[f]\t'))
    return remarkable_files


def getUploadListOfPapers(remarkable_files, papers):
    upload_list = []
    for paper in papers:
        title = paper['title']
        if title not in remarkable_files:
            upload_list.append(paper)
    return upload_list


def uploadPapers(papers):
    for paper in papers:
        path = paper.get('path')
        COMMAND = f"{RMAPI} put \"{path}\" /{FOLDER_NAME}"
        subprocess.call(COMMAND, shell=True)


def getDeleteListOfPapers(remarkable_files, papers):
    delete_list = []
    paperNames = [p.get("title") for p in papers]
    for f in remarkable_files:
        if (f not in paperNames):
            delete_list.append(f)
    return delete_list


def deletePapers(delete_list):
    for paper in delete_list:
        COMMAND = f"{RMAPI} rm /{FOLDER_NAME}/\"{paper}\""
        subprocess.call(COMMAND, shell=True)


print('------- sync started -------')
collection_id = getCollectionId(zotero, COLLECTION_NAME)

# find papers that we want from Zotero Remarkable collection
papers = getPapersTitleAndPathsFromZoteroCollection(zotero, collection_id, STORAGE_BASE_PATH)
print(f"\n{len(papers)} papers in Zotero '{COLLECTION_NAME}' collection")
for p in papers:
    print("\t", p["title"])


# get papers that are currently on remarkable
remarkable_files = getPapersFromRemarkable(RMAPI_LS)
print(f"\n{len(remarkable_files)} papers on Remarkable Device, /{FOLDER_NAME}")
for f in remarkable_files:
    print("\t", f)

upload_list = getUploadListOfPapers(remarkable_files, papers)
delete_list = getDeleteListOfPapers(remarkable_files, papers)

print(f'\nUploading {len(upload_list)} papers, deleting {len(delete_list)} papers\n')

deletePapers(delete_list)
uploadPapers(upload_list)

print('------- sync complete -------')
