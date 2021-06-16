#!/usr/bin/env python
import argparse
import math

# Lon./lat. to tile numbers
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

# Tile numbers to lon./lat.
def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenStreetMap Tile<->Lat/lon translator')
    parser.add_argument('-t', '--tile', help='Tile id in the format "zoom/x/y" (ex: "0/1/2")')
    parser.add_argument('-l', '--latlon', help='Lat/lon (decimal degrees) in the format "lat,lon,zoom" (ex: "1.23,4.56,3")')
    parser.add_argument('-o', '--osm', help='zoom/lat/lon (decimal degrees) in the format "zoom/lat/lon" (ex: "3/1.23/4.56"). This format is what is present at the end of the URL from www.openstreemap.org')

    args = parser.parse_args()
    if args.tile:
        tile_parts = args.tile.split('/') # zoom/x/y
        x = int(tile_parts[1])
        y = int(tile_parts[2])
        zoom = int(tile_parts[0])
        lat, lon = num2deg(x, y, zoom)
        print('lat={} lon={} zoom={}'.format(lat, lon, zoom))
    elif args.latlon:
        latlon_parts = args.tile.split(',') # lat,lon,zoom
        lat = float(latlon_parts[0])
        lon = float(latlon_parts[1])
        zoom = int(latlon_parts[2])
        x, y = deg2num(lat, lon, zoom)
        print('tile={}/{}/{}'.format(zoom, x, y))
    elif args.osm:
        latlon_parts = args.osm.split('/') # zoom/lat/lon
        lat = float(latlon_parts[1])
        lon = float(latlon_parts[2])
        zoom = int(latlon_parts[0])
        x, y = deg2num(lat, lon, zoom)
        print('tile={}/{}/{}'.format(zoom, x, y))
    else:
        print("ERROR: Need to specify either -t/--tile or -l/--latlon")
        exit(1)
