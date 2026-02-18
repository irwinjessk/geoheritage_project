# 🏛️ Projet GeoHeritage - Documentation Complète

## 📋 Vue d'ensemble du projet

**GeoHeritage** est une plateforme web de gestion et de découverte des sites patrimoniaux géolocalisés. L'application permet aux utilisateurs de :
- Répertorier les sites patrimoniaux (monuments, musées, sites naturels, bâtiments historiques)
- Localiser les sites sur des cartes interactives
- Rechercher des patrimoines par proximité géographique
- Gérer les droits d'accès selon les rôles utilisateurs

---

## 🏗️ Architecture Technique

### Backend (Django REST Framework)
- **Framework** : Django 5.2.6 avec Django REST Framework 3.16.1
- **Base de données** : PostgreSQL avec psycopg2-binary
- **Authentification** : JWT (JSON Web Tokens) avec SimpleJWT
- **Documentation API** : Swagger/OpenAPI avec drf-yasg
- **Géolocalisation** : GDAL, Shapely, geopy pour les calculs de distance

### Frontend (Angular)
- **Framework** : Angular 17+ avec architecture standalone
- **Build** : Optimisé (157.22 kB)
- **Architecture** : Feature modules, services, composants réutilisables

---

## 🗄️ Modèle de données - Diagramme des classes

```mermaid
classDiagram
    class User {
        +int id
        +string username
        +string email
        +string phone
        +string address
        +datetime created_at
        +datetime updated_at
        +ManyToMany roles
    }
    
    class Role {
        +int id
        +string name
        +string description
        +int level
        +datetime created_at
    }
    
    class Patrimoine {
        +int id
        +string nom
        +text description
        +string type
        +decimal latitude
        +decimal longitude
        +string ville
        +date date_creation
        +string photo_url
        +datetime created_at
        +datetime updated_at
        +ForeignKey created_by
    }
    
    User ||--o{ Patrimoine : creates
    User }o--o{ Role : has
    Role }|--|{ User : assigned to
    
    note for User "Hérite de AbstractUser Django"
    note for Role "4 niveaux : admin(1), moderateur(2), contributeur(3), utilisateur(4)"
    note for Patrimoine "Types : monument, musee, site_naturel, batiment"
```

---

## 🔐 Système de permissions

### Hiérarchie des rôles
1. **Admin (level 1)** : Accès total à toutes les fonctionnalités
2. **Modérateur (level 2)** : Gestion de tous les patrimoines
3. **Contributeur (level 3)** : Création et gestion de ses patrimoines
4. **Utilisateur (level 4)** : Lecture seule

### Permissions par action
| Action | Admin | Modérateur | Contributeur | Utilisateur |
|--------|-------|------------|--------------|-------------|
| Lire les patrimoines | ✅ | ✅ | ✅ | ✅ |
| Créer un patrimoine | ✅ | ✅ | ✅ | ❌ |
| Modifier ses patrimoines | ✅ | ✅ | ✅ | ❌ |
| Modifier tous patrimoines | ✅ | ✅ | ❌ | ❌ |
| Supprimer ses patrimoines | ✅ | ✅ | ✅ | ❌ |
| Supprimer tous patrimoines | ✅ | ✅ | ❌ | ❌ |

---

## 🌐 Web Service REST API

### Endpoints d'authentification (`/api/v1/auth/`)
```http
POST   /api/v1/auth/login/          # Connexion JWT
POST   /api/v1/auth/refresh/        # Rafraîchir token
POST   /api/v1/auth/logout/         # Déconnexion
GET    /api/v1/auth/profile/        # Profil utilisateur
```

### Endpoints Patrimoines (`/api/v1/patrimoines/`)
```http
GET    /api/v1/patrimoines/                    # Liste avec pagination/filtres
POST   /api/v1/patrimoines/                    # Créer un patrimoine
GET    /api/v1/patrimoines/{id}/               # Détail d'un patrimoine
PUT    /api/v1/patrimoines/{id}/               # Modifier un patrimoine
DELETE /api/v1/patrimoines/{id}/               # Supprimer un patrimoine
GET    /api/v1/patrimoines/map-data/           # Données légères pour carte
GET    /api/v1/patrimoines/nearby/             # Recherche par proximité
```

