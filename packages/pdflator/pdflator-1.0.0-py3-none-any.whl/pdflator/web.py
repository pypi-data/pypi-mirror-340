import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv, set_key
from pathlib import Path

# Import your existing functionality
from pdflator.languages import *
from pdflator.translation import *
from pdflator.translate_pdf import translate_pdf

# Initialize Flask app
app = Flask(__name__)

# Configure upload and download folders
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
ALLOWED_EXTENSIONS = {'pdf'}

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Load environment variables
load_dotenv()
env_path = Path('.') / '.env'

def allowed_file(filename) -> bool:
    """
    Checks if the given filename has an allowed (PDF) extension.

    :param filename: The name of the file to check.
    :type filename: str
    :return: True if the file has an allowed extension, False otherwise.
    :rtype: bool
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    """
    Renders the main index page with available languages and translators.

    :return: The rendered HTML template for the index page.
    :rtype: str
    """
    # Get list of available languages
    languages : list[dict[str,str]] = LanguageFactory.list_languages()
    # Dynamically get the translators from the translation folder
    translators : list[dict[str, str]] = TranslatorFactory.list_translators()
    return render_template('index.html', languages=languages, translators = translators)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles the PDF upload and returns JSON containing file paths.

    :return: JSON response with input and output file paths, or an error message.
    :rtype: flask.Response
    :raises werkzeug.exceptions.BadRequest: If the request does not contain a file,
                                            or if the file has an invalid extension.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filenames for input and output
        filename = secure_filename(file.filename or "")
        file_id = str(uuid.uuid4())
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
        output_filename = f"translated_{file_id}_{filename}"
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)
        
        # Save uploaded file
        file.save(input_path)
        
        # Return file information for the next step
        return jsonify({
            'input_path': input_path,
            'output_path': output_path,
            'output_filename': output_filename
        }), 200
    else:
        return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400

@app.route('/process_translation', methods=['POST'])
def process_translation():
    """
    Processes PDF translation using the provided language and translator.

    :return: JSON response with a redirect URL to the translated file, or an error message.
    :rtype: flask.Response
    :raises ValueError: If any of the required parameters are missing.
    :raises Exception: If an error occurs during the translation process.
    """
    data = request.get_json()
    input_path = data.get('input_path')
    output_path = data.get('output_path')
    output_filename = data.get('output_filename')
    source_language = data.get('source_language', 'auto')
    dest_lang = data.get('target_language', 'en')
    translator_code = data.get('translator', 'gtrans')

    if not all([input_path, output_path, output_filename, dest_lang, translator_code]):
        return jsonify({'error': 'Missing parameters for translation'}), 400
    
    try:
        # Run translation
        translate_pdf(
            input_path=input_path,
            output_path=output_path,
            input_lang=source_language, 
            dest_lang=dest_lang,
            translator_code=translator_code
        )
        
        # Clean up the uploaded file
        os.remove(input_path)
        
        return jsonify({'redirect_url': url_for('download_file', filename=output_filename)}), 200
    except Exception as e:
        return jsonify({'error': f'Error during translation: {str(e)}'}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    """
    Renders a page with a link to download the translated PDF.

    :param filename: The name of the translated file.
    :type filename: str
    :return: The rendered HTML template for the result page.
    :rtype: str
    """
    return render_template('result.html', filename=filename)

@app.route('/get-file/<filename>')
def get_file(filename):
    """
    Sends the requested file from the download folder to the client.

    :param filename: The name of the file to download.
    :type filename: str
    :return: The file as an attachment.
    :rtype: flask.Response
    """
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/history')
def history():
    """
    Displays the user's translation history (placeholder).

    :return: The rendered HTML template for the history page.
    :rtype: str
    """
    # TODO: Implement logic to fetch and display translation history
    return render_template('history.html')

@app.route('/config', methods=['GET'])
def config_page():
    """
    Renders the configuration page.
    """
    output_font_size = os.getenv("OUTPUT_FONT_SIZE", 12)
    # Use the renamed variable
    redaction_color = os.getenv("REDACTION_COLOR", "(1,1,1)")
    scaling_factor = os.getenv("SCALING_FACTOR", 0.75)
    return render_template('config.html',
                           output_font_size=output_font_size,
                           # Pass the renamed variable to the template
                           redaction_color=redaction_color,
                           scaling_factor=scaling_factor)

@app.route('/update_config', methods=['POST'])
def update_config():
    """
    Updates the configuration values in .env.
    """
    output_font_size  = request.form.get('output_font_size')
    # Get values using the new form names
    redaction_color = f"({request.form.get('redaction_color_r')}, {request.form.get('redaction_color_g')}, {request.form.get('redaction_color_b')})"
    scaling_factor = request.form.get('scaling_factor')

    set_key(env_path, "OUTPUT_FONT_SIZE", output_font_size)
    # Save using the new variable name
    set_key(env_path, "REDACTION_COLOR", redaction_color)
    set_key(env_path, "SCALING_FACTOR", scaling_factor)

    return redirect(url_for('config_page'))

def run_web_app(host='127.0.0.1', port=5000, debug=False):
    """
    Start the Flask web application with the specified host and port.
    This function is called when the user runs 'pdflator web'.
    
    Args:
        host (str): The host address to listen on
        port (int): The port to listen on
        debug (bool): Whether to run in debug mode
    """
    # Create necessary folders
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    
    print(f"Starting PDFlator web interface at http://{host}:{port}")
    app.run(debug=debug, host=host, port=port)

def main():
    """
    Main function for the 'pdflator-web' legacy command.
    This will be deprecated in future versions.
    """
    import warnings
    warnings.warn(
        "The 'pdflator-web' command is deprecated. Please use 'pdflator web' instead.",
        DeprecationWarning, 
        stacklevel=2
    )
    run_web_app(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_web_app(debug=True)