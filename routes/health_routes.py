from flask import Blueprint, jsonify

# Création du blueprint
health_bp = Blueprint('health', __name__, url_prefix='/api')

@health_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'OK'}) 