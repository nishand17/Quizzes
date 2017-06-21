
from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from googleapiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/script-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/forms','https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_FILE = 'client_secret_main.json'
APPLICATION_NAME = 'Google Apps Script Execution API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'script-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: 
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main(funcName, params):
    """Shows basic usage of the Apps Script Execution API.

    Creates a Apps Script Execution API service object and uses it to call an
    Apps Script function to print out a list of folders in the user's root
    directory.
    """
    SCRIPT_ID = '1qMCpcZto1Dh3_D0dG5y21DuOCdlrAlL5mzezIax1x7bShqpKH-F7q73F'

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('script','v1', http=http)

    if params is None:
        request = {"function": funcName}
    else:    
        request = {
        "function": funcName,
        "parameters": params
        }

    try:
        response = service.scripts().run(body=request,
                scriptId=SCRIPT_ID).execute()

        if 'error' in response:
            
            error = response['error']['details'][0]
            print("Script error message: {0}".format(error['errorMessage']))

            if 'scriptStackTraceElements' in error:
         
                print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    print("\t{0}: {1}".format(trace['function'],
                        trace['lineNumber']))
        else:
            # The structure of the result will depend upon what the Apps Script
            # function returns. Here, the function returns an Apps Script Object
            # with String keys and values, and so the result is treated as a
            # Python dictionary (folderSet).
            folderSet = response['response'].get('result', {})
            return folderSet;

    except errors.HttpError as e:
        # The API encountered a problem before the script started executing.
        print(e.content)

if __name__ == '__main__':
    main()