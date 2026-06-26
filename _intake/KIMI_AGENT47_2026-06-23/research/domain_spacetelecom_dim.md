# Space, Telecom, Marine & Advanced Technology — Free/Open Data Sources

> **CSOAI Research Document** — Comprehensive catalog of free and open data sources for satellite imagery, space tracking, spectrum/frequency management, maritime AIS vessel tracking, oceanographic data, submarine cable maps, space debris, GNSS performance data, and telecom infrastructure.
> 
> **Last Updated**: 2026-06-28 | **Sources**: 30+ free/open data portals and APIs

---

## Table of Contents

1. [Satellite Imagery & Earth Observation](#1-satellite-imagery--earth-observation)
2. [Space Tracking & Orbital Data](#2-space-tracking--orbital-data)
3. [Space Debris & Safety](#3-space-debris--safety)
4. [Spectrum, Frequency & Telecom Data](#4-spectrum-frequency--telecom-data)
5. [Maritime Tracking (AIS) & Vessel Data](#5-maritime-tracking-ais--vessel-data)
6. [Oceanographic & Marine Data](#6-oceanographic--marine-data)
7. [Submarine Cable & Infrastructure Maps](#7-submarine-cable--infrastructure-maps)
8. [GNSS/GPS Performance Data](#8-gnssgps-performance-data)
9. [Additional Related Data Sources](#9-additional-related-data-sources)

---

## 1. Satellite Imagery & Earth Observation

### 1.1 Copernicus Data Space Ecosystem (ESA Sentinel)

| Field | Details |
|-------|---------|
| **Name** | Copernicus Data Space Ecosystem |
| **URL** | https://dataspace.copernicus.eu/ |
| **Data** | Sentinel-1 (SAR/radar), Sentinel-2 (10m multispectral optical), Sentinel-3 (ocean/land), Sentinel-5P (atmospheric), Sentinel-6 (sea level) |
| **Format** | GeoTIFF, NetCDF, SAFE, Zarr, Cloud-Optimized GeoTIFF (COG) |
| **License** | Copernicus Open Data Policy — free for all use, no restrictions on commercial or non-commercial use |
| **API Access** | OData API, OpenSearch, S3-compatible access; Python `sentinelsat` library; STAC API |
| **Coverage** | Global; Sentinel-2: 5-day revisit at equator, 290km swath |
| **CSOAI Use Case** | Land cover change detection, agricultural monitoring, maritime surveillance (oil spill, vessel detection with SAR), coastal zone monitoring |

- **Key Documentation**: https://documentation.dataspace.copernicus.eu/
- **API Docs**: https://documentation.dataspace.copernicus.eu/APIs.html
- **Also Available Via**: Google Earth Engine, AWS Open Data, Microsoft Planetary Computer
- **Notes**: Replaced the legacy Copernicus Open Access Hub in January 2023. Browser interface for visualization; programmatic access via multiple APIs. [^1069^] [^1690^]

---

### 1.2 NASA Earthdata (MODIS, VIIRS, GRACE, etc.)

| Field | Details |
|-------|---------|
| **Name** | NASA Earthdata |
| **URL** | https://www.earthdata.nasa.gov/ |
| **Data** | MODIS, VIIRS, GRACE, SMAP, ICESat, ASTER, AIRS, OCO-2, and 900+ satellite imagery products |
| **Format** | HDF, NetCDF-4, GeoTIFF, KMZ, Cloud-Optimized GeoTIFF |
| **License** | Open and freely available without restriction |
| **API Access** | Earthdata Login (free) required for protected datasets; CMR Search API; GIBS API for imagery; Harmony API for subsetting; direct S3 access on AWS |
| **Coverage** | Global, various temporal resolutions (daily to sub-hourly) |
| **CSOAI Use Case** | Climate monitoring, fire detection (FIRMS), ocean color, atmospheric composition, land surface temperature |

- **Developer Portal**: https://www.earthdata.nasa.gov/engage/open-data-services-software/earthdata-developer-portal
- **GIBS (Global Imagery Browse Services)**: https://gibs.earthdata.nasa.gov/ — Quick access to 900+ imagery products, daily updates, some spanning 30 years
- **CMR API**: Search and discovery across NASA's entire Earth science data catalog
- **Notes**: Free Earthdata Login account required for downloading protected datasets. All APIs are free to use. [^1687^] [^1692^] [^1683^]

---

### 1.3 USGS Landsat Archive

| Field | Details |
|-------|---------|
| **Name** | USGS Landsat Missions Archive |
| **URL** | https://earthexplorer.usgs.gov/ |
| **Data** | Landsat 1-9 (entire archive since 1972): Level-1, Level-2 Surface Reflectance, Surface Temperature, US ARD, Level-3 science products |
| **Format** | Cloud-Optimized GeoTIFF (COG), GeoTIFF, HDF, STAC metadata |
| **License** | No restrictions; can be used or redistributed as desired |
| **API Access** | EarthExplorer web interface; Machine-to-Machine (M2M) API; Bulk Download Web Application (BDWA); ESPA on-demand processing; STAC API on AWS |
| **Coverage** | Global; 16-day revisit; 30m resolution (Landsat 8/9 includes 15m panchromatic) |
| **CSOAI Use Case** | Long-term land change detection, agriculture, water quality monitoring, urban expansion tracking |

- **Alternative Access**: AWS S3 `s3://usgs-landsat/` (requester-pays), Google Earth Engine
- **LandsatLook Viewer**: https://landsatlook.usgs.gov/ — STAC-enabled viewer
- **STAC API**: https://landsatlook.usgs.gov/stac-server/api.html
- **Notes**: Over 160 million downloads since going free in 2008. The longest continuous space-based record of Earth's land surface. [^1792^] [^1801^] [^1802^] [^1804^]

---

### 1.4 ESA Earth Online

| Field | Details |
|-------|---------|
| **Name** | ESA Earth Online |
| **URL** | https://earth.esa.int/eogateway/ |
| **Data** | ESA mission data: Aeolus, Biomass, CryoSat, SMOS, Swarm, EarthCARE, Third Party Missions, Heritage missions |
| **Format** | NetCDF, HDF, GeoTIFF (varies by mission) |
| **License** | Free of charge; most datasets freely available after registration |
| **API Access** | EO Sign-In SSO (free); FedEO catalogue; MAAP Explorer; direct download portals |
| **Coverage** | Global (varies by mission) |
| **CSOAI Use Case** | Wind profiling (Aeolus), soil moisture (SMOS), ice sheet monitoring (CryoSat), magnetic field (Swarm) |

- **Data Catalog**: https://earth.esa.int/eogateway/catalog
- **CCI Open Data Portal**: https://climate.esa.int/en/odp — 100+ high-quality satellite-derived climate datasets
- **Notes**: Single sign-on account (EO Sign-In) grants access to most tools. Some datasets require "Fast Registration" or data access request approval. [^1682^] [^1693^]

---

### 1.5 Google Earth Engine (GEE)

| Field | Details |
|-------|---------|
| **Name** | Google Earth Engine |
| **URL** | https://earthengine.google.com/ |
| **Data** | Landsat, Sentinel-1/2, MODIS, VIIRS, NAIP, weather data, climate projections — 900+ petabytes of satellite and geospatial data |
| **Format** | Cloud-native (no downloads needed); export to GeoTIFF, TFRecord, CSV, KML |
| **License** | Free for non-commercial use; commercial use requires paid license |
| **API Access** | Python API and JavaScript API; REST API (Earth Engine Cloud API) |
| **Coverage** | Global; multi-decade archives |
| **CSOAI Use Case** | Large-scale satellite analysis, change detection, land cover classification, time-series analysis |

- **Code Editor**: https://code.earthengine.google.com/
- **Data Catalog**: https://developers.google.com/earth-engine/datasets/
- **Notes**: Not strictly "open" for commercial use, but transformative for non-commercial research. Integrates with multiple open datasets including Copernicus and Landsat. [^1827^]

---

## 2. Space Tracking & Orbital Data

### 2.1 Space-Track.org (NORAD TLE Data)

| Field | Details |
|-------|---------|
| **Name** | Space-Track.org |
| **URL** | https://www.space-track.org/ |
| **Data** | NORAD Satellite Catalog (SATCAT); Two-Line Element sets (TLE); Orbital Mean-element Messages (OMM); satellite decay/reentry predictions; 16,000+ tracked objects |
| **Format** | TLE, OMM (XML/JSON/KVN), SATCAT (CSV/JSON), GP data |
| **License** | Free for registered users; express blanket approval for redistribution of basic SSA data with citation |
| **API Access** | REST API with customized queries; authenticated access; free registration required |
| **Coverage** | All tracked objects in Earth orbit |
| **CSOAI Use Case** | Satellite position prediction, conjunction assessment, space situational awareness, orbit visualization |

- **API Documentation**: https://www.space-track.org/documentation
- **Provided By**: USSPACECOM / 18th Space Defense Squadron (18 SDS)
- **Redistribution**: Basic SSA data (TLEs, OMMs, SATCAT, Decay data) can be redistributed with appropriate citation
- **Notes**: The definitive source for satellite orbital data. Three service levels: basic (free), emergency (for operators), advanced. [^1695^]

---

### 2.2 CelesTrak

| Field | Details |
|-------|---------|
| **Name** | CelesTrak |
| **URL** | https://celestrak.org/ |
| **Data** | TLE sets for all satellites; supplemental GP data for Starlink, OneWeb, Iridium, Planet, and other constellations; SOCRATES conjunction assessment |
| **Format** | TLE, OMM (XML/JSON/KVN/CSV), GP data |
| **License** | Free to use; non-profit 501(c)(3) educational resource |
| **API Access** | HTTP query-based API (RESTful); downloadable files; GP Query and Sup GP Query endpoints |
| **Coverage** | All cataloged objects; constellation-specific supplemental data |
| **CSOAI Use Case** | Precise orbit prediction for major constellations; conjunction data messages (CDM); space situational awareness |

- **API Integration Docs**: https://docs.zendir.io/v1.4/Editor/Guides/External/CelesTrak-API-Integration
- **GitHub Orbital Data (auto-updated)**: https://github.com/tannerkoza/celestrak-orbital-data
- **Data Formats**: TLE, 2LE, 3LE, XML (OMM), KVN, JSON, JSON-PRETTY, CSV
- **Notes**: Founded by Dr. T.S. Kelso. Provides higher-fidelity orbital data from operator-sourced feeds not always available through standard catalogs. URGENT: 5-digit catalog numbers running out ~July 2026. [^1841^] [^1840^] [^1839^]

---

### 2.3 N2YO Satellite Tracking API

| Field | Details |
|-------|---------|
| **Name** | N2YO Satellite Tracking API |
| **URL** | https://www.n2yo.com/ |
| **Data** | Real-time satellite positions (lat/lon/alt), TLE data, visual pass predictions, radio passes, above-horizon queries |
| **Format** | JSON REST API |
| **License** | Free API key with daily limits |
| **API Access** | REST API v1; free API key registration |
| **Daily Limits** | TLE: 1,000/day; Position: 1,000/day; Visual passes: 100/day; Radio passes: 100/day; Above: 100/day |
| **CSOAI Use Case** | Real-time satellite tracking apps, pass predictions, visibility calculations |

- **API Documentation**: https://www.n2yo.com/api/
- **Website**: https://www.n2yo.com/ — Real-time satellite tracking with 3D visualization
- **Notes**: Well-documented REST API. Categories include ISS, weather, amateur radio, GPS, Starlink, etc. [^1829^] [^1832^]

---

### 2.4 Starlink / SpaceX Satellite Positions

| Field | Details |
|-------|---------|
| **Name** | Starlink Satellite Tracker (Aviation Edge) |
| **URL** | https://aviation-edge.com/spacex-satellite-tracker-api/ |
| **Data** | Real-time position data for Starlink satellites; NORAD code, ECI coordinates, altitude, latitude, longitude, TLE |
| **Format** | JSON REST API |
| **License** | Paid API with free trial options |
| **API Access** | REST API with filters (code, launchYear, orbitalapogee, orbitalperigee) |
| **Coverage** | All Starlink satellites |
| **CSOAI Use Case** | Starlink constellation tracking, coverage analysis, satellite internet research |

- **Open Source Alternative**: https://github.com/ChrisMichaelPerezSantiago/starlinkapi (community project)
- **Live Map**: https://satellitemap.space/ — Live map of Starlink and 30,000+ satellites using JPL Horizons, CelesTrak data
- **Note**: SpaceX ended user access to dish GPS location data via gRPC API in May 2026. TLE data available via standard sources. [^1689^] [^1688^] [^1678^]

---

### 2.5 Jonathan McDowell's Space Report

| Field | Details |
|-------|---------|
| **Name** | Jonathan's Space Report / GCAT |
| **URL** | https://planet4589.org/space/ |
| **Data** | General Catalog of Artificial Space Objects (GCAT); master orbital launch log; geostationary satellite log; reentry catalog; satellite debris events; space traveler records |
| **Format** | Text, spreadsheet, downloadable files |
| **License** | Free and open; widely cited and respected |
| **API Access** | Static data files; no formal API but data is downloadable |
| **Coverage** | Complete history of all space launches and objects since Sputnik |
| **CSOAI Use Case** | Historical spaceflight analysis, satellite population studies, launch statistics, orbital archaeology |

- **Data Sources**: Used by satellite trackers, UCS database, academic researchers
- **Notes**: Compiled by astrophysicist Dr. Jonathan McDowell since 1989. One of the most reliable independent sources for spaceflight history. [^1834^] [^1843^]

---

## 3. Space Debris & Safety

### 3.1 ESA Space Debris Office — DISCOSweb

| Field | Details |
|-------|---------|
| **Name** | DISCOSweb (Database and Information System Characterising Objects in Space) |
| **URL** | https://discosweb.esoc.esa.int/ |
| **Data** | 40,000+ tracked objects; launch information, object registration, launch vehicle descriptions, spacecraft information (size, mass, shape), orbital data histories |
| **Format** | JSON REST API; interactive web interface |
| **License** | Free of charge for general public |
| **API Access** | Full REST API with elaborate filter/search options; documented at discosweb.esoc.esa.int/apidocs |
| **Operations API**: discosweb-api.sdo.esoc.esa.int (for collision avoidance; requires account) |
| **CSOAI Use Case** | Space debris population analysis, collision risk assessment, reentry predictions, launch traffic studies |

- **Space Debris User Portal**: https://sdup.esoc.esa.int/ — Download MASTER and DRAMA software
- **ESTIMATE**: https://estimate.sdo.esoc.esa.int/ — Material demisability database
- **Notes**: The most comprehensive public space debris database. API enables programmatic access to object data, fragmentation data, and launch histories. [^1798^] [^1799^] [^1804^]

---

### 3.2 NASA Orbital Debris Program Office (ODPO)

| Field | Details |
|-------|---------|
| **Name** | NASA Orbital Debris Program Office |
| **URL** | https://www.nasa.gov/orbital-debris/ |
| **Data** | Orbital debris environment models, breakup models, debris assessment software (ORDEM, LEGEND), measurement data, quarterly newsletters |
| **Format** | Reports, software, data files |
| **License** | Publicly available; free |
| **API Access** | No formal API; software downloads and data files |
| **CSOAI Use Case** | Debris environment modeling, NASA debris assessment reports, policy analysis |

- **Quarterly News**: NASA Orbital Debris Quarterly Newsletter
- **Key Models**: ORDEM (Orbital Debris Engineering Model), LEGEND
- **Notes**: NASA's center of expertise for studying and characterizing the orbital debris environment. [^1803^]

---

### 3.3 UCS Satellite Database

| Field | Details |
|-------|---------|
| **Name** | Union of Concerned Scientists Satellite Database |
| **URL** | https://www.ucsusa.org/resources/satellite-database |
| **Data** | 7,560+ active satellites; 28 data fields per satellite including mass, power, launch date, expected lifetime, orbit (apogee, perigee, inclination, period), purpose, owner, operator, contractor |
| **Format** | Excel (.xlsx), tab-delimited text |
| **License** | Free; unrestricted use; request citation and acknowledgment |
| **API Access** | Direct download; also on Kaggle and Hugging Face datasets |
| **CSOAI Use Case** | Satellite population analysis, country comparisons, purpose categorization, orbital distribution studies |

- **Kaggle**: https://www.kaggle.com/datasets/luisemiliani/ucs-sat-db
- **Hugging Face**: https://huggingface.co/datasets/juliensimon/ucs-satellite-database
- **Update Frequency**: Quarterly (updates paused as of 2023; evaluating resumption)
- **Notes**: The go-to reference for active satellite statistics by country and purpose. [^1873^] [^1871^] [^1868^]

---

## 4. Spectrum, Frequency & Telecom Data

### 4.1 ITU Radio Regulations & Frequency Allocations

| Field | Details |
|-------|---------|
| **Name** | ITU Radio Regulations (RR) — Article 5 Table of Frequency Allocations |
| **URL** | https://www.itu.int/pub/R-REG-RR |
| **Data** | International Table of Frequency Allocations; footnotes; service definitions; regional variations |
| **Format** | PDF (volumes); RR5 TFA software (Windows); BR IFIC (circulars) |
| **License** | Free download in 6 UN languages (Arabic, Chinese, English, French, Russian, Spanish) |
| **API Access** | No formal public API; RR5 TFA software allows export to various formats; BR IFIC published every 2 weeks |
| **CSOAI Use Case** | Spectrum allocation reference, frequency planning, interference analysis, regulatory compliance |

- **BR IFIC (Terrestrial)**: http://www.itu.int/en/ITU-R/terrestrial/brific/
- **BR IFIC (Space)**: http://www.itu.int/en/ITU-R/space/Pages/brificMain.aspx
- **RR5 TFA Software**: https://www.itu.int/pub/R-REG-RR5 — Desktop software for analyzing Article 5 table
- **Notes**: The ITU Radio Regulations is an international treaty. The full regulations can be downloaded free of charge. API is under development for future releases. [^1833^] [^1836^] [^1838^]

---

### 4.2 OpenCellID — Cell Tower Database

| Field | Details |
|-------|---------|
| **Name** | OpenCellID |
| **URL** | https://opencellid.org/ |
| **Data** | World's largest open database of cell towers: GSM, UMTS, LTE, CDMA, NR (5G); ~40 million cell locations globally |
| **Format** | XML, JSON, CSV, KML; bulk database download |
| **License** | CC-BY-SA; free for data contributors; commercial use requires whitelisting |
| **API Access** | REST API (cell lookup, area search); API key required; 1,000 requests/day limit for free tier |
| **CSOAI Use Case** | Mobile network coverage mapping, cell tower geolocation, telecom infrastructure analysis |

- **API Documentation**: https://wiki.opencellid.org/wiki/API
- **Bulk Downloads**: https://opencellid.org/downloads/
- **Parameters**: mcc (mobile country code), mnc (network code), lac (area code), cellid, radio type
- **Notes**: Free API access requires contributing data to the project. Bulk download available for full database. [^1797^]

---

### 4.3 Mozilla Location Services (MLS)

| Field | Details |
|-------|---------|
| **Name** | Mozilla Location Services |
| **URL** | https://location.services.mozilla.com/ |
| **Data** | Crowdsourced cell tower (GSM, UMTS, LTE) and WiFi access point locations |
| **Format** | JSON API; bulk data download in CSV |
| **License** | Open Database License (ODbL) 1.0 |
| **API Access** | Geolocation API (reverse: cell/WiFi -> location); bulk download for full dataset |
| **CSOAI Use Case** | Positioning services, coverage analysis, telecom infrastructure mapping |

- **API Docs**: https://ichnaea.readthedocs.io/en/latest/api/index.html
- **Download**: https://location.services.mozilla.com/downloads
- **Notes**: Community-driven alternative to proprietary geolocation services. Data contributed by Firefox and other applications.

---

### 4.4 OpenSignal Coverage Maps & Reports

| Field | Details |
|-------|---------|
| **Name** | OpenSignal |
| **URL** | https://www.opensignal.com/ |
| **Data** | Independent mobile coverage maps based on crowdsourced app data; coverage, speed, latency measurements for 100+ countries |
| **Format** | Coverage maps via app; reports and data insights |
| **License** | Free maps via app; reports published openly |
| **API Access** | No public API for raw data; reports and analytics available |
| **CSOAI Use Case** | Mobile network quality comparison, coverage gap analysis, telecom market insights |

- **Coverage Maps**: https://insights.opensignal.com/coverage-maps
- **Reports**: https://insights.opensignal.com/
- **Notes**: Largest independent source of crowdsourced mobile network experience data. No bulk data API but regular reports are published freely. [^1749^]

---

### 4.5 National Frequency Allocation Tables (By Country)

Many national regulators publish their frequency allocation tables openly:

| Country | URL | Format |
|---------|-----|--------|
| **USA (NTIA/FCC)** | https://www.ntia.doc.gov/page/2011/united-states-frequency-allocation-chart | PDF, interactive chart |
| **UK (Ofcom)** | https://www.ofcom.org.uk/spectrum/information/ | Interactive, PDF |
| **EU (CEPT/EFIS)** | https://efis.cept.org/ | Interactive web |
| **Hong Kong** | https://www.ofca.gov.hk/en/freq_table.html | PDF |
| **Japan** | https://www.tele.soumu.go.jp/e/adm/freq/search/ | Interactive |

---

## 5. Maritime Tracking (AIS) & Vessel Data

### 5.1 AISstream.io — Free Real-Time AIS API

| Field | Details |
|-------|---------|
| **Name** | AISstream.io |
| **URL** | https://aisstream.io/ |
| **Data** | Real-time global AIS vessel tracking via WebSocket; position, identity, port calls, message types |
| **Format** | WebSocket streaming; JSON |
| **License** | Free tier (no credit card required); generous free tier for real-time streaming |
| **API Access** | WebSocket API; subscribe to bounding boxes (global or regional); MMSI filtering; message type filtering |
| **Coverage** | Global (terrestrial AIS + satellite AIS) |
| **CSOAI Use Case** | Real-time vessel tracking, maritime domain awareness, port traffic monitoring, fishing vessel tracking |

- **GitHub**: https://github.com/aisstream/aisstream
- **Documentation**: OpenAPI 3.0 definition available
- **Notes**: The best free option for real-time AIS streaming. JavaScript/Node.js examples. Community-driven project. [^1744^] [^1741^]

---

### 5.2 AISHub — Community AIS Data Exchange

| Field | Details |
|-------|---------|
| **Name** | AISHub |
| **URL** | https://www.aishub.net/ |
| **Data** | Aggregated global AIS feed from community contributors; real-time vessel positions |
| **Format** | JSON, XML, CSV |
| **License** | Free if you contribute your own AIS receiver data |
| **API Access** | Data-sharing model: share your AIS data to receive global aggregated feed access |
| **Coverage** | Global (coverage depends on contributor network) |
| **CSOAI Use Case** | AIS data access for research projects, vessel tracking applications, port monitoring |

- **How to Join**: Fill form, receive host/IP and UDP port, configure AIS receiver to stream data
- **AIS Dispatcher**: Free tool for receiving/processing/forwarding AIS data (Windows/Linux)
- **Notes**: The original free AIS data exchange model. Ideal for researchers who can contribute shore-based AIS reception. [^1750^]

---

### 5.3 MarineTraffic / Kpler AIS

| Field | Details |
|-------|---------|
| **Name** | Kpler AIS (formerly MarineTraffic) |
| **URL** | https://www.marinetraffic.com/ |
| **Data** | World's largest maritime data platform; 300,000+ vessels daily; 13,000+ AIS receivers |
| **Format** | Web interface, GraphQL API (Kpler Developer API), REST API |
| **License** | Freemium; enterprise pricing for full API |
| **API Access** | Web interface (free); API requires subscription; some data via free tier |
| **Coverage** | Terrestrial + satellite AIS; global port coverage |
| **CSOAI Use Case** | Vessel tracking, port calls, voyage forecasts, commodity flow analytics |

- **API**: Kpler Developer API (GraphQL) — vessel positions, voyage data, commodity flows
- **Note**: Kpler acquired MarineTraffic, FleetMon, and Spire Maritime in 2025. The MarineTraffic API remains widely integrated. [^1741^]

---

### 5.4 VesselFinder API

| Field | Details |
|-------|---------|
| **Name** | VesselFinder API |
| **URL** | https://api.vesselfinder.com/ |
| **Data** | Real-time vessel positions, voyage data, port calls, vessel master data (type, flag, owner, capacity) |
| **Format** | JSON, XML |
| **License** | Credit-based pricing; trial credits for new accounts |
| **API Access** | Credit-based API: 1 credit per terrestrial AIS position, 10 credits per satellite AIS position |
| **Subscription APIs**: VesselsList, LiveData (flat fee) |
| **CSOAI Use Case** | Vessel tracking, maritime logistics, port operations, fleet management |

- **API Docs**: https://api.vesselfinder.com/
- **Notes**: Pay-as-you-go model with credit system. Good documentation and broad vessel coverage. Free trial credits available. [^1751^]

---

### 5.5 Datalastic Vessel API

| Field | Details |
|-------|---------|
| **Name** | Datalastic |
| **URL** | https://datalastic.com/ |
| **Data** | Real-time vessel positions, historical AIS data, port info, vessel specs, ownership, inspections, casualties |
| **Format** | JSON REST API |
| **License** | 14-day free trial; plans from EUR 99/month |
| **API Access** | Self-serve API key provisioning; Python, Ruby, PHP, Java, Go, .NET support |
| **Key Endpoints**: /vessel, /vessel_pro, /vessel_bulk, /vessel_inradius, /vessel_history, /port_find |
| **CSOAI Use Case** | Developer-friendly vessel tracking, maritime intelligence, fleet analytics |

- **Notes**: Best self-serve option for developers. 99.8% uptime. No credit card needed for trial. Overuse protection (failed calls don't consume credits). [^1743^] [^1741^]

---

## 6. Oceanographic & Marine Data

### 6.1 NOAA ERDDAP — Ocean Data Access

| Field | Details |
|-------|---------|
| **Name** | NOAA ERDDAP (Environmental Research Division's Data Access Program) |
| **URL** | https://coastwatch.pfeg.noaa.gov/erddap/ |
| **Data** | Sea surface temperature, ocean currents, salinity, chlorophyll, wind, waves, animal telemetry, buoy data, model outputs; 400+ datasets at ERD alone |
| **Format** | NetCDF, CSV, JSON, GeoTIFF, KML, OPeNDAP, and 40+ other formats |
| **License** | Free and open source software (Apache-like); data is freely available |
| **API Access** | RESTful API (URL-based requests); griddap for gridded data; tabledap for tabular data; WMS/WCS compatible |
| **Coverage** | Global ocean; in-situ and satellite data |
| **CSOAI Use Case** | Oceanographic research, marine ecosystem monitoring, climate studies, fisheries management |

- **Main ERDDAP Portal**: https://www.ncei.noaa.gov/erddap/
- **CoastWatch ERDDAP**: https://coastwatch.pfeg.noaa.gov/erddap/
- **PMEL ERDDAP**: https://data.pmel.noaa.gov/pmel/erddap
- **Global Drifter Program ERDDAP**: https://erddap.aoml.noaa.gov/
- **Key Datasets**: OSCAR ocean currents, RTOFS forecast, World Ocean Atlas, CCMP wind atlas, HYCOM model, Argo floats, NDBC buoys, glider data
- **Notes**: ERDDAP is free and open-source software used by 100+ organizations in 17+ countries. Provides consistent access regardless of underlying data source. RESTful API enables direct programmatic access from Python, R, Matlab, JavaScript, etc. [^1831^] [^1842^] [^1797^] [^1830^]

---

### 6.2 Copernicus Marine Service

| Field | Details |
|-------|---------|
| **Name** | Copernicus Marine Service (CMEMS) |
| **URL** | https://data.marine.copernicus.eu/ |
| **Data** | Physical ocean (Blue Ocean), sea ice (White Ocean), biogeochemistry (Green Ocean): temperature, salinity, currents, sea level, waves, sea ice, ocean color, nutrients, plankton |
| **Format** | NetCDF, Zarr, GeoTIFF, CSV, ARCO |
| **License** | Free, open-access after registration; EUPL for toolbox |
| **API Access** | Copernicus Marine Toolbox (Python CLI & API); WMTS endpoint; CSW endpoint; HTTP subsetting; no quotas |
| **Coverage** | Global and regional seas; real-time, forecast, reanalysis, and climatology products |
| **CSOAI Use Case** | Ocean state monitoring, marine safety, fishery support, pollution tracking, climate change assessment |

- **Toolbox Install**: `pip install copernicusmarine` or `mamba install conda-forge::copernicusmarine`
- **R Package**: `CopernicusMarine` on CRAN
- **Products**: 100+ products across ocean physics, waves, sea ice, biogeochemistry, land monitoring
- **Notes**: Free registration required. The Marine Toolbox provides high-performance data access without download quotas. Supports subsetting by region, time, depth, and variables. [^1867^] [^1870^] [^1872^] [^1874^] [^1878^]

---

### 6.3 Argo Float Data

| Field | Details |
|-------|---------|
| **Name** | Argo (Global array of profiling floats) |
| **URL** | https://argo.ucsd.edu/ |
| **Data** | 2.3+ million temperature and salinity profiles from 16,000+ floats; upper 2000m of the ocean; some with biogeochemical sensors (oxygen, chlorophyll, pH, nitrate) |
| **Format** | NetCDF (profile format); JSON via ERDDAP; CSV; DOI monthly tarballs |
| **License** | Free without restriction; CC0 1.0-like Public Domain Dedication |
| **API Access** | Global Data Assembly Centres (GDACs) via HTTPS/FTP; ERDDAP services; `argopy` Python library; OneArgo toolboxes (R, Python, Matlab); AWS |
| **Update Frequency**: Every 30 minutes at GDACs |
| **CSOAI Use Case** | Ocean heat content, climate change, ocean circulation, El Nino/La Nina monitoring, validation of satellite data |

- **GDACs**: Brest, France (https://dataselection.euro-argo.eu/) and Monterey, USA (https://argo.ucsd.edu/data/)
- **Python Library**: `argopy` — https://argopy.readthedocs.io/
- **Visualization Tools**: EuroArgo Data Selection, Argovis (https://argovis.colorado.edu/)
- **Google Earth Engine**: `projects/sat-io/open-datasets/argo-subset`
- **Notes**: One of the most successful global ocean observation systems. 100,000+ profiles per year. All data publicly available in near real-time. [^1742^] [^1746^] [^1752^]

---

### 6.4 NOAA Ocean Data (GOES, POES, CoastWatch)

| Field | Details |
|-------|---------|
| **Name** | NOAA CoastWatch / OceanWatch |
| **URL** | https://coastwatch.noaa.gov/ |
| **Data** | Sea surface temperature (SST), ocean color (chlorophyll), sea surface height, sea ice, salinity, winds; from GOES, POES, Jason, Sentinel-3 |
| **Format** | NetCDF, HDF, GeoTIFF |
| **License** | Free and open |
| **API Access** | ERDDAP, THREDDS, WMS; direct download; AWS Open Data |
| **Coverage** | Global; near real-time |
| **CSOAI Use Case** | Marine weather, harmful algal bloom detection, fisheries management, climate monitoring |

- **West Coast Node**: https://coastwatch.pfeg.noaa.gov/
- **Data Access**: https://coastwatch.noaa.gov/cw/html/data.html
- **Notes**: Multiple regional nodes (West Coast, East Coast, Great Lakes, Polar). Data available via ERDDAP for easy programmatic access.

---

## 7. Submarine Cable & Infrastructure Maps

### 7.1 TeleGeography Submarine Cable Map

| Field | Details |
|-------|---------|
| **Name** | TeleGeography Submarine Cable Map |
| **URL** | https://www.submarinecablemap.com/ |
| **Data** | Active and planned submarine cable systems, landing stations, cable length, RFS date, owners, suppliers, capacity |
| **Format** | Interactive web map; GeoJSON (for open data); JSON API (licensed) |
| **License** | Interactive map: CC BY-NC-SA 3.0; full data: annual license required |
| **API Access** | Free: Cable routes GeoJSON + Landing points GeoJSON (from GitHub); Licensed: JSON API with GeoJSON |
| **Open Data Downloads** | Submarine Cables GeoJSON + Data; Landing Points GeoJSON + Data |
| **CSOAI Use Case** | Submarine cable infrastructure mapping, internet resilience analysis, geopolitical risk assessment |

- **GitHub/Open Data**: https://github.com/telegeography/www.submarinecablemap.com
- **Data License**: https://www2.telegeography.com/license-geocoded-map-data
- **Notes**: The most authoritative source for submarine cable data. Free interactive map and GeoJSON data available. Full geocoded dataset available via annual license. [^1807^] [^1796^] [^1793^] [^1795^]

---

### 7.2 Internet Exchange Map (TeleGeography)

| Field | Details |
|-------|---------|
| **Name** | TeleGeography Internet Exchange Map |
| **URL** | https://www.internetexchangemap.com/ |
| **Data** | Internet exchange points (IXPs) worldwide |
| **Format** | Interactive map |
| **License** | Free to browse |
| **API Access** | No formal API |
| **CSOAI Use Case** | Internet infrastructure mapping, peering analysis |

---

## 8. GNSS/GPS Performance Data

### 8.1 IGS (International GNSS Service)

| Field | Details |
|-------|---------|
| **Name** | IGS — International GNSS Service |
| **URL** | https://igs.org/ |
| **Data** | High-precision GNSS tracking data from 500+ worldwide reference stations; GPS, GLONASS, Galileo, BeiDou; RINEX format; precise ephemerides, clock products, station coordinates, troposphere/ionosphere products |
| **Format** | RINEX (Receiver Independent Exchange Format); SP3 (precise ephemeris); CLK (clock); SINEX (station coordinates) |
| **License** | Free and open access; most data provided at no charge |
| **API Access** | FTP/HTTP download from data centers; BKG Ntrip Client; Web Services |
| **Coverage** | 500+ global reference stations; data registration rate typically 30s or 1s |
| **CSOAI Use Case** | Precise positioning, reference frame realization (ITRF), geodetic research, GNSS performance assessment, timing applications |

- **Data Centers**: CDDIS (NASA), IGN (France), BKG (Germany), KASI (Korea), etc.
- **Data Access**: https://igs.org/data-access/
- **Station Map**: https://network.igs.org/
- **Products**: Final, rapid, ultra-rapid precise ephemerides and clocks; daily and hourly GNSS data
- **Notes**: Founded in 1994. The gold standard for high-precision GNSS data. Supports realization of the International Terrestrial Reference Frame (ITRF). All data free and openly available. [^1803^] [^1798^]

---

### 8.2 BKG GNSS Data Center (Germany)

| Field | Details |
|-------|---------|
| **Name** | BKG (Bundesamt fuer Kartographie und Geodaesie) |
| **URL** | https://igs.bkg.bund.de/ |
| **Data** | GNSS observation data, real-time streams, precise products |
| **Format** | RINEX, RTCM, SP3, CLK |
| **License** | Free and open |
| **API Access** | FTP, HTTP, NTRIP (real-time) |
| **CSOAI Use Case** | European GNSS data access, real-time positioning |

---

### 8.3 NASA CDDIS (Crustal Dynamics Data Information System)

| Field | Details |
|-------|---------|
| **Name** | NASA CDDIS |
| **URL** | https://cddis.nasa.gov/ |
| **Data** | GNSS, SLR, VLBI, DORIS data; IGS products; precise satellite orbits; station coordinates; Earth orientation parameters |
| **Format** | RINEX, SP3, CLK, SINEX, ERP |
| **License** | Free and open; NASA open data policy |
| **API Access** | FTP, HTTP, Web Services; AWS Open Data |
| **CSOAI Use Case** | Precise orbit determination, reference frame maintenance, geodesy, space geodesy research |

- **Data Access**: https://cddis.nasa.gov/Data_and_Derived_Products/
- **Notes**: NASA's archive for space geodesy data. Primary NASA data center for IGS products.

---

## 9. Additional Related Data Sources

### 9.1 N2YO Real-Time Satellite Tracking

| Field | Details |
|-------|---------|
| **URL** | https://www.n2yo.com/ |
| **Data** | Real-time satellite tracking for 30,000+ objects; pass predictions |
| **API** | REST API with free key (see section 2.3) |
| **License** | Free with limits |

---

### 9.2 NASA GIBS (Global Imagery Browse Services)

| Field | Details |
|-------|---------|
| **Name** | NASA Global Imagery Browse Services |
| **URL** | https://gibs.earthdata.nasa.gov/ |
| **Data** | 900+ satellite imagery products; daily updates; 30-year archives |
| **Format** | WMTS, WMS, TWMS; Cloud-Optimized GeoTIFF |
| **License** | Free and open |
| **API Access** | WMTS/WMS endpoints for direct map tile integration |
| **CSOAI Use Case** | Real-time satellite imagery visualization in web maps |

- **Notes**: Provides quick access to global satellite imagery within hours of observation. [^1683^]

---

### 9.3 SATNOGS — Satellite Networked Open Ground Station

| Field | Details |
|-------|---------|
| **Name** | SatNOGS |
| **URL** | https://satnogs.org/ |
| **Data** | Open-source satellite ground station network; satellite telemetry data, observations, transmitter information |
| **Format** | JSON, via Database API |
| **License** | Open source (hardware and software); AGPL |
| **API Access** | SatNOGS Database API; Network API |
| **CSOAI Use Case** | Satellite telemetry monitoring, amateur satellite tracking, radio signal analysis |

- **Database**: https://db.satnogs.org/ — Open satellite transmitter database
- **Network**: https://network.satnogs.org/ — Observations from ground stations

---

### 9.4 NASA Open APIs Portal

| Field | Details |
|-------|---------|
| **URL** | https://api.nasa.gov/ |
| **Data** | APOD (Astronomy Picture of the Day), Mars Rover Photos, NEO (Near Earth Objects), DONKI (space weather), EPIC (Earth imagery from DSCOVR), satellite imagery |
| **Format** | JSON REST API |
| **License** | Free; API key required (free registration) |
| **CSOAI Use Case** | Space weather monitoring, Earth imagery, near-Earth object tracking |

---

### 9.5 ESA Open Data Portal

| Field | Details |
|-------|---------|
| **URL** | https://open.esa.int/ |
| **Data** | ESA Earth observation, planetary science, and space science data |
| **Format** | Various; web interface and APIs |
| **License** | Free |
| **CSOAI Use Case** | ESA mission data access |

---

### 9.6 OpenSky Network

| Field | Details |
|-------|---------|
| **URL** | https://opensky-network.org/ |
| **Data** | Real-time and historical air traffic data (ADS-B); global aircraft positions |
| **Format** | REST API, Python API; historical data in Parquet format |
| **License** | Free for non-commercial use; commercial license available |
| **API Access** | REST API (rate-limited); Python library |
| **CSOAI Use Case** | Air traffic monitoring, ADS-B data analysis, aviation research |

---

### 9.7 NOAA Space Weather Prediction Center

| Field | Details |
|-------|---------|
| **Name** | NOAA SWPC |
| **URL** | https://www.swpc.noaa.gov/ |
| **Data** | Solar activity, geomagnetic storms, ionospheric conditions, radio blackouts, aurora forecasts; Kp index, solar wind, X-ray flux |
| **Format** | JSON, text, XML, plots |
| **License** | Free and open |
| **API Access** | FTP, JSON endpoints, web services |
| **CSOAI Use Case** | Satellite operations, space weather forecasting, GNSS interference prediction |

- **Data Access**: https://www.swpc.noaa.gov/communities/space-weather-enthusiasts
- **Notes**: Primary source for space weather alerts and warnings. [^1803^]

---

## Summary Matrix

| # | Data Source | Category | Free? | API? | Format |
|---|-------------|----------|-------|------|--------|
| 1 | Copernicus Data Space | Satellite | Yes | Yes | GeoTIFF, NetCDF, SAFE |
| 2 | NASA Earthdata | Satellite/Climate | Yes | Yes | HDF, NetCDF-4, GeoTIFF |
| 3 | USGS Landsat | Satellite | Yes | Yes | COG GeoTIFF, STAC |
| 4 | ESA Earth Online | Satellite | Yes | Yes | NetCDF, HDF |
| 5 | Space-Track.org | Space Tracking | Yes (reg) | Yes | TLE, JSON, XML |
| 6 | CelesTrak | Space Tracking | Yes | Yes | TLE, JSON, XML, CSV |
| 7 | N2YO API | Space Tracking | Yes (limits) | Yes | JSON |
| 8 | ESA DISCOSweb | Space Debris | Yes | Yes | JSON |
| 9 | NASA ODPO | Space Debris | Yes | No | Reports, Software |
| 10 | UCS Satellite DB | Space Data | Yes | No | Excel, CSV |
| 11 | ITU Radio Regulations | Spectrum | Yes | No | PDF, Software |
| 12 | OpenCellID | Telecom | Yes | Yes | JSON, XML, CSV |
| 13 | Mozilla Location Services | Telecom | Yes | Yes | JSON, CSV |
| 14 | OpenSignal | Telecom | Free app | No | Maps, Reports |
| 15 | AISstream.io | Maritime | Yes | Yes | WebSocket/JSON |
| 16 | AISHub | Maritime | Yes (share) | Yes | JSON, XML, CSV |
| 17 | MarineTraffic/Kpler | Maritime | Freemium | Yes | JSON, GraphQL |
| 18 | VesselFinder | Maritime | Trial | Yes | JSON, XML |
| 19 | NOAA ERDDAP | Ocean | Yes | Yes | 40+ formats |
| 20 | Copernicus Marine | Ocean | Yes | Yes | NetCDF, Zarr |
| 21 | Argo Floats | Ocean | Yes | Yes | NetCDF, JSON |
| 22 | TeleGeography Cable Map | Submarine Cables | Yes (map) | Yes (licensed) | GeoJSON |
| 23 | IGS GNSS Service | GNSS | Yes | Yes | RINEX, SP3, CLK |
| 24 | NASA CDDIS | GNSS | Yes | Yes | RINEX, SP3 |
| 25 | NASA GIBS | Imagery | Yes | Yes | WMTS, COG |
| 26 | SatNOGS | Satellite Radio | Yes | Yes | JSON |
| 27 | NASA Open APIs | Space | Yes | Yes | JSON |
| 28 | OpenSky Network | Aviation | Yes (NC) | Yes | JSON, Parquet |
| 29 | NOAA SWPC | Space Weather | Yes | Yes | JSON, XML |

---

## References

[^1069^]: Copernicus Open Access Hub overview. https://atlas.co/data-sources/copernicus-open-access-hub/

[^1443^]: Sentinel Hub — Satellite imagery infrastructure. https://www.sentinel-hub.com/

[^1547^]: USGS Earth Explorer overview. https://atlas.co/data-sources/usgs-earth-explorer/

[^1678^]: Starlink GPS data limits. https://militarnyi.com/en/news/starlink-gps-data-limits-starting-may-20/

[^1681^]: Copernicus Data Space Ecosystem. https://eos.com/blog/free-satellite-imagery-sources/

[^1682^]: ESA — How to access data. https://www.esa.int/Applications/Observing_the_Earth/How_to_access_data

[^1683^]: Top 10 Free Sources of Satellite Data. https://skywatch.com/free-sources-of-satellite-data/

[^1687^]: FIRMS | NASA Earthdata. https://www.earthdata.nasa.gov/data/tools/firms

[^1688^]: Satellite Tracker — Live Map of Starlink. https://satellitemap.space/

[^1689^]: SpaceX Satellite Tracker API — Aviation Edge. https://aviation-edge.com/spacex-satellite-tracker-api/

[^1690^]: Sentinel-2 — Copernicus Data Space. https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-missions/sentinel-2

[^1692^]: NASA Earthdata APIs. https://github.com/api-evangelist/nasa-earthdata

[^1693^]: ESA Earth Online Catalog. https://earth.esa.int/eogateway/catalog

[^1695^]: Space-Track.org Documentation. https://www.space-track.org/documentation

[^1741^]: 50 Best Ship Tracking APIs 2026. https://hormuzmonitor.com/50-best-ship-tracking-apis-2026/

[^1742^]: Argo Ocean Temperature and Salinity Profiles. https://climatedataguide.ucar.edu/climate-data/argo-ocean-temperature-and-salinity-profiles

[^1743^]: Datalastic Vessel Tracking API. https://datalastic.com/

[^1744^]: AISstream.io GitHub. https://github.com/aisstream/aisstream

[^1746^]: Argo Float Data (GEE subset). https://gee-community-catalog.org/projects/argo/

[^1749^]: OpenSignal Coverage Maps. https://insights.opensignal.com/coverage-maps

[^1750^]: AISHub — Free AIS vessel tracking. https://www.aishub.net/

[^1751^]: VesselFinder API. https://api.vesselfinder.com/

[^1752^]: Argo GDAC — SEANOE. https://www.seanoe.org/data/00311/42182/

[^1792^]: Landsat Data — NASA Science. https://science.nasa.gov/mission/landsat/data-overview/

[^1793^]: TeleGeography Submarine Cable Map Trivia. https://www2.telegeography.com/submarine-cable-map-trivia

[^1795^]: TeleGeography Map Data License. https://www2.telegeography.com/license-geocoded-map-data

[^1796^]: Submarine Cable Map — GitHub. https://github.com/lintaojlu/submarine_cable_information

[^1797^]: OpenCellID API Documentation. https://wiki.opencellid.org/wiki/API

[^1798^]: Web Services at ESA's Space Debris Office. https://conference.sdo.esoc.esa.int/proceedings/sdc8/paper/204/SDC8-paper204.pdf

[^1799^]: ESA makes space debris software available online. https://spacenews.com/esa-makes-space-debris-software-available-online/

[^1801^]: USGS EROS Data Access. https://www.usgs.gov/centers/eros/data-access

[^1802^]: How to download Landsat from EarthExplorer. https://www.spatialnode.net/articles/how-to-download-landsat-imagery-from-usgs-earthexplorerec0549

[^1803^]: Satellite Tracking Data Sources. https://orbitalradar.com/data-sources

[^1804^]: Current Status of Web Services at ESA's Space Debris Office. https://conference.sdo.esoc.esa.int/proceedings/sdc8/paper/204

[^1807^]: TeleGeography Submarine Cable Map. https://www.submarinecablemap.com/

[^1811^]: Satellites and Debris Dataset (Kaggle). https://www.kaggle.com/datasets/kandhalkhandeka/satellites-and-debris-in-earths-orbit

[^1826^]: CelesTrak TLE Scraper. https://apify.com/jungle_synthesizer/celestrak-tle-orbital-elements-scraper/api/openapi

[^1829^]: N2YO MCP Server. https://github.com/MaxwellCalkin/N2YO-MCP

[^1830^]: ERDDAP service by NOAA. https://istituto.ingv.it/images/Ufficio_Gestione_Dati/docs/20210507_ERDDAP_service_FRATIANNI_OLIVERI.pdf

[^1831^]: ERDDAP Information. https://erddap.bio-oracle.org/erddap/information.html

[^1832^]: Free satellite tracker with N2YO API. https://medium.com/@prashant.tandan528/heres-how-i-created-a-satellite-tracker-for-free-bea1d12bfb6a

[^1833^]: ITU Article 5 Table of Frequency Allocations. https://www.itu.int/en/ITU-R/seminars/ntfa/ntfa-r3-ws-24/

[^1834^]: Jonathan's Space Report. https://keeptrack.space/resources/jonathan-space-report

[^1836^]: ITU RR5FATViewer User's Guide. https://www.itu.int/en/ITU-R/space/support/smallsat/sshandbook/Documents/RR5FATViewer_UsersGuide.pdf

[^1839^]: CelesTrak Orbital Data (GitHub). https://github.com/tannerkoza/celestrak-orbital-data

[^1840^]: CelesTrak API Integration Guide. https://docs.zendir.io/v1.4/Editor/Guides/External/CelesTrak-API-Integration

[^1841^]: CelesTrak.org. https://celestrak.org/

[^1842^]: NOAA ERDDAP Home Page. https://www.ncei.noaa.gov/erddap/

[^1867^]: Copernicus Marine Toolbox API. https://help.marine.copernicus.eu/en/articles/8283072-copernicus-marine-toolbox-api-subset

[^1868^]: UCS Satellite Database User Guide. https://s3.amazonaws.com/ucs-documents/nuclear-weapons/sat-database/

[^1871^]: UCS Satellite Database (Kaggle). https://www.kaggle.com/datasets/luisemiliani/ucs-sat-db

[^1873^]: UCS Satellite Database. https://www.ucs.org/resources/satellite-database

[^1874^]: Copernicus Marine Service — Mercator Ocean. https://www.mercator-ocean.eu/about-us/mercator-ocean/what-we-do/copernicus-marine-service/

[^1878^]: Copernicus Marine Data Store. https://data.marine.copernicus.eu/products

[^1880^]: UCS Satellite Database Blog. https://blog.ucs.org/lgrego/ucs-satellite-database/

---

*Document compiled for CSOAI Space/Telecom/Marine Hives research. All sources verified as of June 2026.*
