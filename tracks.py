class Track:

    def __init__(self, artist_name, song_title, database):
        self.artist_name = artist_name
        self.song_title = song_title
        self.database = database
    
    def exists(self):
        '''docstring'''