# osmtiles

Small python utility for converting lat/lon to and from OSM tile index used in a tile server URL.

## Understanding index format and zoom levels
https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

## Usage

Convert from lat/lon zoom to tile index:
```shell
# format: lat,lon,zoom
$ python osmtiles.py -l 40.7707,-74.1508,10
tile=10.0/301/384
```

Convert from tile URL format to lat/lon zoom:
```shell
# format: zoom/x/y
$ python osmtiles.py -t 10/301/384
lat=40.97989806962013 lon=-74.1796875 zoom=10
```

Convert from the format in the `openstreemap.org` URL, example: https://www.openstreetmap.org/#map=10/40.7707/-74.1508
```shell
# format: zoom/lat/lon
$ python osmtiles.py -o 10/40.7707/-74.1508
tile=10/301/384
```

## Reference and credit
- https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
