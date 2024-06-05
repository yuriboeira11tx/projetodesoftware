function formatDate(dateString) {
    var dateParts = dateString.split("-");
    return dateParts[2] + "/" + dateParts[1] + "/" + dateParts[0];
}

var map = L.map('mapid').setView([-14.2350, -51.9253], 3);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(map);

var ocorrenciasJsonString = document.getElementById('ocorrencias').textContent;
var ocorrencias = JSON.parse(ocorrenciasJsonString);

ocorrencias.forEach(function (ocorrencia) {
    var marker = L.marker([ocorrencia.fields.latitude, ocorrencia.fields.longitude]).addTo(map);
    var especie = ocorrencia.fields.especie == 'PL' ? 'Peixe Leão' : 'Coral Sol';
    var dataFormatada = formatDate(ocorrencia.fields.data);
    var popupContent =
        '<b>Data:</b> ' + dataFormatada  + '<br>' +
        '<b>Espécie:</b> ' + especie + '<br>' +
        '<b>Quantidade:</b> ' + ocorrencia.fields.quantidade;

    marker.bindPopup(popupContent);

    marker.on('mouseover', function (e) {
        marker.openPopup();
    });

    marker.on('click', function (e) {
        window.location.href = '/ocorrencia/' + ocorrencia.pk + '/';
    });
});

map.on('click', function (e) {
    document.getElementById('latitude').value = e.latlng.lat.toFixed(6);
    document.getElementById('longitude').value = e.latlng.lng.toFixed(6);
});
