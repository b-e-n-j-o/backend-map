# Backend Modulaire - Application Flask

## Structure du Projet

```
backend/
├── app.py                    # Ancienne application monolithique
├── app_modular.py           # Nouvelle application modulaire
├── config.py                # Configuration centralisée
├── requirements.txt         # Dépendances
├── README.md               # Ce fichier
├── services/               # Services métier
│   ├── __init__.py
│   └── wfs_service.py      # Service pour les requêtes WFS
├── utils/                  # Utilitaires
│   ├── __init__.py
│   └── geometry_utils.py   # Utilitaires géométriques
└── routes/                 # Routes organisées par domaine
    ├── __init__.py
    ├── admin_routes.py     # Routes administratives (départements, communes)
    ├── urbanisme_routes.py # Routes d'urbanisme
    ├── cadastre_routes.py  # Routes cadastrales
    └── health_routes.py    # Routes de santé
```

## Avantages de cette Structure

### 1. **Séparation des Responsabilités**
- **Services** : Logique métier et accès aux données
- **Routes** : Gestion des endpoints HTTP
- **Utils** : Fonctions utilitaires réutilisables
- **Config** : Configuration centralisée

### 2. **Maintenabilité**
- Chaque module a une responsabilité claire
- Modifications isolées sans impact sur l'ensemble
- Code plus facile à tester

### 3. **Évolutivité**
- Ajout facile de nouveaux endpoints
- Réutilisation des services existants
- Structure extensible

### 4. **Testabilité**
- Tests unitaires par module
- Mocking facilité
- Isolation des composants

## Utilisation

### Démarrage de l'application modulaire :
```bash
python app_modular.py
```

### Ajout d'un nouveau service :
1. Créer un nouveau fichier dans `services/`
2. Implémenter la logique métier
3. Utiliser dans les routes appropriées

### Ajout d'une nouvelle route :
1. Créer un nouveau blueprint dans `routes/`
2. Implémenter les endpoints
3. Enregistrer le blueprint dans `app_modular.py`

## Migration depuis l'ancienne structure

L'ancien fichier `app.py` est conservé pour référence. La nouvelle structure `app_modular.py` offre les mêmes fonctionnalités mais de manière organisée.

## Configuration

Tous les paramètres sont centralisés dans `config.py` :
- URLs WFS
- Versions des services
- Paramètres Flask
- Limites de requêtes 