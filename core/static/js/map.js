var map;
var initialViewSet = false; // Variável para controlar se a visualização inicial foi definida

function success(pos) {
    console.log(pos.coords.latitude, pos.coords.longitude);

    if (map === undefined) {
        map = L.map('mapid').setView([pos.coords.latitude, pos.coords.longitude], 13);
        initialViewSet = true;
    } else if (!initialViewSet) {
        map.setView([pos.coords.latitude, pos.coords.longitude], 13);
        initialViewSet = true;
    }

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([pos.coords.latitude, pos.coords.longitude]).addTo(map)
        .bindPopup('Você está aqui!');
    
    var ocorrenciasJsonString = document.getElementById('ocorrencias').textContent;
    var ocorrencias = JSON.parse(ocorrenciasJsonString);
    ocorrencias.forEach(function(ocorrencia) {
        var marker = L.marker([ocorrencia.fields.latitude, ocorrencia.fields.longitude]).addTo(map);
        var popupContent =
        '<b>Mergulhador:</b> ' + ocorrencia.fields.mergulhador + '<br>' +
        '<b>Profundidade:</b> ' + ocorrencia.fields.profundidade + 'm<br>' +
        '<b>Visibilidade:</b> ' + ocorrencia.fields.visibilidade + 'm<br>' +
        '<b>Temperatura da Água:</b> ' + ocorrencia.fields.temperatura_agua + '°C<br>' +
        '<b>Quantidade:</b> ' + ocorrencia.fields.quantidade + '<br>' +
        '<b>Data:</b> ' + ocorrencia.fields.data + '<br>' +
        '<b>Espécie:</b> ' + ocorrencia.fields.especie;

        marker.bindPopup(popupContent);

        marker.on('mouseover', function(e) {
            marker.openPopup();
        });

        marker.on('click', function(e) {
            window.location.href = '/ocorrencia/' + ocorrencia.pk + '/';
        });

        map.on('click', function(e) {
            document.getElementById('latitude').value = e.latlng.lat.toFixed(6);
            document.getElementById('longitude').value = e.latlng.lng.toFixed(6);
        });
    });
}

function error(err){
    console.log(err);
}

var watchID = navigator.geolocation.watchPosition(success, error, {
    enableHighAccuracy: false,
    timeout: 5000,
});
