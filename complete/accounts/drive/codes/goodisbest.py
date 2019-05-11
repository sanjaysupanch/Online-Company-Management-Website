
from __future__ import print_function
import httplib2
import os, io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from apiclient import errors
#..

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
from .  import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def listFiles(name):
    results = drive_service.files().list(
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def is_file_in_folder(service, folder_id, file_id):
  """Check if a file is in a specific folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder.
    file_id: ID of the file.
  Returns:
    Whether or not the file is in the folder.
  """
  try:
    service.parents().get(fileId=file_id, parentId=folder_id).execute()
  except errors.HttpError:
    if errors.HttpError.resp.status == 404:
      return False
    else:
      print ('An error occurred: %s' % error)
      raise error
  return True


def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        print("downloading")
        status, done = downloader.next_chunk()
        print(int(status.progress() * 100))

        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

def uploadFilestoFolder(name):
    folder_id = '1bEXlYyXU9rZ37VIL5MojJFI7SJMKmx-3'
    file_metadata = {
        'name': 'photo.jpg',
        'parents': [folder_id]
    }
    media = MediaFileUpload('files/photo.jpg',
                        mimetype='image/jpeg',
                        resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print ('File ID: %s' % file.get('id'))

def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))

folderId='1oMpkxoC5ZlT6wrYBdFqI5Lo7LauaGk-9'

# kwargs = {
#   "q": "{} in parents".format(folderId),
#   # Specify what you want in the response as a best practice. This string
#   # will only get the files' ids, names, and the ids of any folders that they are in
#   "fields": "nextPageToken,incompleteSearch,files(id,parents,name)",
#   # Add any other arguments to pass to list()
# }
# request = drive_service.files().list(**kwargs)
# while request is not None:
#   response = request.execute()
#   # Do stuff with response['files']
#   request = drive_service.files().list_next(request, response)

#uploadFile('unamed123.jpg',"E:/Latestdownloads/models/research/object_detection/Test_image.jpg",'image/jpeg')
#downloadFile('1mt7NjiIz6KT7SI0i6t1GR3ZU5Ye8BKUx','test124.jpg')

#searchFile(10,"name contains 'Getting'")
#listFiles('unamed123.jpg')
#is_file_in_folder(drive_service, '1oMpkxoC5ZlT6wrYBdFqI5Lo7LauaGk-9', '1zsSS2aCgAvcE0Yvclk0jrcLSbXncFP5A')

#drive_service.children().get(folderId='1oMpkxoC5ZlT6wrYBdFqI5Lo7LauaGk-9').execute()

createFolder('Doogle123')

query="'11psgGNCr0tccramh1CdgG-bh6G5rrhree' in parents"

response = drive_service.files().list(q=query,

                                fields='nextPageToken,files(id, name, parents)').execute()
items = response.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))


print(response)
