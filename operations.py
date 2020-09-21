import sqlite3
from pathlib import Path
import os
import os.path
# Sql table format: App, File, contents


def add_config(app: str, file: str, contents: str):
    # Basic way to add an app config
    """
    @param app: Application to link to
    @param file: Filename to use
    @param contents: Contents of file, used for restore
    @desc: Adds the config file @file, with contents @contents under application @app
    """
    with sqlite3.connect(os.path.expanduser("~/.dotfiles.db")) as db:
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM dotfiles WHERE (app=? AND file=?)", (app, file))
        if cur.fetchall():
            cur.close()
            raise Exception
        cur.execute("INSERT INTO dotfiles VALUES (?, ?, ?)",
                    (app, file, contents))
        db.commit()
        cur.close()


def update_file(file, contents):
    """
    @param file: Filename to update, has to be in database
    @param contents: New contents of @file
    @desc: Updates the database entry of @file with the new contents @contents
    @returns: None
    """
    with sqlite3.connect(os.path.expanduser("~/.dotfiles.db")) as db:
        cur = db.cursor()
        cur.execute("UPDATE dotfiles SET contents=? WHERE file=?",
                    (contents, file))
        db.commit()
        cur.close()


def get_file(file):
    """
    @param file: Filename to fetch
    @desc: Get the contents of filename
    @returns: List of tuples [(contents)+]
    """
    with sqlite3.connect(os.path.expanduser("~/.dotfiles.db")) as db:
        cur = db.cursor()
        cur.execute('SELECT contents FROM dotfiles WHERE file=?', (file,))
        contents = cur.fetchall()
        db.commit()
        cur.close()
        return contents


def delete_file(file):
    """
    @param file: Filename to remove.
    @desc: Untrack file (remove) from database
    @returns: None
    """
    with sqlite3.connect(os.path.expanduser("~/.dotfiles.db")) as db:
        cur = db.cursor()
        cur.execute("DELETE FROM dotfiles WHERE file=?", (file,))


def app_exists(app):
    """
    @param app: Name of application to search for
    @desc: Return bool, indicating if the file exists
    @returns: bool
    """
    print(os.path.expanduser("~/.dotfiles.db"))
    with sqlite3.connect(os.path.expanduser("~/.dotfiles.db")) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM dotfiles WHERE app=?", (app,))
        results = cur.fetchall()
        cur.close()
        return bool(results)


def get_app_config(app):
    """
    @param app: Application to select by
    @desc: Returns a list of files tracked by @app
    @returns: List of tuples
    """
    with sqlite3.connect(os.path.expanduser("~/.dotfiles.db")) as db:
        cur = db.cursor()
        cur.execute("SELECT file FROM dotfiles WHERE app=?", (app,))
        results = cur.fetchall()
        cur.close()
        return results


def get_all_files():
    """
    @desc: Gets all files tracked (in database)
    @returns: List of tuples
    """
    with sqlite3.connect(os.path.expanduser("~/.dotfiles.db")) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM dotfiles")
        files = cur.fetchall()
        cur.close()
        return files


def create_database():
    """
    @desc: Create an empty dotfiles database at ~/.dotfiles.db
    """
    os.remove(os.getenv("HOME") + './dotfiles.db')
    with sqlite3.connect(os.path.expanduser("~/.dotfiles.db")) as db:
        cur = db.cursor()
        cur.execute("""
        CREATE TABLE dotfiles (
            app TEXT,
            file TEXT,
            contents TEXT
        );
        """)
        db.commit()
        cur.close()
