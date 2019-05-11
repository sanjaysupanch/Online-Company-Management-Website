from apiclient import errors
# ...

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
  except errors.HttpError, error:
    if error.resp.status == 404:
      return False
    else:
      print 'An error occurred: %s' % error
      raise error
  return True
