# osmtiles

Small python utilities for working with OpenStreetMap tiles.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [osmtiles](#osmtiles)
    - [convert](#convert)
        - [convert Usage](#convert-usage)
        - [convert Examples](#convert-examples)
    - [georender](#georender)
        - [georender Usage](#georender-usage)
        - [georender Examples](#georender-examples)
    - [Reference and credit](#reference-and-credit)

<!-- markdown-toc end -->

```shell
$ ./osmtiles.py --help
usage: osmtiles.py [-h] {convert,georender} ...

OpenStreetMap Tile Utilities

positional arguments:
  {convert,georender}
    convert            Convert OpenStreetMap Tile ID to/from Lat/Lon
    georender          Render all OpenStreetMap tiles in a lat/lon bounding
                       box using the "render_list" utility from mod_tile.

optional arguments:
  -h, --help           show this help message and exit
```

## convert

The `convert` command and can be used to convert lat/lon to and from
OpenStreetMap tile index used by the HTTP `mod_tile` server.

For an understanding of the index format and zoom levels, see:
https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

**NOTE** This command is standalone and can be executed on any machine with python installed.

### convert Usage

```shell
$ ./osmtiles.py convert --help
usage: osmtiles.py convert [-h] [-t TILE] [-l LATLON] [-o OSM]

optional arguments:
  -h, --help            show this help message and exit
  -t TILE, --tile TILE  Tile id in the format "zoom/x/y" (ex: "0/1/2")
  -l LATLON, --latlon LATLON
                        Lat/lon (decimal degrees) in the format "lat,lon,zoom"
                        (ex: "1.23,4.56,3")
  -o OSM, --osm OSM     zoom/lat/lon (decimal degrees) in the format
                        "zoom/lat/lon" (ex: "3/1.23/4.56"). This format is
                        what is present at the end of the URL from
                        www.openstreemap.org
```

### convert Examples

Convert from lat/lon zoom to tile index:
```shell
# format: lat,lon,zoom
$ ./osmtiles.py convert -l 40.7707,-74.1508,10
tile=10.0/301/384
```

Convert from tile URL format to lat/lon zoom:
```shell
# format: zoom/x/y
$ ./osmtiles.py convert -t 10/301/384
lat=40.97989806962013 lon=-74.1796875 zoom=10
```

Convert from the format in the `openstreemap.org` URL, example: https://www.openstreetmap.org/#map=10/40.7707/-74.1508
```shell
# format: zoom/lat/lon
$ ./osmtiles.py convert -o 10/40.7707/-74.1508
tile=10/301/384
```

## georender

The `georender` command can be used to render all tiles in a geographic (lat/lon) bounding
box. Under the hood we utilize the `render_list` utility from `mod_tile`, however this script
does the conversion of lat/lon to tile index and then invokes `render_tile` for those
limits at each zoom level.

**NOTE** This needs  to be executed on the tile server itself where `mod_tile` is
         installed and the tile cache directory is available.

### georender Usage

```shell
$ ./osmtiles.py georender --help
usage: osmtiles.py georender [-h] -x MIN_LON -X MAX_LON -y MIN_LAT -Y MAX_LAT
                             -z MIN_ZOOM -Z MAX_ZOOM [-f] [-m MAP]
                             [-l MAX_LOAD] [-s SOCKET] [-n NUM_THREADS]
                             [-t TILE_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -x MIN_LON, --min-lon MIN_LON
                        start longitude in decimal degrees, WGS84
  -X MAX_LON, --max-lon MAX_LON
                        end longitude in decimal degrees, WGS84
  -y MIN_LAT, --min-lat MIN_LAT
                        start latitude in decimal degrees, WGS84
  -Y MAX_LAT, --max-lat MAX_LAT
                        end latitude in decimal degrees, WGS84
  -z MIN_ZOOM, --min-zoom MIN_ZOOM
                        only render tiles greater or equal to this zoom level
  -Z MAX_ZOOM, --max-zoom MAX_ZOOM
                        only render tiles less than or equal to this zoom
                        level
  -f, --force           render tiles even if they seem current
  -m MAP, --map MAP     render tiles in this map
  -l MAX_LOAD, --max-load MAX_LOAD
                        sleep if load is this high (default: 16)
  -s SOCKET, --socket SOCKET
                        unix domain socket name for contacting renderd
  -n NUM_THREADS, --num-threads NUM_THREADS
                        the number of parallel request threads (default: 1)
  -t TILE_DIR, --tile-dir TILE_DIR
                        tile cache directory
```

### georender Examples

Render all tiles from zoom level 6 to 15 (inclusive) in the bounding box.
```shell
./osmtiles.py georender -z 6 -Z 15 -x 21.8 -X 40.7 -y 44.03 -Y 52.6
```

It is also possible to pass other command line options to `render_list`,
such as `--num-threads 8` in order to parallelize the rendering or `--tile-dir`
if your `mod_tile` cache directory is in a different location:
```shell
./osmtiles.py georender -z 6 -Z 15 -x 21.8 -X 40.7 -y 44.03 -Y 52.6 --num-threads 8 --tile-dir /opt/tile_server/mod_tile
```



## Reference and credit
- https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
- https://github.com/alx77/render_list_geo.pl
