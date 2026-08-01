# HamOHOwnerMap

Search Hamilton County, Ohio parcel data by owner or address and export parcel boundaries as KML.

## Installation
Download the `res` folder from the data link below and place it in the project directory before running.

```bash
git clone https://github.com/make-them-ring/HamOHOwnerMap.git
cd HamOHOwnerMap

python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
python3 main.py
```


## Data Files

The parcel GIS data and property records CSV are not included in this repository due to file size.

Download the required data files here:

https://www.dropbox.com/scl/fo/hpta7wn8lv7eq5ool66vn/AGBao-23cvKut7cFGJHSq6A?rlkey=kfn84yhwd52u9rtd1vridtxly&st=m57g221o&dl=0

Place the downloaded `res` folder in the project directory:

```
HamOHOwnerMap/
├── main.py
├── qml/
├── res/
│   ├── hamilton_parcels_small.gpkg
│   └── property_records.csv
└── requirements.txt
```

The application requires the GIS database and property records inside `res/` to search parcels and generate KML files.

## Viewing KML Files

Generated KML files can be viewed using Google My Maps:

https://www.google.com/maps/about/mymaps/

Import the generated `.kml` file into a new map to view parcel boundaries.
