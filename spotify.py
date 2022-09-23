import regex
import pandas as pd

class Spotify:

    def __init__(self):
        self.spotify_db = self._get_spotify_data()
        self.music_artists = self._format_list_values(self.spotify_db['artist_name'].to_list())
        self.genres = self._format_list_values(self.spotify_db['genre'].to_list())
        self.tracks = self._format_list_values(self.spotify_db['track_name'].to_list())

    
    def _get_spotify_data(self):
        '''
        get list of music artists and genres from database and
        also return the database
        '''
        spotify_df = pd.read_csv('SpotifyFeatures.csv')
        return spotify_df


    def _format_list_values(self, list_of_values):
        '''docstring'''
        lower_list = [each.lower() for each in list_of_values]
        replace_and = [each.replace('&', 'and') for each in lower_list]
        replace_apostrophe = [each.replace("'", '') for each in replace_and]
        replace_full_stop = [each.replace('.', '') for each in replace_apostrophe]
        replace_e = [each.replace('é', 'e') for each in replace_full_stop]
        return replace_e
    
    def _favourite(self, list_of_interest):
        '''docstring'''
        value_of_interest = self._format_list_values([input('\n')])
        while value_of_interest[0] not in list_of_interest \
                and value_of_interest[0] != '':
            value_of_interest = self._format_list_values([input('Invalid value. Enter'
                                                    ' a new value:\n')])
        return (value_of_interest[0])

class Artist(Spotify):

    def favourite_artist_exists(self):
        print('Welcome to the Spotify Song Recommender!\n'
          'We\'ll help you picksome songs that will '
          'become your new favourites!\n\n'
          'Firstly we need to ask you some questions!'
          '\n1. Who is your favourite music artist?\n'
          'Examples include Cardi B, The 1975 and '
           'Beyonce:\n')
        unique_music_artists = list(set(self.music_artists))
        music_artist = self._favourite(unique_music_artists)
        return music_artist


# class Track(Spotify):
