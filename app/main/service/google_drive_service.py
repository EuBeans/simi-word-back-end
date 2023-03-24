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
        LOCAL = False
        if LOCAL:
            self._creds =  {
                "type": "service_account",
                "project_id": "uplifted-kit-381518",
                "private_key_id": "20840c30f7b844e32e485b588dea50d9309866cd",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCodln9eaAKOwCZ\nV/JFZNB1zhDaYSA2JCrhOuCJyy5/tcJyVE/JcCq1HzOhIwePM7UpgIm46DGYVCBg\nMyD83hJknkyq4i+QsUdAqSJBjNmLHF5sPJFLtJ1iFCJ2gR88osyRmWRz8I7MQRbW\nDyg55tDkG9ShGJpMlNz86V2fLNv0qFCW+8APbIUs13vPhpwtlkW3HF8CwPcEmS3u\nly5ULG62HjufpMtwhBahwDsLXI5XtDYvO0b7C5WWn2P60ywpZ1VGktZEelDjxQCh\ngo1b68D3GrsQfG4sGILFEOkj2FajiaEvf1LXh7GY65IRCHm6WjbQgiWRpiA+y+Tg\nISFbsotVAgMBAAECgf8BeDoMfAutpMUPxJsLqpnAj3qWKNxaz8LDNEBJwEBJuswz\nMyKyQVDIuzAnDQ2U5W+moDy1edmflC1ey5vs/zYp3cAz35ITMRJUdYusSv00dTWQ\n3ku7iAKCJVV893A0uVj+dLX8s1hHTcGHYM2sPCyWWWOKBD3/BqLExURpsCUqBcG5\nRuj9i+AqZOl+RG2R5NU47soscL776pUkuYPSjWdOWrIdwEwQTQCjNdvsJUBIDOF8\n0Nz34UV1P0Q3xLqtihVGRLmi+JEfZrVtPH648Mvsa5B/VuDUthoo5VNc/U/O8Zzg\nL0F+QhdZBP3rmDAwrBl2KgmHfUTz3n0LtaQe+H8CgYEA0VMUh8SW6Lh4ZLo9L9Fc\niO0xHKeJ/tq9wD+ZH/YuZ0KpivIDAiMvEBEBks1uPjkMGxJj90hi3JVgYSdAAtKD\nQ2gTlngzRc+NgYeKs9jvllcjNED6bfCWCPUrf5qfnJXelMFez2RUFt6/FRr7pWca\nsLX4HzJTOEwZA4+WUJC8Sc8CgYEAzga5TyH4EYcc3zY3tIO/JeiZoSYWJwf2LYQh\nZKpWv8xZu7O3LsQE2CRImQQXjfwbPPrVUYOvpV6nMN7aL3zg5j/APze1cvlOpe6Z\nqL/ba98AjG+MbqAMDlIJebGEML60Fae9X8l6Kz6treSCTIlyY6hBkKyEvO5K1Ca9\n/vd2NZsCgYEAuBeN9b1yTud1knisOTKyZAXebGn4FfgAa2RDYfWbZ9sbyoP/G1Eg\nIcwjCx26d+Sp/eEVo7O4pnCE28yuIg1Lvet5VpsN1Latp54x4OvIAftOjbUbybaN\n7QDZqZauCwNPRpotrM16msZ5XLFnYVclBQZ0WdNjlx5t3VDZjK9NuMcCgYEAkJLt\nVNdsgbhDjWs5eeX9q7dmn0vfvbH7kYMn/8D8sQjQa0Q4pouNLrN/ckkJ0mv4HTmT\nmekDx9L9FfE8QJisJUbVPEd2f+DszMn7cAx6CF9rviDE9hg/fYkZ9xiXv7EDJDMa\nU+5JWbFZJS62NMk6yS4YHFLDruS1A9zP9OxoOkMCgYBTOleUxD/kMT3Q/8xBFncB\nJ7ekLMV6ZmS7/QHhPJJ7TAYGRg2xKEcGcBSW5okgjzlbOy/hDMfpcDadnMjqPIfe\nHBKBOthMugnIwo6F96LmXVYRYhQ18LWWIO7cPE+hZijYVBl/JYjla5oFdgxvnq8q\nStfSJmfE10YS2TiVxnb76g==\n-----END PRIVATE KEY-----\n",
                "client_email": "simordia@uplifted-kit-381518.iam.gserviceaccount.com",
                "client_id": "103873987444409543365",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/simordia%40uplifted-kit-381518.iam.gserviceaccount.com"
            }
        else:
            self._creds = {
                "type": os.getenv("type"),
                "project_id": os.getenv("project_id"),
                "private_key_id": os.getenv("private_key_id"),
                "private_key": os.getenv("private_key"),
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

        return service