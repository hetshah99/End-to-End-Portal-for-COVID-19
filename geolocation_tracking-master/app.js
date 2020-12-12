'use strict'

// Required modules.
const path = require('path')
const express = require('express')
const http = require('http')
const bbt = require('beebotte')

const app = express()

// Replace by your ACCESS and SECRET Keys
const bclient = new bbt.Connector({
  apiKey: 'paqOJMpVaEQOJRvcO171rLDo',
  secretKey: 'rA7Vch9KU5Oe3QH4xLx2T8jS7SZZHclm'
})

// configure Express
app.use(express.static(path.join(__dirname, 'public')))

app.get('/', function (req, res, next) {
  res.redirect('/track.html')
})

app.get( '/auth', function (req, res, next) {

  const channel = req.query.channel
  const resource = req.query.resource || '*'
  const ttl = req.query.ttl || 0
  const read = req.query.read === 'true'
  const write = req.query.write === 'true'
  const sid = req.query.sid

  if (!sid || !channel) {
    return res.status(403).send('Unauthorized')
  }

  const retval = bclient.sign(
    // string to sign
    `${sid}:${channel}.${resource}:ttl=${ttl}:read=${read}:write=${write}`
  )

  return res.send(retval)
})

const server = app.listen(8080, function () {

  const host = server.address().address
  const port = server.address().port

  console.log('presentit listening at http://%s:%s', host, port)
})
