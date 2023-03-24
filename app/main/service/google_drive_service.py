import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDriveService:
    def __init__(self):
        self._SCOPES=['https://www.googleapis.com/auth/drive']

        _base_path = os.path.dirname(__file__)
        _credential_path=os.path.join(_base_path, 'credential.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _credential_path

        #json object credentials
        print('Loading credentials from environment variables')
        self._creds = {
            "type": os.getenv("type"),
            "project_id": os.getenv("project_id"),
            "private_key_id": os.getenv("private_key_id"),
            "private_key": os.getenv("private_key").replace('\\n', '\n'),
            "client_email": os.getenv("client_email"),
            "client_id": os.getenv("client_id"),
            "auth_uri": os.getenv("auth_uri"),
            "token_uri": os.getenv("token_uri"),
            "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
            "client_x509_cert_url": os.getenv("client_x509_cert_url")
        }
        
    def build(self):
        creds =ServiceAccountCredentials.from_json_keyfile_dict(self._creds)
        service = build('drive', 'v3', credentials=creds)
        print('Google Drive service built successfully')

        return service