### Paramètres de recherche
- **Filtres** : `ville`, `type`, `page`, `page_size`
- **Recherche** : `search` (nom, description, ville)
- **Tri** : `ordering` (nom, ville, date_creation, created_at)

### Recherche par proximité (`/api/v1/patrimoines/nearby/`)
```http
GET /api/v1/patrimoines/nearby/?lat=48.8566&lng=2.3522&radius=10
```
- **lat/lng** : Coordonnées du point de référence
- **radius** : Rayon de recherche en km
- **Algorithme** : Formule de Haversine pour calcul de distance

---

## 📊 Sérialiseurs (Data Transfer Objects)

### PatrimoineSerializer
```json
{
  "id": 1,
  "nom": "Tour Eiffel",
  "description": "Monument emblématique de Paris",
  "type": "monument",
  "latitude": "48.858370",
  "longitude": "2.294481",
  "ville": "Paris",
  "date_creation": "1889-03-31",
  "photo_url": "https://example.com/photo.jpg",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@geoheritage.com"
  },
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### PatrimoineMapSerializer (optimisé pour cartes)
```json
{
  "id": 1,
  "nom": "Tour Eiffel",
  "latitude": "48.858370",
  "longitude": "2.294481",
  "type": "monument",
  "ville": "Paris"
}
```

---

## 🌍 Fonctionnalités géospatiales

### Calcul de distance (Haversine)
```python
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    # ... implémentation formule Haversine
    return distance_km
```

### Types de patrimoine
- **monument** : Monuments historiques, statues
- **musee** : Musées, centres d'exposition
- **site_naturel** : Parcs, réserves naturelles
- **batiment** : Bâtiments historiques, édifices religieux

---

## 🔧 Configuration technique

### Pagination
- **Taille par défaut** : 12 éléments par page
- **Maximum** : 100 éléments par page
- **Paramètre** : `page_size` pour surcharge

### Documentation API
- **Swagger UI** : `/docs/`
- **ReDoc** : `/redoc/`
- **JSON Schema** : `/swagger.json`

### Sécurité
- **JWT Tokens** : Access (15min) + Refresh (7 jours)
- **CORS** : django-cors-headers configuré
- **Permissions** : Basées sur les rôles hérités

---

## 📱 Interfaces web (Templates Django)

### Pages patrimoine
- **list.html** : Liste avec recherche et filtres
- **detail.html** : Fiche détaillée d'un patrimoine
- **create.html** : Formulaire de création
- **update.html** : Formulaire de modification
- **map.html** : Carte interactive des patrimoines
- **nearby.html** : Recherche par proximité
- **search.html** : Recherche avancée

### Composants partagés
- **navbar.html** : Navigation principale
- **footer.html** : Pied de page

---

## 🚀 Déploiement et performance

### Backend
- **Serveur de développement** : Django runserver
- **Production recommandée** : Gunicorn + Nginx
- **Base de données** : PostgreSQL

### Frontend
- **Build optimisé** : 157.22 kB
- **Serveur dev** : Angular CLI (port 4200/4201)
- **Production** : Build statique à déployer

---

## 🎯 Cas d'usage typiques

1. **Touriste** : Recherche des patrimoines à proximité
2. **Contributeur** : Ajout de nouveaux sites patrimoniaux
3. **Modérateur** : Validation et gestion du contenu
4. **Administrateur** : Gestion des utilisateurs et configuration

---

## 📈 Évolutions possibles

- **API mobile** : Application iOS/Android
- **Commentaires/notes** : Systeme d'évaluation
- **Visites virtuelles** : Intégration 360°
- **Multilingue** : Internationalisation i18n
- **Offline** : Service Workers pour mode hors-ligne
