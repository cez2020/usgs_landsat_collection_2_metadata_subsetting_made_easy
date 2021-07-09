# Generate a LIST of USGS Collection 2 Image IDs for ingestion by USGS/EROS Machine-to-Machine API for BULK download.
Python tool in the form of a function() that allows a user to subset USGS Collection 2 metadata CSV file by entering several parameters:
* Path
* Row
* Tier (1 or 2)
* Cloud Cover (<= than %)
* Timeframe (from/to)
* Previous Image ID list (if available--to avoid repeated image downloads)
* Mission (Landsat 4-5,7,8 Level-1 or Level-2)

## Requires
* User credentials to login to USGS EarthExplorer (free).
* Approved access to USGS machine-to-machine API (request for free [here](https://ers.cr.usgs.gov/profile/access)).
* A USGS metadata CSV file (may be obtained [here](https://www.usgs.gov/core-science-systems/nli/landsat/bulk-metadata-service)).
![screenshot1](/screenshots/1.jpg)
* Alternatively, a smaller metada CSV file may be obtained in Earth Explorer (no API required):
![screenshot2](/screenshots/2.jpg)
* Row and Path information may be obtained in the attached kml file or in this [link](https://www.usgs.gov/media/files/landsat-wrs-2-scene-boundaries-kml-file).
Examples:
Catalunya, Spain:
usgsPaths = [197, 198, 199]
usgsRows = [30, 31, 32]
![screenshot3](/screenshots/3.jpg)

Big Island, Hawaii:
usgsPaths = [62, 63]
usgsRows = [46, 47]
![screenshot4](/screenshots/4.jpg)

Uruguay:
usgsPaths = [222, 223, 224, 225]
usgsRows = [81, 82, 83, 84]
![screenshot5](/screenshots/5.jpg)

