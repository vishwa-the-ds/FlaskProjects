from flask import Flask, request, jsonify,Response,send_file
from werkzeug.utils import secure_filename
import fitz  
import os
from intermediateModules import allowed_file,get_pdf_metadata

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/api/1.0/doc/upload' , methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@app.route('/api/1.0/doc/get/<doc_id>', methods=['GET'])
def get_pdf_content(doc_id):
    # Replace 'your_pdf_directory' with the actual directory where your PDFs are stored
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'],f'{doc_id}.pdf')

    try:
        # Open the PDF document
        pdf_document = fitz.open(pdf_path)
        pdf_text = ""

        # Read and render PDF content
        for page in pdf_document:
            pdf_text += page.get_text("text")

        pdf_document.close()

        # Return PDF content as response with formatting intact
        response = Response(pdf_text, content_type='text/plain')
        response.headers['Content-Disposition'] = f'inline; filename={doc_id}.pdf'
        return response

    except Exception as e:
        return str(e), 404

@app.route('/api/1.0/doc/get', methods=['GET'])
def get_all_pdf_metadata():
    pdf_directory = app.config['UPLOAD_FOLDER'] # Replace with the actual directory path

    pdf_metadata_list = []

    # Iterate through PDF files in the directory
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            pdf_metadata = get_pdf_metadata(pdf_path)
            pdf_metadata_list.append(pdf_metadata)

    return jsonify(pdf_metadata_list)

@app.route('/api/1.0/doc/delete/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    pdf_directory = app.config['UPLOAD_FOLDER']  # Replace with the actual directory path where PDFs are stored
    pdf_path = os.path.join(pdf_directory, f'{doc_id}.pdf')

    try:
        # Check if the PDF file exists
        if os.path.exists(pdf_path):
            # Delete the PDF file
            os.remove(pdf_path)         

            return jsonify({'message': 'Document deleted successfully'}), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/1.0/doc/update/<doc_id>', methods=['PUT'])
def update_document(doc_id):
    pdf_directory = app.config['UPLOAD_FOLDER']  # Replace with the actual directory path where PDFs are stored
    pdf_path = os.path.join(pdf_directory, f'{doc_id}.pdf')

    try:
        # Check if the PDF file exists
        if os.path.exists(pdf_path):
            # Delete the existing PDF file
            os.remove(pdf_path)

            # Save the updated PDF file
            new_pdf_file = request.files.get('file')
            if new_pdf_file:
                new_pdf_file.save(pdf_path)
                

                return jsonify({'message': 'Document and metadata updated successfully'}), 200
            else:
                return jsonify({'error': 'No file provided for update'}), 400
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/1.0/doc/download/<doc_id>', methods=['GET'])
def download_document(doc_id):
    pdf_directory = app.config['UPLOAD_FOLDER']   # Replace with the actual directory path where PDFs are stored
    pdf_path = os.path.join(pdf_directory, f'{doc_id}.pdf')

    try:
        # Check if the PDF file exists
        if os.path.exists(pdf_path):
            
            return send_file(pdf_path, as_attachment=True)

        else:
            return jsonify({'error': 'Document not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)





