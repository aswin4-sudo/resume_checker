from flask import Flask, request, jsonify, send_file 
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from analyzer import ResumeAnalyzer
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize analyzer
analyzer = ResumeAnalyzer()

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    """Serve the frontend HTML"""
    return send_file('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Resume Analyzer API is running'})

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Main endpoint to analyze resume"""
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Get job role from form data (optional)
        job_role = request.form.get('job_role', 'General')
        
        # Save file temporarily
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Extract text from PDF
            resume_text = analyzer.extract_text_from_pdf(filepath)
            
            if not resume_text or len(resume_text.strip()) < 50:
                return jsonify({'error': 'Could not extract sufficient text from PDF. Please ensure it contains text.'}), 400
            
            # Analyze resume
            analysis = analyzer.get_role_specific_analysis(resume_text, job_role)
            
            # Add metadata to response
            response = {
                'success': True,
                'filename': original_filename,
                'job_role': job_role,
                'analysis': analysis
            }
            
            return jsonify(response), 200
            
        finally:
            # Clean up: delete temporary file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    """Alternative endpoint to analyze directly pasted text"""
    try:
        data = request.get_json()
        
        if not data or 'resume_text' not in data:
            return jsonify({'error': 'No resume text provided'}), 400
        
        resume_text = data['resume_text']
        job_role = data.get('job_role', 'General')
        
        if len(resume_text.strip()) < 50:
            return jsonify({'error': 'Please provide more text (at least 50 characters)'}), 400
        
        # Analyze resume
        analysis = analyzer.get_role_specific_analysis(resume_text, job_role)
        
        response = {
            'success': True,
            'job_role': job_role,
            'analysis': analysis
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File is too large. Maximum size is 10MB'}), 413

if __name__ == '__main__':
    print("🚀 Starting Resume Analyzer API...")
    print("📍 Server running at: http://localhost:5000")
    print("📝 Endpoints:")
    print("   POST /analyze - Upload PDF file")
    print("   POST /analyze-text - Paste resume text")
    print("   GET  /health - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)