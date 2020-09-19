import sys
import os
import os.path
from operations import *
if len(sys.argv) < 2:
    print("Error: Missing command")
    exit(1)
if sys.argv[1] not in ('add-app', 'config-app', 'get-config', 'update-config'):
    print(f"{sys.argv[1]} is not a valid subcommand")
    exit(1)
command = sys.argv[1]
args = sys.argv[2:len(sys.argv)]
if command == 'add-app':
    if len(args) == 0:
        print('Missing app name')
        exit(1)
    if len(args) == 1:
          print("Missing config file")
          exit(1)
    if not os.path.exists(args[1]):
        print(f"{args[1]}: no such file or directory")
    with open(args[1]) as f:
        try:
            add_config(args[0], args[1], f.read())
            print("Added config")
        except:
            print("Error: Config already added. Use update-config to update a config file")

