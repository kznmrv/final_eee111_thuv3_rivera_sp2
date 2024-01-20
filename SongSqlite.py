import sqlite3
import csv

class PlaylistDbSqlite:
    def __init__(self, dbName='Playlist.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Playlist (
                id TEXT PRIMARY KEY,
                title TEXT,
                artist TEXT,
                album TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Playlist (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    artist TEXT,
                    album TEXT)''')
        self.commit_close()

    def fetch_playlist(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Playlist')
        playlist = self.cursor.fetchall()
        self.conn.close()
        return playlist

    def insert_song(self, id, title, artist, album, rating):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Playlist (id, title, artist, album) VALUES (?, ?, ?, ?)',
                    (id, title, artist, album, rating))
        self.commit_close()

    def delete_song(self, id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Playlist WHERE id = ?', (id,))
        self.commit_close()

    def update_song(self, new_title, new_artist, new_album, new_rating, id):
        self.connect_cursor()
        self.cursor.execute('UPDATE Playlist SET title = ?, artist = ?, album = ? WHERE id = ?',
                    (new_title, new_artist, new_album, new_rating, id))
        self.commit_close()

    def id_exists(self, id):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Playlist WHERE id = ?', (id,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            playlist_entries = self.fetch_playlist()
            for entry in playlist_entries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]} \n")

    def import_csv(self, csv_file_path):
        self.connect_cursor()
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                id, title, artist, album, rating = row
                self.insert_song(id, title, artist, album, rating)
        self.commit_close()

def test_PlaylistDb():
    iPlaylistDb = PlaylistDbSqlite(dbName='PlaylistSql.db')

    for entry in range(30):
        iPlaylistDb.insert_song(entry, f'Song{entry}', f'Artist{entry}', f'Album{entry}', f'Rating{entry} \n')
        assert iPlaylistDb.id_exists(entry)

    all_entries = iPlaylistDb.fetch_playlist()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iPlaylistDb.update_song(f'Song{entry}', f'Artist{entry}', f'New Album{entry}', f'Rating{entry} entry')
        assert iPlaylistDb.id_exists(entry)

    all_entries = iPlaylistDb.fetch_playlist()
    assert len(all_entries) == 30

    for entry in range(10):
        iPlaylistDb.delete_song(entry)
        assert not iPlaylistDb.id_exists(entry) 

    all_entries = iPlaylistDb.fetch_playlist()
    assert len(all_entries) == 20