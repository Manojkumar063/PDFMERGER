# PDF Merger

A simple web application built with Flask that allows users to merge multiple PDF files into a single PDF document.

## Features

- Upload multiple PDF files
- Merge PDFs in the order they were uploaded
- Download the merged PDF file
- File validation (only PDF files allowed)
- File size limit (16MB per file)
- User-friendly interface with drag and drop support
- Error handling for corrupted PDFs and large files

## Requirements

- Python 3.x
- Flask==2.0.1
- PyPDF2==3.0.1
- Werkzeug==2.0.1

## Installation

1. Clone this repository or download the source code.

2. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. Use the web interface to:
   - Click the upload area or drag and drop PDF files
   - Select multiple PDF files you want to merge
   - Click "Merge PDFs" button
   - Download the merged PDF file

## Project Structure

```
pdf_merger/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               
│   └── style.css         # CSS styling
├── templates/
│   └── index.html        # HTML template
└── uploads/              # Directory for temporary files
```

## Error Handling

The application includes error handling for:
- Invalid file types
- Corrupted PDF files
- Files exceeding size limit
- Missing file selections
- General exceptions during merging

## Security Features

- Secure filename handling
- File type validation
- Maximum file size limit
- Secret key configuration

## Development

To run the application in debug mode:
```bash
python app.py
```

The application will start in debug mode, which provides detailed error messages and auto-reloads when code changes are detected.

## Contributing

Feel free to submit issues and enhancement requests!
