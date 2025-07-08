from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from app.webhook import webhook_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Register blueprints
    app.register_blueprint(webhook_bp)
    
    @app.route('/')
    def home():
        return jsonify({
            "message": "Busamed WhatsApp Chatbot API",
            "status": "running",
            "version": "1.0.0"
        })
    
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)