from __future__ import print_function
from HittaSkyddsrum import db
import argparse
import gzip

parser = argparse.ArgumentParser(description='Import given SQL file into MySQL')
parser.add_argument('file', metavar='file') 
args = parser.parse_args()

print('Reading file ' + args.file)

fd = gzip.open(args.file, 'rt')
sqlFile = fd.read()
fd.close()

sqlCommands = sqlFile.split(';')

for command in sqlCommands:
    if not command.strip():
        continue

    try:
        db.engine.execute(command)
    except ValueError as msg:
        print("Command skipped: ", msg)

print("Import ended")
