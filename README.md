## Merciless Carbon Black Response/EDR Export Tool

This is a console-based tool to facilitate exporting date from the Carbon Black Response/EDR web application. CBAPI is leveraged to make this work. This is barely a project. Hopefully, more to come...

### Notable

#### Data Retrieval Speed
The speed of this tool is limited by a value set in the CBAPI. Find query.py under cbapi and modify the following setting:

*self._batch_size = 100

to something like:

*self._batch_size = 5000

This will retrieve more data per trip to the server, but may result in errors if the value is too large. Special thanks to RandomRhythm for this!

#### Requirements

The requirements.txt file is going to be a mess until the interface stabilizes.

### Also see
*https://github.com/RandomRhythm/Rhythm-CB-Scripts
*https://cbapi.readthedocs.io/en/latest/response-api.html
*https://developer.carbonblack.com/reference/enterprise-response/6.3/rest-api/
*https://github.com/carbonblack/cbapi-python

