# Known issues / unverified integrations
- Google Earth Engine requires user authentication and registered project; not verified in this environment.
- Live Open-Meteo connectivity is environment/network dependent and was not used as a software-test oracle.
- UNOSAT quantitative validation layer must be downloaded and its reuse terms checked; not bundled here.
- FAO GAUL boundary redistribution conditions should be reviewed before redistributing derived boundary assets; the app queries it through Earth Engine instead of shipping a copy.
- Leaflet/OpenStreetMap assets use public CDN/tiles; an offline basemap is not bundled.
