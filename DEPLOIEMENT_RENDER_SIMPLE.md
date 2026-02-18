# 🚀 Guide de Déploiement GeoHeritage sur Render

## ✅ **Fichiers créés pour le déploiement**

Votre projet GeoHeritage est maintenant prêt pour Render avec les fichiers suivants :

### 📁 **Fichiers de configuration**
- `build.sh` - Script de build pour Render
- `Procfile` - Commande de démarrage pour Render
- `settings.py` - Configuré pour développement ET production

---

## 🎯 **Étapes suivantes à suivre**

### 1️⃣ **Pousser sur GitHub**
```bash
git add .
git commit -m "preparer pour deploy render"
git push origin main
```

### 2️⃣ **Créer compte Render**
- Allez sur [render.com](https://render.com)
- Connectez votre compte GitHub

### 3️⃣ **Créer la base PostgreSQL**
- Dashboard → **New + → PostgreSQL**
- Nom: `geoheritage-db`
- Laissez les options par défaut

### 4️⃣ **Créer le service Web Django**
- Dashboard → **New + → Web Service**
- Sélectionnez votre dépôt GitHub
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn config.wsgi:application`

### 5️⃣ **Variables d'environnement**
Dans les settings du service web :
- `DATABASE_URL`: Connectez votre base PostgreSQL
- `SECRET_KEY`: Générer une clé sécurisée
- `DEBUG`: `False`

---

## 🔧 **Configuration technique**

### **Database** - Auto-configuré
```python
# Production (Render)
DATABASES = {
    "default": dj_database_url.config(conn_max_age=600)
}
```

### **CORS** - Production ready
```python
# Production - autorise Vercel/Netlify
CORS_ALLOWED_ORIGINS = [
    "https://*.vercel.app",
    "https://*.netlify.app",
]
```

### **Static files** - WhiteNoise déjà configuré

---

## 🌐 **URLs finales après déploiement**

- **Backend**: `https://geoheritage-backend.onrender.com`
- **API Docs**: `https://geoheritage-backend.onrender.com/docs/`
- **Admin**: `https://geoheritage-backend.onrender.com/admin/`

---

## 📱 **Frontend (après le backend)**

Une fois le backend déployé, vous pourrez déployer votre frontend Angular sur :

- **Vercel** (recommandé pour Angular)
- **Netlify**

Le frontend se connectera à votre backend via l'URL Render.

---

## 🎉 **Prêt à déployer !**

Votre projet GeoHeritage est 100% prêt pour Render :

✅ Fichiers de configuration créés  
✅ Database configurée pour PostgreSQL  
✅ CORS configuré pour production  
✅ Build script prêt  
✅ Requirements.txt à jour  

**Suivez les étapes ci-dessus et votre GeoHeritage sera en ligne en quelques minutes !** 🚀
