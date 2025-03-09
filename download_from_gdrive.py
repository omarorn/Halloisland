"""
Download files from Google Drive 'helloiceland' folder
"""
import os
import pickle
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from pathlib import Path

# Set up directory for downloaded files
DOWNLOAD_DIR = Path("helloiceland_files")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Google Drive API scope
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """Authenticate with Google Drive API"""
    creds = None
    
    # Check if token file exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If credentials don't exist or are invalid, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def find_folder_id(service, folder_name="helloiceland"):
    """Find the Google Drive folder ID by name"""
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
    
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        print(f"No folder named '{folder_name}' found.")
        return None
    
    # Return the first matching folder ID
    return items[0]['id']

def list_files_in_folder(service, folder_id):
    """List all files in a specific folder"""
    query = f"'{folder_id}' in parents"
    
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name, mimeType)'
    ).execute()
    
    return results.get('files', [])

def download_file(service, file_id, file_name):
    """Download a file from Google Drive"""
    request = service.files().get_media(fileId=file_id)
    
    file_path = DOWNLOAD_DIR / file_name
    
    with io.BytesIO() as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%")
        
        # Write to file
        fh.seek(0)
        with open(file_path, 'wb') as f:
            f.write(fh.read())
    
    return file_path

def main():
    """Main function to download files from Google Drive"""
    print("Authenticating with Google Drive...")
    
    try:
        # Authenticate
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)
        
        # Find the folder
        print("Looking for 'helloiceland' folder...")
        folder_id = find_folder_id(service)
        
        if not folder_id:
            return
        
        # List files in the folder
        print(f"Listing files in the folder...")
        files = list_files_in_folder(service, folder_id)
        
        if not files:
            print("No files found in the folder.")
            return
        
        print(f"Found {len(files)} files. Starting download...")
        
        # Download each file
        for file in files:
            file_id = file['id']
            file_name = file['name']
            mime_type = file['mimeType']
            
            # Skip folders
            if mime_type == 'application/vnd.google-apps.folder':
                print(f"Skipping subfolder: {file_name}")
                continue
                
            print(f"Downloading {file_name}...")
            file_path = download_file(service, file_id, file_name)
            print(f"Downloaded to {file_path}")
        
        print(f"\nAll files downloaded to {DOWNLOAD_DIR.absolute()}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTo use this script, you need to:")
        print("1. Create a Google Cloud project")
        print("2. Enable the Google Drive API")
        print("3. Create credentials (OAuth client ID)")
        print("4. Download the credentials as 'credentials.json'")
        print("5. Place 'credentials.json' in the same directory as this script")

if __name__ == "__main__":
    main()