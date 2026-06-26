# CSOAI Domain Dimension: Real Estate, Construction & Urban Planning

> **Research compilation of free/open data sources for property, construction, zoning, urban planning, housing, and land use.**
> Last updated: 2025-07

---

## Table of Contents

1. [Property Records & Transaction Data](#1-property-records--transaction-data)
2. [Building Permits & Construction Activity](#2-building-permits--construction-activity)
3. [Zoning & Land Use Data](#3-zoning--land-use-data)
4. [Urban Planning & Settlement Data](#4-urban-planning--settlement-data)
5. [Housing Prices & Market Indicators](#5-housing-prices--market-indicators)
6. [Building Footprints & 3D Models](#6-building-footprints--3d-models)
7. [Address & Cadastral Data](#7-address--cadastral-data)
8. [Broadband & Connectivity](#8-broadband--connectivity)
9. [Walkability & Transit Scores](#9-walkability--transit-scores)
10. [Energy Performance & Building Energy](#10-energy-performance--building-energy)
11. [Construction Cost Indices](#11-construction-cost-indices)
12. [International/EU Construction Statistics](#12-internationaleu-construction-statistics)
13. [Additional Global Sources](#13-additional-global-sources)

---

## 1. Property Records & Transaction Data

### 1.1 Zillow Transaction and Assessment Database (ZTRAX)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.zillow.com/research/ztrax/ |
| **Format** | Custom text/CSV files (very large datasets) |
| **License** | Free for academic/non-profit research; Data Use Agreement (DUA) required |
| **Coverage** | 2,750+ US counties; 400M+ records; 150M parcels |
| **Data** | Property transfers, mortgages, foreclosures, auctions, tax delinquencies, property characteristics |
| **Updates** | ~2x per year |
| **CSOAI Use** | Property valuation models, market trend analysis, foreclosure prediction, investment signals |

> Note: Access requires affiliation with an educational institution, non-profit, government entity, or policy organization. Commercial use prohibited. [^1798^] [^1809^]

### 1.2 UK HM Land Registry - Price Paid Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads |
| **API/Bulk** | Bulk CSV download + Linked Data API |
| **License** | Open Government Licence v3.0 |
| **Coverage** | England & Wales, January 1995 to present; 25M+ transactions |
| **Data** | Sale price, address, postcode, property type (detached/flat/etc.), new/old build, freehold/leasehold, date |
| **Updates** | Monthly (20th working day) |
| **CSOAI Use** | UK housing price indices, property market forecasting, neighborhood valuation models |

> Full dataset ~5GB CSV. Available as single complete file or annual splits (115-230MB each). [^1799^] [^1803^] [^1810^]

### 1.3 UK HM Land Registry - INSPIRE Index Polygons
| Attribute | Detail |
|-----------|--------|
| **URL** | https://use-land-property-data.service.gov.uk/ |
| **Format** | GML, Shapefile |
| **License** | Open Government Licence |
| **Coverage** | England & Wales - all registered freehold properties |
| **Data** | Indicative property boundary polygons (cadastral map) |
| **Updates** | Monthly |
| **CSOAI Use** | Cadastral mapping, property boundary analysis, spatial property research |

### 1.4 UK House Price Index (UKHPI)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.gov.uk/government/collections/uk-house-price-index-reports |
| **Format** | CSV, reports |
| **License** | Open Government Licence |
| **Coverage** | UK (England, Scotland, Wales, Northern Ireland) |
| **Data** | Monthly house price changes by region, property type, buyer status |
| **CSOAI Use** | Macro housing market trends, regional comparison indices |

### 1.5 US County Assessor Data (via OpenAddresses + Direct)
| Attribute | Detail |
|-----------|--------|
| **URL** | Varies by county; see https://openaddresses.io/ |
| **Format** | CSV, Shapefile, GeoJSON |
| **License** | Varies; mostly public domain or open |
| **Coverage** | US counties with digitized assessor records |
| **Data** | Parcel boundaries, assessed values, property characteristics, owner info (varies) |
| **CSOAI Use** | Property valuation, tax assessment analysis, parcel-level GIS |

---

## 2. Building Permits & Construction Activity

### 2.1 US Census Bureau Building Permits Survey (BPS)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.census.gov/construction/bps/ |
| **Format** | Excel, CSV, text; also accessible via housingdata.app Parquet |
| **License** | Public domain (US government) |
| **Coverage** | US national, state, CBSA (metro), county, and place levels |
| **Data** | New privately-owned residential construction permits by housing unit type |
| **History** | Monthly from ~1990s; annual from 19,000 permit-issuing places |
| **CSOAI Use** | Construction pipeline forecasting, housing supply indicators, regional growth analysis |

> Bulk Parquet downloads available: `https://housingdata.app/states_annual.parquet`, `metros_annual.parquet`, `counties_annual.parquet`, `places_annual.parquet` [^1700^] [^1706^]

### 2.2 US Census Survey of Construction (SOC)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.census.gov/construction/soc/ |
| **License** | Public domain |
| **Coverage** | Sample of US cities/projects |
| **Data** | Housing starts, completions, permit-to-start conversion rates |
| **CSOAI Use** | Understanding permit-to-completion pipeline, construction timing models |

### 2.3 EUROSTAT - Building Permits Index
| Attribute | Detail |
|-----------|--------|
| **URL** | https://ec.europa.eu/eurostat/databrowser/product/view/sts_copr_a |
| **Format** | CSV, Excel, SDMX via Eurostat Data Browser |
| **License** | Free reuse with attribution (Eurostat) |
| **Coverage** | EU-27 + EFTA countries |
| **Data** | Building permits granted (dwelling counts) by type; construction production indices |
| **CSOAI Use** | EU construction market forecasting, cross-country comparison |

---

## 3. Zoning & Land Use Data

### 3.1 NYC GIS Zoning Features
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.nyc.gov/content/planning/pages/resources/datasets/gis-zoning-features |
| **Format** | ESRI Shapefile, File Geodatabase |
| **License** | NYC Open Data (public domain) |
| **Coverage** | New York City |
| **Data** | Zoning districts, special purpose districts, commercial overlays, zoning boundaries |
| **CSOAI Use** | Zoning compliance analysis, development potential modeling, FAR calculations |

### 3.2 US City Open Data Census - Zoning GIS
| Attribute | Detail |
|-----------|--------|
| **URL** | http://us-city.census.okfn.org/dataset/zoning.html |
| **Format** | Shapefile (varies by city) |
| **License** | Open data (varies) |
| **Coverage** | 50+ US cities with open zoning data (NYC, SF, Seattle, Chicago, etc.) |
| **CSOAI Use** | Nationwide zoning classification, land use regulation comparison |

### 3.3 Ireland - MyPlan.ie Land Use Zoning
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.myplan.ie/ |
| **Format** | Interactive map; data extract available |
| **License** | Open data |
| **Coverage** | Republic of Ireland |
| **Data** | Statutory land use zonings, development plan areas |
| **CSOAI Use** | Irish planning analysis, land use classification standardization |

### 3.4 UK - MAGIC Land Use Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://magic.defra.gov.uk/ |
| **Format** | Interactive map + data download |
| **License** | Open Government Licence |
| **Coverage** | UK |
| **Data** | Urban areas, green belt, agricultural land, conservation zones |
| **CSOAI Use** | UK land classification, green space analysis, planning constraint mapping |

---

## 4. Urban Planning & Settlement Data

### 4.1 UN-Habitat Urban Indicators Database
| Attribute | Detail |
|-----------|--------|
| **URL** | https://data.unhabitat.org/ |
| **Format** | Web portal, CSV, Excel download |
| **License** | Open data |
| **Coverage** | 132 countries, 77 indicators, 1,500 urban areas |
| **Data** | SDG 11 indicators, urban policy data, housing, slum population, governance |
| **CSOAI Use** | Global urban comparison, SDG tracking, sustainable city indices |

### 4.2 World Bank Urban Development Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://data.worldbank.org/topic/urban-development |
| **Format** | CSV, Excel, API (REST) |
| **License** | Creative Commons BY 4.0 |
| **Coverage** | Global, 1960-present |
| **Data** | Urban population %, city sizes, infrastructure access, slum populations |
| **CSOAI Use** | Global urbanization trends, emerging market city growth analysis |

### 4.3 DLR Global Urban Footprint (GUF)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.dlr.de/en/eoc/research-transfer/projects-missions/global-urban-footprint |
| **Format** | GeoTIFF |
| **License** | Free for scientific use (12m); 84m for non-profit |
| **Coverage** | Global - every human settlement |
| **Data** | Built-up areas at 12m resolution from TerraSAR-X/TanDEM-X radar (2010-2013) |
| **CSOAI Use** | Global settlement mapping, urban extent detection, rural settlement identification |

### 4.4 World Settlement Footprint (WSF) 2015 / WSF-Evolution
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.un-spider.org/links-and-resources/data-sources/world-settlement-footprint-2015-wsf-dlr-eoc |
| **Format** | GeoTIFF |
| **License** | Free with citation |
| **Coverage** | Global |
| **Data** | Human settlement extents from Sentinel-1, Sentinel-2, Landsat (2014-2015); WSF-Evo covers 1985-2015 |
| **CSOAI Use** | Historical urban growth analysis, settlement change detection |

### 4.5 DLR GUF+ Evolution (Urban Extent Time Series)
| Attribute | Detail |
|-----------|--------|
| **Format** | GeoTIFF via DLR EOC Geoservice |
| **License** | Free for scientific use |
| **Coverage** | Global |
| **Data** | Urban extent for 1990, 2000, 2010, 2015 |
| **CSOAI Use** | Long-term urban growth trajectory analysis |

---

## 5. Housing Prices & Market Indicators

### 5.1 Zillow Home Value Index (ZHVI)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.zillow.com/research/data/ |
| **Format** | CSV (bulk download) |
| **License** | Free for research; attribution required |
| **Coverage** | US: national, state, county, city, ZIP code, neighborhood levels |
| **Data** | Smoothed, seasonally adjusted typical home values (35th-65th percentile) |
| **Frequency** | Monthly from 1996 |
| **CSOAI Use** | Housing market trend analysis, neighborhood price comparison, investment signals |

> Also available via FRED: https://fred.stlouisfed.org/series/USAUCSFRCONDOSMSAMID [^1826^] [^1831^]

### 5.2 Zillow Research - Additional Datasets
| Dataset | URL | Description |
|---------|-----|-------------|
| ZHVI (All tiers) | zillow.com/research/data/ | Bottom/middle/top tier home values |
| ZORI (Observed Rent Index) | zillow.com/research/data/ | Monthly asking rents |
| New Construction Sales | zillow.com/research/data/ | New home sale prices |
| Inventory & Days on Market | zillow.com/research/data/ | Housing supply metrics |
| Market Heat Index | zillow.com/research/data/ | Market velocity indicator |

### 5.3 FRED - Federal Reserve Economic Data (Housing Series)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://fred.stlouisfed.org/ |
| **Format** | CSV, Excel, API |
| **License** | Public domain |
| **Coverage** | US national, regional, state, metro |
| **Data** | S&P/Case-Shiller index, FHFA house price index, new home sales, mortgage rates |
| **CSOAI Use** | Macro housing market analysis, interest rate correlation modeling |

### 5.4 UK House Price Index (ONS/Land Registry)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.ons.gov.uk/peoplepopulationandcommunity/housing/bulletins/housepriceindex |
| **Format** | CSV, Excel |
| **License** | Open Government Licence |
| **Coverage** | UK regions, local authorities |
| **Data** | Monthly average house prices, annual change rates |
| **CSOAI Use** | UK regional market analysis, price trend forecasting |

---

## 6. Building Footprints & 3D Models

### 6.1 NYC Building Footprints
| Attribute | Detail |
|-----------|--------|
| **URL** | https://opendata.cityofnewyork.us/dataset/building/ |
| **Format** | Shapefile, GeoJSON, KML, File Geodatabase |
| **License** | NYC Open Data (public) |
| **Coverage** | New York City |
| **Data** | Building polygons, BIN, BBL, ground elevation, roof height, construction year, feature type |
| **Updates** | Daily |
| **CSOAI Use** | 3D city modeling, floor area calculation, construction age analysis, flood risk |

> Features >400 sq ft and >12 ft tall. Positional accuracy +/- 2 feet. [^1741^] [^1742^]

### 6.2 Chicago Building Footprints
| Attribute | Detail |
|-----------|--------|
| **URL** | https://data.cityofchicago.org/d/hz9b-7nh8 |
| **Format** | Shapefile, GeoJSON, KML |
| **License** | MIT License (GitHub open release) |
| **Coverage** | City of Chicago |
| **Data** | Building footprint polygons, number of stories |
| **CSOAI Use** | Urban density analysis, building stock characterization |

### 6.3 Google Open Buildings
| Attribute | Detail |
|-----------|--------|
| **URL** | https://sites.research.google/gr/open-buildings/ |
| **Format** | CSV (gzip), GeoJSON; also GeoParquet via Source Coop |
| **License** | CC BY-4.0 OR ODbL v1.0 (user's choice) |
| **Coverage** | 1.8B buildings across Africa, Latin America, Caribbean, South Asia, Southeast Asia (58M km2) |
| **Data** | Building footprint polygon, confidence score, Plus Code; v3 includes building height estimates (2.5D temporal 2016-2023) |
| **CSOAI Use** | Infrastructure mapping in Global South, population estimation, humanitarian response, urban planning support |

> Cloud-native access: `s3://us-west-2.opendata.source.coop/google-research-open-buildings/` [^1846^] [^1847^] [^1853^]

### 6.4 Microsoft Building Footprints (US + Global)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://github.com/microsoft/USBuildingFootprints |
| **Format** | GeoJSON |
| **License** | Open Data Commons Open Database License (ODbL) |
| **Coverage** | All 50 US states; also Canada, Australia, South America, Africa, India |
| **Data** | ~130M building footprints from aerial imagery using computer vision |
| **Updates** | 2018 (v1), 2021 (v2 improved) |
| **CSOAI Use** | US-wide building inventory, footprint analysis, feature extraction for property models |

### 6.5 OSM Buildings / OSMBuildings
| Attribute | Detail |
|-----------|--------|
| **URL** | https://osmbuildings.org/data/ |
| **Format** | GeoJSON, OSM, 3D formats |
| **License** | ODbL (OpenStreetMap) |
| **Coverage** | Global (completeness varies by region) |
| **Data** | Building footprints with height, type, properties from OSM |
| **CSOAI Use** | 3D urban visualization, worldwide building data (medium completeness, free) |

### 6.6 OpenStreetMap - Building Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://wiki.openstreetmap.org/wiki/Downloading_data |
| **Format** | OSM XML, PBF; extractable to Shapefile/GeoJSON via Osmosis, osm2pgsql |
| **License** | ODbL |
| **Coverage** | Global |
| **Data** | Building polygons (footprints), building:levels, height, type, use, material, year_built |
| **CSOAI Use** | Global building inventory, fill gaps in commercial data, tagging-based classification |

> Bulk extracts via Geofabrik: https://download.geofabrik.de/ ; Planet.osm: ~100GB compressed [^1432^]

### 6.7 LA County Building Outlines
| Attribute | Detail |
|-----------|--------|
| **URL** | https://egis-lacounty.hub.arcgis.com/datasets/c2d500c1ca12481db111b4a74e09e7ff_0 |
| **Format** | Shapefile |
| **License** | Public Domain |
| **Coverage** | Los Angeles County |
| **Data** | Building footprints, height, area |
| **CSOAI Use** | Southern California urban analysis, seismic risk assessment |

---

## 7. Address & Cadastral Data

### 7.1 OpenAddresses.io
| Attribute | Detail |
|-----------|--------|
| **URL** | https://openaddresses.io/ |
| **Format** | CSV, GeoJSON (bulk download); also API |
| **License** | Varies by source; CC0 metadata; individual source attribution |
| **Coverage** | 470+ million addresses across 2,100+ sources worldwide |
| **Data** | Street name, house number, postal code, geographic coordinates |
| **Updates** | Continuous |
| **CSOAI Use** | Address geocoding, property location standardization, global address coverage |

> GitHub: https://github.com/openaddresses/openaddresses [^1736^] [^1745^]

### 7.2 US National Address Database (NAD)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.transportation.gov/gis/national-address-database |
| **Format** | Various |
| **License** | Public domain (varies by state contribution) |
| **Coverage** | US (participating states) |
| **Data** | Authoritative address points with coordinates |
| **CSOAI Use** | US address validation, geocoding baseline |

### 7.3 UK Ordnance Survey OpenData
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.ordnancesurvey.co.uk/products/os-opendata |
| **Format** | Shapefile, GML, CSV |
| **License** | Open Government Licence |
| **Coverage** | Great Britain |
| **Data** | Code-Point Open (postcode centroids), boundary data, terrain, vector maps (1:250k to 1:10k) |
| **CSOAI Use** | UK property location analysis, postcode-level spatial research |

### 7.4 Open Cadastral Data by Country
| Country | Portal | Data |
|---------|--------|------|
| **Australia** | data.gov.au | Cadastral boundaries, land parcels |
| **Canada** | open.canada.ca | Parcel data by province |
| **Netherlands** | kadaster.nl/pdok | Dutch cadastral parcels (free) |
| **Denmark** | datafordeler.dk | Danish cadastral map (free) |
| **Sweden** | lantmateriet.se | Swedish property map |
| **Finland** | maanmittauslaitos.fi | Finnish cadastral data |
| **Estonia** | geoportaal.maaamet.ee | Estonian land parcels |
| **New Zealand** | data.linz.govt.nz | NZ property boundaries |
| **Colombia** | igac.gov.co | Colombian cadastre |
| **Uruguay** | catastro.gub.uy | Uruguayan cadastral data |

---

## 8. Broadband & Connectivity

### 8.1 Ookla Speedtest Open Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://github.com/teamookla/ookla-open-data |
| **Format** | Shapefile, Apache Parquet |
| **License** | Open Data Commons Attribution License (ODC-By) |
| **Coverage** | Global - zoom level 16 tiles (~610m x 610m at equator) |
| **Data** | Fixed broadband + mobile: avg download/upload speeds (Mbps), latency, device counts, per quarter |
| **History** | Q1 2019 to present |
| **CSOAI Use** | Property broadband quality scoring, infrastructure valuation, digital divide analysis |

> Also available via AWS Open Data Registry: `s3://ookla-open-data/` and Esri Living Atlas. [^1738^] [^1739^]

### 8.2 FCC National Broadband Map (US)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://broadbandmap.fcc.gov/home |
| **Format** | API, bulk download |
| **License** | Public domain |
| **Coverage** | US nationwide |
| **Data** | Broadband availability by provider, technology, speed tier, address/location |
| **CSOAI Use** | US property-level broadband assessment, provider competition analysis |

---

## 9. Walkability & Transit Scores

### 9.1 Walk Score API
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.walkscore.com/professional/api.php |
| **Format** | JSON/XML API |
| **License** | Free tier: 5,000 calls/day; Paid tiers for higher volume |
| **Coverage** | US, Canada, Australia, and major global cities |
| **Data** | Walk Score (0-100), Transit Score, Bike Score for any address/coordinate |
| **CSOAI Use** | Property walkability scoring, neighborhood quality indices, walkability premium estimation |

> API provides score details, nearby transit stops, routes. Research data products available on request. [^1785^] [^1789^]

### 9.2 GTFS (General Transit Feed Specification) Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://transitfeeds.com/ |
| **Format** | GTFS (CSV-based) |
| **License** | Varies by agency (mostly open) |
| **Coverage** | 1,000+ transit agencies worldwide |
| **Data** | Routes, stops, schedules, fare data |
| **CSOAI Use** | Transit accessibility modeling, commute time estimation, transit-oriented development analysis |

---

## 10. Energy Performance & Building Energy

### 10.1 UK Energy Performance Certificates (EPC) - Open Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://get-energy-performance-data.communities.gov.uk/ |
| **Format** | CSV bulk download; API (OpenAPI v3 / Swagger) |
| **License** | Open Government Licence v3.0 |
| **Coverage** | England & Wales; ~30 million certificates since 2008 |
| **Data** | Energy rating (A-G), estimated energy costs, CO2 emissions, floor area, construction age, heating type, recommendations |
| **Updates** | Monthly bulk downloads + real-time API |
| **CSOAI Use** | Property energy scoring, retrofit investment analysis, carbon footprint mapping, housing stock characterization |

> Full dataset ~5.6GB. Available by local authority, by time period (monthly/annual), or complete download. [^1781^] [^1782^] [^1783^]

### 10.2 Scotland EPC Open Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://epcdata.scot/ |
| **Format** | CSV download |
| **License** | Open |
| **Coverage** | Scotland |
| **Data** | Same EPC data for Scottish properties |
| **CSOAI Use** | Complete UK energy performance coverage |

### 10.3 US Commercial Buildings Energy Consumption Survey (CBECS)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.eia.gov/consumption/commercial/ |
| **Format** | CSV, SAS, SPSS, Excel |
| **License** | Public domain |
| **Coverage** | US national, census region |
| **Data** | Energy use by building type, size, age, activity; 5.9M buildings represented (2018 survey) |
| **CSOAI Use** | Commercial building energy benchmarking, ENERGY STAR scoring input |

### 10.4 EPA ENERGY STAR Portfolio Manager Data Explorer
| Attribute | Detail |
|-----------|--------|
| **URL** | https://portfoliomanager.energystar.gov/pm-data-explorer/ |
| **Format** | Web explorer + data download |
| **License** | Public |
| **Coverage** | 150,000+ US commercial and multi-family buildings |
| **Data** | Aggregate energy use by building type, size, state, year |
| **CSOAI Use** | Building energy performance comparison, efficiency investment analysis |

### 10.5 EU Building Stock Observatory (BPIE / EC)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://epbd-ca.eu/ca-outcomes/country-reports/ |
| **Format** | Reports, Excel, PDF |
| **License** | Free reuse |
| **Coverage** | EU Member States |
| **Data** | Building stock characteristics, energy performance, renovation rates, national strategies |
| **CSOAI Use** | EU building energy policy analysis, renovation market sizing |

---

## 11. Construction Cost Indices

### 11.1 EUROSTAT - Construction Cost Index (CCI)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://ec.europa.eu/eurostat/databrowser/product/view/sts_copi_a |
| **Format** | CSV, Excel, SDMX via Eurostat Data Browser |
| **License** | Free reuse with attribution |
| **Coverage** | EU-27 + candidate countries, quarterly since ~2000 |
| **Data** | Construction cost index for new residential buildings (input costs: labor, materials); base year = 2015 or 2000 |
| **CSOAI Use** | Cross-country construction cost comparison, cost inflation forecasting, project budgeting |

### 11.2 OECD - Construction Price Statistics
| Attribute | Detail |
|-----------|--------|
| **URL** | https://data-explorer.oecd.org/ |
| **Format** | CSV, Excel, API (SDMX) |
| **License** | CC BY |
| **Coverage** | OECD member countries |
| **Data** | Construction production indices, price indices, cost indices |
| **CSOAI Use** | International construction market analysis, purchasing power parity |

### 11.3 Arcadis International Construction Costs Report
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.arcadis.com/en/insights/international-construction-costs-2025/ |
| **Format** | PDF report + index data |
| **License** | Free download (registration may be required) |
| **Coverage** | 100 global cities |
| **Data** | Construction cost index rankings, inflation forecasts by region |
| **CSOAI Use** | Global project cost benchmarking, city-level construction investment planning |

### 11.4 Engineering News-Record (ENR) Construction Economics
| Attribute | Detail |
|-----------|--------|
| **URL** | https://www.enr.com/economics |
| **Format** | Web + PDF |
| **License** | Free (some articles subscription) |
| **Coverage** | US + 20 major global cities |
| **Data** | Construction Cost Index (CCI), Building Cost Index (BCI), materials prices, labor rates |
| **CSOAI Use** | US construction cost trending, materials cost forecasting |

---

## 12. International/EU Construction Statistics

### 12.1 EUROSTAT - Production in Construction
| Attribute | Detail |
|-----------|--------|
| **URL** | https://ec.europa.eu/eurostat/databrowser/product/page/sts_copr_a |
| **Format** | CSV, Excel, SDMX |
| **License** | Free reuse with attribution |
| **Coverage** | EU-27 + EFTA, monthly/annual |
| **Data** | Production index for construction (buildings + civil engineering), building permits index |
| **CSOAI Use** | EU construction market cycle analysis, macro construction forecasting |

### 12.2 EUROSTAT - Annual Enterprise Statistics for Construction (NACE F)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://doi.org/10.2908/SBS_NA_CON_R2 |
| **Format** | CSV, Excel, SDMX |
| **License** | Free reuse |
| **Coverage** | EU countries, 2005-2020 |
| **Data** | Value added, employment, personnel costs by construction sub-sector |
| **CSOAI Use** | Construction industry structure analysis, labor cost benchmarking |

---

## 13. Additional Global Sources

### 13.1 Humanitarian Data Exchange (HDX) - Building Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://data.humdata.org/ |
| **Format** | GeoJSON, Shapefile, CSV |
| **License** | CC BY or equivalent |
| **Coverage** | Global, focus on developing countries |
| **Data** | Google Open Buildings, health facility data, school locations |
| **CSOAI Use** | Infrastructure gap analysis, humanitarian real estate assessment |

### 13.2 Google Earth Engine - Satellite Urban Data
| Attribute | Detail |
|-----------|--------|
| **URL** | https://earthengine.google.com/ |
| **Format** | Cloud-based raster/vector analysis |
| **License** | Free for research, education, nonprofit use |
| **Data** | Landsat, Sentinel, MODIS, DLR WSF, GHSL (Global Human Settlement Layer) |
| **CSOAI Use** | Custom urban extent analysis, NDVI for green space, time-series urban growth |

### 13.3 GHSL - Global Human Settlement Layer (JRC European Commission)
| Attribute | Detail |
|-----------|--------|
| **URL** | https://ghsl.jrc.ec.europa.eu/ |
| **Format** | GeoTIFF, vector tiles |
| **License** | Free reuse with attribution |
| **Coverage** | Global, epochs: 1975, 1990, 2000, 2014, 2025 (projected) |
| **Data** | Built-up areas, population density, settlement classification (GHS-BUILT, GHS-POP, GHS-SMOD) |
| **CSOAI Use** | Long-term settlement evolution, population density mapping, urban morphology |

### 13.4 Open Data Institute - Land & Property
| Attribute | Detail |
|-----------|--------|
| **URL** | Various national open data portals |
| **Format** | Varies |
| **License** | Varies |
| **Data** | Property ownership, land use, valuations |
| **CSOAI Use** | Country-specific property data aggregation |

### 13.5 US Geological Survey (USGS) - National Map
| Attribute | Detail |
|-----------|--------|
| **URL** | https://apps.nationalmap.gov/downloader/ |
| **Format** | Shapefile, GeoTIFF, KML |
| **License** | Public domain |
| **Coverage** | United States |
| **Data** | Elevation, hydrography, boundaries, transportation, structures, 3D Elevation Program (3DEP) |
| **CSOAI Use** | Terrain analysis, flood modeling, 3D property visualization |

---

## Quick Reference: Top 20 Sources by CSOAI Priority

| Rank | Source | Category | URL |
|------|--------|----------|-----|
| 1 | Zillow Research (ZHVI + datasets) | Housing Prices | zillow.com/research/data |
| 2 | US Census Building Permits Survey | Building Permits | census.gov/construction/bps |
| 3 | UK Land Registry Price Paid | Property Records | gov.uk/government/statistical-data-sets/price-paid-data-downloads |
| 4 | OpenStreetMap (buildings) | Building Footprints | openstreetmap.org |
| 5 | OpenAddresses.io | Addresses | openaddresses.io |
| 6 | Google Open Buildings | Building Footprints | sites.research.google/gr/open-buildings |
| 7 | Microsoft Building Footprints | Building Footprints | github.com/microsoft/USBuildingFootprints |
| 8 | NYC Building Footprints | Building Footprints | opendata.cityofnewyork.us/dataset/building |
| 9 | EUROSTAT Construction Statistics | Construction Data | ec.europa.eu/eurostat/databrowser |
| 10 | Ookla Speedtest Open Data | Broadband | github.com/teamookla/ookla-open-data |
| 11 | Walk Score API | Walkability | walkscore.com/professional/api.php |
| 12 | UK EPC Open Data | Energy Performance | get-energy-performance-data.communities.gov.uk |
| 13 | DLR Global Urban Footprint | Urban Extent | dlr.de/en/eoc/research-transfer/projects-missions/global-urban-footprint |
| 14 | World Settlement Footprint | Settlement Data | un-spider.org (DLR WSF) |
| 15 | Zillow ZTRAX | Property Records | zillow.com/research/ztrax |
| 16 | EPA CBECS | Building Energy | eia.gov/consumption/commercial |
| 17 | UN-Habitat Urban Indicators | Urban Planning | data.unhabitat.org |
| 18 | GHSL (Global Human Settlement Layer) | Settlement Data | ghsl.jrc.ec.europa.eu |
| 19 | Arcadis ICC Report | Construction Costs | arcadis.com/en/insights/international-construction-costs-2025 |
| 20 | FCC National Broadband Map | Broadband | broadbandmap.fcc.gov |

---

## License Summary Table

| License Type | Sources | Restrictions |
|-------------|---------|--------------|
| **Public Domain / OGL** | US Census BPS, FRED, NYC OpenData, UK Land Registry, UK EPC | Free for any use, attribute source |
| **ODbL** | OpenStreetMap, OpenAddresses metadata | Share-alike for derivative databases |
| **CC BY** | Zillow Research, Google Open Buildings, EUROSTAT, Arcadis | Attribution required |
| **Free Research Only** | Zillow ZTRAX | Academic/non-profit only, DUA required |
| **Freemium API** | Walk Score | 5,000 calls/day free; paid above |
| **Scientific / Non-profit** | DLR GUF (12m resolution) | Full resolution for science only |

---

*Document compiled for CSOAI Real Estate/Construction Hive. All URLs verified as of July 2025.*
