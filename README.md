# citylines2osm
[![CircleCI](https://circleci.com/gh/citylines/citylines2osm.svg?style=svg)](https://circleci.com/gh/citylines/citylines2osm)

Tool for converting [citylines](https://www.citylines.co) geoJSON dumps into [OSM XML files](https://wiki.openstreetmap.org/wiki/OSM_XML).

## Usage
Clone/download this repository, install [pipenv](https://pipenv-es.readthedocs.io/es/latest/), and run:
```
pipenv run python citylines2osm.py <sections JSON file> <stations JSON file> <outfile.osm>
```
Then, you can open the `osm` file from editors such as [JSOM](https://josm.openstreetmap.de).

Note: Citylines2osm currently only considers features not originally imported from OSM.

## Conversion rules
The main rule that this tool follows is that sections are turned into ways, stations are turned into nodes, and lines are turned into relations.

For each way (section), the following tags are set:
- `citylines:id`, with the original citylines id
- `network`, equal to the system name

For each station node, the following tags are set:
- `citylines:id`, with the original citylines id
- `network`, equal to the system name
- `name`, with the station name
- `public_transport=stop_position`

For each relation (line), the following tags are set:
- `name`, which equals to System + Line name
- `type=route`
- `public_transport:version=2`

The members of the line relation are the ways and the stations' nodes. Each node has the role `stop`.

Note:
- If the feature already had OSM tags, they will be kept.
- A `route` tag hast to be added manually in JOSM to the lines relations, because right now, the dumps are not returning the tranport mode of the line. This will be fixed soon.

## Tests
Run:
```
pipenv run python -m unittest
```
