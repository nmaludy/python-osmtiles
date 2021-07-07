#!/usr/bin/env python
import argparse
import datetime
import math
import os

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


def minmax(x, y):
    return (min(x, y), max(x, y))


def convert(args):
    if args.tile:
        tile_parts = args.tile.split('/') # zoom/x/y
        x = int(tile_parts[1])
        y = int(tile_parts[2])
        zoom = int(tile_parts[0])
        lat, lon = num2deg(x, y, zoom)
        print('lat={} lon={} zoom={}'.format(lat, lon, zoom))
    elif args.latlon:
        latlon_parts = args.latlon.split(',') # lat,lon,zoom
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


def georender(args):
    # number of tiles per metatile
    BULK_SIZE = 8

    # x
    min_lon = args.min_lon
    max_lon = args.max_lon
    # y
    min_lat = args.min_lat
    max_lat = args.max_lat
    # zoom
    min_zoom = int(args.min_zoom)
    max_zoom = int(args.max_zoom)

    extra_args = []
    if args.force:
        extra_args.append("-f")
    if args.map:
        extra_args.extend(["-m", args.map])
    if args.max_load:
        extra_args.extend(["-l", str(args.max_load)])
    if args.socket:
        extra_args.extend(["-s", args.socket])
    if args.num_threads:
        extra_args.extend(["-n", str(args.num_threads)])
    if args.tile_dir:
        extra_args.extend(["-t", args.tile_dir])
    extra_args_str = " ".join(extra_args)

    # easier to just loop over each zoom level rather than trying to figure out
    # and feed in all of the tile numbers to stdin
    for zoom in range(min_zoom, max_zoom+1):
        # convert lat/lon -> tile number
        min_x, min_y = deg2num(min_lat, min_lon, zoom)
        max_x, max_y = deg2num(max_lat, max_lon, zoom)

        # aligning max range values to the border of meta-bundles
        # (caused by internal bug of render_list)
        max_x = (int(max_x/BULK_SIZE)+1)*BULK_SIZE-1
        min_y = (int(min_y/BULK_SIZE)+1)*BULK_SIZE-1

        # make sure min/max are in the right order
        min_x, max_x = minmax(min_x, max_x)
        min_y, max_y = minmax(min_y, max_y)

        cmd = ("render_list -a {extra_args}"
               " -z {min_z} -Z {max_z} -x {min_x} -X {max_x}"
               " -y {min_y} -Y {max_y}").format(extra_args=extra_args_str,
                                                min_z=zoom, max_z=zoom,
                                                min_x=min_x, max_x=max_x,
                                                min_y=min_y, max_y=max_y)

        now = datetime.datetime.now().isoformat()
        print("Zoom level {} began at: {}".format(zoom, now))
        print(cmd)
        os.system(cmd)
        now = datetime.datetime.now().isoformat()
        print("Zoom level {} ended at: {}".format(zoom, now))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenStreetMap Tile Utilities')
    subparsers = parser.add_subparsers(dest='command')

    # convert
    parser_convert = subparsers.add_parser('convert',
                                           help='Convert OpenStreetMap Tile ID to/from Lat/Lon')
    parser_convert.add_argument('-t', '--tile',
                                help='Tile id in the format "zoom/x/y" (ex: "0/1/2")')
    parser_convert.add_argument('-l', '--latlon',
                                help=('Lat/lon (decimal degrees) in the format'
                                      ' "lat,lon,zoom" (ex: "1.23,4.56,3")'))
    parser_convert.add_argument('-o', '--osm',
                                help=('zoom/lat/lon (decimal degrees) in the format'
                                      ' "zoom/lat/lon" (ex: "3/1.23/4.56"). This format'
                                      ' is what is present at the end of the URL from'
                                      ' www.openstreemap.org'))

    # georender
    parser_georender = subparsers.add_parser('georender',
                                             help=('Render all OpenStreetMap tiles in a'
                                                   ' lat/lon bounding box using the "render_list"'
                                                   ' utility from mod_tile. NOTE: This needs'
                                                   ' to be executed on the tile server itself'
                                                   ' where mod_tile is installed and the tile'
                                                   ' cache directory is available'))
    parser_georender.add_argument('-x', '--min-lon',
                                  help='start longitude in decimal degrees, WGS84',
                                  required=True,
                                  type=float)
    parser_georender.add_argument('-X', '--max-lon',
                                  help='end longitude in decimal degrees, WGS84',
                                  required=True,
                                  type=float)
    parser_georender.add_argument('-y', '--min-lat',
                                  help='start latitude in decimal degrees, WGS84',
                                  required=True,
                                  type=float)
    parser_georender.add_argument('-Y', '--max-lat',
                                  help='end latitude in decimal degrees, WGS84',
                                  required=True,
                                  type=float)
    parser_georender.add_argument('-z', '--min-zoom',
                                  help='only render tiles greater or equal to this zoom level',
                                  required=True,
                                  type=int)
    parser_georender.add_argument('-Z', '--max-zoom',
                                  help='only render tiles less than or equal to this zoom level',
                                  required=True,
                                  type=int)
    parser_georender.add_argument('-f', '--force',
                                  help='render tiles even if they seem current',
                                  action='store_true')
    parser_georender.add_argument('-m', '--map',
                                  help='render tiles in this map')
    parser_georender.add_argument('-l', '--max-load',
                                  help='sleep if load is this high (default: 16)',
                                  type=int)
    parser_georender.add_argument('-s', '--socket',
                                  help='unix domain socket name for contacting renderd')
    parser_georender.add_argument('-n', '--num-threads',
                                  help='the number of parallel request threads (default: 1)',
                                  type=int)
    parser_georender.add_argument('-t', '--tile-dir',
                                  help='tile cache directory')

    args = parser.parse_args()
    if args.command == 'convert':
        convert(args)
    elif args.command == 'georender':
        georender(args)
    elif args.command == None:
        parser.print_help()
    else:
        print("ERROR: Unknown command '{}'".format(args.command))
        exit(1)
