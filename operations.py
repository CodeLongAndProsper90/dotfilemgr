import sqlite3
import os
# Sql table format: App, File, contents


def add_config(app, file, contents):
    # Basic way to add an app config
    with sqlite3.connect(os.getenv('HOME') + '/.dotfiles.db') as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM dotfiles WHERE (app=? AND file=?)", (app, file))
        if cur.fetchall():
            cur.close()
            raise Exception
        cur.execute("INSERT INTO dotfiles VALUES (?, ?, ?)", (app, file, contents))
        db.commit()
        cur.close()


def update_file(file, contents):
    # Update config of file -- ignore app
    with sqlite3.connect(os.getenv('HOME') + '/.dotfiles.db') as db:
        cur = db.cursor()
        cur.execute("UPDATE dotfiles SET contents=? WHERE file=?", (contents, file))
        db.commit()
        cur.close()


def get_file(file):
    # Get config of file, no app
    with sqlite3.connect(os.getenv('HOME') + '/.dotfiles.db') as db:
        cur = db.cursor()
        cur.execute('SELECT contents FROM dotfiles WHERE file=?', (file,))
        contents = cur.fetchall()
        db.commit()
        cur.close()
        return contents[0]


def delete_file(file):
    # remove config file
    with sqlite3.connect(os.getenv('HOME') + '/.dotfiles.db') as db:
        cur = db.cursor()
        cur.execute("DELETE FROM dotfiles WHERE file=?", (file,))


def get_app_config(app):
    # Get all filenames and content of app
    with sqlite3.connect(os.getenv('HOME') + '/.dotfiles.db') as db:
        cur = db.cursor()
        cur.execute("SELECT file, contents FROM dotfiles WHERE app=?", (app,))
