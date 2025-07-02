# Configuration de l'application
class Config:
    # Configuration WFS
    WFS_URL = "https://data.geopf.fr/wfs/ows"
    WFS_VERSION = "2.0.0"
    
    # Configuration Flask
    DEBUG = True
    PORT = 5000
    
    # Limites de requêtes
    MAX_FEATURES = 10000
    DEFAULT_COUNT = 1000 