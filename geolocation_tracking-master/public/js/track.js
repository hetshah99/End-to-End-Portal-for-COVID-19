var opts = {
  enableHighAccuracy: true,
  timeout: 2000,
  maximumAge: 0
}

function init () {

  var tracker = null

  var bbt = new BBT('YOUR_API_KEY', {
    auth_endpoint: '/auth'
  })

  bbt.subscribe({
    channel: 'private-mychannel', // replace this by your channel
    resource: 'location', // replace this by your channel GPS resource
    read: false, // No need to subscribe to data we are publishing
    write: true // We need to publish data
  }, function(message) {})

  function success (position) {

    var latitude = position.coords.latitude
    var longitude = position.coords.longitude

    console.log('publishing position: ', latitude, longitude)
    bbt.publish({
      channel: 'private-mychannel',
      resource: 'location'
    }, {
      'latitude': latitude,
      'longitude': longitude
    })
  }

  function error (error) {
    var errors = {
      1: 'Permission denied',
      2: 'Position unavailable',
      3: 'Request timeout'
    }

    alert('Error: ' + errors[error.code])
  }

  function startTracking () {

    if (navigator.geolocation) {
      tracker = navigator.geolocation.watchPosition(
        success,
        error,
        opts
      )
    } else {
      alert('Geolocation is not supported by this browser')
    }
  }

  function stopTracking () {
    if (tracker != null) {
      navigator.geolocation.clearWatch(tracker)
      tracker = null
    }
  }

  return {
    startTracking: startTracking,
    stopTracking: stopTracking
  }
}
