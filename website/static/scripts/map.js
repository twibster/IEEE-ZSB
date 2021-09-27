const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let labelIndex = 0;

function initMap() {
  try {
    var lati =Number(geoplugin_latitude())
    var lngi =Number(geoplugin_longitude())
  } catch (e) {
      if (e instanceof ReferenceError) {
          var lati = 30.5765
          var lngi = 31.5041
      }
  }
  const where_am_i = { lat:lati, lng:lngi };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10,
    center: where_am_i,
  });

  // This event listener calls addMarker() when the map is clicked.
  google.maps.event.addListener(map, "click", (event) => {
    document.getElementById("lat").value = event.latLng.lat();
    document.getElementById("long").value = event.latLng.lng();
    addMarker(event.latLng, map);
  });
}

// Adds a marker to the map.
function addMarker(location, map) {
  var marker =new google.maps.Marker({
    draggable: true,
    position: location,
    label: labels[labelIndex++ % labels.length],
    map: map,
  });

// this event listener changes the coordinates according to the poisition of the dragged marker.
google.maps.event.addListener(marker, 'dragend', function (event) {
    document.getElementById("lat").value = event.latLng.lat();
    document.getElementById("long").value = event.latLng.lng();
  });
}