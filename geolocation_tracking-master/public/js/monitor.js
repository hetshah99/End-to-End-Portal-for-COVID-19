function init () {

  var map = null
  var marker = null

  var bbt = new BBT('YOUR_API_KEY', {
    auth_endpoint: '/auth'
  })

  bbt.subscribe({
    channel: 'private-mychannel',
    resource: 'location',
    read: true,
    write: false
  }, function(msg) {
    console.log('received position: ', msg.data.latitude, msg.data.longitude)
    displayCarLocation(msg.data.latitude, msg.data.longitude)
  })

  function initializeMap (position) {
    var options = {
      zoom: 17,
      center: position,
      mapTypeId: google.maps.MapTypeId.PLAN
    }

    map = new google.maps.Map(document.getElementById('map'), options)
  }

  function displayCarLocation(lat, lng) {

    if (!map) {
      initializeMap(new google.maps.LatLng(lat, lng))
    }

    // if marker exists remove it
    if (marker) {
      marker.setMap(null)
    }
    // set the marker to the new position
    marker = new google.maps.Marker({
      position: new google.maps.LatLng(lat, lng),
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 8,
        strokeColor: '#FF0000'
      },
      draggable: false,
      map: map
    })
  }
}
