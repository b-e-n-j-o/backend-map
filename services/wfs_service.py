import requests
import json
from config import Config

class WFSService:
    def __init__(self):
        self.wfs_url = Config.WFS_URL
        self.wfs_version = Config.WFS_VERSION
    
    def _make_wfs_request(self, params):
        """Méthode utilitaire pour faire des requêtes WFS"""
        print(f"URL WFS: {self.wfs_url}")
        print(f"Paramètres: {params}")
        
        response = requests.get(self.wfs_url, params=params)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Nombre de features reçues: {len(data.get('features', []))}")
                return data
            except json.JSONDecodeError as e:
                print(f"Erreur JSON: {e}")
                print(f"Contenu de la réponse: {response.text[:500]}")
                return None
        else:
            print(f"Erreur HTTP: {response.status_code}")
            print(f"Contenu de la réponse: {response.text[:500]}")
        return None
    
    def get_departements(self, bbox=None):
        """Récupère les départements"""
        params = {
            'service': 'WFS',
            'version': self.wfs_version,
            'request': 'GetFeature',
            'typename': 'ADMIN-EXPRESS-COG-CARTO-PE.LATEST:departement',
            'outputFormat': 'application/json',
            'srsname': 'EPSG:4326',
            'count': Config.DEFAULT_COUNT
        }
        
        return self._make_wfs_request(params)
    
    def get_communes(self, bbox=None, dept_code=None):
        """Récupère les communes"""
        params = {
            'service': 'WFS',
            'version': self.wfs_version,
            'request': 'GetFeature',
            'typename': 'BDCARTO_V5:commune',
            'outputFormat': 'application/json',
            'srsname': 'EPSG:4326',
            'count': Config.DEFAULT_COUNT
        }
        
        if bbox:
            params['bbox'] = bbox
        
        if dept_code:
            params['cql_filter'] = f"code_insee_du_departement='{dept_code}'"
            
        return self._make_wfs_request(params)
    
    def get_urbanisme_data(self, layer_type, bbox=None, commune_code=None):
        """Récupère les données d'urbanisme"""
        layer_mapping = {
            'servitudes': 'SUP_V3:servitude',
            'zonage_plu': 'PLU_V2:zonage',
        }
        
        typename = layer_mapping.get(layer_type)
        if not typename:
            return None
        
        params = {
            'service': 'WFS',
            'version': self.wfs_version,
            'request': 'GetFeature',
            'typename': typename,
            'outputFormat': 'application/json',
            'srsname': 'EPSG:4326'
        }
        
        if bbox:
            params['bbox'] = bbox
            
        if commune_code:
            params['cql_filter'] = f"code_commune='{commune_code}'"
        
        return self._make_wfs_request(params)
    
    def get_prescriptions_surfaciques(self, bbox_str):
        """Récupère les prescriptions surfaciques (servitudes)"""
        params = {
            'service': 'WFS',
            'version': self.wfs_version,
            'request': 'GetFeature',
            'typeNames': 'wfs_du:prescription_surf',
            'outputFormat': 'application/json',
            'srsName': 'EPSG:4326',
            'bbox': bbox_str,
            'count': Config.DEFAULT_COUNT
        }
        
        return self._make_wfs_request(params)
    
    def get_zonage_plu(self, bbox_str):
        """Récupère le zonage PLU"""
        params = {
            'service': 'WFS',
            'version': self.wfs_version,
            'request': 'GetFeature',
            'typeNames': 'wfs_du:zone_urba',
            'outputFormat': 'application/json',
            'srsName': 'EPSG:4326',
            'bbox': bbox_str,
            'count': Config.DEFAULT_COUNT
        }
        
        return self._make_wfs_request(params)
    
    def get_cadastre_parcelles(self, bbox_str, property_name=None):
        """Récupère les parcelles cadastrales"""
        params = {
            'service': 'WFS',
            'version': self.wfs_version,
            'request': 'GetFeature',
            'typeNames': 'CADASTRALPARCELS.PARCELLAIRE_EXPRESS:parcelle',
            'outputFormat': 'application/json',
            'srsName': 'EPSG:4326',
            'bbox': bbox_str,
            'count': Config.MAX_FEATURES
        }
        
        if property_name:
            params['propertyName'] = property_name
        
        return self._make_wfs_request(params) 