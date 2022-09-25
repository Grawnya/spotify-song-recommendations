import string
import pandas as pd


class Spotify:
    '''
    A class which represents a spotify element i.e. a genre, music artist,
    track or mood type - which represents a quality from a song.
    '''
    def __init__(self):
        self.spotify_db = self.get_spotify_data()
        self.artists_to_format = self.spotify_db['artist_name'].to_list()
        self.music_artists = self._format_list_values(self.artists_to_format)
        self.genres_to_format = self.spotify_db['genre'].to_list()
        self.genres = self._format_list_values(self.genres_to_format)
        self.tracks_to_format = self.spotify_db['track_name'].to_list()
        self.tracks = self._format_list_values(self.tracks_to_format)

    def get_spotify_data(self):
        '''
        Get dataframe of all songs from a Spotify dataset valid up to 2019.

        Returns:
        spotify_df (dataframe): Dataframe of all songs from a Spotify csv file
        '''
        spotify_df = pd.read_csv('SpotifyFeatures.csv')
        spotify_df = spotify_df.drop(columns=['valence', 'time_signature',
                                              'speechiness', 'mode',
                                              'loudness', 'liveness', 'key',
                                              'energy', 'acousticness',
                                              'track_id'])
        return spotify_df

    def _format_list_values(self, list_of_values):
        '''
        Makes all inputted values in a list lowercase, strips trailing
        whitespace and replaces ampersands, apostrophes, fullstops and
        é (which is very common).

        Parameters:
        list_of_values (list): List of all the values that will be
                               formatted
        
        Returns:
        replace_whitespace (list): Cleaned list after whitespace has
                                   been removed
        '''
        lower_list = [each.lower() for each in list_of_values]
        replace_and = [each.replace('&', 'and') for each in lower_list]
        replace_apost = [each.replace("'", '') for each in replace_and]
        replace_full_stop = [each.replace('.', '') for each in replace_apost]
        replace_e = [each.replace('é', 'e') for each in replace_full_stop]
        replace_whitespace = [each.strip(' ') for each in replace_e]
        return replace_whitespace

    def _favourite(self, list_of_interest):
        '''
        Formats the value of a favourite artist, genre or track and checks
        if it exists.

        Parameters:
        list_of_interest (list): List of either the music artists, genres
                                 or tracks found in the Spotify dataset

        Returns:
        valid_value (str): The valid music artist, genre or track
        '''
        value_interest = self._format_list_values([input('\n')])
        while value_interest[0] not in list_of_interest \
                or value_interest[0] == '':
            value_interest = self._format_list_values([input('Invalid value.'
                                                             ' Enter a new '
                                                             'value:\n')])
        valid_value = value_interest[0]
        return valid_value

    def _closed_question_answer_checks(self, y_or_n):
        '''
        Checks if the user inputs a valid y (yes) or n (no) value
        into the terminal.

        Parameter:
        y_or_n (str): Inputted value from the terminal

        Returns:
        valid_y_or_n (str): Valid "y" or "n"
        '''
        remove_whitespace = y_or_n.replace(' ', '')
        while remove_whitespace.isalpha() is False or \
                remove_whitespace.lower() not in ['y', 'yes', 'n', 'no']:
            remove_whitespace = input('\nAnswer not valid. Please enter'
                                      ' y or n:\n')
            remove_whitespace.replace(' ', '')
        if remove_whitespace.lower() == 'yes':
            remove_whitespace = 'y'
        elif remove_whitespace.lower() == 'no':
            remove_whitespace = 'n'
        valid_y_or_n = remove_whitespace.lower()
        return valid_y_or_n


class Artist(Spotify):
    '''docstring'''
    def _favourite_artist_exists(self):
        '''
        Check if the artist exists in the Spotify dataset.

        Returns:
        music_artist (str): A valid music artist from the spotify dataset
        '''
        print('\nWelcome to the Spotify Song Recommender!\n'
              'We\'ll help you pick some songs that will '
              'become your new favourites from our database'
              ' of over 200,000 songs!\n\n'
              'Firstly we need to ask you some questions!'
              '\n1. Who is your favourite music artist?\n'
              'Examples include Cardi B, The 1975 and '
              'Beyonce:')
        unique_music_artists = list(set(self.music_artists))
        music_artist = self._favourite(unique_music_artists)
        return music_artist

    def favourite_artist_songs(self):
        '''
        Gets a list of the indices of all the songs from the user's
        favourite artist.

        Returns:
        music_artist (str): A valid music artist from the spotify dataset
        indices_of_songs (list): List of indices of all the artist's songs
        '''
        music_artist = self._favourite_artist_exists()
        indices_of_songs = []
        for count, value in enumerate(self.music_artists):
            if value == music_artist:
                indices_of_songs.append(count)
        return music_artist, indices_of_songs


class Genre(Spotify):
    '''docstring'''
    def favourite_genre(self):
        '''
        Prints a list of all valid genres and returns a valid inputted genre.

        Returns:
        genre (str): A valid genre from the spotify dataset
        '''
        print('\nNext up is pick your favourite genre. '
              'Pick from one of the following:\n')
        unique_genres = list(set(self.genres))
        list_of_genres = ', '.join(str(genre) for genre in unique_genres)
        print(list_of_genres + '\n')
        genre = self._favourite(unique_genres)
        if genre != 'hip-hop':
            genre = string.capwords(genre)
        else:
            genre = 'Hip-Hop'
        return genre


