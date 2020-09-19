import sqlite3
import os
import argparse
from operations import *
parser = argparse.ArgumentParser()
delete_file('.zshrc')
#add_file("Zsh", '.zshrc', 'source~/.zshrc')
print(get_file('.zshrc'))
