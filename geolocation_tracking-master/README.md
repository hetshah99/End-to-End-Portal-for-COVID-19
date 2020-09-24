# Geolocation Tracking Demo

This project demonstrates how to build a simple geolocation tracking web application
with Beebotte.

* *public/track.html* uses **GeoLocation API** to watch the device Location
and publish it to Beebotte.
* *public/monitor.html* listens to published Geo location and shows it on a
Google Map.

## Install

1. Fork this github repository
2. run: `npm install`
3. replace **apiKey** and **secretKey** with those of your account in *app.js*,
*public/monitor.html*, and, *public/track.html*
4. run: `node app.js`
5. Open your favourite browser and navigate to *localhost:8080/track.html*
6. Open *localhost:8080/monitor.html* is a separate tab to show the location

## License
Copyright 2017 Beebotte.

[The MIT License](http://opensource.org/licenses/MIT)
