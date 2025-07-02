from flask import Flask
from flask_cors import CORS
from config import Config

# Import des blueprints
from routes.admin_routes import admin_bp
from routes.urbanisme_routes import urbanisme_bp
from routes.cadastre_routes import cadastre_bp
from routes.health_routes import health_bp

def create_app():
    """Factory function pour créer l'application Flask"""
    app = Flask(__name__)
    
    # Configuration CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Enregistrement des blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(urbanisme_bp)
    app.register_blueprint(cadastre_bp)
    app.register_blueprint(health_bp)
    
    return app

if __name__ == '__main__':
    import os
    app = create_app()
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=Config.DEBUG, port=Config.PORT) 