class Track(Spotify):
    '''docstring'''
    def _song_position(self, artist):
        '''
        Gets a list of the indices of all the songs from the inputted
        artist.

        Parameters:
        artist (str): A valid music artist from the spotify dataset

        Returns:
        artists_track_indices (list): List of indices of the artist's songs
        '''
        artists_track_indices = []
        i = 0
        for each in self.music_artists:
            if each == artist:
                artists_track_indices.append(i)
            i += 1
        return artists_track_indices

    def _remove_feature(self, song):
        '''
        Removes any featured artists mentioned on a track or any
        extra song information.

        Parameters:
        song (str): Song that needs to be formatted

        Returns:
        song (str): Song that has been stripped of all extra items in title
        '''
        if '(feat' in song:
            song = song.split('(feat')[0]
        elif 'feat' in song:
            song = song.split('feat')[0]
        if ' (' in song:
            song = song.split(' (')[0]
        if ' -' in song:
            song = song.split(' -')[0]
        song.replace('?', '')
        song = song.strip(' ')
        return song

    def _tracks(self, artist):
        '''
        Gets the track names of an artist as they appear in the
        Spotify dataset.

        Parameters:
        artist (str): A valid music artist from the spotify dataset

        Returns:
        track_names (list): List of all the inputted artist's song titles
        '''
        appears_in_db = self._song_position(artist)
        print(f'\n{artist} has {len(appears_in_db)} songs in our database')
        track_names = {}
        for index, song_title in enumerate(self.tracks):
            if index in appears_in_db:
                adjusted_song_title = self._remove_feature(song_title)
                track_names[index] = adjusted_song_title
        return track_names

    def favourite_track(self):
        '''
        Gets a list of all the songs from an inputted artist.

        Returns:
        track (str): A valid song from the spotify dataset
        list_of_tracks_not_unique (list): List of all the songs from the artist
                                          that sang the user's favourite songs.
                                          Not unique (i.e. potential duplicate)
                                          in order to keep the indices
        '''
        print('\nNext step is to search for your favourite song!\n\n'
              'Firstly enter the artist who sings your favourite '
              'song and then we\'ll show you all their songs in '
              'our database. Pick your favourite song or you can '
              'pick another artist if you don\'t like the choice\n'
              '\nChoose an artist\' discography you want to see:\n')
        print('An Example is:\nJennifer Lopez\nDance Again\n')
        unique_music_artists = list(set(self.music_artists))
        singer = self._favourite(unique_music_artists)
        list_of_tracks_not_unique = self._tracks(singer)
        list_of_tracks = list(set(list_of_tracks_not_unique.values()))
        if len(list_of_tracks) < 11:
            print(f'\nThe following tracks exist from {singer}\n')
            tracks_to_print = ', '.join(str(each) for each in list_of_tracks)
            print(tracks_to_print + '\n\n')
            print('\nType in one of the above songs: '
                  '(Make sure it is spelt correctly)')
        else:
            print('\nThe track list is too long to print.\nGuess a song to see'
                  ' if it is in the list: (Make sure it is spelt correctly)')
        track = self._favourite(list_of_tracks)
        return track, list_of_tracks_not_unique


class Mood(Track):
    '''docstring'''
    def _mood_for(self, question, parameter, mood_values_dict):
        '''
        Asks the user about their mood and set it to
        a value comparison operator.

        Parameters:
        question (str): Question that the user is asked regarding their mood
        parameter (str): Name of parameter the corresponds to mood and is also
                         a column name in the Spotify dataset
        mood_values_dict (dict): A dictionary to add the key-value pair of
                                 parameter: "value comparison operator"
        
        Returns:
        mood_values_dict (dict): An updated mood_values_dict
        '''
        task_asked_about = self._closed_question_answer_checks(question)
        if task_asked_about == 'y':
            task_asked_about = '>'
        elif task_asked_about == 'n':
            task_asked_about = '<'
        mood_values_dict[parameter] = task_asked_about
        return mood_values_dict

    def song_style_questions(self):
        '''
        Asks the user if they want to dance, focus and listen to
        something popular and stores the response.

        Returns:
        mood_values (dict): A dictionary with key-value pairs of
                            parameter: "value comparison operator"
        '''
        print('\n\nWe just need to ask a few more questions to pick out'
              '\nthe perfect songs for you!\n'
              'These ones are more mood based\n\n*******\n\n')
        mood_values = {}
        dancing = self._mood_for(input('1. Do you feel like dancing at the '
                                       'moment? y or n\n'),
                                 'danceability', mood_values)
        focus = self._mood_for(input('\n2. Do you want to focus at the '
                                     'moment? y or n\n'),
                               'instrumentalness', mood_values)
        popular = self._mood_for(input('\n3. Do you want to listen to '
                                       'something popular? y or n\n'),
                                 'popularity', mood_values)
        return mood_values
