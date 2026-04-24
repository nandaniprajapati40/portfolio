from flask import Flask, request, jsonify, render_template, render_template_string
from flask_cors import CORS
from flask_pymongo import PyMongo
from datetime import datetime
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Jinja2 to not conflict with Vue.js
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'

# MongoDB Configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/portfolio_db")
mongo = PyMongo(app)

# Data Models
portfolioData = {
    "name": "Nandani Prajapati",
    "email": "nandaniprajapati0104@gmail.com",
    "phone": "+91 9329391862",
    "linkedin": "https://www.linkedin.com/in/nandani-prajapati-7ab229282",
    "title": "Data Science & AI Specialist",
    "bio": "Data Science postgraduate with expertise in Machine Learning, NLP, and backend development.",
    "education": [
        {
            "degree": "Master of Computer Applications in Data Science",
            "institution": "Dev Sanskriti Vishwavidyalaya Haridwar",
            "year": "2024 - 2026 (Pursuing)"
        },
        {
            "degree": "Bachelor of Computer Application",
            "institution": "Barkatullah University, Bhopal",
            "cgpa": 8.4,
            "year": "2021 - 2024"
        }
    ],
    "skills": {
        "programming": ["Python", "SQL", "JavaScript"],
        "ml": ["TensorFlow", "Scikit-learn", "NLP", "Deep Learning"],
        "frameworks": ["Flask", "NumPy", "Pandas", "Matplotlib", "LangChain"],
        "geospatial": ["Google Earth Engine", "GeoServer", "QGIS", "Remote Sensing"],
        "databases": ["MongoDB", "MySQL"],
        "tools": ["Git", "GitHub", "VS Code", "Jupyter", "Power BI"]
    },
    "projects": [
        {
            "title": "Irrigation Crop Water Requirements",
            "description": "IIRS-ISRO Project with satellite-driven crop water estimation",
            "tech": ["Google Earth Engine", "GeoServer", "Remote Sensing"],
            "period": "Jan 2026 - Present",
            "highlights": [
                "Satellite-driven water requirement prediction",
                "GIS layer orchestration and deployment",
                "Real-time irrigation recommendations"
            ]
        },
        {
            "title": "AI-Powered Audiobook Generation",
            "description": "GenAI pipeline converting ebooks to audiobooks",
            "tech": ["LLM", "TTS", "Flask", "MongoDB"],
            "period": "Feb 2026 - Mar 2026",
            "highlights": [
                "LLM-based text processing",
                "Scalable parallel audio generation",
                "Async job tracking system"
            ]
        }
    ]
}

# Routes

@app.route('/')
def index():
    """Serve the portfolio HTML"""
    return render_template('portfolio.html')

@app.route('/admin')
def admin():
    """Serve the admin dashboard"""
    return render_template('admin.html')

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get complete portfolio data"""
    return jsonify(portfolioData), 200

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    return jsonify(portfolioData['skills']), 200

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    return jsonify(portfolioData['projects']), 200

@app.route('/api/education', methods=['GET'])
def get_education():
    """Get education details"""
    return jsonify(portfolioData['education']), 200

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'email', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Store in MongoDB
        contact_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'subject': data.get('subject', ''),
            'message': data.get('message'),
            'timestamp': datetime.now(),
            'status': 'new'
        }
        
        # Insert into database
        result = mongo.db.contacts.insert_one(contact_data)
        
        return jsonify({
            'success': True,
            'message': 'Message received! I will get back to you soon.',
            'id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact/list', methods=['GET'])
def get_contacts():
    """Get all contacts (admin only - would need authentication)"""
    try:
        contacts = list(mongo.db.contacts.find().sort('timestamp', -1))
        # Convert ObjectId to string for JSON serialization
        for contact in contacts:
            contact['_id'] = str(contact['_id'])
            contact['timestamp'] = contact['timestamp'].isoformat()
        return jsonify(contacts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get portfolio statistics"""
    try:
        total_contacts = mongo.db.contacts.count_documents({})
        new_contacts = mongo.db.contacts.count_documents({'status': 'new'})
        
        stats = {
            'total_contacts': total_contacts,
            'new_contacts': new_contacts,
            'total_projects': len(portfolioData['projects']),
            'total_skills': sum(len(v) for v in portfolioData['skills'].values())
        }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact/<contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Update contact status"""
    try:
        from bson.objectid import ObjectId
        
        data = request.get_json()
        result = mongo.db.contacts.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {'status': data.get('status', 'new')}}
        )
        
        return jsonify({
            'success': True,
            'modified': result.modified_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)