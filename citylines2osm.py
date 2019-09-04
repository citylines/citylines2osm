import json
import sys
from lib.citylines_writer import CitylinesWriter

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python citylines2osm.py <infile> <outfile>")
        sys.exit(-1)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    print('Writing ' + outfile)

    with open(infile) as json_file:
        data = json.load(json_file)
        writer = CitylinesWriter(outfile, data['features'])
        writer.call()
