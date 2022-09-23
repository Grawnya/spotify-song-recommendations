import regex

class Spotify:

    def __init__(self, artist_name, songs):
        self.artist_name = artist_name
        self.songs = songs
    
    def artist_exists(self):
        '''docstring'''
        if self.artist_name in songs:
            print('artist exists')
