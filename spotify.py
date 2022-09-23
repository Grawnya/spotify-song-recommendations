import regex

class Spotify:

    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.spotify_db = self._get_spotify_data()
        self.music_artists = self.format_list_values(spotify_df['artist_name'].to_list())
        self.genres = self._format_list_values(spotify_df['genre'].to_list())
        self.tracks = self._format_list_values(spotify_df['track_name'].to_list())

    
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
        value_of_interest = format_list_values([input('\n')])
        while value_of_interest[0] not in list_of_interest \
                and value_of_interest[0] != '':
            value_of_interest = format_list_values([input('Invalid value. Enter'
                                                    ' a new value:\n')])
        return (value_of_interest[0])

    def artist_exists(self):
        '''docstring'''
        if self.artist_name in self.tracks:
            print('artist exists')
