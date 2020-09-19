import sys
import os
import os.path
from operations import *
import pyperclip
if len(sys.argv) < 2:
    print("Error: Missing command")
    exit(1)
if sys.argv[1] not in ('add-config', 'config-app', 'get-config', 'update-config'):
    print(f"{sys.argv[1]} is not a valid subcommand")
    exit(1)

command = sys.argv[1]
args = sys.argv[2:len(sys.argv)]

if command == 'add-config':
    if len(args) == 0:
        print('Missing app name')
        exit(1)
    if len(args) == 1:
        print("Missing config filename")
        exit(1)
    if not os.path.exists(args[1]):
        print(f"{args[1]}: no such file or directory")
    with open(args[1]) as f:
        try:
            add_config(args[0], args[1], f.read())
            print("Added config")
        except:
            print("Error: Config already added. Use update-config to update a config file")
elif command == 'update-config':
    if len(args) == 0:
        print("Missing filename")
        exit(1)
    if not os.path.exists(args[0]):
        print(f"{args[0]}: no such file or directory")
        exit(1)
    if not get_file(args[0]):
        print(f"{args[0]} not tracked, use add-config")
    with open(args[0]) as f:
        update_file(args[0], f.read())
        print(f"Config updated for {args[0]}")

elif command == 'get-config':
    if len(args) == 0:
        print("Missing filename")
        exit(1)
    if not get_file(args[0]):
        print(f"{args[0]} not tracked")
    config = get_file(args[0])[0]
    print(config)
    pyperclip.copy(config)
    
