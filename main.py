import sys
import shutil
import tarfile
#  Tarball support
import subprocess
#  Github support
from pathlib import Path
import os
import os.path
from operations import *

try:
    import pyperclip
    clip = True
except:
    clip = False

if len(sys.argv) < 2:
    print("Error: Missing command")
    exit(1)
df = Dotfiles()

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
            df.add_config(args[0], str(Path(args[1]).absolute()), f.read())
            print("Added config")
        except:
            raise
            print(
                "Error: Config already added. Use update-config to update a config file")
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
        df.update_file(args[0], f.read())
        print(f"Config updated for {args[0]}")

elif command == 'get-config':
    if len(args) == 0:
        print("Missing filename")
        exit(1)

    if not get_file(args[0]):
        print(f"{args[0]} not tracked")

    config = df.get_file(args[0])[0]
    print(config)
    if clip:
        pyperclip.copy(config)

elif command == 'remove-config':
    if len(args) == 0:
        print("Missing filename")

    if not get_file(args[0]):
        print(f"{args[0]} not tracked")

    delete = input(f"Untrack file {args[0]}? (y/N) ").lower() == 'y'

    if delete:
        df.delete_file(args[0])
    else:
        print("Aborting.")


elif command == 'get-app':
    if not app_exists(args[0]):
        print(f"App {args[0]} does not exist, use add-config.")
    for app in df.get_app_config(args[0]):
        print(app[0])


elif command == 'generate-tar':
    files = df.get_all_files()

    if not files:
        print("No files tracked")
        exit()

    with tarfile.open('config.tar', 'w') as tarball:

        for file in files:
            app, filename, content = file
            print(Path(filename).absolute())
            tarball.add(Path(filename).absolute())

elif command == 'sync-gh':

    if len(args) == 0:
        print("Missing repo name")

    if not args[0].startswith('https://'):
        url = 'https://github.com/' + args[0]

    else:
        url = args[0]

    os.mkdir('/tmp/github')
    os.chdir('/tmp/github')
    files = df.get_all_files()
    for file in files:
        filename = file[1]
        shutil.copy(filename, './' +
                    filename.split(os.path.expanduser('~')[-1]))
        #  Copy all files to the /tmp/github repo, remove prefixes.

    subprocess.run(['git', 'init'])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', '"Sync dotfiles to github"'])
    subprocess.run(['git', 'remote', 'add', 'origin', url])
    subprocess.run(['git', 'push', 'origin', 'master'])

    shutil.rmtree('/tmp/github')


elif command == "restore":
    if len(args) == 0:
        print("Missing target, please use `file` or `app`")
        exit(1)

    if len(args) == 1:
        print(f"Missing operand for {args[0]}, please correct")
        exit(1)

    if args[0].lower() == 'file':
        file = str(Path(args[1]).absolute())
        if not df.get_file(file):
            print(f"Cannot restore file {args[1]} because it was not tracked.")
            print("sorry")
            exit(1
                 )
        if os.path.exists(args[1]):
            shutil.copy(args[1], args[1] + '.back')
            print(f"{args[1]} copied to {args[1]}.back")

        with Path(file).open('w') as f:
            f.write(df.get_file(file)[0][0] + '\n')
