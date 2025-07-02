from shapely.geometry import shape
from shapely.ops import unary_union
from collections import defaultdict

def get_bbox_from_geojson(geojson_data):
    """Extrait la bbox d'un GeoJSON"""
    if not geojson_data or 'features' not in geojson_data or not geojson_data['features']:
        return None
    
    commune_poly = shape(geojson_data['features'][0]['geometry'])
    bbox = commune_poly.bounds  # (minx, miny, maxx, maxy)
    return f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},EPSG:4326"

def filter_features_by_commune(features, commune_geojson):
    """Filtre les features pour ne garder que celles dans la commune"""
    if not commune_geojson or 'features' not in commune_geojson or not commune_geojson['features']:
        return []
    
    commune_poly = shape(commune_geojson['features'][0]['geometry'])
    filtered = []
    
    for feat in features:
        try:
            geom = shape(feat['geometry'])
            centroid = geom.centroid
            if commune_poly.contains(centroid):
                filtered.append(feat)
        except Exception as e:
            continue
    
    return filtered

def group_parcelles_by_section(parcelles_features, commune_geojson):
    """Groupe les parcelles par section cadastrale"""
    if not commune_geojson or 'features' not in commune_geojson or not commune_geojson['features']:
        return []
    
    commune_poly = shape(commune_geojson['features'][0]['geometry'])
    sections_data = defaultdict(list)
    
    for feat in parcelles_features:
        try:
            geom = shape(feat['geometry'])
            if commune_poly.contains(geom.centroid):
                section = feat['properties'].get('section', 'INCONNUE')
                sections_data[section].append(geom)
        except Exception as e:
            continue
    
    return sections_data

def create_section_features(sections_data):
    """Crée des features agrégées par section cadastrale"""
    sections_features = []
    
    for section, geometries in sections_data.items():
        if geometries:
            try:
                union_geom = unary_union(geometries)
                
                section_feature = {
                    'type': 'Feature',
                    'geometry': union_geom.__geo_interface__,
                    'properties': {
                        'section': section,
                        'nb_parcelles': len(geometries),
                        'type': 'section_cadastrale'
                    }
                }
                sections_features.append(section_feature)
            except Exception as e:
                print(f"Erreur lors de l'union pour la section {section}: {e}")
                continue
    
    return sections_features 