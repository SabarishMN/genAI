import json
import os
from openai import OpenAI
import pandas as pd
import numpy as np
from getpass import getpass
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SimpleField, SearchFieldDataType, SearchIndex
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# /blob/

load_dotenv()
account_url = "https://mtinternshipsa.blob.core.windows.net"
default_credential = DefaultAzureCredential()
credential = AzureKeyCredential(str(os.getenv("AZURE_KEY_CREDENTIAL")))
blob_service_client = BlobServiceClient(account_url, credential=default_credential)
search_svc_endpoint = os.getenv("SEARCH_SERVICE_ENDPOINT")
rec_endpoint = os.getenv("RECOGNIZER_ENDPOINT")
rec_key = os.getenv("RECOGNIZER_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def writeToBlob(filename):
    blob_client = blob_service_client.get_blob_client(container="mt-intership-us-sabarish", blob=filename)

    print("\nUploading to Azure Storage as blob:\n\t" + filename)

    # Upload the created file
    with open(file=filename, mode="rb") as data:
        blob_client.upload_blob(data, overwrite=True)

