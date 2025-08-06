from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2
import os
from io import BytesIO
import tempfile

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has a valid extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def merge_pdfs(pdf_files):
    """
    Merge multiple PDF files into a single PDF
    Args:
        pdf_files: List of file objects
    Returns:
        BytesIO object containing the merged PDF
    """
    merger = PyPDF2.PdfMerger()
    
    try:
        for pdf_file in pdf_files:
            # Reset file pointer to beginning
            pdf_file.seek(0)
            merger.append(pdf_file)
        
        # Create output buffer
        output_buffer = BytesIO()
        merger.write(output_buffer)
        output_buffer.seek(0)
        
        merger.close()
        return output_buffer
        
    except Exception as e:
        merger.close()
        raise e

@app.route('/')
def index():
    """Display the main page with upload form"""
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdf():
    """Handle PDF file upload and merging"""
    try:
        # Check if files were uploaded
        if 'pdf_files' not in request.files:
            flash('No files selected')
            return redirect(url_for('index'))
        
        files = request.files.getlist('pdf_files')
        
        # Validate that files were selected
        if not files or all(file.filename == '' for file in files):
            flash('No files selected')
            return redirect(url_for('index'))
        
        # Validate file types and collect valid files
        valid_files = []
        for file in files:
            if file and allowed_file(file.filename):
                valid_files.append(file)
            elif file.filename != '':
                flash(f'Invalid file type: {file.filename}. Only PDF files are allowed.')
                return redirect(url_for('index'))
        
        # Check if we have at least 2 files to merge
        if len(valid_files) < 2:
            flash('Please select at least 2 PDF files to merge')
            return redirect(url_for('index'))
        
        # Merge the PDF files
        merged_pdf = merge_pdfs(valid_files)
        
        # Generate filename for merged PDF
        merged_filename = 'merged_document.pdf'
        
        # Return the merged PDF as download
        return send_file(
            merged_pdf,
            as_attachment=True,
            download_name=merged_filename,
            mimetype='application/pdf'
        )
        
    except PyPDF2.errors.PdfReadError:
        flash('Error: One or more files are corrupted or not valid PDF files')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An error occurred while merging PDFs: {str(e)}')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File is too large. Maximum size is 16MB per file.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
