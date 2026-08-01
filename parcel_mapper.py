import geopandas as gpd
import simplekml
import folium
import os


GDB_PATH = "res/hamilton_parcels_small.gpkg"

LAYER = "parcels"

PARCEL_CACHE = None
PARCEL_ID_CACHE = None


def load_parcels():

    global PARCEL_CACHE

    if PARCEL_CACHE is None:

        PARCEL_CACHE = gpd.read_file(
            GDB_PATH,
            layer=LAYER
        )

    return PARCEL_CACHE



def get_parcel_ids(gdf):

    global PARCEL_ID_CACHE

    if PARCEL_ID_CACHE is None:

        PARCEL_ID_CACHE = (
            gdf["AUDPTYID"]
            .astype(str)
            .str.strip()
            .str.zfill(13)
        )

    return PARCEL_ID_CACHE



def search_parcels(gdf, parcel_ids):

    gdf_ids = get_parcel_ids(
        gdf
    )

    search_ids = [
        str(x)
        .strip()
        .zfill(13)
        for x in parcel_ids
    ]

    return gdf[
        gdf_ids.isin(search_ids)
    ]



def get_coordinates(parcels):

    if parcels.empty:

        return []


    parcels = parcels.to_crs(
        "EPSG:4326"
    )


    coordinates = []


    for _, parcel in parcels.iterrows():

        centroid = parcel.geometry.centroid

        coordinates.append(
            {
                "parcel_id": str(
                    parcel["AUDPTYID"]
                ),

                "latitude": centroid.y,

                "longitude": centroid.x
            }
        )


    return coordinates



def get_next_filename(
    base="parcels",
    ext=".kml"
):

    counter = 1

    while True:

        filename = f"{base}-{counter}{ext}"

        if not os.path.exists(filename):

            return filename

        counter += 1



def create_kml(
    parcels,
    output_directory=None
):

    if output_directory:

        output = os.path.join(
            output_directory,
            get_next_filename()
        )
    else:

        output = get_next_filename()

    parcels = parcels.to_crs(
        "EPSG:4326"
    )


    kml = simplekml.Kml()


    for _, parcel in parcels.iterrows():

        geom = parcel.geometry

        parcel_id = str(
            parcel["AUDPTYID"]
        )


        if geom.geom_type == "Polygon":

            polygons = [geom]


        elif geom.geom_type == "MultiPolygon":

            polygons = list(
                geom.geoms
            )


        else:

            continue


        for polygon in polygons:

            coords = [
                (x, y)
                for x, y, *_
                in polygon.exterior.coords
            ]


            p = kml.newpolygon(
                name=parcel_id,
                outerboundaryis=coords
            )


            p.description = (
                f"Parcel ID: {parcel_id}"
            )


            p.style.linestyle.width = 3

            p.style.polystyle.fill = 0


    kml.save(
        output
    )


    return output



def generate_parcel_maps(
    parcel_ids,
    status_callback=None,
    output_directory=None
):

    def status(message):

        if status_callback:

            status_callback(
                message
            )

        else:

            print(message)


    status(
        "Loading GIS data..."
    )


    gdf = load_parcels()


    status(
        "Searching parcel geometries..."
    )


    results = search_parcels(
        gdf,
        parcel_ids
    )


    status(
        f"Found {len(results)} parcel geometries"
    )


    if results.empty:

        status(
            "No matching parcels found"
        )

        return None


    status(
        "Creating KML..."
    )


    output = create_kml(
        results,
        output_directory
    )


    status(
        f"{len(results)} parcels mapped to {output}"
    )


    return output
