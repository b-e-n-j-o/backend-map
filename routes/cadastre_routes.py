from flask import Blueprint, jsonify, request
from services.wfs_service import WFSService
from utils.geometry_utils import (
    get_bbox_from_geojson, 
    group_parcelles_by_section, 
    create_section_features
)

# Création du blueprint
cadastre_bp = Blueprint('cadastre', __name__, url_prefix='/api')
wfs_service = WFSService()

@cadastre_bp.route('/sections_cadastrales', methods=['POST'])
def get_sections_cadastrales():
    """Récupère les sections cadastrales distinctes pour une commune"""
    data = request.get_json()
    if not data or 'features' not in data or not data['features']:
        return jsonify({'error': 'GeoJSON de commune requis'}), 400

    bbox_str = get_bbox_from_geojson(data)
    if not bbox_str:
        return jsonify({'error': 'Impossible d\'extraire la bbox du GeoJSON'}), 400

    # Récupérer les parcelles dans la bbox avec seulement les attributs nécessaires
    data_cadastre = wfs_service.get_cadastre_parcelles(bbox_str, property_name='section,geom')
    if not data_cadastre:
        return jsonify({'error': 'Erreur lors de la récupération du cadastre'}), 500

    features_cadastre = data_cadastre.get('features', [])

    # Grouper par section et créer des polygones agrégés
    sections_data = group_parcelles_by_section(features_cadastre, data)

    # Créer des features agrégées par section
    sections_features = create_section_features(sections_data)

    return jsonify({
        'type': 'FeatureCollection',
        'features': sections_features
    })

@cadastre_bp.route('/parcelles_section', methods=['POST'])
def get_parcelles_section():
    """Récupère toutes les parcelles dans la bbox d'une section"""
    try:
        data = request.get_json()
        if not data or 'bbox' not in data:
            return jsonify({'error': 'bbox requis'}), 400

        bbox = data['bbox']  # [minx, miny, maxx, maxy]
        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},EPSG:4326"

        print(f"Récupération parcelles bbox: {bbox_str}")

        data_parcelles = wfs_service.get_cadastre_parcelles(bbox_str)
        if not data_parcelles:
            return jsonify({'error': 'Erreur WFS'}), 500

        nb_parcelles = len(data_parcelles.get('features', []))
        print(f"Parcelles récupérées: {nb_parcelles}")

        return jsonify(data_parcelles)

    except Exception as e:
        print(f"Erreur parcelles_section: {e}")
        return jsonify({'error': str(e)}), 500 