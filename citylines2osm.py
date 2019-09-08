import json
import sys
from lib.writer import CitylinesWriter

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python citylines2osm.py <sections> <stations> <outfile>")
        sys.exit(-1)

    sections_file = sys.argv[1]
    stations_file = sys.argv[2]
    outfile = sys.argv[3]

    print('Writing ' + outfile)

    with open(sections_file) as json_sec_file:
        with open(stations_file) as json_sta_file:
            sections = json.load(json_sec_file)
            stations = json.load(json_sta_file)
            writer = CitylinesWriter(sections['features'], stations['features'], outfile)
            writer.run()
