import sys
import tarfile
from pathlib import Path
import os
import os.path
from operations import *
import pyperclip
if len(sys.argv) < 2:
    print("Error: Missing command")
    exit(1)
if sys.argv[1] not in ('add-config', 'get-config', 'update-config', 'remove-config', 'get-app', 'generate-tar'):
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

elif command == 'remove-config':
    if len(args) == 0:
        print("Missing filename")
    if not get_file(args[0]):
        print(f"{args[0]} not tracked")
    delete = input(f"Untrack file {args[0]}? (y/N) ").lower() == 'y'
    if delete:
        delete_file(args[0])
    else:
        print("Aborting.")
elif command == 'get-app':
    if not app_exists(args[0]):
        print(f"App {args[0]} does not exist, use add-config.")
    for app in get_app_config(args[0]):
        print(app[0])
elif command == 'generate-tar':
    files = get_all_files()
    if not files:
        print("No files tracked")
        exit()
    with tarfile.open('config.tar', 'w') as tarball:

        for file in files:
            app, filename, content = file
            print(Path(filename).absolute())
            tarball.add(Path(filename).absolute())




