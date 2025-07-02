from flask import Blueprint, jsonify, request
from services.wfs_service import WFSService

# Création du blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api')
wfs_service = WFSService()

@admin_bp.route('/departements')
def get_departements():
    """Endpoint pour récupérer les départements"""
    bbox = request.args.get('bbox')
    print(f"Requête départements avec bbox: {bbox}")
    
    data = wfs_service.get_departements(bbox)
    
    if data:
        print(f"Données WFS reçues, nombre de features: {len(data.get('features', []))}")
        # Simplification des données pour l'affichage
        features = []
        for feature in data.get('features', []):
            properties = feature.get('properties', {})
            print(f"Feature properties: {properties}")
            simplified_feature = {
                'type': 'Feature',
                'geometry': feature.get('geometry'),
                'properties': {
                    'code': properties.get('code_insee', ''),
                    'nom': properties.get('nom', ''),
                    'code_insee': properties.get('code_insee', ''),
                    'region': properties.get('nom_region', '')
                }
            }
            features.append(simplified_feature)
        
        result = {
            'type': 'FeatureCollection',
            'features': features
        }
        print(f"Résultat final: {len(features)} features")
        return jsonify(result)
    
    print("Aucune donnée reçue de l'API WFS")
    return jsonify({'error': 'Erreur lors de la récupération des départements'}), 500

@admin_bp.route('/communes')
def get_communes():
    """Endpoint pour récupérer les communes"""
    bbox = request.args.get('bbox')
    dept_code = request.args.get('dept_code')
    
    print(f"Requête communes avec dept_code: {dept_code}, bbox: {bbox}")
    
    data = wfs_service.get_communes(bbox, dept_code)
    
    if data:
        print(f"Données communes WFS reçues, nombre de features: {len(data.get('features', []))}")
        # Simplification des données
        features = []
        for feature in data.get('features', []):
            properties = feature.get('properties', {})
            print(f"Commune properties: {properties}")
            simplified_feature = {
                'type': 'Feature',
                'geometry': feature.get('geometry'),
                'properties': {
                    'code_insee': properties.get('code_insee', ''),
                    'nom': properties.get('nom', ''),
                    'code_dept': properties.get('code_dept', ''),
                    'population': properties.get('population', 0)
                }
            }
            features.append(simplified_feature)
        
        result = {
            'type': 'FeatureCollection',
            'features': features
        }
        print(f"Résultat communes final: {len(features)} features")
        return jsonify(result)
    
    print("Aucune donnée reçue de l'API WFS pour les communes")
    return jsonify({'error': 'Erreur lors de la récupération des communes'}), 500 