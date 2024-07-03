import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive API credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Replace with your credentials file path

# ID of the folder in Google Drive where you want to upload the PDF
FOLDER_ID = 'your_folder_id'

# Function to convert Word document to PDF using LibreOffice (requires LibreOffice installed)
def convert_to_pdf(word_file, pdf_file):
    os.system(f'libreoffice --headless --convert-to pdf {word_file} --outdir {os.path.dirname(pdf_file)}')

# Function to upload file to Google Drive
def upload_to_drive(service, file_path, folder_id):
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

# Main function
def main():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    word_file = 'resume.docx'  # Replace with your Word document file path
    pdf_file = 'resume.pdf'    # Replace with desired PDF file path

    # Monitor for changes in the Word document
    while True:
        if os.path.exists(word_file):
            # Check if the Word document has been modified
            current_time = os.path.getmtime(word_file)
            if 'last_modified' not in locals() or current_time != last_modified:
                last_modified = current_time
                # Convert Word document to PDF
                convert_to_pdf(word_file, pdf_file)
                # Upload PDF to Google Drive
                upload_to_drive(service, pdf_file, FOLDER_ID)
                print(f'Updated {pdf_file} on Google Drive')
        time.sleep(10)  # Check every 10 seconds

if __name__ == '__main__':
    main()
