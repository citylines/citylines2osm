# citylines2osm
Tool for converting [citylines](https://www.citylines.co) geoJSON dumps to OSM XML files

(Work in progress)

## Conversion rules:
The main rule that this tool follows is that sections are turned into ways, stations are turned into nodes, and lines are turned into relations.

For each way (section), the following tags are set:
- `citylines:id`, with the original citylines id
- `network`, equal to the system name

For each station node, the following tags are set:
- `citylines:id`, with the original citylines id
- `network`, equal to the system name
- `name`, with the station name
- `public_transport=stop`


For each relation (line), the following tags are set:
- `name`, which equals to System + Line name
- `type=route`
