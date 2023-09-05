# FlaskProjects
Project 1

/api/1.0/doc/upload - Uploads the pdf document to uploads/ folder in server and returns a success response once the document is uploaded else returns the error message and code.

/api/1.0/doc/get/<doc_id> -  Renders all the contents of the PDF document as a response keeping the formatting intact.

/api/1.0/doc/get - Returns all the uploaded PDF document’s metadata as a list in response.

/api/1.0/doc/delete/<doc_id>  - Deletes the document from the uploads/ folder and also deletes the metadata from tables.

/api/1.0/doc/update/<doc_id> - Updates the existing document in uploads folder and also updates the metadata

/api/1.0/doc/download/<doc_id> - Downloads the file to local system and updates the metadata.
