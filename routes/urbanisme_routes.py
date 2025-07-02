from flask import Blueprint, jsonify, request
from services.wfs_service import WFSService
from utils.geometry_utils import get_bbox_from_geojson, filter_features_by_commune

# Création du blueprint
urbanisme_bp = Blueprint('urbanisme', __name__, url_prefix='/api')
wfs_service = WFSService()

@urbanisme_bp.route('/urbanisme/<layer_type>')
def get_urbanisme_data(layer_type):
    """Endpoint générique pour les données d'urbanisme"""
    bbox = request.args.get('bbox')
    commune_code = request.args.get('commune_code')
    
    data = wfs_service.get_urbanisme_data(layer_type, bbox, commune_code)
    
    if data:
        return jsonify(data)
    
    return jsonify({'error': f'Erreur lors de la récupération des données {layer_type}'}), 500

@urbanisme_bp.route('/zonage_plu', methods=['POST'])
def get_zonage_plu():
    """Endpoint pour récupérer les entités du zonage PLU qui intersectent le polygone de la commune sélectionnée"""
    data = request.get_json()
    if not data or 'features' not in data or not data['features']:
        return jsonify({'error': 'GeoJSON de périmètre requis'}), 400

    bbox_str = get_bbox_from_geojson(data)
    if not bbox_str:
        return jsonify({'error': 'Impossible d\'extraire la bbox du GeoJSON'}), 400

    # Récupérer les entités du zonage PLU dans la bbox
    data_plu = wfs_service.get_zonage_plu(bbox_str)
    if not data_plu:
        return jsonify({'error': 'Erreur lors de la récupération du zonage PLU'}), 500

    features_plu = data_plu.get('features', [])
    
    # Filtrer : ne garder que les entités dont le centroïde est dans le polygone de la commune
    filtered = filter_features_by_commune(features_plu, data)

    return jsonify({
        'type': 'FeatureCollection',
        'features': filtered
    })

@urbanisme_bp.route('/prescriptions_surfaciques', methods=['POST'])
def get_prescriptions_surfaciques():
    """Endpoint pour récupérer les prescriptions surfaciques (servitudes) qui intersectent le polygone de la commune sélectionnée"""
    data = request.get_json()
    if not data or 'features' not in data or not data['features']:
        return jsonify({'error': 'GeoJSON de périmètre requis'}), 400

    bbox_str = get_bbox_from_geojson(data)
    if not bbox_str:
        return jsonify({'error': 'Impossible d\'extraire la bbox du GeoJSON'}), 400

    # Récupérer les prescriptions surfaciques dans la bbox
    data_prescriptions = wfs_service.get_prescriptions_surfaciques(bbox_str)
    if not data_prescriptions:
        return jsonify({'error': 'Erreur lors de la récupération des prescriptions surfaciques'}), 500

    features_prescriptions = data_prescriptions.get('features', [])
    
    # Filtrer : ne garder que les entités dont le centroïde est dans le polygone de la commune
    filtered = filter_features_by_commune(features_prescriptions, data)

    # Extraire les libellés uniques présents dans les données filtrées
    libelles_uniques = set()
    for feature in filtered:
        libelle = feature.get('properties', {}).get('libelle', 'Inconnu')
        if libelle:
            libelles_uniques.add(libelle)

    return jsonify({
        'type': 'FeatureCollection',
        'features': filtered,
        'libelles_uniques': list(libelles_uniques)
    }) 