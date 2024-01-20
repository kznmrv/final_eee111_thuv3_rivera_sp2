from SongEntry import SongEntry
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class PlaylistDb:
    """
    A simple database to store SongEntry objects for a playlist.
    """

    def __init__(self, init=False, dbName='PlaylistDb.csv'):
        """
        Initialize database variables here.
        """
        self.dbName = dbName
        self.dbEntries = []
        print('TODO: __init__')

    def fetch_playlist(self):
        """
        Returns a list of tuples containing song entry fields.
        """
        tupleList = []
        print('TODO: fetch_playlist')
        for entry in self.dbEntries:
            tupleList.append((entry.id, entry.title, entry.artist, entry.album, entry.rating))
        return tupleList

    def insert_song(self, id, title, artist, album, rating):
        """
        Inserts a song entry in the database.
        """
        newEntry = SongEntry(id=id, title=title, artist=artist, album=album, rating=rating)
        self.dbEntries.append(newEntry)
        print('TODO: insert_song')

    def delete_song(self, id):
        """
        Deletes the corresponding song entry in the database as specified by 'id'.
        """
        print('TODO: delete_song')
        self.dbEntries = [entry for entry in self.dbEntries if getattr(entry, "id") != id]

    def update_song(self, new_title, new_artist, new_album, new_rating, id):
        """
        Updates the corresponding song entry in the database as specified by 'id'.
        """
        print('TODO: update_song')
        for entry in self.dbEntries:
            if entry.id == id:
                entry.title = new_title
                entry.artist = new_artist
                entry.album = new_album
                entry.rating = new_rating

    def export_csv(self):
        """
        Exports playlist entries as a CSV file.
        """
        print('TODO: export_csv')
        with open(self.dbName, "w") as file:
            for entry in self.dbEntries:
                file.write(f"{entry.id},{entry.title},{entry.artist},{entry.album},{entry.rating} \n")

    def import_csv(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')],
                                                   title='Choose a CSV file to import')
        if file_path:
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        values = line.strip().split(',')
                        if len(values) == 5:
                            id, title, artist, album, rating = values
                            if not self.id_exists(id):
                                self.insert_song(id, title, artist, album, rating)
                            else:
                                print(f"Skipping import for existing ID: {id}")
                        else:
                            print(f"Skipping invalid entry: {line}")

    def id_exists(self, id):
        """
        Returns True if an entry exists for the specified 'id', else returns False.
        """
        return any(getattr(entry, "id") == id for entry in self.dbEntries)