import sqlite3
from pathlib import Path
import os
import os.path
"""
Operations.py

BSD 2-Clause License

Copyright (c) 2020, Scott Little
All rights reserved.

This file is the basic Python interface to the SQL database.

"""


class Dotfiles():
    def __init__(self):
        self.db = sqlite3.connect(os.path.expanduser("~/.dotfiles.db"))
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.commit()
        self.db.close()

    def add_config(self, app: str, file: str, contents: str):
        # Basic way to add an app config
        """
        @param app: Application to link to
        @param file: Filename to use
        @param contents: Contents of file, used for restore
        @desc: Adds the config file @file, with contents @contents under application @app
        """
        self.cur.execute(
            "SELECT * FROM dotfiles WHERE (app=? AND file=?)", (app, file))
        if self.cur.fetchall():
            self.cur.close()
            raise Exception
        self.cur.execute("INSERT INTO dotfiles VALUES (?, ?, ?)",
                         (app, file, contents))
        self.db.commit()

    def update_file(self, file, contents):
        """
        @param file: Filename to update, has to be in database
        @param contents: New contents of @file
        @desc: Updates the database entry of @file with the new contents @contents
        @returns: None
        """
        self.cur.execute("UPDATE dotfiles SET contents=? WHERE file=?",
                         (contents, file))
        self.db.commit()

    def get_file(self, file):
        """
        @param file: Filename to fetch
        @desc: Get the contents of filename
        @returns: List of tuples [(contents)+]
        """
        self.cur.execute('SELECT contents FROM dotfiles WHERE file=?', (file,))
        contents = cur.fetchall()
        return contents

    def delete_file(self, file):
        """
        @param file: Filename to remove.
        @desc: Untrack file (remove) from database
        @returns: None
        """
        self.cur.execute("DELETE FROM dotfiles WHERE file=?", (file,))
        self.db.commit()

    def app_exists(self, app):
        """
        @param app: Name of application to search for
        @desc: Return bool, indicating if the file exists
        @returns: bool
        """
        self.cur.execute("SELECT * FROM dotfiles WHERE app=?", (app,))
        results = cur.fetchall()
        return bool(results)

    def get_app_config(self, app):
        """
        @param app: Application to select by
        @desc: Returns a list of files tracked by @app
        @returns: List of tuples
        """
        self.cur.execute("SELECT file FROM dotfiles WHERE app=?", (app,))
        results = cur.fetchall()
        return results

    def get_all_files(self):
        """
        @desc: Gets all files tracked (in database)
        @returns: List of tuples
        """
        cur.execute("SELECT * FROM dotfiles")
        files = cur.fetchall()
        return files

    def create_database(self):
        """
        @desc: Create an empty dotfiles database at ~/.dotfiles.db
        """
        os.remove(os.getenv("HOME") + './dotfiles.db')
        self.cur.execute("""
            CREATE TABLE dotfiles (
                app TEXT,
                file TEXT,
                contents TEXT
            );
            """)
        self.db.commit()
