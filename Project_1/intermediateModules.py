import os
import fitz  # PyMuPDF library

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def get_pdf_metadata(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)

        # Get basic metadata
        metadata = {
            'filename': os.path.basename(pdf_path),
            'page_count': len(pdf_document),
            'author': pdf_document.metadata.get('author', ''),
            'title': pdf_document.metadata.get('title', ''),
            # Add more metadata fields as needed
        }

        pdf_document.close()

        return metadata

    except Exception as e:
        return {'error': str(e)}