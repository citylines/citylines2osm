import json
import sys
from lib.writer import CitylinesWriter

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python citylines2osm.py <sections> <stations> <lines_info> <outfile>")
        sys.exit(-1)

    sections_file = sys.argv[1]
    stations_file = sys.argv[2]
    lines_file    = sys.argv[3]
    outfile       = sys.argv[4]

    print('Writing ' + outfile)

    with open(sections_file) as sections_json, open(stations_file) as stations_json, open(lines_file) as lines_json:
        sections = json.load(sections_json)
        stations = json.load(stations_json)
        lines    = json.load(lines_json)
        writer   = CitylinesWriter(sections['features'], stations['features'], lines, outfile)
        writer.run()
