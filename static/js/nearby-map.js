// Initialiser la carte
function initNearbyMap(centerLat, centerLng, zoom, patrimoines) {
    var map = L.map('nearby-map').setView([centerLat, centerLng], zoom);

    // Ajouter la couche de tuiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Ajouter les marqueurs
    var markers = [];
    patrimoines.forEach(function(patrimoine) {
        var marker = L.marker([patrimoine.lat, patrimoine.lng]).addTo(map);
        
        var popupContent = '<div style="min-width: 200px;">' +
            '<h6>' + patrimoine.nom + '</h6>' +
            '<p class="small mb-1">' + patrimoine.ville + '</p>' +
            '<p class="small mb-1">' + patrimoine.type + '</p>';
        
        if (patrimoine.distance > 0) {
            popupContent += '<p class="small text-primary"><strong>Distance: ' + patrimoine.distance + ' km</strong></p>';
        }
        
        popupContent += '<a href="' + patrimoine.url + '" class="btn btn-primary btn-sm">Voir détails</a>' +
            '</div>';
        
        marker.bindPopup(popupContent);
        markers.push(marker);
    });

    // Ajuster la vue si des résultats sont trouvés
    if (markers.length > 0) {
        var group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

// Fonction pour rechercher avec les coordonnées du formulaire
function searchNearby() {
    var lat = document.getElementById('latitude').value;
    var lng = document.getElementById('longitude').value;
    var radius = document.getElementById('radius').value;
    
    if (!lat || !lng) {
        alert('Veuillez entrer des coordonnées GPS');
        return;
    }
    
    // Rediriger vers la même page avec les paramètres
    window.location.href = '/heritage/nearby/?lat=' + lat + '&lng=' + lng + '&radius=' + radius;
}

// Fonction de géolocalisation
function geolocateMe() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            document.getElementById('latitude').value = position.coords.latitude.toFixed(6);
            document.getElementById('longitude').value = position.coords.longitude.toFixed(6);
        }, function(error) {
            alert('Impossible d\'obtenir votre position: ' + error.message);
        });
    } else {
        alert('La géolocalisation n\'est pas supportée par votre navigateur');
    }
}
